#!/usr/bin/env python3
"""Regenerates docs/*.html from shared components. Run from the repo root: python3 resources/build_pages.py

Edit this file, never the generated HTML. CV_LIVE stays False until the CV PDF has been reviewed.
"""
import json
from html import escape
from pathlib import Path
from PIL import Image

D = Path("docs")
SITE = "https://theekmind.com"
EMAIL = "homemadeict@gmail.com"
GITHUB = "https://github.com/HomemadeICT"
LINKEDIN = "https://www.linkedin.com/in/theekshana-prabodha/"
BLOG = "https://blogs.theekmind.com"
TIMER_APP = "https://tmtimer.theekmind.com"
CV_FILE = "assets/Theekshana-Prabodha-CV.pdf"
CV_LIVE = (D / CV_FILE).exists()  # the CV is only linked once the reviewed PDF is copied into docs/assets/

NAV = [("projects.html", "Projects"), ("about.html", "About"), (BLOG, "Blog")]


def dims(rel):
    with Image.open(D / rel) as im:
        return im.size


def img(rel, alt, cls="", lazy=True):
    w, h = dims(rel)
    c = f' class="{cls}"' if cls else ""
    ld = ' loading="lazy"' if lazy else ""
    return f'<img{c} src="{rel}" alt="{escape(alt)}" width="{w}" height="{h}"{ld}>'


def fig(rel, alt, cap):
    return f"<figure>{img(rel, alt)}<figcaption>{cap}</figcaption></figure>"


def gallery(items, one=False):
    return f'<div class="gallery{" one" if one else ""}">' + "".join(fig(*i) for i in items) + "</div>"


def chips(items):
    return '<ul class="roles">' + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul>"


def sec(heading, inner, alt=False, lead=None, sid=None):
    i = f' id="{sid}"' if sid else ""
    head = f'<div class="section-head"><h2>{heading}</h2>' + (f"<p>{lead}</p>" if lead else "") + "</div>"
    return f'<section class="block reveal{" alt" if alt else ""}"{i}><div class="wrap">{head}{inner}</div></section>'


def prose(inner):
    return f'<div class="prose">{inner}</div>'


def table(head, rows):
    th = "".join(f"<th>{h}</th>" for h in head)
    tr = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def cta(title="Let's work together", text="I'm looking for a junior software, web or DevOps role in Sri Lanka or remote. The fastest way to reach me is email."):
    cv = f'<a class="btn" href="{CV_FILE}">Download CV</a>' if CV_LIVE else ""
    return (f'<div class="wrap"><div class="cta reveal"><h2>{title}</h2><p>{text}</p>'
            f'<div class="btns"><a class="btn primary lg" href="mailto:{EMAIL}">Email me</a>'
            f'<a class="btn lg" href="{LINKEDIN}">LinkedIn</a>{cv}</div></div></div>')


