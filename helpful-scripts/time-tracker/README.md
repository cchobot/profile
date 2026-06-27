# Time Tracker

Time Tracker is a small local Python CLI for tracking personal work time. It uses SQLite, stores data locally, and has no external package dependencies.

This is useful when I want lightweight notes about where support or project time is going without opening a larger time-tracking system.

## Requirements

- Python 3
- PowerShell, if using the optional `tt` shortcut
- No external Python packages

## Setup

Run commands directly from this folder:

```powershell
python .\timetracker.py status
```

The SQLite database is created automatically on first run as `timetracker.db` next to `timetracker.py`. The database contains local work history after use and is intentionally ignored by git.

To keep the database somewhere else, set `TIMETRACKER_DB` before running commands:

```powershell
$env:TIMETRACKER_DB = "$PWD\local.timetracker.db"
python .\timetracker.py status
```

To add a PowerShell shortcut, open your PowerShell profile:

```powershell
notepad $PROFILE
```

Add this function, updating the path if needed:

```powershell
function tt {
    python "C:\src\Work\profile\helpful-scripts\time-tracker\timetracker.py" @args
}
```

Restart PowerShell or reload your profile after saving it.

## Usage

Start a session:

```powershell
tt start support "investigate login issue"
tt start support
```

If no comment is provided, Time Tracker stores a default comment like `support started`.

Stop a session:

```powershell
tt stop support
```

Show currently running sessions:

```powershell
tt status
```

Show reports:

```powershell
tt report today
tt report week
tt report month
```

Reports include stopped sessions, currently running sessions, and manual corrections.

Subtract time without editing old sessions:

```powershell
tt subtract support "30 minutes"
```

Add time when tracking was not started:

```powershell
tt add support "1 hour"
tt add support "90 minutes"
```

Remove every entry for an exact business, client, or category name:

```powershell
tt remove support
tt remove support --yes
```

`remove` also works as `delete`. Without `--yes`, Time Tracker shows how many rows will be removed and asks you to type the exact name before deleting.

Supported duration formats include:

- `30 minutes`
- `30 min`
- `1 hour`
- `1.5 hours`
- `90 minutes`

## Direct Python Examples

The same commands can be run without the PowerShell function:

```powershell
python .\timetracker.py start support "investigate login issue"
python .\timetracker.py start support
python .\timetracker.py stop support
python .\timetracker.py status
python .\timetracker.py report today
python .\timetracker.py report month
python .\timetracker.py add support "1 hour"
python .\timetracker.py subtract support "30 minutes"
python .\timetracker.py remove support
```

## Data Model

Time Tracker stores rows in a `sessions` table:

- Normal work sessions use `entry_type = "session"`.
- Manual corrections use `entry_type = "correction"` and store positive or negative `duration_seconds`.
- Reports include stopped sessions, currently running sessions, and correction rows for the selected period.

Session time is counted only for the portion that overlaps the selected period. Corrections count on the date they are created.

See [schema.sql](schema.sql) for the SQLite schema.
