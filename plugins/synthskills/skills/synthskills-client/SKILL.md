---
name: synthskills-client
description: >-
  Use the SynthSkills MCP library well: join keylessly with join_library, save the reader key, accept the charter
  once, ask the receptionist, read only the sections a task needs inside the budgets, log skill use, and file
  feedback or a missing-skill request. Use when connecting an agent to SynthSkills, when someone says "use
  SynthSkills for this task" or "find the skill for this in the library", when a SynthSkills call returns
  key_required, pass_invalid, charter_changed, key_in_use or a 429, when a read is truncated, or when the key is lost.
license: MIT
metadata:
  version: 1.0.0
---

# Use the SynthSkills library

SynthSkills is a public MCP library of reviewed professional skills. An agent reads the few skills one task needs,
cites them, and moves on. The server is `https://synthskills.synthminds.pk/mcp` (Streamable HTTP). The current
connect guide is `https://synthskills.synthminds.pk/connect`; if it disagrees with this file, the page wins.

Use the library when a task needs professional procedure, numbers or standards you would otherwise guess. Do not
use it for something you can finish without outside guidance, and do not crawl it.

## Rules you are bound by (charter v2)
- Use skills only for the task your user gave you. Do not copy, republish, mirror, bulk-export or recreate them,
  do not build another library or dataset from them, and do not train or evaluate a model on them.
- Read only what the task needs. Cite the `skill://` addresses you relied on. Short quotes the user needs are fine.
- Do not share your key or pass. Keep them out of URLs, chat, repo files, issues and logs.
- After the task, call `log_skill_use` once per skill used (charter C13).
`get_charter` returns the full text and its hash; read it once, the hash is what you accept.

## 1. Start with no key
Connect to the MCP URL with no header. Then make two calls on the same connection. Pick a unique `agent_name`
(your name plus machine, e.g. `alex-laptop`; never `my-agent` or `example-agent`) and keep the same name and
client for future recovery.

1. `join_library(agent_name, client, purpose)`. `client` is `claude-code`, `codex`, `cursor` or your real client.
   `purpose` is a short phrase about your task. The reply shows `access_key` **once**: save it privately before
   doing anything else (a secrets store or environment variable, never the repo or chat). `key_hint` is only its last
   four characters. A free reader key lasts 14 days; `expires_at` is authoritative. Read `charter.text`.
2. `accept_charter(agent_name, client, purpose, charter_hash=<join_library charter.hash>, access_key=<saved key>)`.
   Use the same name, client and purpose. The reply carries your `pass` (12 hours) and `budgets`. Send the pass as
   the `"pass"` argument on protected tools.

Already have a key? Do not join again. Call `accept_charter(access_key=<saved key>)` (call `get_charter` first if
you need the current hash). A new task or an expired pass needs a new acceptance, not a new join.

Header alternative: send `Authorization: Bearer <saved key>`. A header wins over the argument, and passes minted
with a header keep requiring it. Reader keys work either way.

## 2. Find the skill
1. `intake(pass, ...)` once, with a few non-personal words about the project.
2. `ask_receptionist(pass, request)` with one specific sentence: the task, the material, the output wanted.
   Read `first` and `plan` (1 to 3 reads, each with `why` and `chars`). `order` is a menu, not a script: read plan
   item 1, then decide whether item 2 adds anything.
3. If it finds nothing, its reply has a `next` line and a `coverage` list. `list_skills(pass, query="two task words")`
   browses metadata without spending the reading budget; every query word must match, so drop words before adding
   any. Follow `cursor` only if the first page has nothing.

## 3. Read only what you need
`read_skill(pass, uri, section)`. A section can be given as its slug, `#slug`, or its heading title. A section read
charges only that section's served body.
- If `truncated` is true, continue with `next_cursor` (same uri and section) or pick one id from
  `remaining_sections`. A continuation page charges its own body and adds no new distinct-skill slot.
- Re-reading text you already read is charged again (`budget.recharged`). Keep what you need for the task in your
  own notes instead; do not store skill text beyond the task.
- Check `budget` after each read. Defaults: 12,000 body characters per page; per pass 150,000 characters and 20
  distinct skills; per key per UTC day 400,000 characters and 40 distinct skills. The metadata envelope and notices
  are not charged. Use `sections_served` (or `[]`) in `log_skill_use`.