def page(fname, title, desc, body, nav=None, jsonld=None, root=""):
    links = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == nav else ""}>{t}</a>' for h, t in NAV)
    contact = f'<a class="pill" href="{root}contact.html"{" aria-current=\"page\"" if nav == "contact.html" else ""}>Contact</a>'
    url = SITE + "/" + ("" if fname == "index.html" else fname)
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ""
    # navigation hrefs relative to the page location (404 is served from any path, so it uses root-relative URLs)
    def fix(s):
        if not root:
            return s
        out = s
        for h, _ in NAV:
            if not h.startswith("http"):
                out = out.replace(f'href="{h}"', f'href="{root}{h}"')
        return out
    links = fix(links)
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title>
<meta name="description" content="{escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="icon" href="{root}assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="96x96" href="{root}assets/favicon-96.png">
<link rel="apple-touch-icon" href="{root}assets/apple-touch-icon.png">
<meta property="og:type" content="website">
<meta property="og:site_name" content="TheekMind">
<meta property="og:title" content="{escape(title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0F2D5B">
<script>document.documentElement.classList.add('js');try{{var t=localStorage.getItem('tm-theme');if(t)document.documentElement.setAttribute('data-theme',t)}}catch(e){{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{root}styles.css">
{ld}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="{root or "index.html"}"><img src="{root}assets/logo-badge.png" alt="" width="40" height="40">TheekMind</a>
    <nav class="nav" id="nav" aria-label="Main">{links}<a class="only-small cta-link" href="{root}contact.html">Contact</a></nav>
    <div class="actions">
      {contact}
      <button class="switch" id="theme" type="button" role="switch" aria-checked="false" aria-label="Dark mode">
        <svg class="ico sun" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/></svg>
        <svg class="ico moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>
        <span class="knob"></span>
      </button>
      <button class="menu-btn" id="menu" type="button" aria-label="Menu" aria-controls="nav" aria-expanded="false"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></button>
    </div>
  </div>
</header>
<main id="main">
{body}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div><strong>TheekMind</strong><p>Build the skills. Create the future.</p><p>Theekshana Prabodha, ICT learner and builder from Sri Lanka.</p></div>
    <div><h3>Explore</h3><a href="{root}projects.html">Projects</a><a href="{root}about.html">About</a><a href="{BLOG}">Blog</a><a href="{root}contact.html">Contact</a></div>
    <div><h3>Elsewhere</h3><a href="{GITHUB}">GitHub</a><a href="{LINKEDIN}">LinkedIn</a><a href="{TIMER_APP}">Toastmasters Timer</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
    <div class="legal">&copy; 2026 Theekshana Prabodha. Toastmasters International names and logos belong to Toastmasters International.</div>
  </div>
</footer>
<script src="{root}site.js" defer></script>
</body>
</html>
'''
    (D / fname).write_text(html)


# ---------------------------------------------------------------- data
SHOT = "assets/shots/"
TIMER = "assets/timer/"
COVER = "assets/covers/"

PROJECTS = [
    dict(slug="timer.html", title="Toastmasters Timer", cats=["software", "devops"], img=TIMER + "timer-green.png", feature=True,
         blurb="A live meeting timer for the club Timer: full-screen colour cards, a speaker roster and a print-ready A4 report. Used at real club meetings, with accounts and a GitHub Actions deploy.",
         stack=["PHP", "MySQL", "Docker", "GitHub Actions"], code="https://github.com/HomemadeICT/toastmasters-timer", live=TIMER_APP),
    dict(slug="petty-cash.html", title="Petty Cash Management System", cats=["software"], img=COVER + "cover-petty-cash.png",
         blurb="A desktop app for the Ceylon Electricity Board, Haliela branch, replacing a manual ledger. Business-rule engine, 22+ permissions, audit log, Sinhala and English reports.",
         stack=["VB.NET", "SQLite", ".NET 8"], code="https://github.com/HomemadeICT/Petty-Cash-Management-System-Standalone-Deployable-Desktop-App-"),
    dict(slug="pos-inventory.html", title="POS and Inventory System", cats=["software", "devops"], img=COVER + "cover-pos-ims.png",
         blurb="A supermarket point of sale and stock system with three roles, receipts and reports. Runs with one docker-compose up.",
         stack=["PHP 8.2", "MySQL 8", "Docker", "Bootstrap"], code="https://github.com/HomemadeICT/NVQ-Level-5-POS-IMS"),
    dict(slug="packet-tracer-labs.html", title="Packet Tracer Networking Labs", cats=["networking"], img=COVER + "cover-packet-tracer-labs.png",
         blurb="15+ Cisco Packet Tracer labs with working .pkt files, from a first LAN to an enterprise design with VLANs, ACLs and SSH.",
         stack=["Cisco Packet Tracer", "VLAN", "DHCP/DNS"], code="https://github.com/HomemadeICT/networking-packet-tracer-labs"),
    dict(slug="network-lab.html", title="Network Lab 80: 3D Lab in a Box", cats=["networking"], img=SHOT + "lab80-overview.jpg", showcase=True,
         blurb="An interactive 3D model of an 80-workstation campus lab network: 4 VLANs, a Layer 3 core, DHCP relay, NAT and live packet animation. Orbit it, click any device, watch the traffic.",
         stack=["Three.js", "Cisco Packet Tracer", "VLAN", "NAT/PAT"], code="https://github.com/HomemadeICT/LAN-Proposal-Project", live="network-lab-80/", live_label="Launch 3D lab"),
    dict(slug=None, title="Certificate Management with Selenium Tests", cats=["software"], img=COVER + "cover-selenium-certificates.png",
         blurb="Certificate tracking and verification with an admin dashboard, tested end to end with Selenium WebDriver.",
         stack=["PHP", "MySQL", "Python", "Selenium"], code="https://github.com/HomemadeICT/Selenium-Automation-Mini-Project-PHP-Mysql-Project-Certificate-Management-System"),
    dict(slug=None, title="PHP and MySQL Micro Projects", cats=["software"], img=COVER + "cover-php-micro-projects.png",
         blurb="Small teaching projects: a school library system, an institute admission system and a certificate system.",
         stack=["PHP", "MySQL", "JavaScript"], code="https://github.com/HomemadeICT/PHP-MySQL-Micro-Projects"),
]


def pcard(p, home=False):
    w, h = dims(p["img"])
    tags = "".join(f'<span class="chip">{escape(s)}</span>' for s in p["stack"])
    links = []
    if p["slug"]:
        links.append(f'<a href="{p["slug"]}">Case study</a>')
    links.append(f'<a href="{p["code"]}">Code</a>')
    if p.get("live"):
        links.append(f'<a href="{p["live"]}">{p.get("live_label", "Live app")}</a>')
    cls = "pcard feature" if p.get("feature") and not home else "pcard"
    return (f'<article class="{cls} reveal" data-cats="{" ".join(p["cats"])}">'
            f'<img src="{p["img"]}" alt="" width="{w}" height="{h}" loading="lazy">'
            f'<div class="body"><div class="tags">{tags}</div><h3>{escape(p["title"])}</h3><p>{escape(p["blurb"])}</p>'
            f'<div class="links">{"".join(links)}</div></div></article>')


# ---------------------------------------------------------------- home
def home():
    cv = f'<a class="btn lg" href="{CV_FILE}">Download CV</a>' if CV_LIVE else ""
    hero = f'''<div class="wrap"><div class="hero">
  <div>
    <span class="eyebrow">Learn / Build / Grow</span>
    <h1>Hey, I'm Theekshana, welcome to TheekMind.</h1>
    <p class="lead">I'm an ICT learner and builder from Sri Lanka. I build practical systems, fix them properly, and write down what I learn so you can use it too.</p>
    {chips(["Junior Software Engineer", "Junior Web Developer", "Junior DevOps", "Sri Lanka or remote"])}
    <div class="btns"><a class="btn primary lg" href="projects.html">See my projects</a><a class="btn lg" href="contact.html">Contact me</a>{cv}</div>
    <p class="note">NDICT (NVQ Level 5) graduate, studying BIT at UCSC.</p>
  </div>
  <div class="collage" aria-hidden="true">
    <div class="frame back"><div class="bar"><i></i><i></i><i></i></div>{img(SHOT + "petty-dashboard.webp", "", lazy=False)}</div>
    <div class="frame front"><div class="bar"><i></i><i></i><i></i></div>{img(TIMER + "timer-green.png", "", lazy=False)}</div>
  </div>
</div></div>
<div class="wrap"><div class="stats">
  <div class="stat"><b>22+</b><span>separate permissions in the CEB petty cash app</span></div>
  <div class="stat"><b>15+</b><span>Cisco Packet Tracer labs with working files</span></div>
  <div class="stat"><b>1 command</b><span>starts the POS app, MySQL and phpMyAdmin in Docker</span></div>
  <div class="stat"><b>2 languages</b><span>Sinhala and English reports in the CEB app</span></div>
</div></div>'''

    featured = [p for p in PROJECTS if p["slug"] and not p.get("showcase")][:3]
    showcase = f'''<section class="block reveal alt"><div class="wrap"><div class="split">
<div class="prose"><span class="eyebrow">Interactive demo</span><h2>Walk through an 80-workstation network in 3D</h2>
<p>I designed a campus lab network in Cisco Packet Tracer, then built it as a 3D model you can orbit, zoom and click. See the VLANs, the Layer 3 core, the server room and live DHCP, routed and NAT traffic.</p>
<div class="btns"><a class="btn primary lg" href="network-lab-80/">Launch the 3D lab</a><a class="btn lg" href="network-lab.html">Read the case study</a></div></div>
<a class="frame" href="network-lab-80/" aria-label="Launch the 3D network lab"><div class="bar"><i></i><i></i><i></i></div>{img(SHOT + "lab80-overview.jpg", "3D model of the 80-workstation lab network with its VLAN-coloured labs")}</a>
</div></div></section>'''

    projects = sec("Selected projects", '<div class="projects">' + "".join(pcard(p, home=True) for p in featured) + "</div>"
                   '<p style="margin-top:24px"><a class="btn" href="projects.html">All projects</a></p>',
                   lead="Things I built for real users and for my studies. Each has a case study with the problem, the approach and the result.")

    skills = sec("What I work with", skills_html(short=True), alt=True,
                 lead="The tools I've actually used in the projects above.")

    tm = sec("Beyond code: communication", '''<div class="split"><div class="prose">
<p>Good engineers explain their work. I work on that in the <strong>Voice Your Dream Toastmasters Club</strong>, where I practise public speaking and design the club's marketing.</p>
<p>I also built the club's meeting timer, a web app the Timer runs on the projector, and I write about what I learn on the blog.</p>
<p><a href="timer.html">Read the Timer case study</a></p></div>
<div class="frame"><div class="bar"><i></i><i></i><i></i></div>''' + img(TIMER + "timer-red.png", "Full-screen red timer card from the Toastmasters Timer app") + "</div></div>")

    blog = sec("From the blog", f'''<div class="posts" id="latest-posts"><a class="post" href="{BLOG}"><span class="meta">Blog</span><h3>Read the TheekMind blog</h3><span style="color:var(--link);font-weight:600">Visit blogs.theekmind.com &rarr;</span></a></div>
<p style="margin-top:20px"><a href="{BLOG}">All articles</a></p>''',
               lead="Clear, practical notes on networking, development, Linux and learning.")

    ld = {"@context": "https://schema.org", "@type": "Person", "name": "Theekshana Prabodha", "url": SITE + "/",
          "email": EMAIL, "sameAs": [GITHUB, LINKEDIN, BLOG], "image": SITE + "/assets/favicon-512.png",
          "knowsAbout": ["PHP", "MySQL", "Docker", "Linux", "Cisco networking", "VB.NET"]}
    page("index.html", "Theekshana Prabodha | TheekMind", "Portfolio of Theekshana Prabodha, an ICT learner and builder from Sri Lanka: PHP, MySQL, Docker, Linux and networking projects.",
         hero + showcase + projects + skills + tm + blog + cta(), jsonld=ld)


SKILLS = [
    ("Languages", ["PHP", "VB.NET", "JavaScript", "Python", "SQL", "HTML & CSS"]),
    ("Data", ["MySQL", "SQLite", "phpMyAdmin"]),
    ("Linux & DevOps", ["Linux (Ubuntu)", "Docker", "Docker Compose", "Git & GitHub", "GitHub Actions"]),
    ("Networking", ["Cisco Packet Tracer", "VLAN & VTP", "Inter-VLAN routing", "DHCP & DNS", "Port security", "ACL & SSH"]),
    ("Quality", ["Selenium WebDriver", "Unit & integration testing", "Audit logging", "Role-based access"]),
    ("Communication", ["Toastmasters", "Technical writing", "Public speaking", "Marketing design"]),
]


def skills_html(short=False):
    groups = SKILLS[:4] if short else SKILLS
    return '<div class="skills">' + "".join(
        f'<div class="skill"><h3>{g}</h3><ul>' + "".join(f"<li>{escape(i)}</li>" for i in items) + "</ul></div>"
        for g, items in groups) + "</div>"


# ---------------------------------------------------------------- projects index
def projects_page():
    filt = ('<div class="filters" id="filters" hidden role="group" aria-label="Filter projects">'
            '<button type="button" data-filter="all" aria-pressed="true">All</button>'
            '<button type="button" data-filter="software" aria-pressed="false">Software</button>'
            '<button type="button" data-filter="networking" aria-pressed="false">Networking</button>'
            '<button type="button" data-filter="devops" aria-pressed="false">DevOps</button></div>')
    body = f'''<div class="wrap"><div class="cs-hero" style="padding-top:56px"><span class="eyebrow">Work</span><h1>Projects</h1>
<p class="lead">Software, networking and web projects I built while learning, with the code on GitHub. Five of them have full case studies.</p></div></div>
<section class="block" style="border-top:0;padding-top:0"><div class="wrap">{filt}<div class="projects">{"".join(pcard(p) for p in PROJECTS)}</div></div></section>'''
    page("projects.html", "Projects | TheekMind", "Software, networking and DevOps projects by Theekshana Prabodha, with case studies and code.", body + cta(), nav="projects.html")


# ---------------------------------------------------------------- about
def about():
    exp = '''<ul class="timeline">
<li><h3>On-the-job trainee, Ceylon Electricity Board (Haliela branch)</h3><span class="when">NDICT work placement</span>
<p>Replaced the branch's manual petty cash ledger with a desktop app that enforces the branch's spending rules and prints the official monthly report in Sinhala and English.</p></li>
<li><h3>Member, Voice Your Dream Toastmasters Club</h3><span class="when">Ongoing</span>
<p>Public speaking, club marketing design, and building the meeting timer the club uses.</p></li>
</ul>'''
    edu = '''<ul class="timeline">
<li><h3>BIT, University of Colombo School of Computing (UCSC)</h3><span class="when">In progress</span>
<p>Semester projects and self-study notes across software, networking and communication courses.</p></li>
<li><h3>NDICT, NVQ Level 5</h3><span class="when">Completed</span>
<p>Software development and networking. My POS and Inventory System and the Packet Tracer labs come from this course.</p></li>
</ul>'''
    body = f'''<div class="wrap"><div class="cs-hero" style="padding-top:56px"><span class="eyebrow">About</span><h1>I build practical systems and explain them clearly.</h1>
<p class="lead">I'm Theekshana Prabodha, an ICT learner and builder from Sri Lanka. I hold the NDICT (NVQ Level 5) and I'm studying for the BIT at UCSC.</p></div></div>''' + \
        sec("My story", prose('''<p>I learn by building things that someone actually uses. At the Ceylon Electricity Board I turned a paper ledger into an app with real business rules. For my NDICT I built a supermarket POS that starts with one Docker command, and a book of networking labs you can open and break.</p>
<p>On my own Linux machine I troubleshoot problems down to the cause and write them up. TheekMind is where I share that, in plain words, so the next person saves time.</p>
<p>I'm looking for a junior software, web or DevOps role, in Sri Lanka or remote.</p>''')) + \
        sec("Skills", skills_html(), alt=True, lead="Grouped by what I've used in the projects, not by what I've read about.") + \
        sec("Experience", exp) + sec("Education", edu, alt=True) + cta()
    page("about.html", "About | TheekMind", "About Theekshana Prabodha: NDICT graduate, BIT student at UCSC, builder of practical PHP, VB.NET, Docker and networking projects.", body, nav="about.html")


