from app import create_app
from app.auth.routes import auth_bp
from app.main.blueprint import main_bp
import app.main.routes  

app, db = create_app()

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == "__main__":
    app.run(debug=True)
