#!/bin/bash
# 로컬 프리미엄 인증 테스트 스크립트

echo "🧪 로컬 프리미엄 인증 테스트"
echo "========================================"
echo ""

# 1. 환경변수 확인
echo "1️⃣  환경변수 확인:"
if [ -z "$LOTTO_DEV_MODE" ]; then
    echo "   ✅ LOTTO_DEV_MODE: 설정 안 됨 (정상)"
    echo "   📋 예상 동작: 액세스 코드 입력 필요"
else
    echo "   ⚠️  LOTTO_DEV_MODE=$LOTTO_DEV_MODE"
    echo "   📋 예상 동작: 자동 활성화 (개발자 모드)"
fi
echo ""

# 2. Secrets 파일 확인
echo "2️⃣  Secrets 파일 확인:"
SECRETS_FILE="src/.streamlit/secrets.toml"
if [ -f "$SECRETS_FILE" ]; then
    echo "   ✅ $SECRETS_FILE 존재"
    # 첫 3줄만 표시
    echo "   📄 내용 (처음 3줄):"
    head -3 "$SECRETS_FILE" | sed 's/^/      /'
else
    echo "   ❌ $SECRETS_FILE 없음"
    echo "   ⚠️  액세스 코드 인증 실패할 수 있음"
fi
echo ""

# 3. 테스트 시나리오
echo "3️⃣  테스트 시나리오:"
echo "   a) 웹 앱 실행: ./run_web.sh"
echo "   b) '🔬 백테스팅 결과' 메뉴 클릭"
echo "   c) '⚙️ 가중치 최적화' 탭 클릭"
echo "   d) 예상 결과:"
echo "      - ⚠️ '이 기능은 프리미엄 전용입니다' 메시지"
echo "      - 🔑 액세스 코드 입력창 표시"
echo "      - 💡 로컬 개발자 모드 안내 표시"
echo ""

# 4. 테스트 코드
echo "4️⃣  테스트용 액세스 코드 (첫 3개):"
if [ -f "$SECRETS_FILE" ]; then
    grep "PREM-" "$SECRETS_FILE" | head -3 | sed 's/^/      /'
else
    echo "      (Secrets 파일 없음)"
fi
echo ""

echo "========================================"
echo "💡 개발자 모드 활성화 방법:"
echo "   export LOTTO_DEV_MODE=true"
echo "   ./run_web.sh"
echo "========================================"
