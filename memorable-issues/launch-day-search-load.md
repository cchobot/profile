# The Feature Worked In Testing. Launch-Day Load Found The Real Limit.

## Context

It was launch day for a new, highly anticipated feature. The feature had already been tested in several smaller branches of the organization, and it behaved as expected there.

The next step was rolling it out to the largest group of users.

Shortly after launch, the system crashed.

## What We Knew

- The feature had passed functional testing in smaller environments.
- The failure appeared only after the largest user group started using it.
- The issue happened around search behavior.
- The searches included records with images, not just lightweight text data.

## Investigation

The important clue was that the feature had worked correctly in smaller branches. That made it less likely that the core workflow was broken and more likely that scale had exposed a hidden assumption.

Looking at what the application was doing during searches, the problem became clear: the application was trying to load all matching records, including images, for each search.

That worked when the number of users and records was smaller. Under the much larger launch-day load, the same behavior caused the system to grind to a halt.

## Root Cause

The search implementation loaded too much data at once. It treated a search result as something that could be fully fetched and rendered immediately, including image data.

That assumption held up in smaller branches but failed when the largest group of users began searching at the same time.

## Resolution

The fix was conceptually simple: limit the amount of data loaded for each search.

That meant reducing the number of records returned at once and avoiding unnecessary image loading until the user actually needed those results. The system did not need every matching record and image immediately. It needed a useful, bounded set of results that could load reliably.

## Support Lessons

- A feature can pass functional testing and still fail under real-world load.
- Search results should be bounded, especially when they include images or other heavy data.
- Smaller branches can prove workflow correctness, but they may not expose the performance limits of the targeted launch environment.
- Launch support needs fast triage: what changed, who is affected, which workflow is involved, and what resource is being exhausted.
- Simple fixes are easier to see once the investigation identifies the actual bottleneck.
- A softer rollout can protect user confidence when the remaining unknowns are operational rather than purely functional.

## Lesson Learned

Stress testing needs to match the targeted environment before launch. It is not enough to know that a feature works in smaller branches. For a major rollout, it also has to work with the expected user group, realistic record counts, and the kind of data the system will actually load.

At the same time, not every potential issue can be foreseen. When a launch moves into unknown operational territory, practical rollout decisions matter: a softer launch, staged release, or closer launch monitoring can reduce disruption and help preserve user confidence in the feature.
