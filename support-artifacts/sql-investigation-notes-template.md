# SQL Investigation Notes Template

## Question Being Answered

What specific support question should this investigation answer?

## Safety Note

Use read-only queries only unless an explicitly approved change plan exists. Do not run updates, deletes, migrations, or data repairs from an investigation note.

## Tables / Entities Checked

- Table/entity:
- Why it matters:
- Relevant IDs:
- Expected data state:

## Query Snippets

Use sanitized placeholders. Do not include customer data, PHI, secrets, or private identifiers.

```sql
-- Example: confirm record exists and belongs to expected organization
select
  id,
  organization_id,
  status,
  created_at,
  updated_at
from example_table
where id = '<record_id>'
  and organization_id = '<organization_id>';
```

```sql
-- Example: inspect recent related events
select
  event_type,
  created_at,
  actor_id,
  metadata
from example_events
where object_id = '<record_id>'
order by created_at desc
limit 20;
```

## Findings

- Finding:
- Evidence:
- What it means:

## Confidence Level

- High / Medium / Low:
- Why:
- What would increase confidence:

## Follow-Up Questions

- Question:
- Owner:
- Needed by:

## Customer-Safe Explanation

Write the explanation in plain language without exposing internal table names, private IDs, PHI, or implementation details.
