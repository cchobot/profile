# API Integration Troubleshooting Checklist

## Problem Statement

- What is the customer trying to do?
- What is failing?
- When did it start?
- Is the issue constant, intermittent, or tied to a specific workflow?

## Customer Impact

- Who is affected?
- Is work blocked, delayed, or degraded?
- Is there a workaround?
- Is there time sensitivity or a business deadline?

## Integration Path

- Source system:
- Destination system:
- Triggering workflow:
- API endpoint or event:
- Expected direction of data flow:

## Request / Response Basics

- Request method:
- Endpoint:
- Status code:
- Response body or error:
- Request ID / trace ID / correlation ID:
- Timestamp and timezone:

## Authentication / Authorization Checks

- Is the token, key, session, or OAuth connection valid?
- Does the integration user have the required permissions?
- Did credentials rotate or expire?
- Is the request being made against the expected environment?

## Payload Validation

- Required fields present?
- Data types correct?
- IDs valid and scoped to the right customer/org/user?
- Date/time format and timezone correct?
- Enum/status values supported?
- Payload size within limits?

## Webhook / Event Timing

- Was the event emitted?
- Was it delivered?
- Was it retried?
- Was it received out of order?
- Was there a timeout or duplicate delivery?

## Idempotency / Duplicate Handling

- Could the same event be processed more than once?
- Is there an idempotency key or external ID?
- Are duplicate records being created?
- Is a retry safe?

## Logs / Correlation IDs

- Customer/org/user:
- Time window:
- Request ID:
- Correlation ID:
- Error text:
- Related logs:

## Reproduction Notes

- Exact steps:
- Test account or sanitized sample:
- Expected behavior:
- Actual behavior:
- Reproduction result:

## When To Escalate To Engineering

Escalate when:

- The request appears valid but fails due to application behavior.
- Logs show an unhandled exception or unexpected internal state.
- The issue affects multiple customers or a critical workflow.
- Support cannot safely correct the data/configuration.
- A product defect or unclear API contract is likely.

## Escalation Packet Checklist

- Clear summary and impact
- Exact workflow and reproduction steps
- Request/response details
- Logs, errors, request IDs, and correlation IDs
- What support checked or ruled out
- Workaround status
- Suggested next investigation path
