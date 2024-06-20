from quart import Blueprint, request
from src.api.v1.action import action
from src.core.producer import get_producer
from src.schemas.base import Click, CustomEvent, Film, KafkaTopic, Page, QualityChange

v1_router = Blueprint("v1", __name__)


@v1_router.route("/click", methods=["POST"])
async def click():
    data = await request.get_json()
    producer = get_producer()
    result = await action(producer, data, Click, KafkaTopic.CLICK.value)
    return result


@v1_router.route("/quality", methods=["POST"])
async def quality():
    data = await request.get_json()
    producer = get_producer()
    result = await action(producer, data, QualityChange, KafkaTopic.QUALITY_CHANGE.value)
    return result


@v1_router.route("/event", methods=["POST"])
async def event():
    data = await request.get_json()
    producer = get_producer()
    result = await action(producer, data, CustomEvent, KafkaTopic.CUSTOM_EVENT.value)
    return result


@v1_router.route("/film", methods=["POST"])
async def film():
    data = await request.get_json()
    producer = get_producer()
    result = await action(producer, data, Film, KafkaTopic.FILM.value)
    return result


@v1_router.route("/page", methods=["POST"])
async def page():
    data = await request.get_json()
    producer = get_producer()
    result = await action(producer, data, Page, KafkaTopic.PAGE.value)
    return result
