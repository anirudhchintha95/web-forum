from application.models.post import Post


def create_post(user, msg):
    """
    Create a new post
    """

    post = Post(msg=msg, user=user)
    post.save()
    return post


def get_post_by_counter_id(user, counter_id):
    """
    Get a post by counter id
    """

    post = Post.objects(counter_id=int(counter_id)).first()

    if user:
        if post.user and str(post.user.id) != str(user.id):
            raise Exception("Post not found")

    if not post:
        raise Exception("Post not found")
    
    return post


def delete_post(user, counter_id, id):
    """
    Delete a post
    """
    if user:
        user = user.to_response()

    post = get_post_by_counter_id(user, counter_id)
    if not post:
        raise Exception("Post not found")

    if str(post.id) != id:
        raise Exception("Post not found")

    post.delete()
    return post

def get_posts():
    """
    Get a post
    """
    posts = Post.objects()
    return list(map(lambda post: post.to_response(), posts))