# ---------------------------------------------------------------- contact
def contact():
    cv = f'<li><b>CV</b><a href="{CV_FILE}">Download as PDF</a></li>' if CV_LIVE else ""
    body = f'''<div class="wrap"><div class="cs-hero" style="padding-top:56px"><span class="eyebrow">Contact</span><h1>Let's talk.</h1>
<p class="lead">I'm open to junior software engineer, web developer and DevOps roles in Sri Lanka or remote. Email is the quickest way to reach me.</p></div></div>
<section class="block" style="border-top:0;padding-top:0"><div class="wrap"><div class="prose"><ul class="contact-list">
<li><b>Email</b><a href="mailto:{EMAIL}">{EMAIL}</a></li>
<li><b>LinkedIn</b><a href="{LINKEDIN}">Theekshana Prabodha</a></li>
<li><b>GitHub</b><a href="{GITHUB}">HomemadeICT</a></li>
<li><b>Blog</b><a href="{BLOG}">blogs.theekmind.com</a></li>
{cv}</ul></div></div></section>'''
    page("contact.html", "Contact | TheekMind", "Contact Theekshana Prabodha for junior software, web or DevOps roles.", body, nav="contact.html")


# ---------------------------------------------------------------- case studies
def case(fname, title, tagline, tags, facts, buttons, sections, hero_rel=None, hero_alt="", next_=None, desc=""):
    btns = "".join(f'<a class="btn{" primary" if i == 0 else ""} lg" href="{u}">{l}</a>' for i, (l, u) in enumerate(buttons))
    fl = "".join(f"<li><b>{k}</b>{v}</li>" for k, v in facts)
    hero = f'''<div class="wrap"><p class="crumbs"><a href="projects.html">&larr; All projects</a></p>
<div class="cs-hero"><span class="eyebrow">Case study</span><h1>{title}</h1><p class="lead">{tagline}</p>{chips(tags)}
<div class="btns">{btns}</div></div>
<ul class="facts">{fl}</ul></div>'''
    if hero_rel:
        hero += f'<div class="wrap" style="padding-top:32px"><div class="frame">{img(hero_rel, hero_alt, lazy=False)}</div></div>'
    nxt = ""
    if next_:
        nxt = f'<div class="wrap"><div class="next"><a href="projects.html">&larr; All projects</a><a href="{next_[1]}">{next_[0]} &rarr;</a></div></div>'
    page(fname, f"{title} | TheekMind", desc or tagline, hero + "".join(sections) + cta() + nxt, nav="projects.html")


