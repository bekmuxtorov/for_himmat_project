async def set_username(username):
    if username:
        return f"https://{username}.t.me"
