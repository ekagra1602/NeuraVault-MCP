# Shared text/formatting helpers (no HTTP layer).

import codecs as _codecs
import html as _html
import json as _json
import re as _re
import textwrap as _textwrap
import zlib as _zlib
from urllib.parse import quote as _percent_quote, unquote as _percent_unquote

_SPACE_RUN = _re.compile(r' +')


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


def truncate_each_line(text: str, max_len: int) -> str:
    """Apply truncate_plain to every line; line breaks preserved."""
    lines = text.splitlines()
    if not lines:
        return text
    return '\n'.join(truncate_plain(line, max_len) for line in lines)


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


def number_lines(text: str, start: int = 1, sep: str = ': ') -> str:
    """Prefix each line with a line number and separator (default '1: ')."""
    lines = text.splitlines()
    if not lines:
        return text
    return '\n'.join(f'{i}{sep}{line}' for i, line in enumerate(lines, start=start))


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


def prefix_each_line(text: str, prefix: str) -> str:
    """Prepend prefix to every line; splitlines/rejoin with LF (no trailing newline added)."""
    lines = text.splitlines()
    if not lines:
        return text
    return '\n'.join(prefix + line for line in lines)


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


def suffix_each_line(text: str, suffix: str) -> str:
    """Append suffix to every line; splitlines/rejoin with LF (no trailing newline added)."""
    lines = text.splitlines()
    if not lines:
        return text
    return '\n'.join(line + suffix for line in lines)


def url_quote_utf8(text: str, safe: str = '') -> str:
    """Percent-encode for URLs using UTF-8; characters listed in safe are left as-is."""
    return _percent_quote(text, safe=safe, encoding='utf-8')


def url_unquote_utf8(text: str) -> str:
    """
    Decode percent-encoded octets as UTF-8. Uses strict error handling so invalid
    %-sequences or non-UTF-8 byte runs surface as UnicodeDecodeError to callers.
    """
    return _percent_unquote(text, encoding='utf-8', errors='strict')


def escape_html(text: str) -> str:
    """Escape &, <, >, and double quotes for safe use in HTML text or attributes."""
    return _html.escape(text, quote=True)


def rot13(text: str) -> str:
    """Apply ROT13 to ASCII letters; digits and symbols unchanged. Self-inverse."""
    return _codecs.decode(text, 'rot_13')


def json_string_literal(text: str) -> str:
    """Encode as a JSON string token (quotes, escapes, and Unicode as needed)."""
    return _json.dumps(text, ensure_ascii=False)


def crc32_hex_utf8(text: str) -> str:
    """CRC-32 over UTF-8 bytes; return 8 lowercase hex digits (IEEE polynomial)."""
    n = _zlib.crc32(text.encode('utf-8')) & 0xFFFFFFFF
    return f'{n:08x}'


def dedent_block(text: str) -> str:
    """Remove common leading whitespace from each line (textwrap.dedent)."""
    return _textwrap.dedent(text)


def indent_block(text: str, width: int = 4) -> str:
    """Prefix every line with width spaces; width clamped to 1..32."""
    w = max(1, min(width, 32))
    prefix = ' ' * w
    lines = text.splitlines()
    if not lines:
        return text
    return '\n'.join(prefix + line for line in lines)


def reverse_lines(text: str) -> str:
    """Reverse order of lines (splitlines); join with LF only. Trailing newline not preserved."""
    return '\n'.join(reversed(text.splitlines()))


def sort_lines(text: str) -> str:
    """Sort lines lexicographically (splitlines); join with LF. Empty input yields empty string."""
    return '\n'.join(sorted(text.splitlines()))


def unique_lines(text: str) -> str:
    """Drop duplicate lines; keep first occurrence order (splitlines; rejoin with LF)."""
    return '\n'.join(dict.fromkeys(text.splitlines()))


def fill_wrapped(text: str, width: int) -> str:
    """Reflow text like a paragraph (textwrap.fill); width clamped to 1..500."""
    w = max(1, min(width, 500))
    return _textwrap.fill(text, width=w, break_long_words=True, break_on_hyphens=True)


def expand_tabs(text: str, tabsize: int) -> str:
    """Replace tab characters with spaces; tabsize clamped to 1..32."""
    ts = max(1, min(tabsize, 32))
    return text.expandtabs(ts)


def zfill_to_width(text: str, width: int) -> str:
    """Left-pad numeric strings with zeros (str.zfill); width clamped 1..10_000."""
    w = max(1, min(width, 10_000))
    return text.zfill(w)


def remove_blank_lines(text: str) -> str:
    """Drop lines that are empty or whitespace-only (splitlines; rejoin with LF)."""
    return '\n'.join(line for line in text.splitlines() if line.strip())


def casefold_text(text: str) -> str:
    """Unicode case folding (str.casefold); stronger than lower() for comparisons."""
    return text.casefold()


def squeeze_spaces_per_line(text: str) -> str:
    """Collapse runs of spaces within each line; line breaks preserved."""
    return '\n'.join(_SPACE_RUN.sub(' ', line) for line in text.splitlines())


def strip_each_line(text: str) -> str:
    """Strip leading and trailing whitespace from each line; line breaks preserved."""
    return '\n'.join(line.strip() for line in text.splitlines())


def count_vowels(text: str) -> int:
    """Count ASCII vowels in the text, treating uppercase and lowercase equally."""
    vowels = {'a', 'e', 'i', 'o', 'u'}
    return sum(1 for ch in text.casefold() if ch in vowels)


def count_consonants(text: str) -> int:
    """Count ASCII consonants (a-z minus vowels), treating case equally."""
    vowels = {'a', 'e', 'i', 'o', 'u'}
    return sum(1 for ch in text.casefold() if 'a' <= ch <= 'z' and ch not in vowels)


def count_digits(text: str) -> int:
    """Count ASCII decimal digits (0-9) in the text."""
    return sum(1 for ch in text if '0' <= ch <= '9')


def count_whitespace(text: str) -> int:
    """Count whitespace characters (str.isspace), including spaces, tabs, and newlines."""
    return sum(1 for ch in text if ch.isspace())


def count_letters(text: str) -> int:
    """Count alphabetic characters (str.isalpha); covers Unicode letters, not just ASCII."""
    return sum(1 for ch in text if ch.isalpha())


def count_uppercase(text: str) -> int:
    """Count uppercase characters (str.isupper); Unicode-aware."""
    return sum(1 for ch in text if ch.isupper())


def count_lowercase(text: str) -> int:
    """Count lowercase characters (str.islower); Unicode-aware."""
    return sum(1 for ch in text if ch.islower())


def count_words(text: str) -> int:
    """Count whitespace-delimited tokens (str.split with no args collapses runs)."""
    return len(text.split())


def count_lines(text: str) -> int:
    """Count lines using str.splitlines (no trailing empty line for terminal newline)."""
    return len(text.splitlines())


def swap_case(text: str) -> str:
    """Swap uppercase and lowercase characters (str.swapcase); Unicode-aware."""
    return text.swapcase()