def timer_case():
    sections = [
        sec("The problem", prose('''<p>Toastmasters meetings are time-sensitive. Agendas change at the last minute, speakers swap places, and the Timer has to signal the whole room without losing focus. Paper sheets invite errors, and a generic stopwatch knows nothing about roles or thresholds.</p>
<p>I built this to fix three things: a flexible roster, colour signals everyone can see, and an automatic report.</p>''')),
        sec("How it works", gallery([
            (TIMER + "timer-green.png", "Full-screen green timer card", "The whole tab turns green, yellow or red at each role's thresholds, readable from across the room."),
            (TIMER + "timer-yellow.png", "Full-screen yellow timer card", "Yellow: the speaker should be wrapping up."),
            (TIMER + "timer-red.png", "Full-screen red timer card", "Red: time is up.")]) + '<div class="grid cols-3" style="margin-top:28px">'
            '<div class="card"><h3>Colour cards</h3><p>Role-specific thresholds drive a full-screen card everyone in the room can read.</p></div>'
            '<div class="card"><h3>Flexible roster</h3><p>Type a sequence number to move anyone; conflicts resolve automatically. Edit names, roles and times inline.</p></div>'
            '<div class="card"><h3>Round Robin</h3><p>A 20-second limit with a single clean red cue and no early alerts.</p></div>'
            '<div class="card"><h3>A4 report</h3><p>One click gives a print-ready report with out-of-time highlighting.</p></div>'
            '<div class="card"><h3>Custom roles</h3><p>Save your own event types, such as a Q&amp;A session, with their own thresholds.</p></div>'
            '<div class="card"><h3>Accounts and limits</h3><p>Each user sees only their own meetings. Retention limits and export-before-delete keep free hosting tidy.</p></div></div>', alt=True),
        sec("Setting up a meeting", gallery([
            (TIMER + "meetings.png", "Create a meeting", "Create a meeting."),
            (TIMER + "roster.png", "Speaker roster", "Build and reorder the roster.")])),
        sec("Timing rules", table(["Role", "Green", "Yellow", "Red"], [
            ["Prepared Speech", "5:00", "6:00", "7:00"], ["Ice Breaker Speech", "4:00", "5:00", "6:00"],
            ["Table Topic", "1:00", "1:30", "2:00"], ["Evaluator", "2:00", "2:30", "3:00"],
            ["Round Robin", "n/a", "n/a", "0:20"], ["Custom", "configurable", "configurable", "configurable"]]), alt=True),
        sec("The report", '<div style="max-width:560px">' + fig(TIMER + "report.png", "Print-ready A4 timer report", "The A4 report, ready to print or save as PDF.") + "</div>"),
        sec("Under the hood", prose('''<ul><li>Plain PHP, JavaScript and CSS, with no framework to maintain.</li>
<li>The stopwatch runs in the browser, so timing does not depend on the network.</li>
<li>Thresholds come from role definitions stored in the database.</li>
<li>Docker Compose for a one-command local setup; deployed to shared hosting by a GitHub Actions FTP job.</li>
<li>Hardened for shared hosting: blocked source folders, HTTPS redirect, per-account data.</li></ul>
<p class="small">Screenshots show sample data and the Toastmasters International logo, which belongs to Toastmasters International.</p>'''), alt=True),
    ]
    case("timer.html", "Toastmasters Timer", "A web app that lets the club Timer run live meeting timing, manage the speaker roster and print the report, all from a browser on a projector screen.",
         ["PHP", "MySQL", "Docker", "GitHub Actions"],
         [("Role", "Designer and developer"), ("Used for", "Voice Your Dream Toastmasters Club meetings"), ("Stack", "PHP 8.2, MySQL, Docker"), ("Hosting", "Shared hosting via GitHub Actions FTP")],
         [("Open the app", TIMER_APP), ("View the code", "https://github.com/HomemadeICT/toastmasters-timer")], sections,
         next_=("Petty Cash Management System", "petty-cash.html"),
         desc="A web app for live Toastmasters meeting timing: colour cards, speaker roster and A4 reports.")


