import os
import signal
from app.bootstrap import create_app
from app.bootstrap.config import Config

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.APP_HOST,
        port=Config.APP_PORT,
        debug=Config.DEBUG)