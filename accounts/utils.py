

def is_logged_in(request):
    """Return True if the session contains a `user_id` key.

    Usage:
        from accounts.utils import is_logged_in
        if is_logged_in(request):
            # user is logged in (session contains user_id)
    """
    try:
        return bool(request.session.get('user_id'))
    except Exception:
        return False
