from login import create_app


todo_app = create_app()

if __name__ == '__main__':
    todo_app.run(debug=True)