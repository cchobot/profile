# The Feature Worked In Testing. Launch-Day Load Found The Real Limit.

## Customer Symptom

Shortly after a new, highly anticipated feature was rolled out to the largest user group, the system crashed.

The feature had already worked in smaller branches, so the failure was surprising and disruptive.

## Context

The feature had passed functional testing in several smaller areas of the organization. The next step was rolling it out to a much larger group of users.

The issue appeared around search behavior, and the searches involved records with images, not just lightweight text data.

## Evidence Gathered

- The feature behaved as expected in smaller environments.
- The failure appeared only after the largest user group started using it.
- The system slowed or crashed around searches.
- Search results included records and images.
- The workflow was valid, but the amount of data being loaded changed under launch-day usage.

## Investigation Path

The important clue was that the feature worked correctly in smaller branches. That made it less likely that the core workflow was broken and more likely that scale had exposed a hidden assumption.

Looking at what the application was doing during searches, the problem became clear: it was trying to load all matching records, including images, for each search.

That worked when the number of users and records was smaller. Under the much larger launch-day load, the same behavior caused the system to grind to a halt.

## Root Cause

The search implementation loaded too much data at once. It treated a search result as something that could be fully fetched and rendered immediately, including image data.

That assumption held up in smaller branches but failed when the largest group of users began searching at the same time.

## Resolution

The fix was conceptually simple: limit the amount of data loaded for each search.

That meant reducing the number of records returned at once and avoiding unnecessary image loading until the user actually needed those results. The system did not need every matching record and image immediately. It needed a useful, bounded set of results that could load reliably.

## Prevention / Durable Improvement

Stress testing should match the targeted launch environment before a major rollout. It is not enough to know that a feature works in smaller branches. It also needs to work with the expected user group, realistic record counts, and the kind of data the system will actually load.

Not every potential issue can be foreseen. When a launch moves into unknown operational territory, practical rollout decisions matter: a softer launch, staged release, or closer launch monitoring can reduce disruption and help preserve user confidence in the feature.

## What This Demonstrates

- A feature can pass functional testing and still fail under real-world load.
- Search results should be bounded, especially when they include images or other heavy data.
- Smaller branches can prove workflow correctness, but they may not expose the performance limits of the targeted launch environment.
- Launch support needs fast triage: what changed, who is affected, which workflow is involved, and what resource is being exhausted.
- Simple fixes are easier to see once the investigation identifies the actual bottleneck.
- A softer rollout can protect user confidence when the remaining unknowns are operational rather than purely functional.
