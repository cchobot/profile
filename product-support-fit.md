# Product Support Fit / Evidence Map

## Summary Fit

The pattern of work I have done maps closely to Product Support Engineer and Product Support Specialist roles: customer-facing troubleshooting, complex workflow investigation, API/log/data analysis, clear escalation writing, documentation, and product feedback from real support patterns.

Much of my strongest work happened in private or internal environments, so this repository uses sanitized case studies, reusable support templates, and small public utilities to show the working style without exposing private data.

## Role Requirements I Can Demonstrate

- Investigating ambiguous customer-reported issues without assuming the first description is the root cause.
- Using logs, API request details, correlation IDs, user context, and data checks to narrow down behavior.
- Communicating clearly with customers while keeping technical details organized for internal teams.
- Escalating to engineering when that is the right next step, with evidence and reproduction context attached.
- Creating documentation, templates, and small utilities that reduce repeated support effort.
- Working across varied domains, including healthcare, e-commerce, ERP, purchasing, accounting, planning, scheduling, project management, hosting, and SaaS product workflows.

## Evidence Map

| Product support requirement | Evidence |
| --- | --- |
| Complex troubleshooting | [Off-screen modal case study](support-case-studies/access-vba-offscreen-modal.md) |
| Launch/load investigation | [Launch-day search load case study](support-case-studies/launch-day-search-load.md) |
| API/integration support | [API integration troubleshooting checklist](support-artifacts/api-integration-troubleshooting-checklist.md) and resume experience with request/response analysis |
| Log investigation | [Log investigation checklist](support-artifacts/log-investigation-checklist.md) and resume examples using correlation IDs and detailed logs |
| SQL/data investigation | [SQL investigation notes template](support-artifacts/sql-investigation-notes-template.md) |
| Engineering escalation | [Technical escalation template](support-artifacts/technical-escalation-template.md) |
| Customer communication | [Customer update template](support-artifacts/customer-update-template.md) |
| Support enablement | [Support enablement note template](support-artifacts/support-enablement-note-template.md) |
| Automation and personal tooling | [Time Tracker](helpful-scripts/time-tracker/) |
| SaaS/product exposure | HIPAAList project summary in [resume.md](resume.md) |

## How I Approach Complex Tickets

I try to start with the customer's experience without treating it as the final diagnosis. A user saying "the app froze" may be exactly what they experienced, but the system might be waiting on a hidden modal, a failed request, a permissions issue, stale configuration, a slow search, or a data condition that only appears in one workflow.

My usual pattern is:

- Clarify the affected user, workflow, time window, and expected result.
- Gather and inspect evidence: logs, API requests, correlation IDs, screenshots, data state, environment details, and recent changes.
- Reproduce what I can or narrow the problem to a specific branch of behavior.
- Resolve directly when the support path is responsible and safe.
- Escalate with a concise packet when engineering is the right next step.

## How I Work With Engineering

I do not want to hand engineering a vague report. I want to hand them the cleanest version of the problem I can produce: what the customer experienced, what should have happened, what I checked, what evidence points to the issue, what I ruled out, and where I think the next investigation should start.

Good escalation should reduce rework. It should also preserve the customer context so the technical fix still maps back to the real-world workflow.

## How I Improve Support Systems Over Time

The best support work does not stop at closing one ticket. Repeated issues should become better documentation, clearer product behavior, improved logging, safer rollout plans, training material, automation, or support playbooks.

That is why this repo includes support templates and small tools in addition to a resume. They show the kind of reusable structure I like to build around repeated work.

## Notes On Public And Private Work

Some of the most relevant work came from private client, internal, or nonprofit environments. I am intentionally not publishing private organization names, customer details, PHI, credentials, domains, screenshots, or proprietary code.

This repository is meant to show the shape of the work: how I investigate, document, communicate, escalate, and improve support systems over time.
