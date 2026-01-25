#!/bin/bash

# 로또 645 분석 프로젝트 가상환경 설정 스크립트

echo "=================================="
echo "로또 645 분석 프로젝트 설정"
echo "=================================="
echo ""

# 가상환경이 이미 존재하는지 확인
if [ -d "venv" ]; then
    echo "⚠️  가상환경이 이미 존재합니다."
    read -p "기존 가상환경을 삭제하고 새로 만드시겠습니까? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  기존 가상환경 삭제 중..."
        rm -rf venv
    else
        echo "✅ 기존 가상환경을 사용합니다."
        source venv/bin/activate
        echo "📦 패키지를 업데이트합니다..."
        pip install --upgrade pip
        pip install -r requirements.txt
        echo ""
        echo "✅ 설정 완료!"
        echo ""
        echo "가상환경이 활성화되었습니다."
        echo "프로그램을 실행하려면: cd src && python main.py"
        exit 0
    fi
fi

# Python 버전 확인
echo "🔍 Python 버전 확인 중..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
    PYTHON_VERSION=$(python3 --version)
    echo "✅ $PYTHON_VERSION 발견"
else
    echo "❌ Python3이 설치되어 있지 않습니다."
    echo "Python 3.7 이상을 설치해주세요."
    exit 1
fi

# 가상환경 생성
echo ""
echo "📦 가상환경 생성 중..."
$PYTHON_CMD -m venv venv

# 가상환경 활성화
echo "🔧 가상환경 활성화 중..."
source venv/bin/activate

# pip 업그레이드
echo "📦 pip 업그레이드 중..."
pip install --upgrade pip

# 필수 패키지 설치
echo "📦 필수 패키지 설치 중..."
pip install -r requirements.txt

echo ""
echo "=================================="
echo "✅ 설정 완료!"
echo "=================================="
echo ""
echo "가상환경이 활성화되었습니다."
echo ""
echo "프로그램 실행 방법:"
echo "  cd src && python main.py"
echo ""
echo "가상환경 종료: deactivate"
echo ""
