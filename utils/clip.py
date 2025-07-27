import pyperclip


def check_clipboard(last_clipboard: str) -> str | None:
    """Check clipboard for new content."""
    current = pyperclip.paste()
    if current and current != last_clipboard:
        return current
    return ''