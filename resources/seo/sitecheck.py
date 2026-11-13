#!/usr/bin/env python3
"""Checks theekmind.com, blogs.theekmind.com and tmtimer.theekmind.com against sites.toml.

    python3 resources/seo/sitecheck.py [--host NAME] [--max-urls N] [--extra-ca PATH]

Exit code 1 if any check FAILs. A host behind a JavaScript bot challenge is reported as
UNVERIFIABLE and never worked around; use Search Console's URL Inspection for it.

--extra-ca PATH (a PEM file or a folder of .pem files, e.g. resources/seo/ca) is for a host whose
server sends only its own certificate (tmtimer on InfinityFree). Only if the strict check fails
with a certificate error is the host retried with those intermediates, and then it is reported
as WARN, never PASS. Keep only genuine public CA certificates in that folder.
"""
import argparse
import json
import re
import ssl
import sys
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
from html.parser import HTMLParser
from pathlib import Path
from xml.etree import ElementTree

REGISTRY = Path(__file__).with_name("sites.toml")
UA = "TheekMindSiteCheck/1.0 (+https://theekmind.com)"
SM_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        return None


OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect)
EXTRA_OPENER = None  # set by --extra-ca; used only for hosts in EXTRA_HOSTS
EXTRA_HOSTS = set()


def extra_ca_context(path):
    """System roots plus the certificates in PATH (a PEM file or a folder of .pem files)."""
    p = Path(path)
    files = sorted(p.glob("*.pem")) if p.is_dir() else [p]
    if not files or not all(f.is_file() for f in files):
        raise SystemExit(f"--extra-ca: no .pem files at {path}")
    ctx = ssl.create_default_context()
    for f in files:
        ctx.load_verify_locations(cafile=str(f))
    return ctx


def fetch(url, tries=2):
    """Returns (status, headers, body) without following redirects or using a proxy.

    Connection errors are retried once (the home LTE link drops handshakes now and then);
    certificate errors are not, since a retry can't fix them.
    """
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    opener = EXTRA_OPENER if EXTRA_OPENER and urllib.parse.urlsplit(url).hostname in EXTRA_HOSTS else OPENER
    try:
        with opener.open(req, timeout=20) as r:
            return r.status, r.headers, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read().decode("utf-8", "replace")
    except (urllib.error.URLError, TimeoutError) as e:
        reason = getattr(e, "reason", e)
        if tries > 1 and not isinstance(reason, ssl.SSLCertVerificationError):
            return fetch(url, tries - 1)
        return 0, {}, f"{reason}"


CHALLENGE_NOTE = "bot challenge; check with Search Console URL Inspection"


def is_challenge(body):
    return "aes.js" in body and "__test" in body


def parse_robots(text):
    """Returns (sitemaps, disallows for the * group)."""
    sitemaps, disallow, groups, in_star, last_was_agent = [], [], [], False, False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, val = (s.strip() for s in line.split(":", 1))
        key = key.lower()
        if key == "sitemap":
            sitemaps.append(val)
        elif key == "user-agent":
            in_star = (in_star and last_was_agent) or val == "*"
            last_was_agent = True
            continue
        elif key == "disallow" and in_star and val:
            disallow.append(val)
        last_was_agent = False
    return sitemaps, disallow


def parse_sitemap(xml):
    root = ElementTree.fromstring(xml.encode())
    return [el.text.strip() for el in root.iter(SM_NS + "loc") if el.text]


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title, self.canonical, self.site_name, self.robots = "", None, None, ""
        self.ld, self._in_title, self._in_ld = [], False, False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = self.canonical or a.get("href")
        elif tag == "meta" and a.get("property") == "og:site_name":
            self.site_name = a.get("content")
        elif tag == "meta" and (a.get("name") or "").lower() == "robots":
            self.robots += (a.get("content") or "").lower()
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_ld = True
            self.ld.append("")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        elif self._in_ld:
            self.ld[-1] += data


def page_facts(html):
    p = Head()
    p.feed(html)
    nodes, errors = [], []
    for block in p.ld:
        try:
            data = json.loads(block)
            nodes.extend(data if isinstance(data, list) else data.get("@graph", [data]))
        except json.JSONDecodeError as e:
            errors.append(str(e))
    return {"title": " ".join(p.title.split()), "canonical": p.canonical, "site_name": p.site_name,
            "noindex": "noindex" in p.robots, "ld": nodes, "ld_errors": errors}


def ld_problems(nodes):
    """Template leftovers or empty values, e.g. Blogger's "Can't find substitution for tag"."""
    bad = []

    def walk(v, path):
        if isinstance(v, dict):
            for k, x in v.items():
                walk(x, f"{path}.{k}")
        elif isinstance(v, list):
            for i, x in enumerate(v):
                walk(x, f"{path}[{i}]")
        elif isinstance(v, str) and ("<!--" in v or "substitution" in v or not v.strip()):
            bad.append(path)
    for n in nodes:
        walk(n, n.get("@type", "?") if isinstance(n, dict) else "?")
    return bad


def refs_person(nodes, person_id):
    return person_id in json.dumps(nodes)


class Report:
    def __init__(self):
        self.rows = []

    def add(self, status, host, check, detail=""):
        self.rows.append((status, host, check, detail))
        print(f"{status:<12} {host:<22} {check:<22} {detail}")

    @property
    def failed(self):
        return any(r[0] == "FAIL" for r in self.rows)


