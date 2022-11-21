from src import create_app, app
if __name__ == "__main__":
    socketio = create_app()
    socketio.run(app=app, debug=True, port=5000)
