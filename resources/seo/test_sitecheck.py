import unittest

import sitecheck as sc

BLOGGER_ROBOTS = """User-agent: Mediapartners-Google
Disallow:

User-agent: *
Disallow: /search
Allow: /

Sitemap: https://blogs.theekmind.com/sitemap.xml
Sitemap: https://theekmind.com/sitemap.xml
"""

# Shape of the live v2.9 post page: BlogPosting in <head>, where data:post is out of scope.
BROKEN_POST = """<html><head><title>Theekmind: Putting My Portfolio</title>
<link href='https://blogs.theekmind.com/2026/11/p.html' rel='canonical'/>
<meta content='Theekmind' property='og:site_name'/>
<script type='application/ld+json'>{"@type":"BlogPosting","headline":"<!--Can't find substitution for tag [post.title.escaped]-->","author":{"@type":"Person","name":"T"}}</script>
</head><body></body></html>"""

GOOD_HOME = """<html><head><title>Theekshana Prabodha | TheekMind</title>
<link rel="canonical" href="https://theekmind.com/">
<meta name="robots" content="index,follow">
<meta property="og:site_name" content="TheekMind">
<script type="application/ld+json">{"@context":"https://schema.org","@graph":[{"@type":"Person","@id":"https://theekmind.com/#person","name":"Theekshana Prabodha"},{"@type":"WebSite","url":"https://theekmind.com/","publisher":{"@id":"https://theekmind.com/#person"}}]}</script>
</head></html>"""


class RobotsTest(unittest.TestCase):
    def test_star_group_and_sitemaps(self):
        sitemaps, disallow = sc.parse_robots(BLOGGER_ROBOTS)
        self.assertEqual(disallow, ["/search"])
        self.assertEqual(len(sitemaps), 2)

    def test_shared_agent_group(self):
        _, disallow = sc.parse_robots("User-agent: Bingbot\nUser-agent: *\nDisallow: /api/\n")
        self.assertEqual(disallow, ["/api/"])

    def test_other_agent_ignored(self):
        _, disallow = sc.parse_robots("User-agent: BadBot\nDisallow: /\n\nUser-agent: *\nAllow: /\n")
        self.assertEqual(disallow, [])


class SitemapTest(unittest.TestCase):
    def test_locs(self):
        xml = "<?xml version='1.0' encoding='UTF-8'?><urlset xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'><url><loc>https://a/</loc></url><url><loc> https://a/b </loc></url></urlset>"
        self.assertEqual(sc.parse_sitemap(xml), ["https://a/", "https://a/b"])


class PageTest(unittest.TestCase):
    def test_broken_blogger_ld_is_caught(self):
        f = sc.page_facts(BROKEN_POST)
        self.assertEqual(f["site_name"], "Theekmind")
        self.assertEqual(sc.ld_problems(f["ld"]), ["BlogPosting.headline"])
        self.assertFalse(sc.refs_person(f["ld"], "https://theekmind.com/#person"))

    def test_good_home(self):
        f = sc.page_facts(GOOD_HOME)
        self.assertEqual(f["canonical"], "https://theekmind.com/")
        self.assertFalse(f["noindex"])
        self.assertEqual(len(f["ld"]), 2)
        self.assertEqual(sc.ld_problems(f["ld"]), [])
        self.assertTrue(sc.refs_person(f["ld"], "https://theekmind.com/#person"))

    def test_noindex_and_bad_json(self):
        f = sc.page_facts('<meta name="robots" content="NOINDEX"><script type="application/ld+json">{bad</script>')
        self.assertTrue(f["noindex"])
        self.assertEqual(len(f["ld_errors"]), 1)

    def test_challenge(self):
        self.assertTrue(sc.is_challenge('<script src="/aes.js"></script>document.cookie="__test=..."'))
        self.assertFalse(sc.is_challenge("User-agent: *"))


if __name__ == "__main__":
    unittest.main()
