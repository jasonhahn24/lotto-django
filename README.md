# 🎰 Lucky Lotto - Django + Docker 기반 6/45 로또 웹 서비스

Django 웹 프레임워크와 Docker 멀티 컨테이너 환경을 활용하여 구현한 6/45 온라인 로또 서비스이다.

---

## 🛠️ 기술 스택

| 구분 | 기술 |
|---|---|
| Backend | Django 5.0, Gunicorn |
| Database | PostgreSQL 16 |
| Cache | Redis 7 |
| Web Server | Nginx 1.25 |
| Container | Docker, Docker Compose |

---

## ⚙️ 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/jasonhahn24/lotto-django.git
cd lotto-django
```

### 2. 환경변수 설정
`.env` 파일 생성 후 아래 내용 입력:

  DJANGO_SECRET_KEY=your-secret-key
  DJANGO_DEBUG=True
  DATABASE_URL=postgres://lotto_user:lotto_pass@db:5432/lotto_db
  POSTGRES_DB=lotto_db
  POSTGRES_USER=lotto_user
  POSTGRES_PASSWORD=lotto_pass
  REDIS_URL=redis://redis:6379/0


### 3. 컨테이너 빌드 및 실행
```bash
docker-compose up --build -d
```

### 4. 관리자 계정 생성
```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. 브라우저 접속  
http://localhost


---

## 🎯 주요 기능

### 일반 사용자
- 회원가입 / 로그인
- 복권 구매 (수동 번호 선택 / 자동 번호 생성)
- 내 티켓 목록 조회
- 당첨 확인

### 관리자
- 판매 내역 확인
- 추첨 실행 (당첨 번호 자동 생성)
- 당첨 내역 확인
- 대시보드 (총 판매량, 수익 통계)

---

## 🐋 컨테이너 구성

| 서비스 | 이미지 | 포트 | 역할 |
|---|---|---|---|
| nginx | nginx:1.25-alpine | 80 | 리버스 프록시, 정적 파일 서빙 |
| web | python:3.12-slim | 8000 | Django 애플리케이션 |
| db | postgres:16-alpine | 5432 | 데이터베이스 |
| redis | redis:7-alpine | 6379 | 캐시, 세션 |

---

## 🧪 테스트 실행

```bash
docker-compose exec web python manage.py test apps.lotto --verbosity=2
```

---

## 📁 프로젝트 구조
```
lotto-django/
├── docker-compose.yml
├── .env
├── nginx/
│   ├── Dockerfile
│   └── nginx.conf
└── web/
    ├── Dockerfile
    ├── requirements.txt
    ├── manage.py
    ├── config/
    │   ├── settings/
    │   ├── urls.py
    │   └── wsgi.py
    ├── apps/
    │   ├── accounts/
    │   └── lotto/
    └── templates/
```



---

## 👤 개발 정보
- 학번: 32204818
- 이름: 한상윤
