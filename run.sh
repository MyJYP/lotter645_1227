#!/bin/bash

# 로또 645 분석 프로그램 실행 스크립트

# 가상환경이 존재하는지 확인
if [ ! -d "venv" ]; then
    echo "❌ 가상환경이 존재하지 않습니다."
    echo "먼저 setup.sh를 실행해주세요:"
    echo "  chmod +x setup.sh"
    echo "  ./setup.sh"
    exit 1
fi

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# 프로그램 실행
echo "🎰 로또 645 분석 프로그램 실행"
echo ""
cd src && python main.py

# 가상환경 비활성화
deactivate
