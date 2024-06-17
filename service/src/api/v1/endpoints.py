from quart import request
from src.api import v1_router
from src.api.v1 import action
from src.core.config.base import KafkaTopic
from src.schemas.base import Click, CustomEvent, Film, Page, QualityChange


@v1_router.route("/click", methods=["POST"])
async def click():
    await action(data=await request.get_json(), schema=Click, topic=KafkaTopic.CLICK)


@v1_router.route("/quality", methods=["POST"])
async def quality():
    await action(data=await request.get_json(), schema=QualityChange, topic=KafkaTopic.QUALITY_CHANGE)


@v1_router.route("/event", methods=["POST"])
async def event():
    await action(data=await request.get_json(), schema=CustomEvent, topic=KafkaTopic.CUSTOM_EVENT)


@v1_router.route("/film", methods=["POST"])
async def film():
    await action(data=await request.get_json(), schema=Film, topic=KafkaTopic.FILM)


@v1_router.route("/page", methods=["POST"])
async def page():
    await action(data=await request.get_json(), schema=Page, topic=KafkaTopic.PAGE)
