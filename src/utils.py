def parse_lms_event(event_str: str) -> str:
    """Normalize event types."""
    event_map = {
        "login": "login",
        "submit": "assignment",
        "post": "forum",
        "attempt": "quiz"
    }
    return event_map.get(event_str.lower(), "other")