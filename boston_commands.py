"""Boston-specific exact-match BBS command aliases."""
SHORTCUTS = {'/boston': 'x', '/hub': 'x', '/menu': 'x', '/help': 'q', '/mail': 'cm', '/inbox': 'cm', '/boards': 'b', '/neighborhood': 'b', '/fortune': 'f', '/tools': 'u', '/dispatch': 'u', '/cancel': 'x'}

def resolve_shortcut(message, state=None):
    if not isinstance(message, str):
        return None
    key = message.strip().casefold()
    if (state or {}).get('command') in {'BULLETIN_POST', 'BULLETIN_POST_CONTENT', 'MAIL', 'BULLETIN_READ'} and key not in {'/boston', '/hub', '/menu', '/help', '/cancel'}:
        return None
    return SHORTCUTS.get(key)
