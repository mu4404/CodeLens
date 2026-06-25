def get_user_age(user):
    return user["age"]


def is_adult(user):
    return get_user_age(user) > 18