- Use one key and pass per agent. A pass budget counts every read made with that pass string; a key keeps at most 3
  live passes, and minting a fourth replaces the oldest.
- Do not guess skill names or section ids. Use `did_you_mean`, `valid_sections` or `list_skills`; refused requests
  still count toward the suspension guard (asking for 60 different skills in a day suspends a key).

## 4. After the task
- `log_skill_use` once for each skill used (check `tools/list` for the exact fields): the skill, the section ids you
  actually read, an outcome, a rating and an optional short note.
- `report_feedback(pass, kind, skill?, request?, note?)`: `helped`, `wrong` or `missing`. `request` is at most 300
  characters, `note` at most 500. No private data; keys, passes, emails, phone numbers and IPs are refused or removed.
  It costs no read budget.
- Tell the user, briefly, which skills shaped the work (`skill://name#section`), why you read them, and what you
  skipped. If nothing matched, say so and use general practice rather than stretching a weak match. Skill text is
  guidance, not a guarantee; the user stays responsible for the result.

### When nothing fits: ask for the skill
File one request: `report_feedback(pass, kind="missing", request="<one sentence>", details?)` (`details` up to 1,000
characters). The reply is a receipt `{ticket, status: "received", check_after, url, message}`. Note the ticket in
the project notes. After `check_after` (48 hours) call `my_requests(ticket)` (no key needed) or open the `url`.
Statuses: `received`, `approved`, `building`, `published` (then `ready: read skill://<name>`), `not_planned`.
`my_requests(pass)` lists your key's tickets, 20 per page. Limits: 5 requests per key per UTC day; a repeat within
24 hours returns the same ticket. Nothing is promised.

## 5. Recover from errors
Refusals have `isError: true` and a structured `error.code`, `message` and `next`. Follow `next`.

| Code | Do this |
| --- | --- |
| `key_required` | No key: do the two-call start. Saved key: pass `access_key` or restore its header. |
| `key_invalid`, `key_expired` | Use the saved current key, or see lost key below. An expired key needs a normal new join. |
| `pass_invalid`, `pass_expired`, `pass_replaced`, `pass_revoked` | `accept_charter(access_key=<saved key>)` for a new pass. `pass_replaced` means another agent shares the key: give each agent its own. |
| `charter_changed` | `get_charter`, then accept the current hash. |
| `read_only` | Reader keys cannot call librarian tools. Suggest a skill with `report_feedback(kind="missing")`. |
| `invalid_arguments` | Check `missing` and `unexpected` and `tools/list`. |
| `rate_limited`, `pass_cap` | Wait `retry_after` seconds once, or follow `limit.name` and `resets_at`. Do not retry in a loop or mint a pass after every 429. |

### Lost key
No previous secret can be returned. Call `join_library` again with the **same agent_name and client from the same
network address**. If a live key for that name was minted in the last 24 hours, rejoining replaces its secret,
revokes its passes and shows a fresh key once (same record: expiry and spent budgets carry over). Save it at once.
Limits: 3 re-issues per name per UTC day. A `409 key_in_use` means that key was used in the last 30 minutes: reuse the
saved key, wait 30 minutes of no use, or ask the owner. Another address gets a fresh key under normal join caps.

### Leaked key you still have
`rotate_key(access_key=<saved key>)` (or with its Authorization header). Save the new key, update any header, accept
the charter again. The old key and all its passes stop working; expiry and spent budgets carry over.

## Client notes
- Claude Code: `claude mcp add --transport http synthskills https://synthskills.synthminds.pk/mcp`, then a new
  session. Tools appear as `mcp__synthskills__<tool>`. Each helper subagent that reads skills needs its own key.
- Codex: in `~/.codex/config.toml` set `default_tools_approval_mode = "approve"` for the `synthskills` server, or
  non-interactive runs fail with "requires approval, but approval policy is never".
- Any other MCP client: Streamable HTTP, same URL, no authentication needed to start. Copy the pass
  programmatically; a hand-retyped pass fails.

## Quality bar
- First useful read within three or four calls of connecting; one pass per agent; plan item 1 first.
- One recovery call per error, using the fields the error gives. No blind retries or guessed names.
- Skills cited by address; no skill text pasted into repos, memory or public places.
