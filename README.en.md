# master-blog

[![CI](https://github.com/system-conf/master-blog-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/system-conf/master-blog-skill/actions/workflows/ci.yml)

**English** · [Türkçe](README.md)

An end-to-end SEO/GEO content production skill for [Claude](https://claude.com/claude-code),
plus the documentation site that explains it.

> **Language note:** The skill's instructions, its 66-term glossary and the documentation
> site are written in **Turkish**. Claude reads them fine regardless of your own language,
> and the skill produces content in whatever language the project publishes in — but if you
> want to *maintain* or extend the skill, you'll be editing Turkish text. This README exists
> so you can decide that before installing.

## What it actually does

Most content tooling stops at "here is your draft". This skill runs the work **before** and
**after** the writing too — which is where content usually fails:

| # | Phase | Output |
|---|---|---|
| 0 | Project discovery | Framework, content source, **working mode**, project profile, preview directives |
| 1 | Topic + data rationale | A candidate topic *and* the data signal that justifies it |
| 1.5 | Archive decision | Write new, or refresh existing? (kicks in at 15+ posts) |
| 2 | Intent + SERP | Intent label and the right format for it |
| **3** | **CANNIBALIZATION GATE** | CLEAN / CHANGE ANGLE / UPDATE — overlap computed as a number **[cannot be skipped]** |
| 4 | Brief | A 16-line contract incl. 8-12 fan-out sub-questions — no body text without approval |
| 5-9 | Writing layers | SEO · GEO · E-E-A-T · linking · technical package |
| **10** | **SELF-AUDIT GATE** | 43 items; a red item stops publication **[cannot be skipped]** |
| 11 | Publish + verify | Build, deploy, live URL 200, publication report |
| 12 | Measurement | 14/28/90 days + a control group |

Three things it guarantees: **accuracy** (every technical claim comes from the project's own
data), **differentiation** (new content doesn't cannibalize existing rankings), and
**citability** (structured so both Google and AI engines can quote a block of it).

## Install

**As a plugin (recommended — versioned, receives updates):**

```
/plugin marketplace add system-conf/master-blog-skill
/plugin install master-blog@system-conf
```

**One command (always installs the current release):**

```bash
curl -fsSL https://system-conf.github.io/master-blog-skill/kur.sh -o kur.sh
less kur.sh     # 1.8 KB — don't run what you haven't read
sh kur.sh       # project-scoped: sh kur.sh --proje
```

We deliberately don't offer a `curl | sh` one-liner: an installer that encourages running
unread code would contradict our own security policy.

**No terminal at all** — one sentence to Claude Code:
*install skills/master-blog from github.com/system-conf/master-blog-skill into ~/.claude/skills/*

**As files:**

```bash
cp -r skills/master-blog ~/.claude/skills/          # personal, all projects
cp -r skills/master-blog <project>/.claude/skills/  # project-scoped, shared with the team
```

File installs never update. Since this skill's evidence log is re-verified every three
months, that difference matters more here than in a typical skill.

**Tune thresholds per project.** Don't edit `kontrol.py` — an update overwrites it. Put a
`master-blog.toml` in your project root instead:

```toml
[esikler]
IC_LINK_MIN = 2        # a new site doesn't have 4 pages to link to yet
KELIME_MIN  = 400
PARA_MAX_KELIME = 70
```

## Working mode — what happens without repo access

The skill reads files and runs commands. When it can't, some phases **cannot run**, and it
doesn't hide that:

| Mode | Condition | Result |
|---|---|---|
| **FULL** | Content files in the working directory (Astro, Next, Hugo, plain Markdown) | All phases |
| **LIMITED** | Content lives in a panel (WordPress, Wix, Shopify) | Cannibalization gate, mechanical check and live verification don't run |

In limited mode it never marks a gate as passed; it reports `NOT VERIFIABLE (limited mode)`.
Faking approval is worse than not checking at all.

## The mechanical checker

The measurable half of the 43-item gate isn't left to judgement:

```bash
python3 skills/master-blog/scripts/kontrol.py <post.md> --kelime "target keyword" --net
```

It counts: word count (excluding frontmatter, code and URLs), H1 count, heading-level jumps,
title and meta description length, keyword position in the title, slug format, ratio of
question-style H2s, internal link count, generic and duplicated anchor texts, external link
HTTP status, presence of a table and a summary section, image alt text, paragraph length.

Exit code **1** = blocker (usable in CI), **2** = usage error. What it deliberately does not
judge: search intent, cannibalization, source truthfulness, E-E-A-T. Those stay with the model.

## Evidence discipline

`skills/master-blog/references/kaynaklar.md` binds every **time-sensitive** claim to a dated
source, classified as `PRIMARY` (provider documentation), `MEASUREMENT` (third-party data,
with its sample size) or `INDUSTRY` (reported, no official announcement).

The skill's 12th red line enforces it: no claim about search engine behaviour enters the text
without a matching record, and a record older than three months must be re-verified. Every
external URL in that file has been checked with `curl` for a 200 response.

This exists because the field moves: FAQ rich results were removed on 7 May 2026, Search
Console's Generative AI report landed on 3 June 2026, and the `&num=100` removal on
12 Sept 2025 left a permanent discontinuity in Search Console data. Advice written before
those dates is quietly wrong today.

## Staying current

The skill reports its own age at the start of every session:

```bash
python3 skills/master-blog/scripts/surum-kontrol.py
```

`GUNCEL` (≤90 days) · `YENI SURUM` (a newer release exists) · `TAZELENMELI` (91-180 days,
refresh the evidence log before writing time-sensitive claims) · `ESKIMIS` (>180 days —
it warns and asks permission, and won't write unverified claims about search behaviour).

The published version is read from
<https://system-conf.github.io/master-blog-skill/surum.json>. Offline use is fine
(`--cevrimdisi`); that's reported, not treated as an error.

## Repository layout

```
.claude-plugin/             plugin.json + marketplace.json
agents/icerik-envanteri.md  inventory + overlap subagent (Haiku)
skills/master-blog/
  SKILL.md                  the 13-phase process, 2 gates, 12 red lines
  references/               writing layers · publishing & measurement · checklist ·
                            glossary (generated) · scenarios · sources
  scripts/kontrol.py        mechanical pre-publish checker
  scripts/surum-kontrol.py  version and knowledge-freshness check
  evals/evals.json          trigger and behaviour scenarios
site/                       template.html + data/terms.js (single source of truth)
  assets/                   favicon set, generated by tools/favicon-uret.py (no deps)
tests/                      11 regression tests, no dependencies
build.py                    terms.js + skill files -> docs/ + dist/
docs/                       GitHub Pages: 73 static pages, sitemap, robots
dist/artifact.html          single-file build (for Claude Artifacts, no HTML skeleton)
```

`build.py` produces two outputs because the two environments have opposite requirements:
`docs/` needs a real `<!doctype>`/`lang`/`viewport` skeleton and per-page URLs; the Artifact
runtime supplies its own skeleton and forbids writing `<html>`. Collapsing them into one file
is what broke mobile rendering once — don't.

## Development

```bash
python3 build.py            # docs/ + dist/ + generated glossary
python3 tests/calistir.py   # regression tests
```

Data validation is part of the build: a broken `related` slug, a duplicate slug, a missing
required field, an invalid level, an orphan term or an unescaped `${...}` in `terms.js` all
**stop the build** rather than passing silently.

See [CONTRIBUTING.md](CONTRIBUTING.md) (Turkish) · [SECURITY.md](SECURITY.md) ·
[CHANGELOG.md](CHANGELOG.md)

## Deliberate non-goals

- **`terms.js` was not moved to JSON.** `eval` is an injection sink in general, but the file
  read here is the repo's own source, not user input. JSON would bury multi-line prose in
  `\n` escapes and make hand-editing impractical. The real risk — missing validation — is
  solved in `build.py` instead.
- **No `og:image`.** Left absent rather than fabricated; social cards render without an image.
- **No full English translation.** 66 terms × 6 long fields plus a 19 KB `SKILL.md` is a
  permanent maintenance cost, not a one-off. This README is the exception because it's one
  file that rarely changes.

## License

MIT. Site: <https://system-conf.github.io/master-blog-skill/>
