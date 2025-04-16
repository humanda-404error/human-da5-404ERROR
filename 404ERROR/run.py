from app import create_app
from app.auth.routes import auth_bp  # auth 블루프린트 임포트
from app.main.blueprint import main_bp  # 또는 from app.main import main_bp
from app.main.routes import *  # 모든 라우트 연결 코드 포함

app, db = create_app()  # app과 db를 반환받습니다

# auth 블루프린트와 main 블루프린트 등록
app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)


if __name__ == "__main__":
    app.run(debug=True)  # 서버 실행
