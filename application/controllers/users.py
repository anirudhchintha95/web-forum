from application.models.user import User
from application.models.post import Post


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

def get_user_by_key(counter_id):
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
    post_list = [post.to_response() for post in posts]
    return post_list

def delete_post(user, counter_id, id):
    """
    Delete a post
    """
    if user:
        user = user.to_response()

    post = Post.objects(counter_id=int(counter_id)).first()
    if not post:
        raise Exception("Post not found")

    if str(post.id) != id:
        raise Exception("Post not found")

    post.delete()
    return post


