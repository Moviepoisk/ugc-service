from quart import Quart
from src.api.v1.endpoints import v1_router
from src.core.producer import start_producer, stop_producer

app = Quart(__name__)
app.register_blueprint(v1_router, url_prefix="/api/v1")


@app.before_serving
async def startup():
    await start_producer()


@app.after_serving
async def cleanup():
    await stop_producer()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Сервер будет слушать на всех интерфейсах
