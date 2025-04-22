from app import create_app
from app.auth.routes import auth_bp
from app.main.blueprint import main_bp
import app.main.routes  

app, db = create_app()

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
