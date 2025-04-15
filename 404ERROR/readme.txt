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
