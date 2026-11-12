# LinkedIn Content Strategy

Goal of my LinkedIn posts, and what I change so that the people I connect with ([[LinkedIn Connection Strategy]]) take me seriously.

## Goal
Get a **Junior Software Engineer, Junior Web Developer or DevOps Engineer** role in Sri Lanka or at a remote-first company.

Every post should leave a recruiter, hiring manager or architect thinking: *"This person builds real things, fixes real problems, and explains them clearly."*

Measure it by conversations, not likes: recruiter messages, interview invites, and comments from people in my target tiers.

## Where I am now (2026-10-11)
- **Posts:** none. My activity shows only reposts.
- **Profile:** a good headline, "Open to work" (recruiters only), 340 followers. I could not see About, Experience, Education, Projects or Skills sections.
- **Connections:** about 46 new invites sent to architects, recruiters, DevOps leads and hiring managers. When they accept, the first thing they see is my profile and my latest posts.
- **Unused material:** six project write-ups in `Blog/Drafts`, and a lot of real Linux troubleshooting on my own machine.

**The problem:** new connections will look at my profile in the next 1–2 weeks. Right now it shows a headline and nothing to back it up.

## Step 1: Fix the profile first (this week)
Posts send people to my profile, so it has to show proof.

- [ ] **About**
  - Who I am: an ICT builder from Sri Lanka, NDICT (NVQ 5), studying BIT at UCSC.
  - What I build, with three proofs: CEB Petty Cash, POS + Docker, the 80-workstation network.
  - The roles I want.
  - Links to GitHub (HomemadeICT) and blogs.theekmind.com.
- [ ] **Experience:** the CEB Haliela on-the-job training, with the Petty Cash system as the main result.
- [ ] **Education:** BIT (UCSC, in progress) and NDICT (NVQ Level 5).
- [ ] **Featured:** the Petty Cash repo, the POS repo and the blog. Later, my best post.
- [ ] **Skills (top 5):** Linux, Docker, Git, PHP/MySQL, Networking (Cisco).
- [ ] **Check the headline claim** "Built & deployed a production app at CEB". Is the app actually in use at the branch? If yes, keep it and say so in the post. If not, change it to "Built a petty cash system for CEB". Being caught overclaiming does more damage than the claim helps.

## Step 2: Who the posts are for, and what impresses each group

| Who | What they look for | What to give them |
|---|---|---|
| **Recruiters** (Tier 2) | Role keywords, clear proof, someone active | The stack named in every project post (VB.NET, PHP, MySQL, Docker, Linux). Post consistently. Say plainly what roles I want. |
| **Hiring managers / CTOs** (Tier 1) | Someone who ships and owns problems | A real user (CEB), real constraints (business rules, Sinhala/English reports), testing, and deployment. What went wrong and how I fixed it. |
| **Architects / DevOps leads** (Tier 3) | Depth and judgement | Why I chose X over Y. Linux troubleshooting with the actual cause. Network design decisions such as VLANs. No buzzwords. |

## Step 3: Content pillars
These match the blog topics, so every post can link to a write-up.

1. **Project case studies.** Problem → what I built → one key decision → result → link. *(Projects / Development)*
2. **Fix logs.** A real Linux or DevOps problem I hit: symptom, cause, fix, lesson. This is the pillar that best supports "DevOps". *(Linux & DevOps)*
3. **Networking explained.** One design decision or concept, with a diagram. *(Networking & ICT)*
4. **Learning in public.** One BIT topic or study method, explained plainly. Toastmasters skills applied to tech. *(Learning & Communication)*

Rough mix: 40% projects, 30% fix logs, 15% networking, 15% learning.

## Rhythm
- **2 posts a week.** For example, Tuesday and Thursday mornings, Sri Lanka time. Consistency matters more than volume.
- **Comment on 3–5 posts a week** from people in my target tiers. Add a real point or question, not "Great post!". This is the fastest way to get noticed by people who just accepted my invite.
- **Write in English.** Recruiters at multinationals are part of the audience.
- **Format:** a hook line under 200 characters, short paragraphs, one screenshot or diagram, at most 3 hashtags, and the link in the post. Follow [[Voice and Messaging]].

## Rules
- Only real work and real numbers. Never invent results.
- One topic per post.
- Explain every acronym the first time it appears.
- Each post ends with something useful, or one honest question.
- Don't post about automating LinkedIn itself.

## First 8 posts (weeks 1–4)

| # | Post | Pillar | Source |
|---|---|---|---|
| 1 | Who I am and what I'm looking for: three things I've built, and the roles I want. Pin it. | Intro | About page draft |
| 2 | Replacing a paper ledger at CEB: business rules, audit log, Sinhala/English reports | Project | [[Petty Cash Management System for CEB Haliela]] |
| 3 | One command to run my POS system: what Docker changed for me | Project | [[POS and Inventory Management System with PHP, MySQL and Docker]] |
| 4 | Fix log: resizing a mounted root partition on Ubuntu (the partx trick) | Fix log | My disk merge work |
| 5 | Designing an 80-workstation network: why four VLANs and a multilayer core | Networking | [[Designing an 80-Workstation Network for an IT Institute]] |
| 6 | What my Selenium tests caught that I missed by hand | Project | [[Certificate Management System with Selenium Tests]] |
| 7 | Fix log: tuning a 15 W laptop CPU by doing less work, not raising power limits | Fix log | My ThinkPad power tuning |
| 8 | 16 Packet Tracer labs, free: how I turned NVQ practicals into a lab book | Networking | [[Networking Packet Tracer Labs]] |

Drafts go in `LinkedIn/Drafts` using `Templates/LinkedIn Post.md`. I post them myself.

## Check monthly
- Profile views and search appearances (LinkedIn dashboard)
- Acceptance rate of connection invites (the `sent-log.csv` from the connection skill)
- Recruiter messages and interview invites
- Comments from people in my target tiers
- Which pillar gets the most comments from those people. Do more of that.
