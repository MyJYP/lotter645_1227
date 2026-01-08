#!/usr/bin/env python3
"""
프리미엄 인증 시스템 테스트 스크립트
"""
import socket
import os

def is_local_environment():
    """로컬 환경 여부 감지 (웹앱 로직 복사)"""
    # 1. 호스트명 체크
    hostname = socket.gethostname().lower()
    if 'local' in hostname or hostname in ['localhost', '127.0.0.1']:
        return True

    # 2. Streamlit Cloud 환경 변수 체크
    if os.getenv('HOSTNAME', '').startswith('streamlit-'):
        return False

    # 3. 환경 변수 체크
    if os.getenv('STREAMLIT_RUNTIME_ENV') == 'cloud':
        return False

    # 5. 기본값 (안전하게 로컬로 간주)
    return True

def test_environment_detection():
    """환경 감지 테스트"""
    print("🔍 환경 감지 테스트")
    print("=" * 50)

    # 현재 환경 정보
    hostname = socket.gethostname()
    print(f"호스트명: {hostname}")
    print(f"HOSTNAME 환경변수: {os.getenv('HOSTNAME', '(없음)')}")
    print(f"STREAMLIT_RUNTIME_ENV: {os.getenv('STREAMLIT_RUNTIME_ENV', '(없음)')}")

    # 환경 판단
    is_local = is_local_environment()
    print(f"\n판단 결과: {'🏠 로컬 환경' if is_local else '☁️ 서버 환경'}")

    if is_local:
        print("✅ 프리미엄 기능이 자동으로 활성화됩니다.")
    else:
        print("🔒 프리미엄 기능에 액세스 코드가 필요합니다.")

    print("=" * 50)
    return is_local

def test_secrets_file():
    """Secrets 파일 존재 여부 테스트"""
    print("\n📁 Secrets 파일 테스트")
    print("=" * 50)

    secrets_path = "../.streamlit/secrets.toml"

    if os.path.exists(secrets_path):
        print(f"✅ Secrets 파일 존재: {secrets_path}")

        # 파일 크기 확인
        file_size = os.path.getsize(secrets_path)
        print(f"   파일 크기: {file_size} bytes")

        # 첫 몇 줄 읽기 (실제 코드는 표시하지 않음)
        with open(secrets_path, 'r') as f:
            lines = f.readlines()
            print(f"   총 줄 수: {len(lines)}")
            print(f"   첫 줄: {lines[0].strip() if lines else '(비어있음)'}")
    else:
        print(f"❌ Secrets 파일 없음: {secrets_path}")
        print("   로컬 테스트는 가능하지만, 서버 배포 시 필요합니다.")

    print("=" * 50)

def test_gitignore():
    """Gitignore 설정 테스트"""
    print("\n🔒 Gitignore 보안 테스트")
    print("=" * 50)

    security_files = [
        "PREMIUM_SETUP.md",
        "premium_codes.txt",
        ".streamlit/secrets.toml"
    ]

    for file in security_files:
        result = os.system(f"cd .. && git check-ignore -q '{file}' 2>/dev/null")
        status = "✅ Git에서 제외됨" if result == 0 else "❌ Git에서 추적됨 (위험!)"
        print(f"{status} - {file}")

    print("=" * 50)

if __name__ == "__main__":
    print("\n🔐 프리미엄 인증 시스템 테스트")
    print("=" * 60)

    # 테스트 1: 환경 감지
    is_local = test_environment_detection()

    # 테스트 2: Secrets 파일
    test_secrets_file()

    # 테스트 3: Gitignore 보안
    test_gitignore()

    print("\n" + "=" * 60)
    print("✅ 테스트 완료!")
    print("\n💡 다음 단계:")
    print("1. 웹 앱을 실행하여 '🔬 백테스팅 결과' 페이지 확인")
    print("2. '⚙️ 가중치 최적화' 탭에 접근 가능한지 확인")
    print("3. '🚀 실시간 재학습' 탭에 접근 가능한지 확인")

    if is_local:
        print("4. ✅ 로컬 환경이므로 코드 입력 없이 바로 사용 가능해야 함")
    else:
        print("4. 🔒 서버 환경이므로 액세스 코드 입력창이 표시되어야 함")

    print("=" * 60 + "\n")