def check_host(host, reg, rep, titles, max_urls):
    name, base = host["name"], host["base"]
    all_sitemaps = sorted(h["base"] + s for h in reg["host"] for s in h["sitemaps"])

    status, _, body = fetch(base + "/robots.txt")
    if status == 0 and "CERTIFICATE_VERIFY_FAILED" in body and EXTRA_OPENER:
        EXTRA_HOSTS.add(name)
        status, _, body = fetch(base + "/robots.txt")
        if status:
            rep.add("WARN", name, "certificate chain", "server sends an incomplete chain; verified with the --extra-ca intermediates")
    if is_challenge(body):
        rep.add("UNVERIFIABLE", name, "robots.txt", CHALLENGE_NOTE)
        return
    if status != 200:
        rep.add("FAIL", name, "robots.txt", f"HTTP {status}" if status else f"connection: {body}")
        return
    sitemaps, disallow = parse_robots(body)
    missing = [s for s in all_sitemaps if s not in sitemaps]
    rep.add("FAIL" if missing else "PASS", name, "robots sitemaps", "missing " + ", ".join(missing) if missing else f"{len(sitemaps)} listed")
    if sorted(disallow) != sorted(host["blocked"]):
        rep.add("FAIL", name, "robots disallow", f"live {sorted(disallow)} != registry {sorted(host['blocked'])}")
    else:
        rep.add("PASS", name, "robots disallow", f"{len(disallow)} paths")
    robots = urllib.robotparser.RobotFileParser()
    robots.parse(body.splitlines())

    urls = []
    for sm in host["sitemaps"]:
        status, _, xml = fetch(base + sm)
        if is_challenge(xml):
            rep.add("UNVERIFIABLE", name, f"sitemap {sm}", CHALLENGE_NOTE)
            continue
        try:
            locs = parse_sitemap(xml) if status == 200 else None
        except ElementTree.ParseError:
            locs = None
        rep.add("PASS" if locs else "FAIL", name, f"sitemap {sm}", f"{len(locs)} URLs" if locs else f"HTTP {status} or not a urlset")
        urls += locs or []

    for url in urls[:max_urls]:
        status, headers, html = fetch(url)
        path = url[len(base):] or "/"
        problems = []
        if is_challenge(html):
            rep.add("UNVERIFIABLE", name, path[:22], CHALLENGE_NOTE)
            continue
        if status != 200:
            problems.append(f"HTTP {status}")
        else:
            f = page_facts(html)
            if f["canonical"] != url:
                problems.append(f"canonical {f['canonical']}")
            if f["noindex"] or "noindex" in (headers.get("X-Robots-Tag") or "").lower():
                problems.append("noindex")
            if f["site_name"] != host["site_name"]:
                problems.append(f"og:site_name {f['site_name']!r}")
            if f["ld_errors"]:
                problems.append("JSON-LD does not parse")
            if bad := ld_problems(f["ld"]):
                problems.append("JSON-LD empty or template leftovers at " + ", ".join(bad))
            if path in host["person_on"] and not refs_person(f["ld"], reg["person_id"]):
                problems.append("no reference to " + reg["person_id"])
            titles.setdefault(f["title"].lower(), []).append(url)
        if not robots.can_fetch("*", url):
            problems.append("in sitemap but blocked by robots.txt")
        rep.add("FAIL" if problems else "PASS", name, path[:22], "; ".join(problems))
    if len(urls) > max_urls:
        rep.add("SKIP", name, "pages", f"{len(urls) - max_urls} more URLs not fetched (--max-urls)")

    for path in host["noindex"]:
        status, headers, html = fetch(base + path)
        if is_challenge(html):
            rep.add("UNVERIFIABLE", name, f"noindex {path}", CHALLENGE_NOTE)
            continue
        ok = "noindex" in (headers.get("X-Robots-Tag") or "").lower() or page_facts(html)["noindex"]
        rep.add("PASS" if ok else "FAIL", name, f"noindex {path}", "" if ok else "page can be indexed")

    for src, dst in host["redirects"].items():
        status, headers, body = fetch(src)
        if is_challenge(body):
            rep.add("UNVERIFIABLE", name, "redirect", f"{src}: {CHALLENGE_NOTE}")
            continue
        ok = status in (301, 308) and headers.get("Location") == dst
        rep.add("PASS" if ok else "FAIL", name, "redirect", f"{src} -> {status} {headers.get('Location')}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host")
    ap.add_argument("--max-urls", type=int, default=50)
    ap.add_argument("--extra-ca", metavar="PATH", help="PEM file or folder of intermediates for hosts that send an incomplete chain")
    args = ap.parse_args()
    if args.extra_ca:
        global EXTRA_OPENER
        EXTRA_OPENER = urllib.request.build_opener(
            urllib.request.ProxyHandler({}), NoRedirect, urllib.request.HTTPSHandler(context=extra_ca_context(args.extra_ca)))
    reg = tomllib.loads(REGISTRY.read_text())
    rep, titles = Report(), {}
    for host in reg["host"]:
        if not args.host or args.host == host["name"]:
            check_host(host, reg, rep, titles, args.max_urls)
    for title, urls in titles.items():
        hosts = {u.split("/")[2] for u in urls}
        if len(hosts) > 1:
            rep.add("FAIL", "cross-host", "duplicate title", f"{title!r}: {', '.join(urls)}")
    counts = {s: sum(r[0] == s for r in rep.rows) for s in ("PASS", "WARN", "FAIL", "UNVERIFIABLE", "SKIP")}
    print("\n" + ", ".join(f"{v} {k}" for k, v in counts.items() if v))
    sys.exit(1 if rep.failed else 0)


if __name__ == "__main__":
    main()
