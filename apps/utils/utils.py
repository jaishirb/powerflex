import asyncio
import re
from datetime import datetime
from typing import Dict, Callable, Awaitable, Tuple, Any, Mapping
from zoneinfo import ZoneInfo

import html2text
import markdown
import pytz
from babel.dates import format_datetime


def format_date(date: str, time: str) -> datetime:
    """Format the given dates and times into datetime objects.

    Args:
        date (str): The date of the range.
        time (str): The time of the range.

    Returns:
        datetime: The datetime objects for the start and end of the range.
    """
    date = datetime.strptime(date, "%d/%m/%Y")

    time = datetime.strptime(time, "%H:%M").time()

    start_datetime = datetime.combine(date.date(), time)

    colombian_timezone = pytz.timezone("America/Bogota")
    start_datetime_colombian = colombian_timezone.localize(start_datetime)

    return start_datetime_colombian


def markdown_to_plain_text(markdown_text: str) -> str:
    html_content = markdown.markdown(markdown_text)
    combined_pattern = re.compile(r"<[^<]+?>|## |\*\*")
    plain_text = combined_pattern.sub("", html_content)
    plain_text = html2text.html2text(plain_text)
    return plain_text.strip()


def map_to_datetime(date_calendar: Dict[str, str]) -> datetime:
    naive_datetime = datetime.fromisoformat(date_calendar.get("dateTime"))
    timezone = ZoneInfo(date_calendar.get("timeZone"))
    return naive_datetime.astimezone(timezone)


def format_event_time(start_time: datetime, end_time: datetime) -> str:
    start_day = format_datetime(start_time, "EEEE", locale="es")
    start_date = format_datetime(start_time, "d 'de' MMMM 'de' yyyy", locale="es")
    start_hour = format_datetime(start_time, "h:mm a", locale="es")

    end_day = format_datetime(end_time, "EEEE", locale="es")
    end_date = format_datetime(end_time, "d 'de' MMMM 'de' yyyy", locale="es")
    end_hour = format_datetime(end_time, "h:mm a", locale="es")

    if start_date == end_date:
        return f"{start_day} {start_date} desde las {start_hour} hasta las {end_hour}"
    else:
        return (
            f"{start_day} {start_date} desde las {start_hour} hasta el "
            f"{end_day.lower()} {end_date} a las {end_hour}"
        )


def sync_wrapper(
    async_func: Callable[..., Awaitable[None]],
    *args: Tuple[Any, ...],
    **kwargs: Mapping[str, Any],
) -> None:
    """
    Wrapper to run an async function synchronously.

    Args:
        async_func (Callable[..., Awaitable[None]]): The async function to be run.
        *args (Tuple[Any, ...]): Positional arguments to pass to the async function.
        **kwargs (Mapping[str, Any]): Keyword arguments to pass to the async function.
    """

    async def coroutine_wrapper():
        await async_func(*args, **kwargs)

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop and loop.is_running():
        # If there's already a running event loop, create a new task and run it
        future = asyncio.ensure_future(coroutine_wrapper())
        loop.run_until_complete(future)
    else:
        asyncio.run(coroutine_wrapper())
