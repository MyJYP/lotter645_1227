# 💝 후원 시스템 계정 생성 가이드

투네이션과 Buy Me a Coffee 계정을 생성하고 연동하는 방법입니다.

---

## 🎁 1. 투네이션 (Toonation) - 국내 사용자용

### 특징
- ✅ **100% 익명** - 실명/계좌번호 노출 없음
- ✅ **100원부터** 소액 후원 가능
- ✅ 카카오페이, 토스 등 국내 결제 수단
- ✅ 수수료 약 3-5%

### 계정 생성 방법 (5분)

#### 1단계: 회원가입
1. https://toon.at/ 접속
2. 우측 상단 "로그인" 클릭
3. "회원가입" 선택
4. 이메일 또는 소셜 계정으로 가입
   - 구글, 네이버, 카카오 계정 사용 가능

#### 2단계: 닉네임 설정
1. 가입 후 "프로필 설정" 이동
2. 닉네임 입력 (예: `로또645분석`)
3. 소개 작성 (선택):
   ```
   로또 645 데이터 분석 및 번호 추천 서비스를 운영하고 있습니다.
   통계, 머신러닝 기반 분석으로 더 나은 서비스를 제공합니다.
   ```
4. 프로필 이미지 업로드 (선택)

#### 3단계: 후원 링크 확인
1. 프로필 페이지에서 후원 링크 복사
2. 형식: `https://toon.at/donate/YOUR_NICKNAME`
3. 예시: `https://toon.at/donate/lotto645`

#### 4단계: 코드에 적용

**수정할 파일**: `src/web_app.py`

**위치 1: 사이드바 (157번째 라인)**
```python
# 현재 (임시)
<a href="https://toon.at/donate/lotto645" target="_blank"

# 변경 후 (실제 닉네임)
<a href="https://toon.at/donate/YOUR_NICKNAME" target="_blank"
```

**위치 2: 번호 추천 페이지 (657번째 라인)**
```python
# 현재 (임시)
<a href="https://toon.at/donate/lotto645" target="_blank"

# 변경 후 (실제 닉네임)
<a href="https://toon.at/donate/YOUR_NICKNAME" target="_blank"
```

#### 5단계: 정산 계좌 등록
1. 투네이션 대시보드 → "정산 설정"
2. 본인 명의 계좌번호 입력
3. 본인 인증 완료
4. 후원금은 매월 1일 자동 정산

---

## ☕ 2. Buy Me a Coffee - 해외 사용자용

### 특징
- ✅ 전 세계 사용자 지원
- ✅ 카드, PayPal 결제
- ✅ 수수료 5%
- ✅ 깔끔한 UI

### 계정 생성 방법 (5분)

#### 1단계: 회원가입
1. https://www.buymeacoffee.com/ 접속
2. 우측 상단 "Sign Up" 클릭
3. 이메일 또는 Google 계정으로 가입

#### 2단계: 프로필 설정
1. "Creator Dashboard" 이동
2. "Profile" 탭 선택
3. 프로필 정보 입력:
   - **Creator Name**: 로또 645 분석
   - **Username**: lotto645 (원하는 닉네임)
   - **Bio**:
     ```
     Lotto 645 Data Analysis & Number Recommendation Service
     로또 데이터 분석 및 번호 추천 서비스
     ```
   - **Profile Image**: 로고 또는 이미지 업로드 (선택)

#### 3단계: 후원 링크 확인
1. "Support Me" 페이지 URL 복사
2. 형식: `https://www.buymeacoffee.com/YOUR_USERNAME`
3. 예시: `https://www.buymeacoffee.com/lotto645`

#### 4단계: 코드에 적용

**수정할 파일**: `src/web_app.py`

**위치 1: 사이드바 (176번째 라인)**
```python
# 현재 (임시)
<a href="https://www.buymeacoffee.com/lotto645" target="_blank">

# 변경 후 (실제 사용자명)
<a href="https://www.buymeacoffee.com/YOUR_USERNAME" target="_blank">
```

**위치 2: 번호 추천 페이지 (675번째 라인)**
```python
# 현재 (임시)
<a href="https://www.buymeacoffee.com/lotto645" target="_blank">

# 변경 후 (실제 사용자명)
<a href="https://www.buymeacoffee.com/YOUR_USERNAME" target="_blank">
```

#### 5단계: 결제 정보 설정
1. "Payments" 탭 이동
2. Stripe 계정 연결 또는 생성
3. 은행 계좌 정보 입력 (정산용)
4. 본인 인증 완료

---

## 🚀 배포 및 테스트

### 1. 로컬 테스트
```bash
# Streamlit 실행 중이면 자동 새로고침됨
# 브라우저에서 http://localhost:8501 확인

# 확인할 사항:
# 1. 사이드바에 투네이션 + Buy Me a Coffee 버튼
# 2. 번호 추천 후 하단에 두 버튼 모두 표시
# 3. 각 버튼 클릭 시 올바른 페이지로 이동
```

