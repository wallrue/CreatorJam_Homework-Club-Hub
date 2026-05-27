---
doc_kind: team-playbook
status: draft
visibility: public_sample
last_updated: 2026-05-25
---

# Team Playbook — Using the Vision Spec Template

This playbook describes how a Creator Jam team creates its own branch, writes a Vision Spec, and merges the work back into the Creator Jam Spec Kit. Any team can follow these steps. AI agents can read this document directly and help a team carry it out.

## What This Is For

The Creator Jam Spec Kit is a shared repository for participant specs, templates, and examples. This playbook is a team-specific path into that shared repo. It answers:

- How does my team claim its own space?
- How do we write a Vision Spec that another person, mentor, builder, or agent can understand?
- How do we merge our work back so the whole group can see it?

## Prerequisites

The team needs:

- A GitHub account with push access to `indigenomicsxyz/CreatorJamSpecKit`
- Git installed on a machine or in an agent's environment
- The Vision Spec template (located at `specs/<team-name>/vision-spec.md`)

## Step 1 — Create the Team Branch

Each team gets its own branch. Use the naming pattern `team/<name>` where `<name>` is a short lowercase slug.

```bash
git clone git@github.com:indigenomicsxyz/CreatorJamSpecKit.git
cd CreatorJamSpecKit
git checkout -b team/<your-team-name>
```

If a branch already exists:

```bash
git fetch origin
git checkout team/<your-team-name>
```

## Step 2 — Create the Team Folder and Vision Spec File

Create a folder under `specs/` named after the team. Inside it, create the Vision Spec file:

```
specs/<team-name>/vision-spec.md
```

The Vision Spec template has frontmatter and 11 sections:

```yaml
---
doc_kind: vision-spec
status: draft
visibility: public_sample
last_updated: <date>
team: <team-slug>
---
```

### The 11 Sections

1. **Context and Problem Statement** — Why does this vision exist now?
2. **North Star Vision** — The larger possibility the team wants to make visible.
3. **Design Principles** — Values, boundaries, and commitments that guide choices.
4. **Current-State Assumptions and Unknowns** — What the team believes, what needs checking, what should stay open.
5. **Research Notes or Evidence** — Sources, stories, links, observations that shaped the vision.
6. **Proposed Architecture or Operating Model** — How it works: people, roles, screens, flows, data, prompts, tools.
7. **Multi-Phase Roadmap** — What during the Jam, what on demo day, what after, what needs review.
8. **Acceptance Criteria** — What shows the prototype honoured the vision.
9. **Risks, Constraints, and Mitigations** — What could go wrong and how to reduce that risk.
10. **Dependencies and Open Questions** — What the team needs from mentors, permissions, tools, data, cultural guidance.
11. **First 3-5 Next Actions** — Concrete next moves.

Teams can fill the sections in any order. Sections can be empty while a team is still thinking — empty sections are fine and are flagged during review.

## Step 3 — Write the Vision Spec

Each team member can contribute. The most effective pattern is:

1. One person owns the file and pushes updates.
2. Other team members share their inputs (via chat, voice notes, or their own edits if the agent can commit for them).
3. The owner drafts, commits, and pushes after each meaningful addition.

Commit messages should follow this pattern:

```
<author-initials or name>: <what section> - <what was added>
```

Example:

```
DJ: section 1 - added problem statement about student isolation
```

## Step 4 — Push to GitHub

After each meaningful write:

```bash
git add specs/<team-name>/vision-spec.md
git commit -m "<commit message>"
git push origin team/<team-name>
```

Other team members keep their local branch in sync:

```bash
git fetch origin
git pull origin team/<team-name>
```

## Step 5 — Validate Before Merging

The kit ships two lightweight validation scripts. Run them before considering the spec merge-ready:

```bash
python3 scripts/validate-frontmatter.py
python3 scripts/validate-bundle-links.py
```

These check that templates and specs carry frontmatter and that any bundle references resolve. They do **not** check permission, authority, or correctness — they only check shape.

## Step 6 — Merge Into Main

When the team is ready:

1. Open a pull request from `team/<team-name>` into `main` (or whichever branch is the current working branch).
2. A facilitator or reviewer can assess the spec using the kit's review patterns:
   - **Fit state**: Is this spec ready to compose into a candidate bundle?
   - **Permission state**: Is the material public sample, display approved, review required, or protected?
   - **Review state**: Has the right review happened for the stated use?
3. Once approved, merge via GitHub UI or CLI.

## AI Agent Instructions

If you are an AI agent reading this document to help a team, follow these rules:

1. **Never push protected, cultural, linguistic, ceremonial, or private material.** The only safe material is public sample, fictional, or explicitly display-approved.
2. **Do not edit files outside the team's branch.** Write only under `specs/<team-name>/`.
3. **Do not compute on `do_not_compute` or `refused` content.** If a team member indicates something is private or review-required, record that boundary — do not process the content.
4. **Frontmatter is required.** Every markdown file in `specs/` must start with `---\n` followed by YAML frontmatter.
5. **One section at a time.** Help the team fill one section, commit, and push before moving to the next.
6. **Ask, don't assume.** If a section is ambiguous, surface questions back to the team. Do not invent content the team has not provided.
7. **Preserve team voice.** The Vision Spec should sound like the team, not like an AI summary. Edit for clarity but do not rewrite the team's language.

## When the Vision Spec Is Ready for the Kit

A Vision Spec alone is not a bundle or a build. After it is complete, the kit expects the team to move through these further steps (not covered by this playbook):

1. **Wrap as a Spec Fragment** — Use `templates/spec-fragment.md` to add permission state, fit state, review state, and bundle context.
2. **Offering Integration Session** — The team presents the fragment to the group. A facilitator records fit, review, and bundle decisions.
3. **Build Attempt** — If the group selects the bundle, the team creates `templates/build-attempt-instructions.md` and attempts a build.
4. **Reviewer Check and Witness Rollup** — Record what passed, what was partial, what failed, what was refused.
5. **Display Review** — Before any story, receipt wall item, or public slide, run `templates/display-review-checklist.md`.

## Troubleshooting

- **Branch push fails with permission denied** — The team needs push access to the `indigenomicsxyz/CreatorJamSpecKit` repo. A repo owner must grant it.
- **Validation script reports missing frontmatter** — Add a YAML frontmatter block (`---` on the first line, then key-value pairs, then `---`) at the top of the file.
- **Merge conflicts during a pull** — Team members should pull each other's changes frequently (`git pull origin team/<name>`) to minimize conflicts. If a conflict arises, resolve it together and commit the merged result.
- **Agent cannot push** — Some agent environments lack SSH key access. In that case, the human team member should push on behalf of the agent, or the team should set up an SSH key in the agent's environment.

## Source

This playbook is part of the Creator Jam Spec Kit (`github.com/indigenomicsxyz/CreatorJamSpecKit`). The full kit includes spec templates, spec backlog, composition lab, witness receipt schema, and validation scripts. See `README.md` for the complete kit map.
