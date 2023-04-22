from application.models.user import User


def create_user(username, password):
    """
    Create a new user
    """
    already_exists = User.objects(username=username).first()

    if already_exists:
        raise Exception("User already exists")

    
    user = User.init_for_create(username, password)
    user.save()
    return user
