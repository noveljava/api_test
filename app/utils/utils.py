from datetime import datetime


def get_current_time() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

