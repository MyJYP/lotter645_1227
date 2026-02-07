# ✅ 배포 준비 체크리스트 (v6.2.1)

## 📦 배포 전 확인 사항

### 1. 파일 준비 상태

- [x] `.gitignore` 생성 완료
- [x] `requirements.txt` 확인 완료
- [x] `.streamlit/config.toml` 생성 완료
- [x] `VERSION` 파일 업데이트 (v6.2.1)
- [x] `DEPLOY.md` 가이드 작성 완료
- [x] 이미지 파일을 텍스트 그리드로 변경 완료 (용량 절감)

### 2. 코드 최적화 & 보안

- [x] 이미지 604개 → 텍스트 그리드 변환 (15MB 절감)
- [x] Streamlit 캐싱 적용 (`@st.cache_data`, `@st.cache_resource`)
- [x] 모든 경로를 상대 경로로 변경
- [x] 모든 페이지 정상 작동 확인
- [x] **프리미엄 인증 시스템** 작동 확인 (로컬/서버 감지)
- [x] Secrets 파일 분리 확인 (`.streamlit/secrets.toml` Git 제외)

### 3. 데이터 파일

- [x] `Data/645_251227.csv` 포함 (필수)
- [x] 인코딩 UTF-8 확인
- [ ] 최신 데이터로 업데이트 (필요시)

### 4. 신규 기능 테스트 (v6.2.1)

- [x] **고정 모드 고도화**: 결정론적 추천, 앙상블, 제외수 필터링
- [x] **사용자 튜닝**: 추천 번호 교체 기능 (Semi-Auto)
- [x] **나의 번호**: 당첨 연대기 및 알고리즘 진단
- [x] **모바일 반응형**: CSS Flexbox 적용 확인

### 4. 의존성 패키지

현재 `requirements.txt`:

```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scikit-learn>=1.3.0
streamlit>=1.28.0
plotly>=5.17.0
openpyxl>=3.1.0
```

모두 PyPI에서 설치 가능 ✅

---

## 🚀 배포 단계별 가이드

### Step 1: 버전 정보 업데이트

```bash
# VERSION 파일 확인
cat VERSION
# v6.2.1 출력 확인
```

### Step 2: Git 커밋 및 푸시

```bash
# 프로젝트 폴더로 이동
cd lotter645_1227

# 변경사항 추가
git add .

# 커밋
git commit -m "release: v6.2.1 - Fixed Mode Advanced & User Tuning"

# 푸시
git push origin main
```

### Step 4: Streamlit Community Cloud 배포

1. https://streamlit.io/cloud 접속
2. **GitHub로 로그인**
3. "New app" 클릭
4. 설정:
   ```
   Repository: MyJYP/lotter645_1227
   Branch: main
   Main file path: src/web_app.py
   ```
5. "Deploy!" 클릭

### Step 5: 배포 완료 🎉

- 약 5-10분 소요
- URL: `https://YOUR-APP-NAME.streamlit.app`
- 공유 및 사용 가능!

---

## 📊 리소스 사용량

### Streamlit Community Cloud 무료 플랜

- **RAM**: 1GB (충분함 ✅)
- **CPU**: 1 vCPU (충분함 ✅)
- **스토리지**: 제한 없음
- **대역폭**: 제한 없음

### 예상 용량

- **코드**: ~500KB
- **데이터 (CSV)**: ~200KB
- **총 용량**: ~700KB (매우 가벼움 ✅)

---

## 🔧 배포 후 확인사항

### 1. 모든 페이지 동작 확인

- [ ] 🏠 홈
- [ ] 📊 데이터 탐색
- [ ] 🎯 번호 추천
- [ ] 🔍 번호 분석
- [ ] 🤖 예측 모델
- [ ] 🎨 그리드 패턴
- [ ] 🖼️ 이미지 패턴
- [ ] 🎲 번호 테마

### 2. 기능 테스트

- [ ] 하이브리드 추천 생성
- [ ] 코어 번호 추출
- [ ] 고정 번호 조합 생성
- [ ] 신뢰도 점수 확인
- [ ] 복권 용지 그리드 표시
- [ ] 차트 렌더링

### 3. 성능 확인

- [ ] 첫 로딩 시간 (30초 이내)
- [ ] 캐싱 동작 (두 번째 로딩은 빠름)
- [ ] 차트 인터랙티브 동작

---

## 🎯 다음 단계

### 배포 완료 후

1. **README 업데이트**
   - 실제 Streamlit URL 추가
   - 배지 업데이트

2. **공유**
   - SNS, 블로그 등에 공유
   - QR 코드 생성

3. **유지보수**
   - 새 회차 데이터 추가 시:
     ```bash
     git add Data/645_251227.csv
     git commit -m "Update to round XXXX"
     git push
     # Streamlit이 자동으로 재배포
     ```

---

## ⚠️ 문제 해결

### 배포가 실패하면?

1. **requirements.txt 확인**

   ```bash
   # 로컬에서 테스트
   pip install -r requirements.txt
   streamlit run src/web_app.py
   ```

2. **로그 확인**
   - Streamlit Cloud 대시보드에서 로그 확인
   - 에러 메시지 확인

3. **경로 문제**
   - 모든 경로가 상대 경로인지 확인
   - `../Data/` 형식 사용

---

## 📞 도움말

- Streamlit Community Cloud 문서
- Streamlit 포럼
- GitHub 도움말

---

**준비 완료! 🚀 이제 배포하세요!**