def petty_case():
    s = [
        sec("The problem", prose('''<p>During my on-the-job training at the Ceylon Electricity Board (CEB), Haliela branch, petty cash was tracked in a manual ledger. Every expense had to respect fixed limits, every month needed a printed report in the official format, and mistakes were hard to trace.</p>
<p>I built a desktop app to replace that ledger. It was also part of my NDICT (NVQ Level 5) assessment.</p>''')),
        sec("What it does", gallery([
            (SHOT + "petty-dashboard.webp", "Petty cash dashboard", "The dashboard: this month's total, the remaining balance and spending by category."),
            (SHOT + "petty-add-expense.webp", "Adding an expense", "Expense entry: the app blocks a wrong entry before it is saved.")]) +
            prose('''<ul style="margin-top:24px"><li><strong>Expense entry with rules</strong> that mirror how the branch handles petty cash.</li>
<li><strong>Monthly reports</strong> in Sinhala and English in the official CEB format, ready to print.</li>
<li><strong>Excel export</strong> with live formulas.</li>
<li><strong>Users and permissions:</strong> role-based access with 22+ separate permissions.</li>
<li><strong>Audit log</strong> of every action, <strong>backup and restore</strong>, and a <strong>setup wizard</strong> that installs it as a normal Windows app.</li></ul>'''), alt=True),
        sec("The business rules", prose('''<p>The rules engine is the heart of the app. They come straight from how the branch handles petty cash:</p>
<ul><li>The monthly total cannot go over <strong>LKR 25,000</strong>.</li><li>A single bill cannot go over <strong>LKR 5,000</strong>.</li>
<li>Amounts must be positive, bill numbers cannot repeat, and dates cannot be in the future.</li></ul>''')),
        sec("How it is built", prose('''<p>A 3-tier architecture keeps the screens away from the database: Windows Forms screens, a business logic layer of services that apply the rules, and a data access layer of repositories over SQLite. SQLite keeps it fully offline with zero configuration, which suits a branch office with no server.</p>''') +
            table(["Part", "Technology"], [["Language", "VB.NET (.NET 8)"], ["UI", "Windows Forms"], ["Database", "SQLite 3"], ["Passwords", "BCrypt.Net-Next (hashing)"], ["Excel export", "ClosedXML"], ["Installer", "Inno Setup 6"]]), alt=True),
        sec("Reports and administration", gallery([
            (SHOT + "petty-report.webp", "Monthly report", "The monthly report prints cleanly in Sinhala or English."),
            (SHOT + "petty-permissions.webp", "Permissions manager", "Administrators choose exactly what each user can do."),
            (SHOT + "petty-audit.webp", "Audit log", "The audit log shows who did what and when.")])),
        sec("How I built it", prose('''<p>I developed it with significant help from AI pair programming (Gemini / Antigravity). The repository includes a development journey that documents that process, plus requirements, business rules, architecture, a user manual and an administrator guide. The final release is <strong>v1.3.0</strong>.</p>'''), alt=True),
    ]
    case("petty-cash.html", "Petty Cash Management System", "A VB.NET and SQLite desktop app that replaced a manual petty cash ledger at the Ceylon Electricity Board, Haliela branch.",
         ["VB.NET", "SQLite", ".NET 8", "Windows Forms"],
         [("Role", "Sole developer"), ("Context", "CEB Haliela on-the-job training and NDICT assessment"), ("Stack", "VB.NET (.NET 8), SQLite"), ("Release", "v1.3.0")],
         [("View the code", "https://github.com/HomemadeICT/Petty-Cash-Management-System-Standalone-Deployable-Desktop-App-")], s,
         hero_rel=SHOT + "petty-dashboard.webp", hero_alt="Petty Cash Management dashboard", next_=("POS and Inventory System", "pos-inventory.html"),
         desc="A VB.NET and SQLite desktop app that replaced a manual petty cash ledger at the Ceylon Electricity Board, Haliela branch.")


