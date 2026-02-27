waiting_users = []
active_chats = {}


def find_match(user_id):

    if user_id in active_chats:
        return None

    if user_id in waiting_users:
        return None

    if waiting_users:
        partner = waiting_users.pop(0)

        active_chats[user_id] = partner
        active_chats[partner] = user_id

        return partner

    waiting_users.append(user_id)
    return None


def get_partner(user_id):
    return active_chats.get(user_id)


def leave_chat(user_id):

    partner = active_chats.pop(user_id, None)

    if partner:
        active_chats.pop(partner, None)

    return partner