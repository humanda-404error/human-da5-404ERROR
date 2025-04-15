from flask import Flask
from app.main.routes import main_bp
from app.auth.routes import auth_bp

import secrets

app = Flask(__name__, 
            template_folder='app/main/templates',
            static_folder='app/static')
app.secret_key = secrets.token_hex(32)

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    app.run(debug=True)  # debug=True로 실행하면 코드 수정 시 자동으로 서버가 재시작됩니다.