from application.models.post import Post
from application.models.errors import NotFoundError, UnauthorizedError


def create_post(user, msg):
    """
    Create a new post
    """

    post = Post(msg=msg, user=user)
    post.save()
    return get_post_by_counter_id(user, post.counter_id)


def get_post_by_counter_id(user, counter_id):
    """
    Get a post by counter id
    """

    post = Post.objects(counter_id=int(counter_id)).first()

    if post is None:
        raise NotFoundError("Post not found")

    return post


def delete_post(user, counter_id, id):
    """
    Delete a post
    """

    post = get_post_by_counter_id(user, counter_id)

    if not post:
        raise NotFoundError("Post not found")
    
    if str(post.id) != id:
        raise UnauthorizedError("Could not find post with that key")
    
    if not user and post.user:
        raise UnauthorizedError("You cant delete this post.")

    if user and post.user and str(post.user.id) != str(user.id):
        raise UnauthorizedError("You cant delete this post.")

    post.delete()
    return post


def get_posts():
    """
    Get a post
    """
    posts = Post.objects()
    return list(map(lambda post: post.to_response(), posts))


def get_posts_search(search):
    """
    Get a post
    """
    if not isinstance(search, str):
        raise Exception("Search is not string")

    search = search.strip()
    if not search:
        raise Exception("Search is empty")

    posts = Post.objects(msg__icontains=search)
    post_list = [post.to_response(True) for post in posts]
    return post_list
