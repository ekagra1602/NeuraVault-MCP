# Shared text/formatting helpers (no HTTP layer).

from urllib.parse import quote as _percent_quote


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


def line_statistics(text: str) -> dict[str, int]:
    """Count lines from splitlines(); non_blank ignores whitespace-only lines."""
    lines = text.splitlines()
    return {
        'total_lines': len(lines),
        'non_blank_lines': sum(1 for ln in lines if ln.strip()),
    }


def normalize_newlines(text: str) -> str:
    """Convert CRLF and lone CR to LF for consistent cross-platform text."""
    return text.replace('\r\n', '\n').replace('\r', '\n')


def utf8_byte_length(text: str) -> int:
    """Length of the string when encoded as UTF-8 (not the same as len(text) for non-ASCII)."""
    return len(text.encode('utf-8'))


def reverse_word_order(text: str) -> str:
    """Split on arbitrary whitespace, reverse token order, join with single spaces."""
    return ' '.join(reversed(text.split()))


def hex_encode_utf8(text: str) -> str:
    """Lowercase hex string of the UTF-8 byte representation (two hex chars per byte)."""
    return text.encode('utf-8').hex()


def pad_left(text: str, width: int, fill_char: str) -> str:
    """Pad on the left until len(text) >= width using repeated fill_char (caller should pass len(fill_char)==1)."""
    if width <= len(text):
        return text
    gap = width - len(text)
    return (fill_char * gap) + text


def pad_right(text: str, width: int, fill_char: str) -> str:
    """Pad on the right until len(text) >= width using repeated fill_char (caller should pass len(fill_char)==1)."""
    if width <= len(text):
        return text
    gap = width - len(text)
    return text + (fill_char * gap)


def pad_center(text: str, width: int, fill_char: str) -> str:
    """Pad both sides until len(text) >= width; leftover space goes to the right when odd."""
    if width <= len(text):
        return text
    total_gap = width - len(text)
    left = total_gap // 2
    right = total_gap - left
    return (fill_char * left) + text + (fill_char * right)


def strip_optional_prefix(text: str, prefix: str) -> str:
    """Remove leading prefix once if present; empty prefix leaves text unchanged."""
    if not prefix:
        return text
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def strip_optional_suffix(text: str, suffix: str) -> str:
    """Remove trailing suffix once if present; empty suffix leaves text unchanged."""
    if not suffix:
        return text
    if text.endswith(suffix):
        return text[: -len(suffix)]
    return text


def url_quote_utf8(text: str, safe: str = '') -> str:
    """Percent-encode for URLs using UTF-8; characters listed in safe are left as-is."""
    return _percent_quote(text, safe=safe, encoding='utf-8')
