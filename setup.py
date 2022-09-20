from flask_todo import create_app


flask_todo_app = create_app()

if __name__ == '__main__':
    flask_todo_app.run(debug=True)