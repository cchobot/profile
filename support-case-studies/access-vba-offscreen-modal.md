# The App Was Not Frozen. The Window Was Off-Screen.

## Customer Symptom

Users reported that an Access/VBA application was "freezing" after they clicked a specific button.

That description was true to the user experience. The application appeared stuck, and the user could not continue the workflow.

## Context

The application was older, but important, and users depended on it to get their work done. It also saved user settings, including modal window positions.

Users sometimes moved between machines with different monitor layouts and screen resolutions.

## Evidence Gathered

- The issue happened after a specific button click.
- The application saved modal window positions.
- Users moved between machines with different display setups.
- The application was not consistently crashing or showing a visible error.
- The workflow appeared blocked, but the application process was still alive.

## Investigation Path

The key was treating "freezing" as a symptom, not a conclusion.

We looked at the workflow, the button behavior, and the user's environment. Once we connected saved window positions with users switching between display layouts, the pattern became clear.

The application was opening a modal window, but the saved coordinates placed it outside the visible screen area. From the user's point of view, the app was frozen because the modal had focus and was waiting for input. The user just could not see it.

## Root Cause

The application remembered a modal window position from a different machine or monitor layout. When the user returned to another machine with a different screen size or arrangement, the modal opened off-screen.

The app was not frozen. It was waiting on a hidden modal dialog.

## Resolution

The immediate fix was to use the Windows keyboard shortcut for moving an active window, then use the arrow keys to bring the modal back into view.

That was the "aha" moment. Showing a user that the supposedly frozen application was still alive, then watching the hidden window slide back onto the visible screen, was deeply satisfying.

## Prevention / Durable Improvement

A durable fix would validate saved window coordinates against the current screen layout before opening modal dialogs. If the saved position is outside the visible range, the application should reset the modal to a safe visible position.

## What This Demonstrates

- User descriptions are true to the experience, but not always the technical root cause.
- Environmental details matter, especially monitor layouts, saved preferences, roaming profiles, and machine switching.
- A good support investigation often starts by asking, "What is the system waiting for?"
- The most helpful fix is not always complicated. Sometimes the best support moment is making the invisible visible.
- The root cause is often not what you think.
