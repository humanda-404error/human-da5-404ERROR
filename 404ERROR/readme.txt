#######################################################
find . -type d -name "__pycache__" -exec rm -r {} +
**Prj Setting
1. pip install -r requirements.txt
2. execute : python run.py
#######################################################
#######################################################
**Prj make files
404ERROR/
│
├── app/
└── main/
    ├── __init__.py                  # main 모듈 초기화
    ├── blueprint.py                 # main Blueprint 등록
    ├── routes.py                    # 공통 라우팅 처리

    ├── commons/
    │   └── common_routes.py         # 공통 기능에 대한 라우터

    ├── JSC/
    │   ├── __init__.py
    │   ├── JSC_analyze_logic.py     # JSC 데이터 분석 로직
    │   ├── jSC_routes.py            # JSC 페이지 라우팅
    │   └── merged_data.csv          # 분석용 데이터 파일

    ├── LHK/
    │   ├── LHK_routes.py            # LHK 담당 기능 라우팅
    │   └── test.ipynb               # 실험용 Jupyter 노트북

    ├── SHS/
    │   ├── SHS_routes.py            # SHS 기능 라우팅
    │   └── readme.txt               # SHS 전용 설명 파일

    ├── static/                      # main 전용 정적 자원 (이미지, css 등)

    └── templates/
        ├── common/
        │   ├── base.html            # 모든 템플릿의 기본 구조
        │   └── main.html            # 메인 대시보드 템플릿

        ├── DB_static/
        │   ├── DB_bus.html
        │   ├── DB_members.html
        │   ├── DB_population.html
        │   ├── DB_train.html
        │   └── DB_weather.html

        ├── JSC/
        │   ├── dashboard.html
        │   └── district.html

        ├── LHK/
        │   ├── auth_base.html
        │   ├── find_account.html
        │   ├── login.html
        │   ├── profile_edit.html
        │   ├── register.html
        │   └── weather.html

        ├── SHS/
        │   ├── chat.html
        │   ├── compare.html
        │   └── support.html
        ├── chart.html
    ├── chat.html
    ├── explorer.html
    ├── outlier.html        
    ├── profile_edit.html
    └── support.html        
│
├── config.py             # 앱 설정 파일
├── requirements.txt      # 프로젝트 종속성 목록
├── run.py                # 앱 실행 스크립트
└── README.md             # 프로젝트 설명서
######################################################

######################################################
