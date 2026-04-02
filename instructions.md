# AI Talent Agent Instructions

Use the two separate instruction files in this repo:

- `talent_agent_instructions.md`
- `talent_acquisition_agent_instructions.md`

Workflow:

1. Use the `Talent Agent` instructions to tailor the CV for a specific role.
2. Use the `Talent Acquisition Agent` instructions to evaluate the tailored CV as if reviewing it from the recruiter / headhunter side.

Storage rule:

- Store any user-specific working materials in a subdirectory under `private/`.
- This includes original CVs, anonymized CVs, tailored CVs, recruiter reviews, copied job descriptions, notes, and any derivative artifacts.
- Treat anonymized materials as private too, because they still derive from private source information and should stay under `private/` by default.
- Prefer a per-role or per-workstream folder such as `private/company_role/` rather than placing generated files directly at the root of `private/`.

The two roles are intentionally separate:

- the `Talent Agent` improves positioning,
- the `Talent Acquisition Agent` pressure-tests credibility, fit, and likely recruiter response.
