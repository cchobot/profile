# Log Investigation Checklist

## Time Window

- Customer-reported time:
- Timezone:
- Start:
- End:
- Any repeated occurrences:

## Affected User / Org / Workflow

- Organization/customer:
- User:
- Role/permissions:
- Workflow:
- Page, action, job, or integration:

## Correlation IDs

- Request ID:
- Trace ID:
- Correlation ID:
- Session ID:
- Job ID:

## Error Messages

- User-facing error:
- Server/application error:
- HTTP status:
- Stack trace or exception:
- Related warning messages:

## Recent Changes

- Deployment:
- Configuration:
- Permissions:
- Data import/migration:
- Customer workflow change:
- External service change:

## Environment Differences

- Browser/device:
- Network/VPN:
- Machine/display setup:
- Production vs. test:
- User-specific vs. organization-wide:

## Authentication / Session Clues

- Login state:
- Token/session expiration:
- SSO or identity-provider behavior:
- Permission mismatch:
- Account/organization membership:

## Retry Patterns

- Did the same action later succeed?
- Did retries produce the same error?
- Was the issue intermittent?
- Did the error happen after a timeout?

## What Changed / What Did Not Change

- Changed:
- Not changed:
- Ruled out:
- Still unknown:

## Summary Format

Use this format when sharing findings:

```text
Summary:
Impact:
Time window:
Evidence:
Most likely cause:
What was ruled out:
Recommended next step:
```
