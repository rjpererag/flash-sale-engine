from .redis_app.api import app


def start_app() -> None:
    app.run(host="0.0.0.0", port=8080, debug=True)


if __name__ == '__main__':
    start_app()
