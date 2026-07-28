#!/usr/bin/env python3
"""Generate .claude-plugin/plugin.json per pack + the root marketplace.json.

Three pack layouts, three treatments:
  - `<pack>/skills/<skill>/`  -> default scan; no `skills` field needed
  - `<pack>/<skill>/` (flat)  -> explicit `skills` array, one entry per skill
  - `<pack>/SKILL.md`         -> auto single-skill plugin; no `skills` field
"""
import json, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PACKS = {
    "pm-frameworks": ("product-management",
        "43 battle-tested product management frameworks — PRDs, discovery, JTBD, opportunity solution trees, prioritization, roadmaps, story mapping, positioning, and SaaS metrics.",
        ["pm", "product-management", "prd", "discovery", "prioritization"]),
    "pm-agents": ("product-management",
        "Multi-agent PM system. /pm: commands for specs, strategy, opportunity discovery, simulation, and parallel six-agent review, over a compounding set of PM components.",
        ["pm", "multi-agent", "strategy", "spec-review"]),
    "thinking-tools": ("productivity",
        "Domain-agnostic reasoning primitives — relentless grilling, session handoff, background research, multi-session teaching, and wayfinding a foggy effort into decision tickets.",
        ["grilling", "thinking", "handoff", "research", "planning"]),
    "engineering-tools": ("engineering",
        "Engineering workflows in two families: advisory skills that produce an artifact (ADRs, test plans, postmortems) and flow skills that drive work through your issue tracker (spec, tickets, TDD, implement, triage).",
        ["engineering", "tdd", "code-review", "spec", "triage"]),
    "meta-tools": ("development",
        "Build and maintain your own toolkit — skill creation and editorial craft, ADRs, automation planning, frontend design, artifact building, and project bootstrapping.",
        ["meta", "skills", "automation", "tooling"]),
    "document-tools": ("productivity",
        "Create real document files — Word, PowerPoint, Excel, and PDF — with formatting, formulas, charts, and production-grade templates.",
        ["docx", "pptx", "xlsx", "pdf", "documents"]),
    "analytics-tools": ("data",
        "Quantitative analysis for data-driven product work — A/B test statistics, natural-language SQL generation, and cohort/retention analysis.",
        ["analytics", "ab-testing", "sql", "cohort"]),
    "gtm-tools": ("marketing",
        "Go-to-market execution — beachhead segment scoring, sales-ready competitive battlecards, and growth loop design.",
        ["gtm", "growth", "battlecard", "market-entry"]),
    "domain-tools": ("business",
        "Specialist founder/consultant workflows with executable Python — competitive teardowns, financial modeling, revenue operations, product marketing, and demand generation.",
        ["competitive-analysis", "finance", "revops", "marketing"]),
    "operations-tools": ("business",
        "Optimize business operations — vendor management, process documentation, change management, capacity planning, risk assessment, and compliance tracking.",
        ["operations", "process", "compliance", "risk"]),
    "sales-tools": ("business",
        "Prospect, craft outreach, and build deal strategy faster. Call prep, pipeline review, forecasting, and personalized messaging that moves deals forward.",
        ["sales", "pipeline", "outreach", "forecast"]),
    "design-tools": ("design",
        "Accelerate product design — critique, design system management, UX writing, accessibility audits, research synthesis, and developer handoff.",
        ["design", "ux", "accessibility", "research"]),
    "prd-partner": ("product-management",
        "Turn raw ideas into actionable PRDs. Discovery Mode sharpens thinking through a grilling session; PRD Mode generates AI-Build, Dev-Team, or Stakeholder documents.",
        ["prd", "product-management", "spec"]),
    "doc-coauthoring": ("productivity",
        "Structured document co-authoring: context gathering, section-by-section refinement, then fresh-eyes reader testing.",
        ["writing", "documentation", "collaboration"]),
    "context-management": ("development",
        "Keep project context alive across AI coding sessions with two lean files plus on-demand docs.",
        ["context", "state", "memory"]),
}

AUTHOR = {"name": "Omri Lorch", "url": "https://github.com/Lorch19/operator-kit"}
VERSION = "1.0.0"
plugins = []

for pack, (category, desc, keywords) in PACKS.items():
    manifest = {
        "name": pack,
        "version": VERSION,
        "description": desc,
        "author": AUTHOR,
        "homepage": "https://github.com/Lorch19/operator-kit",
        "repository": "https://github.com/Lorch19/operator-kit",
        "license": "MIT",
        "keywords": keywords,
    }

    if os.path.isfile(f"{pack}/SKILL.md"):
        layout = "single-skill (auto)"
    elif os.path.isdir(f"{pack}/skills"):
        layout = "skills/ (default scan)"
    else:
        dirs = sorted(
            os.path.dirname(p)[len(pack) + 1:]
            for p in glob.glob(f"{pack}/*/SKILL.md"))
        manifest["skills"] = [f"./{d}" for d in dirs]
        layout = f"flat ({len(dirs)} explicit paths)"

    os.makedirs(f"{pack}/.claude-plugin", exist_ok=True)
    with open(f"{pack}/.claude-plugin/plugin.json", "w") as f:
        json.dump(manifest, f, indent=2)
        f.write("\n")

    n = len(glob.glob(f"{pack}/**/SKILL.md", recursive=True))
    print(f"{pack:<20} {n:>2} skills  {layout}")

    plugins.append({
        "name": pack,
        "source": f"./{pack}",
        "description": desc,
        "category": category,
        "keywords": keywords,
    })

marketplace = {
    "name": "operator-kit",
    "owner": AUTHOR,
    "metadata": {
        "description": "Tools for building, shipping, and running products — PM frameworks, multi-agent workflows, thinking primitives, engineering flows, and document generation.",
        "version": VERSION,
    },
    "plugins": sorted(plugins, key=lambda p: p["name"]),
}
os.makedirs(".claude-plugin", exist_ok=True)
with open(".claude-plugin/marketplace.json", "w") as f:
    json.dump(marketplace, f, indent=2)
    f.write("\n")
print(f"\nmarketplace.json: {len(plugins)} plugins")
