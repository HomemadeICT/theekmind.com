# theekmind.com: GitHub Pages + Cloudflare

Site root is `docs/` (Pages source: branch `main`, folder `/docs`). `resources/` holds brand and content source material and is **not** published.

Current state (checked 2026-11-12): the domain's nameservers are already Cloudflare (`zod` / `autumn`.ns.cloudflare.com); the apex `theekmind.com` has no A/AAAA records yet; `blogs.theekmind.com` is the Blogger blog and must not be touched.

## 1. Repo
GitHub Pages on a free plan needs a **public** repo (private needs a paid plan). The site holds nothing secret.

```bash
cd ~/projects/theekmind.com
git init -b main
git add . && git commit -m "Initial site"
gh repo create HomemadeICT/theekmind.com --public --source=. --push
```

## 2. Pages
```bash
gh api -X POST repos/HomemadeICT/theekmind.com/pages \
  -f 'source[branch]=main' -f 'source[path]=/docs'
gh api -X PUT repos/HomemadeICT/theekmind.com/pages -f cname=theekmind.com
```
`docs/CNAME` already says `theekmind.com`. After DNS validates (step 4): `gh api -X PUT repos/HomemadeICT/theekmind.com/pages -F https_enforced=true`.

## 3. Cloudflare DNS (zone theekmind.com, DNS tab)
Set every record below to **DNS only** (grey cloud) until GitHub has issued the HTTPS certificate.

| Type | Name | Content |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| AAAA | `@` | `2606:50c0:8000::153` |
| AAAA | `@` | `2606:50c0:8001::153` |
| AAAA | `@` | `2606:50c0:8002::153` |
| AAAA | `@` | `2606:50c0:8003::153` |
| CNAME | `www` | `homemadeict.github.io` |

Leave the `blogs` record alone (Blogger).

Recommended: verify the domain on GitHub (Settings, Pages, Add a domain) so nobody else can claim it; add the `_github-pages-challenge-HomemadeICT` TXT record it shows.

## 4. Check
```bash
dig +short theekmind.com A
dig +short www.theekmind.com CNAME
gh api repos/HomemadeICT/theekmind.com/pages | grep -E 'status|https_enforced|cname'
curl -I https://theekmind.com
```
GitHub issues the certificate a few minutes to an hour after DNS resolves.

## 5. Optional: turn the Cloudflare proxy on (orange cloud)
Only after HTTPS works. Set SSL/TLS mode to **Full (strict)** first, or you get redirect loops. Add a Redirect Rule `www.theekmind.com` to `https://theekmind.com` if you want one canonical host. The proxy hides GitHub's IPs and adds caching; purge the cache after each deploy if a change doesn't appear.

## Brand constraints
Palette, Inter weights 400/500/600, logo rules and voice are in `resources/brand/`. The header uses the badge plus the name as text, because no standalone horizontal lockup file exists in the vault; drop the official lockup into `docs/assets/` and swap it in when you have it (min 220px wide).

## Gaps to fill
- A social preview image (1200x630); `og:image` currently points at the 512px badge.
- Real About/Projects copy beyond the starter text in `resources/content/`.
- Contact email: `theekmind@gmail.com` (brand guide) vs `homemadeict@gmail.com` (dev default); confirm which goes public.
