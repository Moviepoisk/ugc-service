import logging
from quart import request, jsonify
from motor.motor_asyncio import AsyncIOMotorClient
from quart import Blueprint
from elasticsearch import AsyncElasticsearch
import os

from src.api.v1.utils import common_endpoint
from src.schemas.base import Click, CustomEvent, Film, KafkaTopic, Page, QualityChange

v1_router = Blueprint("v1", __name__)

# Настройка логгера для UGC сервиса
logger = logging.getLogger("ugc_service")
logger.setLevel(logging.INFO)

# Настройка обработчика для отправки логов в Elasticsearch
es_host = os.getenv("ES_HOST", "http://elasticsearch:9200")
es = AsyncElasticsearch([es_host])

class ElasticsearchHandler(logging.Handler):
    async def emit(self, record):
        log_entry = self.format(record)
        tag = getattr(record, 'tag', 'default')
        index = f"{tag}-%{self.format_date()}"
        await es.index(index=index, document=log_entry)

    def format_date(self):
        return self.formatter.formatTime(self.formatter.converter(), "%Y.%m.%d")

handler = ElasticsearchHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

@v1_router.errorhandler(Exception)
async def handle_exception(e):
    logger.error(f"An error occurred: {e}", extra={'tag': 'ugc_app'})
    return {"status": "error", "message": str(e)}, 500

@v1_router.route("/click", methods=["POST"])
@common_endpoint(Click, KafkaTopic.CLICK.value)
async def click():
    logger.info("Click event received", extra={'tag': 'ugc_app'})
    pass

@v1_router.route("/quality", methods=["POST"])
@common_endpoint(QualityChange, KafkaTopic.QUALITY_CHANGE.value)
async def quality():
    logger.info("Quality change event received", extra={'tag': 'ugc_app'})
    pass

@v1_router.route("/event", methods=["POST"])
@common_endpoint(CustomEvent, KafkaTopic.CUSTOM_EVENT.value)
async def event():
    logger.info("Custom event received", extra={'tag': 'ugc_app'})
    pass

@v1_router.route("/film", methods=["POST"])
@common_endpoint(Film, KafkaTopic.FILM.value)
async def film():
    logger.info("Film event received", extra={'tag': 'ugc_app'})
    pass

@v1_router.route("/page", methods=["POST"])
@common_endpoint(Page, KafkaTopic.PAGE.value)
async def page():
    logger.info("Page event received", extra={'tag': 'ugc_app'})
    pass

# Подключение к MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["movie_database"]

# Конвертация ObjectId в строку
def convert_objectid(data):
    if isinstance(data, list):
        for item in data:
            item["_id"] = str(item["_id"])
    else:
        data["_id"] = str(data["_id"])
    return data

# Маршрут для добавления лайка
@v1_router.route("/like", methods=["POST"])
async def add_like():
    data = await request.get_json()
    result = await db.likes.insert_one(data)
    logger.info(f"Like added: {str(result.inserted_id)}", extra={'tag': 'ugc_app'})
    return jsonify({"_id": str(result.inserted_id)}), 201

# Маршрут для получения лайков фильма
@v1_router.route("/likes/<movie_id>", methods=["GET"])
async def get_likes(movie_id):
    likes = await db.likes.find({"movie_id": movie_id}).to_list(length=None)
    logger.info(f"Likes retrieved for movie: {movie_id}", extra={'tag': 'ugc_app'})
    return jsonify(convert_objectid(likes))

# Маршрут для добавления закладки
@v1_router.route("/bookmark", methods=["POST"])
async def add_bookmark():
    data = await request.get_json()
    result = await db.bookmarks.insert_one(data)
    logger.info(f"Bookmark added: {str(result.inserted_id)}", extra={'tag': 'ugc_app'})
    return jsonify({"_id": str(result.inserted_id)}), 201

# Маршрут для получения закладок пользователя
@v1_router.route("/bookmarks/<user_id>", methods=["GET"])
async def get_bookmarks(user_id):
    bookmarks = await db.bookmarks.find({"user_id": user_id}).to_list(length=None)
    logger.info(f"Bookmarks retrieved for user: {user_id}", extra={'tag': 'ugc_app'})
    return jsonify(convert_objectid(bookmarks))

# Маршрут для добавления рецензии
@v1_router.route("/review", methods=["POST"])
async def add_review():
    data = await request.get_json()
    result = await db.reviews.insert_one(data)
    logger.info(f"Review added: {str(result.inserted_id)}", extra={'tag': 'ugc_app'})
    return jsonify({"_id": str(result.inserted_id)}), 201

# Маршрут для получения рецензий фильма
@v1_router.route("/reviews/<movie_id>", methods=["GET"])
async def get_reviews(movie_id):
    reviews = await db.reviews.find({"movie_id": movie_id}).to_list(length=None)
    logger.info(f"Reviews retrieved for movie: {movie_id}", extra={'tag': 'ugc_app'})
    return jsonify(convert_objectid(reviews))

# Маршрут для добавления лайка к рецензии
@v1_router.route("/review/like", methods=["POST"])
async def add_review_like():
    data = await request.get_json()
    result = await db.review_likes.insert_one(data)
    logger.info(f"Review like added: {str(result.inserted_id)}", extra={'tag': 'ugc_app'})
    return jsonify({"_id": str(result.inserted_id)}), 201

# Маршрут для получения лайков рецензии
@v1_router.route("/review/likes/<review_id>", methods=["GET"])
async def get_review_likes(review_id):
    likes = await db.review_likes.find({"review_id": review_id}).to_list(length=None)
    logger.info(f"Review likes retrieved for review: {review_id}", extra={'tag': 'ugc_app'})
    return jsonify(convert_objectid(likes))

# Закрытие соединений при завершении работы приложения
@v1_router.before_app_shutdown
async def shutdown():
    await client.close()
    await es.close()
