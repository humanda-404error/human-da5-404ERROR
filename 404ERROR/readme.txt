#######################################################
**Prj Setting
1. pip install -r requirements.txt
2. execute : python run.py
#######################################################
#######################################################
**Prj make files
404ERROR/
│
├── app/
│   ├── __init__.py       # 앱 생성 함수
│   ├── main/
│   │   ├── __init__.py  # main 모듈 초기화
│   │   ├── routes.py    # URL 라우팅 정의
│   │   └── templates/
│   │       └── main/
│   │           └── index.html  # main 관련 HTML 템플릿
│   ├── auth/
│   │   ├── __init__.py  # auth 모듈 초기화
│   │   ├── routes.py    # 인증 관련 URL 라우팅 정의
│   │   └── templates/
│   │       └── auth/
│   │           └── login.html  # 로그인 페이지 템플릿
│   ├── models/
│   │   ├── __init__.py  # 모델 모듈 초기화
│   │   ├── user.py      # 사용자 관련 데이터 모델
│   │   └── post.py      # 게시물 관련 데이터 모델
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css  # 스타일 시트
│   │   ├── js/
│   │   │   └── script.js  # 자바스크립트 파일
│   │   └── img/
│   │       └── logo.png  # 이미지 파일
│   └── templates/
│       ├── base.html     # 공통 템플릿
│       └── includes/
│           ├── header.html  # 헤더 템플릿
│           └── footer.html  # 푸터 템플릿
│
├── config.py             # 앱 설정 파일
├── requirements.txt      # 프로젝트 종속성 목록
├── run.py                # 앱 실행 스크립트
└── README.md             # 프로젝트 설명서
######################################################

######################################################
**작업해야될 내용**
@main_bp.route('/db_user_data/<int:user_id>')
def db_user_data(user_id):
    # 1. 사용자의 정보 가져오기
    member = Member.query.get_or_404(user_id)
    
    # 2. 사용자의 트레인 데이터 가져오기
    trains = Train.query.filter_by(district=member.district).all()
    
    # 3. 사용자의 날씨 데이터 가져오기
    weather_data = Weather.query.filter_by(date=member.weather_date).all()
    
    # 4. 사용자의 인구 데이터 가져오기
    population_data = Population.query.filter_by(district=member.district).all()
    
    # 데이터 분석 (예: 평균 승차총승객수)
    avg_boarding_passengers = sum([train.total_boarding_passengers for train in trains]) / len(trains) if len(trains) > 0 else 0
    
    return render_template('db_user_data.html', 
                           member=member, 
                           trains=trains, 
                           weather_data=weather_data,
                           population_data=population_data, 
                           avg_boarding_passengers=avg_boarding_passengers)