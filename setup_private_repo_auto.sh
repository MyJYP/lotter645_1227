#!/bin/bash
# 프라이빗 레파지토리 자동 설정 스크립트 (URL을 인자로 받음)

# 색상 출력
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PUBLIC_DIR="/Users/joopark/Downloads/cursorai0514/MyVibecoding/lotter645_1227"
PRIVATE_DIR="/Users/joopark/Downloads/cursorai0514/MyVibecoding/lotter645_1227_private"

# 프라이빗 레파지토리 URL을 인자로 받음
PRIVATE_REPO_URL=$1

if [ -z "$PRIVATE_REPO_URL" ]; then
    echo -e "${RED}❌ 프라이빗 레파지토리 URL이 필요합니다.${NC}"
    echo ""
    echo "사용법:"
    echo "  ./setup_private_repo_auto.sh <프라이빗_레파지토리_URL>"
    echo ""
    echo "예시:"
    echo "  ./setup_private_repo_auto.sh git@github.com:MyJYP/lotter645_1227_private.git"
    echo ""
    echo "또는 인터랙티브 모드:"
    echo "  ./setup_private_repo.sh"
    exit 1
fi

echo -e "${BLUE}🔧 프라이빗 레파지토리 초기 설정${NC}"
echo -e "${YELLOW}프라이빗 레파지토리 URL: $PRIVATE_REPO_URL${NC}"
echo ""

# 0. 공개 레파지토리 확인
if [ ! -d "$PUBLIC_DIR" ]; then
    echo -e "${RED}❌ 공개 레파지토리 디렉토리가 없습니다: $PUBLIC_DIR${NC}"
    exit 1
fi

# 1. 프라이빗 디렉토리 생성
if [ -d "$PRIVATE_DIR" ]; then
    echo -e "${YELLOW}⚠️ 프라이빗 디렉토리가 이미 존재합니다: $PRIVATE_DIR${NC}"
    read -p "계속하시겠습니까? (기존 디렉토리의 .git이 초기화됩니다) [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
    # .git만 제거하고 파일은 유지
    if [ -d "$PRIVATE_DIR/.git" ]; then
        rm -rf "$PRIVATE_DIR/.git"
    fi
    echo -e "${GREEN}✓ 기존 .git 제거 완료${NC}"
else
    echo -e "${GREEN}📁 프라이빗 디렉토리 생성 중...${NC}"
    # rsync로 복사 (더 안전)
    mkdir -p "$PRIVATE_DIR"
    rsync -av --exclude='.git' \
              --exclude='venv' \
              --exclude='__pycache__' \
              --exclude='*.pyc' \
              "$PUBLIC_DIR/" "$PRIVATE_DIR/"
    echo -e "${GREEN}✓ 디렉토리 생성 완료${NC}"
fi

cd "$PRIVATE_DIR"

# 2. .gitignore 교체
echo -e "${GREEN}📝 .gitignore 교체 중...${NC}"
if [ -f ".gitignore.private" ]; then
    mv .gitignore .gitignore.public
    cp .gitignore.private .gitignore
    echo -e "${GREEN}✓ .gitignore 교체 완료${NC}"
else
    echo -e "${RED}❌ .gitignore.private 파일이 없습니다!${NC}"
    exit 1
fi

# 3. Git 초기화
echo -e "${GREEN}🔧 Git 초기화 중...${NC}"
git init
git branch -M main

# 4. Remote 설정
echo -e "${GREEN}🔗 Remote 설정 중...${NC}"
git remote add origin "$PRIVATE_REPO_URL"

# 5. 첫 커밋
echo -e "${GREEN}📦 첫 커밋 생성 중...${NC}"
echo -e "${YELLOW}추가할 파일 확인 중...${NC}"
git add .
echo ""
echo -e "${YELLOW}커밋할 파일 목록 (일부):${NC}"
git status --short | head -20
echo ""

git commit -m "Initial commit (private repository - all files included)"

# 6. 푸시
echo -e "${GREEN}📤 프라이빗 레파지토리로 푸시 중...${NC}"
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ 프라이빗 레파지토리 설정 완료!${NC}"
    echo ""
    echo -e "${BLUE}다음 단계:${NC}"
    echo "1. 공개 레파지토리에서 개발"
    echo "2. 주기적으로 './sync_to_private.sh' 실행하여 동기화"
    echo "3. 프라이빗 레파지토리는 백업 및 전체 파일 보관용"
    echo ""
    echo -e "${YELLOW}프라이빗 레파지토리 보안 검증:${NC}"
    echo "cd ../lotter645_1227_private"
    echo "../lotter645_1227/verify_repo_security.sh private"
else
    echo -e "${RED}❌ 푸시 실패. 레파지토리 URL과 권한을 확인하세요.${NC}"
    exit 1
fi

