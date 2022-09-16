import logging

from flask import Blueprint, jsonify, abort
from blue_post.dao.comment import Comment
from blue_post.dao.comment_dao import CommentDAO
from blue_post.dao.post import Post
from config import DATA_PATH_POSTS, DATA_PATH_COMMENTS
from blue_post.dao.post_dao import PostDAO

blue_api = Blueprint("blue_api", __name__)

post_dao = PostDAO(DATA_PATH_POSTS)

comments_dao = CommentDAO(DATA_PATH_COMMENTS)
api_logger = logging.getLogger("api_logger")


@blue_api.route('/')
def api_posts_hello():
    return "Это апи. Смотри документацию"


@blue_api.route('/posts/')
def api_posts_all():
    """Эндпоинт всех постов"""
    all_posts: list[Post] = post_dao.get_all()
    all_posts_as_dicts: list[dict] = [post.as_dict() for post in all_posts]
    api_logger.debag("Запрошены все посты")
    return jsonify(all_posts_as_dicts), 200


@blue_api.route('/posts/<int:pk>')
def api_posts_single(pk: int):
    """Эндпоинт одного поста"""
    post: Post | None = post_dao.get_by_bk(pk)
    if post is None:
        api_logger.debag(f"Обращение к несуществующему посту {pk}")
        abort(404)
    api_logger.debag(f"Запрошен пост {pk}")

    return jsonify(post.as_dict()), 200


@blue_api.errorhandler(404)
def api_error_404(error):
    api_logger.error(f"Ошибка {error}")
    return jsonify({"error": str(error)}), 404
