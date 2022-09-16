from flask import Flask, render_template

import logger
from blue_api.views import blue_api
from blue_post.views import blue_post
from data.exceptions.exceptions import DataSourceError


def create_and_config_app(config_path):
    app = Flask(__name__)

    app.register_blueprint(blue_post)
    app.register_blueprint(blue_api, url_prefix='/api')
    app.config.from_pyfile(config_path)
    logger.config(app)

    return app


app = create_and_config_app("config.py")


@app.errorhandler(404)
def page_error_404(error):
    return f"Такой страницы нет {error}", 404


@app.errorhandler(500)
def page_error_500(error):
    return f"На сервере произошла ошибка - {error}", 500


@app.errorhandler(DataSourceError)
def page_error_data_source(error):
    return f"Ошибка, на сайте сломались данные - {error}", 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