### 2. Git 커밋 및 배포
```bash
git add src/web_app.py DONATION_GUIDE.md
git commit -m "feat: Add Toonation and Buy Me a Coffee donation system

- Replace Toss with Toonation for Korean users (anonymous)
- Keep Buy Me a Coffee for international users
- Add donation buttons in sidebar and recommendation page
- Update donation guide with setup instructions

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

git push
```

### 3. Streamlit Cloud 재배포
- Push 후 1-2분 내 자동 재배포
- https://lo645251227.streamlit.app/ 에서 확인

---

## 💰 예상 수익 (투네이션 + Buy Me a Coffee)

### 보수적 시나리오 (3개월 후)
| 플랫폼 | 일 방문자 | 전환율 | 평균 후원 | 월 수익 |
|--------|----------|--------|----------|---------|
| 투네이션 | 400명 | 0.5% | 3,000원 | 18만원 |
| Buy Me a Coffee | 100명 | 0.3% | $3 | 4만원 |
| **합계** | **500명** | - | - | **22만원** |

### 중립적 시나리오 (6개월 후)
| 플랫폼 | 일 방문자 | 전환율 | 평균 후원 | 월 수익 |
|--------|----------|--------|----------|---------|
| 투네이션 | 1,200명 | 0.7% | 4,000원 | 100만원 |
| Buy Me a Coffee | 300명 | 0.5% | $4 | 20만원 |
| **합계** | **1,500명** | - | - | **120만원** |

### 낙관적 시나리오 (1년 후)
| 플랫폼 | 일 방문자 | 전환율 | 평균 후원 | 월 수익 |
|--------|----------|--------|----------|---------|
| 투네이션 | 2,500명 | 1.0% | 5,000원 | 375만원 |
| Buy Me a Coffee | 500명 | 0.8% | $5 | 65만원 |
| **합계** | **3,000명** | - | - | **440만원** |

---

## 💡 후원 전환율을 높이는 팁

### 1. 타이밍 최적화
- ✅ **번호 추천 직후**: 만족도가 가장 높은 순간 (현재 적용됨)
- ✅ **사이드바 상단**: 항상 보이는 위치 (현재 적용됨)
- 추천: 당첨 후기 페이지 추가 (소셜 증거)

### 2. 메시지 개선
- ✅ 감성적 메시지 사용 (현재 적용됨)
- 추천: "23명이 이번 달 후원했습니다" 추가
- 추천: 후원자 명단 (익명) 표시

### 3. 보상 시스템
- 추천: 월 1만원 이상 후원자에게 프리미엄 기능 제공
- 추천: 후원자 전용 Discord/카톡방 운영
- 추천: 월 최고 후원자 특별 감사 메시지

### 4. 투명성
- 추천: "후원금 사용 내역" 페이지 추가
- 추천: 목표 설정 (예: "월 50만원 달성 시 API 기능 추가")

---

## ✅ 체크리스트

설정 완료 후 체크하세요:

### 투네이션
- [ ] 투네이션 계정 생성
- [ ] 닉네임 설정
- [ ] 정산 계좌 등록
- [ ] 코드에 링크 2곳 수정 (사이드바 + 추천 페이지)
- [ ] 실제 후원 테스트 (본인이 직접)

### Buy Me a Coffee
- [ ] Buy Me a Coffee 계정 생성
- [ ] 프로필 설정
- [ ] Stripe 연결 및 결제 정보 등록
- [ ] 코드에 링크 2곳 수정 (사이드바 + 추천 페이지)
- [ ] 실제 후원 테스트 (본인이 직접)

### 배포
- [ ] 로컬 테스트 완료
- [ ] Git 커밋 및 푸시
- [ ] Streamlit Cloud 재배포 확인
- [ ] 실제 사이트에서 버튼 작동 확인

---

## 🆘 문제 해결

### Q1: 투네이션 링크가 404 에러
A: 닉네임을 정확히 입력했는지 확인하세요. 대소문자 구분 없이 소문자로 통일됩니다.

### Q2: Buy Me a Coffee 결제가 안 돼요
A: Stripe 계정이 제대로 연결되지 않았을 수 있습니다. Dashboard → Payments에서 확인하세요.

### Q3: 후원금이 입금되지 않아요
A:
- **투네이션**: 매월 1일 자동 정산 (최소 정산 금액 확인)
- **Buy Me a Coffee**: 15일마다 자동 정산 (Stripe 설정 확인)

### Q4: 어느 플랫폼이 더 수익성이 좋나요?
A: 한국 사용자가 대부분이라면 **투네이션**이 압도적으로 유리합니다. 국내 결제 수단과 소액 후원이 편리하기 때문입니다.

---

## 📞 지원

- **투네이션 고객센터**: https://toon.at/support
- **Buy Me a Coffee 고객센터**: support@buymeacoffee.com

---

**다음 단계**: 계정 생성 후 링크를 코드에 적용하고 배포하세요!
