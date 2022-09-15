import json
from json import JSONDecodeError

from blue_post.dao.comment import Comment
from data.exceptions.exceptions import DataSourceError

class CommentDAO:
    def __init__(self, path):
        self.path = path
    def _load_data(self):
        """
        Загружает данные из JSON и возвращает список словарей
        """
        try:
            with open(self.path, 'r', encoding='utf-8') as file:
                posts_data = json.load(file)
        except (FileNotFoundError, JSONDecodeError):
            raise DataSourceError(f'Не удается получить данные из файла {self.path}')

        return posts_data

    def _load_comments(self):
        """Возвращает список элементов Comment"""
        comments_data = self._load_data()
        list_of_posts = [Comment(**comment_data) for comment_data in comments_data]

        comments = [Comment(**comment_data) for comment_data in comments_data]

        return list_of_posts

    def get_comments_by_post_pk(self, post_pk: int) -> list[Comment]:
        """Получает все комментарии к посту по его пк"""
        comments: list[Comment] = self._load_comments()
        comments_match: list[Comment] = [c for c in comments if c.post_pk == post_pk]
        return comments_match