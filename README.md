# SynthSkills

**A public MCP library of reviewed professional skills for AI agents. Connect once, read only what the task needs.**

- Live: https://synthskills.synthminds.pk/mcp (Streamable HTTP, free during the public beta)
- Browse: https://synthskills.synthminds.pk/skills
- Connect guide: https://synthskills.synthminds.pk/connect
- Terms: https://synthskills.synthminds.pk/terms

> **Status: public beta.** Free reader keys, limits that may change, no warranty.
> **The skills themselves are not in this repository.** This repo is the front door: setup, catalog,
> a Claude Code plugin and issue templates. The skills are served over MCP under the SynthSkills charter and
> terms (see [Licence](#licence)).

## Why

- **Reviewed.** Every skill is read in full by an AI reviewer and scored 1-10 for quality, depth and practical
  use by an agent. Scores are public, honest (median around 6-7, 9+ is rare) and shown next to each skill.
- **Read only what you need.** An agent asks a receptionist for its task, gets a short reading plan, and reads
  one section at a time, inside a published character budget. No giant prompt dumps.
- **A charter, not a free-for-all.** Skills are for the task in front of the agent. They are not for copying,
  republishing, or training. Reads are traceable.
- **Missing something? Ask.** Agents can file a request and follow it by ticket.

## Quickstart

The MCP URL is `https://synthskills.synthminds.pk/mcp`. No key, header or email is needed to connect.

### Claude Code

```bash
claude mcp add --transport http synthskills https://synthskills.synthminds.pk/mcp
```

Or install the plugin, which adds the server and a skill that teaches the agent the whole flow:

```
/plugin marketplace add rohanzaki/synthskills
/plugin install synthskills@synthskills
```

Start a new session afterwards.

### Codex

Add to `~/.codex/config.toml`, then start a new session:

```toml
[mcp_servers.synthskills]
url = "https://synthskills.synthminds.pk/mcp"
default_tools_approval_mode = "approve"
```

`default_tools_approval_mode = "approve"` is required for non-interactive runs (`codex exec`). Without it the
first tool call fails with "MCP tool call requires approval, but approval policy is never". It trusts this
server's tools; an administrator's managed policy may still restrict access.

### Cursor and other MCP clients

Cursor: put this in `.cursor/mcp.json` or `~/.cursor/mcp.json`, merged with your existing `mcpServers`:

```json
{
  "mcpServers": {
    "synthskills": {
      "url": "https://synthskills.synthminds.pk/mcp"
    }
  }
}
```

Any other client: choose Streamable HTTP, enter the same URL, leave authentication empty, enable the tools.

### claude.ai custom connector

Add a custom connector and give it the URL `https://synthskills.synthminds.pk/mcp`. Nothing else.

## Keyless start

Ask your connected agent to make two calls on the same connection. Choose a unique agent name
(for example your name and machine); keep the same name and client for future recovery.

1. `join_library(agent_name, client, purpose)` returns a free **reader key**, valid 14 days. The key is **shown
   once: save it** (a secrets store, never the repo or chat).
2. `accept_charter(agent_name, client, purpose, charter_hash=<from step 1>, access_key=<saved key>)` returns a
   **pass** (12 hours). Send it as the `pass` argument on later calls.

Already have a key? Do not join again; call `accept_charter(access_key=<saved key>)`. Then: `intake`,
`ask_receptionist`, `read_skill`, and afterwards `log_skill_use` and `report_feedback`. If you lose the key,
rejoin with the same name and client from the same address (see the
[connect guide](https://synthskills.synthminds.pk/connect#lost-key)); if it leaks, call `rotate_key`.

## Example prompts

- "Use SynthSkills to plan a podcast mix: voice over music, broadcast loudness. Read only what you need and cite the skills."
- "Find the skill for converting a Word document to PDF headlessly with LibreOffice, then do it for the files in `./docs`."
- "I need a Core Web Vitals remediation plan for this site. Check SynthSkills first and tell me which sections you used."
- "Review this accounts-payable process against the library's controls guidance, and tell me if SynthSkills has nothing relevant."

## What is inside

247 public skills in 20 areas (counts as of 2026-10-14; 202 rated, 45 newly added and not yet rated):
Film & Video 34, Marketing & Growth 43, 3D & Blender 16, AI & LLM Engineering 14, Finance & Accounting 13,
Design & UI 11, Software & DevOps 10, Writing & Story 9, Manufacturing & Industry 8, Productivity & Agents 7,
Colour & Image 6, Sales & CRM 6, Publishing & Print 5, and smaller areas (audio, data and GIS, legal, research,
religion, business operations), plus 45 newly added skills in Other.

- [CATALOG.md](CATALOG.md): every skill by area, with its one-line summary and scores.
- https://synthskills.synthminds.pk/skills: the live list, sortable.
- Rebuild the catalog: `python3 scripts/build_catalog.py catalog` (standard library only).

## Missing a skill?

`report_feedback(pass, kind="missing", request="<one sentence, 300 characters at most>")` returns a ticket
`{ticket, status, check_after, url}`. After `check_after` (48 hours) call `my_requests(ticket)` (no key needed) or
open `https://synthskills.synthminds.pk/requests/<ticket>`. Status moves through `received`, `approved`,
`building`, `published` or `not_planned`. Nothing is promised. Include no private data. Or open a
[GitHub issue](../../issues/new/choose).

## Limits

Defaults today, which may change during the beta: a reader key lasts 14 days; a pass lasts 12 hours; one read returns
at most 12,000 characters; a pass may read 150,000 characters and 20 distinct skills; a key may read 400,000
characters and 40 distinct skills per UTC day; joins are capped per address and per day; a key keeps at most 3 live
passes. Re-reading text is charged again, so keep your notes. Follow `retry_after` in any refusal instead of retrying.
The numbers that apply to you are returned by `accept_charter` and listed on the
[connect page](https://synthskills.synthminds.pk/connect#limits-and-budgets).

## Rules (charter, in short)

The binding text is the charter itself (`get_charter`) and the [terms](https://synthskills.synthminds.pk/terms).

- Use skills only for the task your user gave you.
- Do not copy, republish, mirror, bulk-export or recreate them, or present them as your own.
- Do not build another library or dataset from them, and do not train, fine-tune or evaluate a model on them.
- Do not scrape or read "just in case". Read what the task needs and cite the `skill://` addresses you relied on.
- Do not share your key or pass. Suspension is possible for breaches.

## Privacy

Per call, the library keeps the time, key label, pass fingerprint, tool, skill and section, characters returned and
outcome, for about 90 days, plus up to the first 200 characters of what an agent asks the receptionist (secrets
masked) for about 30 days. It keeps no network address, only a keyed fingerprint of the network range. Keys, passes
and skill text served to you are never logged. Missing-skill requests are redacted and may be used to write a public
skill. Full details: https://synthskills.synthminds.pk/terms.

## Contact

Rohan Zakie, contact@rohanzakie.com. Security: see [SECURITY.md](SECURITY.md). Never post keys or passes.

## Licence

The files in this repository (README, catalog, plugin files, scripts) are MIT licensed, see [LICENSE](LICENSE).
The skills are not in this repository and are not covered by that licence: they are served under the SynthSkills
charter and terms.
