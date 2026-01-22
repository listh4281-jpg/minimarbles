from app import create_app

app = create_app()

if __name__ == '__main__':
    # debug=True auto-reloads when you change code
    app.run(debug=True)
