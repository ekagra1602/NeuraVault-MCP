# Shared text/formatting helpers (no HTTP layer).


def seconds_as_compact_label(total_seconds: float) -> str:
    """
    Turn a float second count into a short label, e.g. 90 -> "1m30s", 45 -> "45s".
    """
    if total_seconds < 0:
        total_seconds = 0.0
    whole = int(round(total_seconds))
    if whole < 60:
        return f'{whole}s'
    minutes, sec = divmod(whole, 60)
    if minutes < 60:
        return f'{minutes}m{sec}s'
    hours, rest_m = divmod(minutes, 60)
    return f'{hours}h{rest_m}m{sec}s'


def truncate_plain(text: str, max_len: int) -> str:
    """Cut text to max_len chars; if shortened, append an ellipsis (one unicode char)."""
    if max_len < 1:
        return ''
    if len(text) <= max_len:
        return text
    if max_len == 1:
        return text[0]
    return text[: max_len - 1] + '…'


def collapse_whitespace(text: str) -> str:
    """Replace any run of whitespace with single spaces and strip ends."""
    return ' '.join(text.split())
