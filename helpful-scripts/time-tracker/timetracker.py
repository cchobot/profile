#!/usr/bin/env python3
"""A small local CLI for tracking work time in SQLite."""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
import sys
from collections import defaultdict
from datetime import datetime, time, timedelta
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
DEFAULT_DB_PATH = APP_DIR / "timetracker.db"
DB_PATH = Path(os.environ.get("TIMETRACKER_DB", DEFAULT_DB_PATH))

DURATION_RE = re.compile(
    r"^\s*(?P<amount>\d+(?:\.\d+)?)\s*"
    r"(?P<unit>minutes?|mins?|min|m|hours?|hrs?|hr|h)\s*$",
    re.IGNORECASE,
)


def local_now() -> datetime:
    """Return the current local time with timezone offset information."""
    return datetime.now().astimezone().replace(microsecond=0)


def to_iso(value: datetime) -> str:
    return value.isoformat(timespec="seconds")


def from_iso(value: str) -> datetime:
    return datetime.fromisoformat(value)


def format_datetime(value: datetime) -> str:
    # Windows strftime does not support %-I, so remove the leading hour zero.
    return value.strftime("%Y-%m-%d %I:%M %p").replace(" 0", " ", 1)


def format_duration(total_seconds: int) -> str:
    sign = "-" if total_seconds < 0 else ""
    seconds = abs(int(total_seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours:
        return f"{sign}{hours}h {minutes}m"
    if minutes:
        return f"{sign}{minutes}m"
    return f"{sign}{seconds}s"


def parse_duration(value: str) -> int:
    match = DURATION_RE.match(value)
    if not match:
        raise ValueError(
            'Use a duration like "30 minutes", "30 min", "1 hour", or "1.5 hours".'
        )

    amount = float(match.group("amount"))
    if amount <= 0:
        raise ValueError("Duration must be greater than zero.")

    unit = match.group("unit").lower()
    multiplier = 3600 if unit.startswith("h") else 60
    return int(round(amount * multiplier))


def connect() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    initialize_database(connection)
    return connection


def initialize_database(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY,
            business TEXT NOT NULL,
            comment TEXT,
            start_time TEXT,
            end_time TEXT,
            duration_seconds INTEGER,
            entry_type TEXT NOT NULL CHECK (entry_type IN ('session', 'correction')),
            created_at TEXT NOT NULL
        )
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_sessions_active
        ON sessions (business, entry_type, end_time)
        """
    )
    connection.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_sessions_report
        ON sessions (entry_type, end_time, created_at)
        """
    )
    connection.commit()


def find_active_session(connection: sqlite3.Connection, business: str) -> sqlite3.Row | None:
    return connection.execute(
        """
        SELECT *
        FROM sessions
        WHERE business = ?
          AND entry_type = 'session'
          AND end_time IS NULL
        ORDER BY start_time DESC
        LIMIT 1
        """,
        (business,),
    ).fetchone()


def command_start(args: argparse.Namespace) -> int:
    comment = (args.comment or "").strip() or f"{args.business} started"

    with connect() as connection:
        active = find_active_session(connection, args.business)
        if active:
            started_at = format_datetime(from_iso(active["start_time"]))
            active_comment = active["comment"] or "(no comment)"
            print(
                f"{args.business} is already running. "
                f"Started at {started_at} with comment: {active_comment}"
            )
            return 1

        now = to_iso(local_now())
        connection.execute(
            """
            INSERT INTO sessions (
                business, comment, start_time, end_time,
                duration_seconds, entry_type, created_at
            )
            VALUES (?, ?, ?, NULL, NULL, 'session', ?)
            """,
            (args.business, comment, now, now),
        )
        connection.commit()

    print(f"{args.business} started at {format_datetime(from_iso(now))}.")
    return 0


def command_stop(args: argparse.Namespace) -> int:
    with connect() as connection:
        active = find_active_session(connection, args.business)
        if not active:
            print(f"No active session found for {args.business}.")
            return 1

        started = from_iso(active["start_time"])
        ended = local_now()
        duration_seconds = max(0, int((ended - started).total_seconds()))

        connection.execute(
            """
            UPDATE sessions
            SET end_time = ?, duration_seconds = ?
            WHERE id = ?
            """,
            (to_iso(ended), duration_seconds, active["id"]),
        )
        connection.commit()

    print(f"{args.business} stopped. Duration: {format_duration(duration_seconds)}.")
    return 0


def command_status(_args: argparse.Namespace) -> int:
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT *
            FROM sessions
            WHERE entry_type = 'session'
              AND end_time IS NULL
            ORDER BY start_time ASC
            """
        ).fetchall()

    if not rows:
        print("No sessions are currently running.")
        return 0

    now = local_now()
    print("Running sessions:")
    for row in rows:
        started = from_iso(row["start_time"])
        elapsed_seconds = max(0, int((now - started).total_seconds()))
        comment = row["comment"] or "(no comment)"
        print(f"- {row['business']}")
        print(f"  Comment: {comment}")
        print(f"  Started: {format_datetime(started)}")
        print(f"  Elapsed: {format_duration(elapsed_seconds)}")

    return 0


def period_bounds(period: str, now: datetime | None = None) -> tuple[datetime, datetime, str]:
    now = now or local_now()
    today_start = datetime.combine(now.date(), time.min, tzinfo=now.tzinfo)

    if period == "today":
        start = today_start
        end = start + timedelta(days=1)
        label = start.strftime("%Y-%m-%d")
        return start, end, label

    if period == "week":
        start = today_start - timedelta(days=today_start.weekday())
        end = start + timedelta(days=7)
        label = f"{start.strftime('%Y-%m-%d')} to {(end - timedelta(days=1)).strftime('%Y-%m-%d')}"
        return start, end, label

    if period == "month":
        start = today_start.replace(day=1)
        if start.month == 12:
            end = start.replace(year=start.year + 1, month=1)
        else:
            end = start.replace(month=start.month + 1)
        label = f"{start.strftime('%Y-%m-%d')} to {(end - timedelta(days=1)).strftime('%Y-%m-%d')}"
        return start, end, label

    raise ValueError(f"Unsupported report period: {period}")


def overlaps_period(start: datetime, end: datetime, period_start: datetime, period_end: datetime) -> bool:
    return start < period_end and end >= period_start


def overlap_seconds(
    start: datetime,
    end: datetime,
    period_start: datetime,
    period_end: datetime,
) -> int:
    overlap_start = max(start, period_start)
    overlap_end = min(end, period_end)
    return max(0, int((overlap_end - overlap_start).total_seconds()))


def command_report(args: argparse.Namespace) -> int:
    now = local_now()
    start, end, label = period_bounds(args.period, now)
    start_text = to_iso(start)
    end_text = to_iso(end)
    totals: dict[str, int] = defaultdict(int)
    entry_count = 0

    with connect() as connection:
        sessions = connection.execute(
            """
            SELECT business, start_time, end_time
            FROM sessions
            WHERE entry_type = 'session'
              AND start_time IS NOT NULL
            """
        ).fetchall()

        corrections = connection.execute(
            """
            SELECT business, duration_seconds
            FROM sessions
            WHERE entry_type = 'correction'
              AND duration_seconds IS NOT NULL
              AND created_at >= ?
              AND created_at < ?
            """,
            (start_text, end_text),
        ).fetchall()

    for row in sessions:
        session_start = from_iso(row["start_time"])
        session_end = from_iso(row["end_time"]) if row["end_time"] else now
        if not overlaps_period(session_start, session_end, start, end):
            continue

        totals[row["business"]] += overlap_seconds(session_start, session_end, start, end)
        entry_count += 1

    for row in corrections:
        totals[row["business"]] += int(row["duration_seconds"])
        entry_count += 1

    titles = {
        "today": "Today",
        "week": "This week",
        "month": "This month",
    }
    title = titles[args.period]
    print(f"{title} ({label})")

    if entry_count == 0:
        print("No tracked time for this period.")
        return 0

    grand_total = 0
    for business in sorted(totals):
        total = totals[business]
        grand_total += total
        print(f"- {business}: {format_duration(total)}")

    print(f"Total: {format_duration(grand_total)}")
    return 0


def command_subtract(args: argparse.Namespace) -> int:
    try:
        seconds = parse_duration(args.duration)
    except ValueError as error:
        print(f"Could not parse duration. {error}", file=sys.stderr)
        return 1

    now = to_iso(local_now())
    comment = f"Manual subtraction: {args.duration}"

    with connect() as connection:
        connection.execute(
            """
            INSERT INTO sessions (
                business, comment, start_time, end_time,
                duration_seconds, entry_type, created_at
            )
            VALUES (?, ?, NULL, NULL, ?, 'correction', ?)
            """,
            (args.business, comment, -seconds, now),
        )
        connection.commit()

    print(f"Subtracted {format_duration(seconds)} from {args.business}.")
    return 0


def command_add(args: argparse.Namespace) -> int:
    try:
        seconds = parse_duration(args.duration)
    except ValueError as error:
        print(f"Could not parse duration. {error}", file=sys.stderr)
        return 1

    now = to_iso(local_now())
    comment = f"Manual addition: {args.duration}"

    with connect() as connection:
        connection.execute(
            """
            INSERT INTO sessions (
                business, comment, start_time, end_time,
                duration_seconds, entry_type, created_at
            )
            VALUES (?, ?, NULL, NULL, ?, 'correction', ?)
            """,
            (args.business, comment, seconds, now),
        )
        connection.commit()

    print(f"Added {format_duration(seconds)} to {args.business}.")
    return 0


def pluralize(count: int, singular: str, plural: str | None = None) -> str:
    word = singular if count == 1 else (plural or f"{singular}s")
    return f"{count} {word}"


def command_remove(args: argparse.Namespace) -> int:
    with connect() as connection:
        counts = connection.execute(
            """
            SELECT
                COUNT(*) AS total_count,
                SUM(CASE WHEN entry_type = 'session' THEN 1 ELSE 0 END) AS session_count,
                SUM(CASE WHEN entry_type = 'correction' THEN 1 ELSE 0 END) AS correction_count,
                SUM(
                    CASE
                        WHEN entry_type = 'session' AND end_time IS NULL THEN 1
                        ELSE 0
                    END
                ) AS active_count
            FROM sessions
            WHERE business = ?
            """,
            (args.business,),
        ).fetchone()

        total_count = int(counts["total_count"] or 0)
        if total_count == 0:
            print(f"No entries found for {args.business}.")
            return 0

        session_count = int(counts["session_count"] or 0)
        correction_count = int(counts["correction_count"] or 0)
        active_count = int(counts["active_count"] or 0)

        if not args.yes:
            summary_parts = [
                pluralize(session_count, "session"),
                pluralize(correction_count, "correction"),
            ]
            if active_count:
                summary_parts.append(pluralize(active_count, "active session"))

            print(
                f"This will permanently remove {pluralize(total_count, 'entry', 'entries')} "
                f"for {args.business} ({', '.join(summary_parts)})."
            )
            try:
                confirmation = input(f'Type "{args.business}" to confirm: ')
            except EOFError:
                print("Remove cancelled.")
                return 1
            if confirmation != args.business:
                print("Remove cancelled.")
                return 1

        deleted_count = connection.execute(
            """
            DELETE FROM sessions
            WHERE business = ?
            """,
            (args.business,),
        ).rowcount
        connection.commit()

    print(f"Removed {pluralize(deleted_count, 'entry', 'entries')} for {args.business}.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="tt",
        description="Track personal work time locally in SQLite.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    start_parser = subparsers.add_parser("start", help="Start a work session.")
    start_parser.add_argument("business", help="Business or client name.")
    start_parser.add_argument(
        "comment",
        nargs="?",
        help='Optional short note about the work. Defaults to "<business> started".',
    )
    start_parser.set_defaults(func=command_start)

    stop_parser = subparsers.add_parser("stop", help="Stop a running work session.")
    stop_parser.add_argument("business", help="Business or client name.")
    stop_parser.set_defaults(func=command_stop)

    status_parser = subparsers.add_parser("status", help="Show running sessions.")
    status_parser.set_defaults(func=command_status)

    report_parser = subparsers.add_parser("report", help="Show tracked time totals.")
    report_parser.add_argument("period", choices=["today", "week", "month"], help="Report period.")
    report_parser.set_defaults(func=command_report)

    subtract_parser = subparsers.add_parser(
        "subtract",
        help="Add a negative correction entry.",
    )
    subtract_parser.add_argument("business", help="Business or client name.")
    subtract_parser.add_argument(
        "duration",
        help='Duration to subtract, such as "30 minutes" or "1.5 hours".',
    )
    subtract_parser.set_defaults(func=command_subtract)

    add_parser = subparsers.add_parser(
        "add",
        help="Add a positive correction entry.",
    )
    add_parser.add_argument("business", help="Business or client name.")
    add_parser.add_argument(
        "duration",
        help='Duration to add, such as "30 minutes" or "1.5 hours".',
    )
    add_parser.set_defaults(func=command_add)

    remove_parser = subparsers.add_parser(
        "remove",
        aliases=["delete"],
        help="Permanently remove all entries for an exact business name.",
    )
    remove_parser.add_argument("business", help="Business or client name to remove.")
    remove_parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Skip confirmation and remove matching entries immediately.",
    )
    remove_parser.set_defaults(func=command_remove)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except sqlite3.Error as error:
        print(f"Database error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