def pos_case():
    s = [
        sec("What I built", prose('''<p>A web-based Point of Sale (POS) and Inventory Management System for a small, single-branch supermarket. I built it as my NVQ Level 5 (NDICT) software development portfolio project, to show the full lifecycle: requirements, design, a normalised database, role-based access, testing and deployment.</p>''')),
        sec("Features", gallery([
            (SHOT + "pos-dashboard.webp", "Admin dashboard", "The admin dashboard."),
            (SHOT + "pos-checkout.webp", "POS checkout", "Cart-based checkout at the point of sale."),
            (SHOT + "pos-products.webp", "Products list", "Products linked to categories and suppliers.")]) +
            prose('''<ul style="margin-top:24px"><li><strong>Session-based login</strong> with bcrypt password hashing.</li>
<li><strong>Stock control:</strong> stock IN and OUT transactions with a full audit trail.</li>
<li><strong>Point of sale</strong> with a cart and a printable receipt.</li>
<li><strong>Reports:</strong> low stock, daily sales and stock movement history, each with a print view.</li></ul>''') +
            table(["Role", "What they do"], [["Admin", "Full access: all modules, user management and reports"], ["Inventory Manager", "Manages stock, products and suppliers; views reports"], ["Cashier", "Processes sales at the POS; read-only on inventory"]]), alt=True),
        sec("Reports and receipts", gallery([
            (SHOT + "pos-reports.webp", "Reports hub", "The reports hub."),
            (SHOT + "pos-receipt.webp", "Receipt", "A printable receipt.")])),
        sec("How it is built", prose('''<p>Three Docker containers share one network: <code>web</code> (PHP 8.2 with Apache), <code>mysql</code> (MySQL 8.0 with a volume so data survives restarts) and <code>pma</code> (phpMyAdmin). The code is split into modules for products, categories, suppliers, transactions, sales, reports and users, with shared pieces for the database connection, access control and audit logging. One <code>schema.sql</code> is the source of truth for the database.</p>''') +
            table(["Layer", "Technology"], [["Backend", "PHP 8.2"], ["Database", "MySQL 8.0"], ["Frontend", "Bootstrap 5, Chart.js"], ["Auth", "PHP sessions and bcrypt"], ["Deployment", "Docker and Docker Compose"]]), alt=True),
        sec("What it demonstrates", prose('''<ul><li>The software development lifecycle using the V-Model.</li><li>A database designed to third normal form (3NF).</li>
<li>CRUD operations behind role-based access control.</li><li>SOLID principles applied practically.</li>
<li>Unit, integration, system and user acceptance testing.</li><li>Containerised deployment with Docker.</li></ul>''')),
        sec("Run it yourself", prose('''<p>With Docker installed:</p><pre><code>git clone https://github.com/HomemadeICT/NVQ-Level-5-POS-IMS.git
cd NVQ-Level-5-POS-IMS
docker-compose up -d</code></pre><p>Then open <code>http://localhost:8080</code>. The repository includes twelve documentation chapters, from requirements and database design to testing and a user manual.</p>'''), alt=True),
    ]
    case("pos-inventory.html", "POS and Inventory Management System", "A supermarket point of sale and stock system in PHP, MySQL and Docker, built as my NVQ Level 5 portfolio project.",
         ["PHP 8.2", "MySQL 8", "Docker", "Bootstrap 5"],
         [("Role", "Sole developer"), ("Context", "NDICT (NVQ Level 5) portfolio project"), ("Stack", "PHP 8.2, MySQL 8, Docker"), ("Roles", "Admin, Inventory Manager, Cashier")],
         [("View the code", "https://github.com/HomemadeICT/NVQ-Level-5-POS-IMS")], s,
         hero_rel=SHOT + "pos-dashboard.webp", hero_alt="POS admin dashboard", next_=("Packet Tracer Networking Labs", "packet-tracer-labs.html"),
         desc="A supermarket POS and inventory system in PHP, MySQL and Docker with role-based access, receipts and reports.")


