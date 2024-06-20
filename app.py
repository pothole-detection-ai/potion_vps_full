from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from config import Config
from routes import register_routes
from socketio_handlers import register_socketio_handlers

app = Flask(__name__, static_folder="./templates/static")
CORS(app)
app.config.from_object(Config)
socketio = SocketIO(app, async_mode="eventlet", cors_allowed_origins="*")

register_routes(app)
register_socketio_handlers(socketio)

if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')
    # socketio.run(app, debug=True, port=5000)
