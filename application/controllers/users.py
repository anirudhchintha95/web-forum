from application.models.user import User
from application.models.post import Post


def create_user(username, password, firstname):
    """
    Create a new user
    """
    already_exists = User.objects(username=username).first()

    if already_exists:
        raise Exception("User already exists")

    user = User.init_for_create(username, password, firstname)
    user.save()
    return user

def get_user_by_key(user_key):
    """
    Get a user by user_key
    """
    user = User.objects(key=user_key).first()
    if not user:
        raise Exception("User not found")
    return user

def edit_user_by_key(user_key, username, password, firstname):
    """
    Edit a user by user_key
    """
    user = User.objects(key=user_key).first()
    if not user:
        raise Exception("User not found")

    hasUpdates = False
    if username and username.lower() != user.username.lower():
        hasUpdates = True
        user.username = username
    if password and not user.check_password(password):
        hasUpdates = True
        user.password = password
    if firstname and firstname.lower() != user.firstname.lower():
        hasUpdates = True
        user.firstname = firstname

    if not hasUpdates:
        raise Exception("Please provide at least one update to change user details")

    user.save()
    return user

def get_user_by_counterId(counter_id):
    """
    Get a user by counter_id
    """
    user = User.objects(counter_id=int(counter_id)).first()
    if not user:
        raise Exception("User not found")
    return user

def create_post(user, msg):
    """
    Create a new post
    """
    post = Post(msg=msg, user=user)
    post.save()
    return post

def get_posts(user):
    """
    Get all posts
    """
    posts = Post.objects(
        user=user
    )
    post_list = [post.to_response(True) for post in posts]
    return post_list

def delete_post(user, counter_id, id):
    """
    Delete a post
    """

    post = Post.objects(counter_id=int(counter_id)).first()
    if not post:
        raise Exception("Post not found")

    if str(post.id) != id:
        raise Exception("Post not found")

    post.delete()
    return post


