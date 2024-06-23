import logging

from quart import Blueprint
from src.api.v1.utils import common_endpoint
from src.schemas.base import Click, CustomEvent, Film, KafkaTopic, Page, QualityChange

v1_router = Blueprint("v1", __name__)
logger = logging.getLogger(__name__)


@v1_router.errorhandler(Exception)
async def handle_exception(e):
    logger.error(f"An error occurred: {e}")
    return {"status": "error", "message": str(e)}, 500


@v1_router.route("/click", methods=["POST"])
@common_endpoint(Click, KafkaTopic.CLICK.value)
async def click():
    pass


@v1_router.route("/quality", methods=["POST"])
@common_endpoint(QualityChange, KafkaTopic.QUALITY_CHANGE.value)
async def quality():
    pass


@v1_router.route("/event", methods=["POST"])
@common_endpoint(CustomEvent, KafkaTopic.CUSTOM_EVENT.value)
async def event():
    pass


@v1_router.route("/film", methods=["POST"])
@common_endpoint(Film, KafkaTopic.FILM.value)
async def film():
    pass


@v1_router.route("/page", methods=["POST"])
@common_endpoint(Page, KafkaTopic.PAGE.value)
async def page():
    pass
