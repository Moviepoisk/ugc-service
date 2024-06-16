from quart import Blueprint

v1_router = Blueprint("router", __name__, url_prefix="/api/v1")
