from app import create_app

# Flask app from create_app function
flask_app = create_app()

if __name__ == "__main__":
    # Threaded option to enable multiple instances for multiple user access support
    flask_app.run(threaded=True, port=8080)