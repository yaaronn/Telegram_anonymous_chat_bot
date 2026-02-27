reports = {}
banned_users = set()
message_counts = {}


def is_banned(user_id):
    return user_id in banned_users


def record_message(user_id):
    message_counts[user_id] = message_counts.get(user_id, 0) + 1

    if message_counts[user_id] > 20:
        return True

    return False


def report_user(user_id):

    reports[user_id] = reports.get(user_id, 0) + 1

    if reports[user_id] >= 3:
        banned_users.add(user_id)
        return True

    return False