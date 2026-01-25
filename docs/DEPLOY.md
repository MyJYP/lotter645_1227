# 🚀 배포 가이드

## Streamlit Community Cloud에 배포하기

### 1단계: GitHub 리포지토리 생성

1. https://github.com 접속
2. "New repository" 클릭
3. 리포지토리 이름 입력 (예: `lotto645-analyzer`)
4. Public 선택 (무료 배포를 위해)
5. "Create repository" 클릭

### 2단계: 로컬 코드를 GitHub에 업로드

```bash
# 프로젝트 폴더로 이동
cd lotter645_1227

# Git 초기화 (아직 안했다면)
git init

# 모든 파일 추가 (.gitignore에 있는 파일은 제외됨)
git add .

# 커밋
git commit -m "Initial commit: Lotto 645 Analyzer with 8 features"

# GitHub 리포지토리 연결 (YOUR-USERNAME를 본인 GitHub 아이디로 변경)
git remote add origin https://github.com/MyJYP/lotter645_1227.git

# 업로드
git branch -M main
git push -u origin main
```

### 3단계: Streamlit Community Cloud에 배포

1. https://streamlit.io/cloud 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 다음 정보 입력:
   - **Repository**: MyJYP/lotter645_1227
   - **Branch**: main
   - **Main file path**: src/web_app.py
5. "Deploy!" 클릭

### 4단계: 배포 완료! 🎉

- 약 5-10분 후 배포 완료
- 공유 가능한 URL 제공 (예: `https://YOUR-APP-NAME.streamlit.app`)

---

## 📝 배포 시 주의사항

### ✅ 포함된 파일

- `src/` - 모든 Python 코드
- `Data/` - CSV 데이터 파일
- `requirements.txt` - 필수 패키지
- `.streamlit/config.toml` - Streamlit 설정

### ❌ 제외된 파일 (.gitignore)

- `venv/` - 가상환경 (필요없음)
- `images/` - PNG 이미지 (텍스트 그리드로 대체)
- `output/charts/` - 생성된 차트 (동적 생성)
- `__pycache__/` - Python 캐시

### 📊 데이터 업데이트

새로운 회차 데이터 추가 시:

```bash
# 1. Data/645_251227.csv 파일 업데이트
# 2. Git에 커밋 및 푸시
git add Data/645_251227.csv
git commit -m "Update to round XXXX"
git push

# 3. Streamlit Cloud가 자동으로 재배포
```

---

## 🔧 트러블슈팅

### 문제: 앱이 시작되지 않음

**해결**: `requirements.txt`의 패키지 버전 확인

```bash
# 로컬에서 테스트
pip install -r requirements.txt
streamlit run src/web_app.py
```

### 문제: 메모리 부족

**해결**:

- Streamlit Cloud 무료 플랜: 1GB RAM
- 캐싱 최적화 (이미 적용됨)
- 필요시 유료 플랜 업그레이드

### 문제: 느린 로딩

**해결**:

- `@st.cache_data`, `@st.cache_resource` 이미 적용됨
- 첫 로딩 후 빠름

---

## 🌟 배포 후 공유

배포 완료 후 URL을 공유하세요:

- 블로그, SNS
- GitHub README.md에 링크 추가
- QR 코드 생성 (https://www.qr-code-generator.com/)

---

## 📚 참고 자료

- Streamlit Cloud 공식 문서
- Streamlit 포럼
- GitHub 도움말