def labs_case():
    s = [
        sec("What this is", prose('''<p>While studying for my NDICT (NVQ Level 5), I turned my networking practicals into a practical book in Cisco Packet Tracer: 15+ labs and projects, from a first LAN to a full enterprise network design.</p>
<p>Every lab comes with the <code>.pkt</code> file, so you can open a working network, read the configuration, break it and fix it. Each lab also has its own step-by-step guide with verification commands.</p>''')),
        sec("The sections", table(["Section", "What it covers", "Labs"], [
            ["Basic connectivity", "LAN topology and routing basics", "1"], ["Network services", "DHCP, DNS, web and mail servers", "5"],
            ["VLANs and switching", "VLANs, VTP and inter-VLAN routing", "4"], ["Security and remote access", "Telnet and port security", "2"],
            ["Wireless and IoT", "Wi-Fi and smart devices", "2"], ["Final projects", "Enterprise design and an 80-workstation proposal", "2"]]), alt=True),
        sec("Highlights", gallery([
            (SHOT + "lab-basic.webp", "One router, four switches and eight PCs", "Lab 1: one router, four switches and eight PCs on 192.168.1.0/24."),
            (SHOT + "lab-dhcp.webp", "DHCP server lab", "A DHCP server that hands out addresses automatically."),
            (SHOT + "lab-vlan.webp", "VLANs on a managed switch", "VLANs: devices in the same VLAN can ping, devices in different VLANs cannot."),
            (SHOT + "lab-rots.webp", "Router on a stick", "Router-on-a-stick: inter-VLAN routing through one interface with 802.1Q subinterfaces."),
            (SHOT + "lab-portsec.webp", "Port security", "Port security: an unauthorised PC is blocked from a switch port."),
            (SHOT + "lab-capstone.webp", "TechNova enterprise network", "The capstone: a hierarchical enterprise design.")])),
        sec("Capstone and the 80-workstation design", prose('''<p>The <strong>TechNova enterprise network</strong> is a hierarchical design for a fictional mid-sized company: VLANs per department, routing, port security, ACLs, SSH, network services and wireless. My NVQ final proposal, a <strong>network lab for 80 workstations</strong> for an IT institute with three computer labs, is in its own repository with a cost estimate.</p>
<p><a href="network-lab.html">Explore the 80-workstation network in 3D</a> &middot; <a href="https://github.com/HomemadeICT/LAN-Proposal-Project">proposal on GitHub</a></p>'''), alt=True),
        sec("How to use the labs", prose('''<ol><li>Get Cisco Packet Tracer free from Cisco Networking Academy (the labs use 8.1 or newer).</li>
<li>Clone the repository or download it as a ZIP.</li><li>Open a lab folder, double-click the <code>.pkt</code> file and follow that folder's guide.</li></ol>
<p>Tip: use Simulation mode to watch packets move hop by hop, and break a lab on purpose, then use the <code>show</code> commands from the guide to find the fault.</p>''')),
    ]
    case("packet-tracer-labs.html", "Packet Tracer Networking Labs", "15+ Cisco Packet Tracer labs with working files and step-by-step guides, from a first LAN to an enterprise design.",
         ["Cisco Packet Tracer", "VLAN", "DHCP/DNS", "ACL & SSH"],
         [("Role", "Author"), ("Context", "NDICT (NVQ Level 5) networking practicals"), ("Tool", "Cisco Packet Tracer 8.1+"), ("Size", "15+ labs, each with a .pkt file")],
         [("View the labs", "https://github.com/HomemadeICT/networking-packet-tracer-labs")], s,
         hero_rel=SHOT + "lab-capstone.webp", hero_alt="TechNova enterprise network in Packet Tracer", next_=("Toastmasters Timer", "timer.html"),
         desc="15+ Cisco Packet Tracer labs covering DHCP, DNS, VLANs, inter-VLAN routing, port security and an enterprise design.")


