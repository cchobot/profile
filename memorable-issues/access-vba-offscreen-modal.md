# The App Was Not Frozen. The Window Was Off-Screen.

## Context

We were supporting an Access/VBA application that users reported was "freezing" during a specific workflow. The app was older, but important, and the users depended on it to get their work done.

The report sounded straightforward at first: click a specific button, and the application appeared to stop responding.

## What We Knew

- The issue happened after users clicked a specific button.
- The application saved user preferences, including window positions for modal dialogs.
- Users moved between machines with different monitor setups and screen resolutions.
- The application itself was not consistently crashing or throwing a visible error.

## Investigation

The key was treating "freezing" as a symptom, not a conclusion.

We looked at the workflow, the button behavior, and the user's environment. Once we connected the saved window position behavior with users switching between different screen layouts, the pattern became clear.

The application was opening a modal window, but the saved coordinates placed it outside the visible screen area. From the user's point of view, the app was frozen because the modal window had focus and was waiting for input. The user just could not see it.

## Root Cause

The application remembered a modal window position from a different machine or monitor layout. When the user returned to another machine with a different screen size or arrangement, the modal opened off-screen.

The app was not frozen. It was waiting on a hidden modal dialog.

## Resolution

The immediate fix was to use the Windows keyboard shortcut for moving an active window, then use the arrow keys to bring the modal back into view.

That was the "aha" moment. Showing a user that the supposedly frozen application was still alive, then watching the hidden window slide back onto the visible screen, was deeply satisfying.

## Support Lessons

- User descriptions are true to the experience, but not always the technical root cause.
- Environmental details matter, especially monitor layouts, saved preferences, roaming profiles, and machine switching.
- A good support investigation often starts by asking, "What is the system waiting for?"
- The most helpful fix is not always complicated. Sometimes the best support moment is making the invisible visible.
- Durable fixes should validate saved window coordinates against the current screen layout before opening modal dialogs.

## Lesson Learned

The root cause is often not what you think. In this case, the application looked frozen because that was the user's real experience, but the actual problem was a hidden modal dialog waiting for input off-screen.
