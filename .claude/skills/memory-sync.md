# memory-sync

The discipline this whole repo's guardrail stack exists to enforce. Read this when:
- The user says "update memory" or "sync memory" or "fix memory"
- You learn anything about deployed state, DNS, or hosting that contradicts a memory entry or doc
- You're about to write something to memory ABOUT this repo

## The contract

For this repo, the canonical truth lives in three files:
- `firebase.json` — hosting config, headers, project link via `.firebaserc`
- `.firebaserc` — GCP project alias
- `cloudbuild.yaml` — CI/CD pipeline definition

Memory entries point to those files. Memory does NOT itself describe deploy state in detail — that detail rots, and stale-but-confident memory is exactly the failure mode that triggered this guardrail stack in the first place.

## When to update memory

**Always update memory in the same session that you change canonical config**, never in a separate session. If you:
- Change `firebase.json` hosting target → update `project_plainlydigital_site.md`
- Move the GCP project ID → update both `project_plainlydigital_site.md` AND `reference_plainly_gcp_billing.md`
- Change DNS authority → update `project_plainlydigital_site.md` AND fix `project_gcp_migration.md` if it mentions plainlydigital.com
- Set up a new Cloud Build trigger → update `project_plainlydigital_site.md`

**Do NOT update memory** for:
- Per-task progress, in-flight work, todo state — that's TaskCreate/TaskUpdate territory
- File paths or code structure — Glob/Grep finds those
- Recent commits or who-changed-what — `git log` is authoritative

## When to read memory

When the user asks about plainlydigital.com infra, DON'T just quote memory. Verify, then quote with citation:

```
WRONG (the failure case this whole stack exists to prevent):
> "The site is hosted on Cloudflare Pages." — memory says so

RIGHT:
> "Per `firebase.json` + `.firebaserc` (verified just now), the site is hosted on
> Firebase Hosting under GCP project `plainlydigital-www`. Memory entry
> `project_plainlydigital_site.md` agrees."
```

If memory and the live config disagree, **the live config wins**, and you must:
1. Tell the user there's a stale memory entry and what's actually true.
2. Update the memory entry in the same session.
3. If the stale memory was the source of any prior assertion you made to the user, retract that assertion explicitly.

## Memory file locations (this user)

```
C:\Users\jbroc\.claude\projects\C--Users-jbroc\memory\
├── MEMORY.md                                    # index — must stay <200 lines after truncation
├── project_plainlydigital_site.md               # this site's pointer entry
├── project_gcp_migration.md                     # cross-app GCP migration plan
├── reference_plainly_gcp_billing.md             # billing acct + org IDs
└── ... (others)
```

## How to write a good memory entry for this repo

Type=project frontmatter. Body sections:
1. **Pointer:** repo path, GitHub remote, deploy target one-liner
2. **Authoritative source:** name the files in the repo that describe state
3. **Why:** what this site is for at the LLC level
4. **How to apply:** "before answering questions about plainlydigital.com infra, run the verify-before-claim commands listed in the repo CLAUDE.md and read firebase.json directly"
5. **Last verified:** ISO date + what command verified it

Do NOT write into the memory entry:
- The actual hosting URL (Firebase web.app URL might change)
- The Firebase IP records (those rotate)
- The current Cloud Build trigger ID (regenerated when you reconnect GitHub)
- Anything that's better looked up live

## The recovery move

If you're partway through a session and realize a memory entry is stale or wrong, fix it immediately, then proceed. Do not finish the session with a known-stale memory entry — the next session will trip on it. This is non-negotiable; the user has explicitly called out this failure pattern.
