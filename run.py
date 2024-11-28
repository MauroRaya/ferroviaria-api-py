from services import create_app
from services.db import db

app = create_app()

with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80, debug=True)