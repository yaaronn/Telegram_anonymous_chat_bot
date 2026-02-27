stats = {
    "users": set(),
    "searching": 0,
    "matches": 0,
    "messages": 0
}


def user_started(user_id):
    stats["users"].add(user_id)


def searching_add():
    stats["searching"] += 1


def searching_remove():
    if stats["searching"] > 0:
        stats["searching"] -= 1


def match_created():
    stats["matches"] += 1


def message_sent():
    stats["messages"] += 1


def get_stats():
    return {
        "users": len(stats["users"]),
        "searching": stats["searching"],
        "matches": stats["matches"],
        "messages": stats["messages"]
    }