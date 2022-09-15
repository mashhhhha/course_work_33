from flask import Blueprint, render_template, current_app, request
from werkzeug.exceptions import abort

from blue_post.dao.comment import Comment
from blue_post.dao.comment_dao import CommentDAO
from blue_post.dao.post import Post
from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS
from blue_post.dao.post_dao import PostDAO

blue_post = Blueprint("blue_post", __name__, template_folder="templates")
post_dao = PostDAO(DATA_PATH_POSTS)
comments_dao = CommentDAO(DATA_PATH_COMMENTS)

@blue_post.route("/")
def page_posts_index():
    """Страничка всех постов"""
    all_posts = post_dao.get_all()
    return render_template("posts_index.html", posts=all_posts)

@blue_post.route("/posts/<int:pk>/")
def page_posts_single(pk: int):
    """Страничка одного поста"""
    post: Post | None = post_dao.get_by_bk(pk)
    comments: list[Comment] = comments_dao.get_comments_by_post_pk(pk)

    if post is None:
        abort(404)

    return render_template("posts_single.html", post=post, comments=comments, comments_len=len(comments))

@blue_post.route("/users/<user_name>")
def page_posts_by_user(user_name: str):
    """Возвращает посты пользователя"""
    posts: list[Post] = post_dao.get_by_poster(user_name)
    if posts == []:
        abort(404, "Такого пользователя не существует")
    return render_template("posts_user-feed.html", posts=posts, user_name=user_name)

@blue_post.route("/search/")
def page_posts_search():
    """Возвращает посты пользователя"""

    query: str = request.args.get("s", "")

    if query == "":
        posts: list = []
    else:
        posts: list[Post] = post_dao.search_in_content(query)

    return render_template("posts_search.html", posts=posts, query=query, posts_len=len(posts))