def lab80_case():
    sections = [
        sec("The 3D lab", f'''<div class="frame"><div class="bar"><i></i><i></i><i></i></div>{img(SHOT + "lab80-overview.jpg", "3D overview of the lab: four rooms, VLAN-coloured PCs and the cabling")}</div>
<p class="small" style="margin-top:10px">A screenshot of the interactive model. <a href="network-lab-80/">Launch it</a> to orbit, zoom and click devices (best on a laptop).</p>'''),
        sec("What this is", prose('''<p>The network is my NVQ final proposal for an IT institute with three computer labs and a staff room: 80 PCs, 7 laptops and 3 printers on four VLANs, routed by a Layer 3 core switch, with one server for DHCP, DNS and web, and a router doing NAT/PAT to the internet.</p>
<p>I designed and tested it in Cisco Packet Tracer, then turned it into an interactive 3D model so anyone can explore it without installing anything.</p>''') , alt=True),
        sec("What you can do in the model", '''<div class="grid cols-3">
<div class="card"><h3>Fly around</h3><p>Orbit, pan and zoom, or jump to preset views: overview, staff room, server rack, each lab and the floor plan.</p></div>
<div class="card"><h3>Click any device</h3><p>Select a PC, switch, the router, the core switch or the server to see its configuration from the project.</p></div>
<div class="card"><h3>Watch traffic</h3><p>Run a live simulation of DHCP, inter-VLAN routing and internet (NAT) traffic, with counters for each.</p></div>
<div class="card"><h3>Peel the layers</h3><p>Toggle the glass case, walls, labels, PC numbers and each VLAN's cabling.</p></div>
<div class="card"><h3>Preview the ACLs</h3><p>Switch on the planned lab-isolation policy and see which flows would be dropped.</p></div>
<div class="card"><h3>Read the design</h3><p>IP plan, security matrix, hardware list and the configuration order are in the side panel.</p></div></div><div style="height:28px"></div>''' + gallery([
            (SHOT + "lab80-staff-server.jpg", "Staff room and server room", "The staff room and server room: router, core switch, server and the ISP link."),
            (SHOT + "lab80-hardware.jpg", "Hardware lab and NDICT lab", "The hardware lab (VLAN 10) with its access switch, and the NDICT lab beside it.")])),
        sec("Addressing plan", table(["VLAN", "Lab", "Subnet", "Gateway (SVI)", "PCs"], [
            ["10", "Hardware", "192.168.10.0/24", "192.168.10.1", "15 + laptop"], ["20", "NDICT", "192.168.20.0/24", "192.168.20.1", "35 + laptop, printer"],
            ["30", "Graphics", "192.168.30.0/24", "192.168.30.1", "30 + laptop, printer"], ["40", "Staff and servers", "192.168.40.0/24", "192.168.40.1", "server .5, router LAN .254"]]) +
            prose('''<p>DHCP pools start at .10 (245 hosts per VLAN) and a relay (<code>ip helper-address</code>) on the core switch forwards requests to the server. The router's WAN side is 203.0.113.1/30.</p>'''), alt=True),
        sec("Security policy", prose('''<p>Each lab is isolated from the others and every lab can reach the staff and server VLAN. The ACLs are documented as a planned step (the 3D model lets you preview their effect), and port security (sticky MAC, restrict) is tested on the hardware lab switch.</p>''') +
            table(["From \\ To", "HW (10)", "NDICT (20)", "GFX (30)", "Staff/Net (40)"], [
                ["HW (10)", "n/a", "deny", "deny", "permit"], ["NDICT (20)", "deny", "n/a", "deny", "permit"],
                ["GFX (30)", "deny", "deny", "n/a", "permit"], ["Staff (40)", "permit", "permit", "permit", "permit"]])),
        sec("Physical design", prose('''<ul><li><strong>Building:</strong> 7 m wide. Staff and server room 2.8 m, hardware lab 6 m, NDICT lab 8.8 m, graphics lab 11.8 m, with 30 cm walls between labs.</li>
<li><strong>Distributed access switches</strong> per lab keep every Cat6 run well under 100 m, with one trunk uplink per lab along the wall.</li>
<li><strong>Hardware list:</strong> TP-Link TL-ER6120 dual-WAN VPN router; TL-SG3428 24-port and TL-SG2218 16-port managed switches; 6U wall rack with cooling fans, PDU and a 650 VA UPS; Cat6 cable, keystone jacks, faceplates and trunking.</li></ul>'''), alt=True),
        sec("Configuration order", prose('''<ol><li>DHCP server pools</li><li>Core switch: <code>ip routing</code>, SVIs, relay, trunks</li><li>Access switches</li><li>End devices (DHCP)</li><li>Router WAN and NAT/PAT</li><li>ACLs</li><li>SSH</li><li>Port security rollout</li><li>End-to-end verification</li></ol>''')),
        sec("How the viewer is built", prose('''<p>The whole model is one HTML file that uses <a href="https://threejs.org">Three.js</a> (loaded from a CDN) for the 3D scene, with no build step and no backend. It runs entirely in your browser.</p>
<p><a href="https://github.com/HomemadeICT/networking-packet-tracer-labs">Packet Tracer labs on GitHub</a> &middot; <a href="https://github.com/HomemadeICT/LAN-Proposal-Project">80-workstation proposal on GitHub</a></p>'''), alt=True),
    ]
    case("network-lab.html", "Network Lab 80: 3D Lab in a Box", "An interactive 3D model of an 80-workstation campus lab network, designed in Cisco Packet Tracer: VLANs, a Layer 3 core, DHCP relay, NAT and live traffic.",
         ["Three.js", "Cisco Packet Tracer", "VLAN", "NAT/PAT"],
         [("Role", "Network designer"), ("Context", "NDICT (NVQ Level 5) final proposal"), ("Scale", "80 PCs, 7 laptops, 3 printers, 4 VLANs"), ("Tools", "Cisco Packet Tracer, Three.js")],
         [("Launch the 3D lab", "network-lab-80/"), ("View the code", "https://github.com/HomemadeICT/LAN-Proposal-Project")], sections,
         next_=("Toastmasters Timer", "timer.html"),
         desc="Interactive 3D model of an 80-workstation campus lab network: VLANs, Layer 3 core switching, DHCP relay, NAT and live packet animation.")


def not_found():
    body = '''<div class="wrap"><div class="cs-hero" style="padding:96px 0"><span class="eyebrow">404</span><h1>Page not found</h1>
<p class="lead">That page doesn't exist. Try the <a href="/">home page</a>, the <a href="/projects.html">projects</a> or the <a href="https://blogs.theekmind.com">blog</a>.</p></div></div>'''
    page("404.html", "Page not found | TheekMind", "Page not found.", body, root="/")


def sitemap():
    urls = ["", "projects.html", "about.html", "contact.html", "network-lab-80/"] + [p["slug"] for p in PROJECTS if p["slug"]]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
          "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    (D / "sitemap.xml").write_text(xml)


if __name__ == "__main__":
    home(); projects_page(); about(); contact()
    timer_case(); petty_case(); pos_case(); labs_case(); lab80_case()
    not_found(); sitemap()
    print("built", len(list(D.glob("*.html"))), "pages; CV linked:", CV_LIVE)
