# 💝 후원 시스템 설정 가이드

후원 시스템이 추가되었습니다! 아래 단계를 따라 실제 계정 정보를 연동하세요.

---

## 📋 설정해야 할 항목

### 1. Buy Me a Coffee 계정 생성 (5분 소요)

#### 단계 1: 계정 생성
1. https://www.buymeacoffee.com/ 접속
2. 우측 상단 "Sign Up" 클릭
3. 이메일 또는 Google 계정으로 가입
4. 사용자명 설정 (예: `lotto645`)

#### 단계 2: 프로필 설정
1. "Creator Dashboard" 이동
2. "Profile" 탭에서 프로필 정보 입력
   - 이름: 로또 645 분석
   - 설명: 로또 데이터 분석 및 번호 추천 서비스
   - 프로필 이미지 업로드 (선택)

#### 단계 3: 링크 가져오기
1. "Support Me" 페이지 URL 복사
2. 예시: `https://www.buymeacoffee.com/yourusername`

#### 단계 4: 코드에 적용
`src/web_app.py` 파일에서 아래 부분을 찾아 수정:

**위치 1: 사이드바 (154-165번째 라인)**
```python
# 현재 (임시)
<a href="https://www.buymeacoffee.com/lotto645" target="_blank">

# 변경 후 (실제 링크)
<a href="https://www.buymeacoffee.com/YOUR_USERNAME" target="_blank">
```

**위치 2: 추천 결과 페이지 (653-664번째 라인)**
```python
# 현재 (임시)
<a href="https://www.buymeacoffee.com/lotto645" target="_blank">

# 변경 후 (실제 링크)
<a href="https://www.buymeacoffee.com/YOUR_USERNAME" target="_blank">
```

---

### 2. Toss 계좌번호 설정 (1분 소요)

#### 단계 1: Toss 계좌 확인
1. Toss 앱 실행
2. "전체" 탭 → 계좌 선택
3. 계좌번호 복사

#### 단계 2: 코드에 적용
`src/web_app.py` 파일에서 아래 부분을 찾아 수정:

**위치 1: 사이드바 (168-185번째 라인)**
```python
# 현재 (임시)
계좌번호: <code>토스뱅크 1000-0000-0000</code><br>
예금주: 박주영

# 변경 후 (실제 정보)
계좌번호: <code>토스뱅크 YOUR_ACCOUNT_NUMBER</code><br>
예금주: YOUR_NAME
```

**위치 2: 추천 결과 페이지 (666-681번째 라인)**
```python
# 현재 (임시)
계좌번호: <code>토스뱅크 1000-0000-0000</code><br>
예금주: 박주영

# 변경 후 (실제 정보)
계좌번호: <code>토스뱅크 YOUR_ACCOUNT_NUMBER</code><br>
예금주: YOUR_NAME
```

#### 단계 3: Toss QR 코드 추가 (선택)
1. Toss 앱에서 "받기" → "QR 코드" 생성
2. QR 코드 이미지 저장 (`toss_qr.png`)
3. 프로젝트 루트에 `images/` 폴더 생성
4. `toss_qr.png` 업로드

코드 수정:
```python
# 현재 (주석 처리됨)
# st.image("toss_qr.png", use_column_width=True)

# 변경 후 (활성화)
st.image("../images/toss_qr.png", use_column_width=True)
```

---

## 🚀 배포 방법

### 방법 1: 로컬 테스트
```bash
cd src
streamlit run web_app.py
```

브라우저에서 확인:
- 사이드바에 후원 섹션이 보이는지
- 번호 추천 후 후원 안내가 나오는지
- 버튼 클릭 시 올바른 페이지로 이동하는지

### 방법 2: Streamlit Cloud 배포
```bash
git add src/web_app.py DONATION_SETUP.md
git commit -m "feat: Add donation system (Buy Me a Coffee + Toss)"
git push
```

Streamlit Cloud에서 자동으로 재배포됩니다 (1-2분 소요).

---

## 📊 예상 수익

### 보수적 시나리오
- 일 방문자 500명
- 후원 전환율 0.3% (500명 중 1-2명)
- 평균 후원 금액: 3,000원
- **월 수익**: 4.5만원 - 9만원

### 중립적 시나리오
- 일 방문자 1,500명
- 후원 전환율 0.5% (1,500명 중 7-8명)
- 평균 후원 금액: 4,000원
- **월 수익**: 8.4만원 - 9.6만원

### 낙관적 시나리오
- 일 방문자 3,000명
- 후원 전환율 1.0% (3,000명 중 30명)
- 평균 후원 금액: 5,000원
- **월 수익**: 45만원

---

## 💡 후원 전환율을 높이는 팁

### 1. 타이밍
- ✅ **번호 추천 직후**: 가장 만족도가 높은 시점 (현재 적용됨)
- ✅ **사이드바**: 항상 보이도록 (현재 적용됨)
- 추천: 홈 페이지 하단에도 추가 고려

### 2. 메시지
- ✅ 감성적 메시지 ("응원해주세요")
- ✅ 구체적 금액 표시 ("커피 한 잔")
- 추천: 후원자 명단 또는 감사 메시지 추가

### 3. 사회적 증거
- 추천: "지난달 23명이 후원했습니다" (실제 데이터)
- 추천: 후원자 감사 페이지 추가

### 4. 간편성
- ✅ Buy Me a Coffee: 원클릭 후원
- ✅ Toss: QR 코드로 간편 송금
- 추천: 카카오페이 추가 고려

---

## ✅ 체크리스트

후원 시스템 설정을 완료했다면 체크하세요:

- [ ] Buy Me a Coffee 계정 생성
- [ ] Buy Me a Coffee 링크 2곳 수정 (사이드바 + 추천 페이지)
- [ ] Toss 계좌번호 2곳 수정 (사이드바 + 추천 페이지)
- [ ] Toss QR 코드 생성 및 업로드 (선택)
- [ ] 로컬 테스트 완료
- [ ] Git 커밋 및 푸시
- [ ] Streamlit Cloud 재배포 확인
- [ ] 실제 후원 테스트 (본인이 직접)

---

## 🆘 문제 해결

### Q1: Buy Me a Coffee 버튼이 안 보여요
A: 브라우저 광고 차단기가 활성화되어 있을 수 있습니다. 다른 브라우저로 테스트해보세요.

### Q2: Toss 계좌번호를 공개해도 안전한가요?
A: 네, 계좌번호는 받는 용도로만 사용되므로 안전합니다. 단, 보안을 위해 출금 알림을 켜두세요.

### Q3: 수익이 안 나오면 어떻게 하나요?
A: 트래픽이 적으면 후원도 적습니다. 먼저 SEO 최적화와 커뮤니티 홍보로 방문자를 늘리세요.

### Q4: 다른 후원 플랫폼도 추가할 수 있나요?
A: 네! 카카오페이, 네이버페이, Patreon 등 추가 가능합니다. 필요하면 요청하세요.

---

**다음 단계**: [사업화 전략 문서](BUSINESS_STRATEGY.md) 참조
