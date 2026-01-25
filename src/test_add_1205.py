"""
1205회 데이터 자동 추가 테스트 스크립트
"""
import sys
sys.path.append('src')

from data_updater import DataUpdater

# 1205회 데이터 (사용자 제공)
draw_data_1205 = {
    '회차': 1205,
    '일자': '2026.01.03',
    '당첨번호': [1, 4, 16, 23, 31, 41],
    '보너스번호': 2,
    '1등 당첨자수': 10,
    '1등 당첨액': 32263862630,
    '2등 당첨자수': 97,
    '2등 당첨액': 5377310527,
    '3등 당첨자수': 3486,
    '3등 당첨액': 5377311870,
    '4등 당첨자수': 174740,
    '4등 당첨액': 8737000000,
    '5등 당첨자수': 2915978,
    '5등 당첨액': 14579890000
}

def main():
    csv_path = "./../Data/645_251227.csv"
    updater = DataUpdater(csv_path)

    print("="*60)
    print("🧪 1205회 데이터 추가 테스트")
    print("="*60)

    # 1. 현재 최신 회차 확인
    print("\n[1단계] 현재 상태 확인")
    current_latest = updater.get_current_latest_round()
    print(f"  ✓ 현재 최신 회차: {current_latest}회")

    # 2. 데이터 검증
    print("\n[2단계] 데이터 검증")
    is_valid, error_msg = updater.validate_draw_data(draw_data_1205)

    if not is_valid:
        print(f"  ❌ 검증 실패: {error_msg}")
        return False

    print("  ✓ 데이터 검증 통과")
    print(f"    - 회차: {draw_data_1205['회차']}")
    print(f"    - 일자: {draw_data_1205['일자']}")
    print(f"    - 당첨번호: {draw_data_1205['당첨번호']}")
    print(f"    - 보너스: {draw_data_1205['보너스번호']}")
    print(f"    - 1등: {draw_data_1205['1등 당첨자수']}명 / {draw_data_1205['1등 당첨액']:,}원")

    # 3. CSV 업데이트
    print("\n[3단계] CSV 파일 업데이트")
    success, message = updater.update_csv_with_new_draw(draw_data_1205)

    if success:
        print(f"  ✅ {message}")
        return True
    else:
        print(f"  ❌ {message}")
        return False


if __name__ == "__main__":
    result = main()

    print("\n" + "="*60)
    if result:
        print("✅ 테스트 성공!")
        print("\n다음 단계:")
        print("  1. 웹 앱 실행: ./run_web.sh")
        print("  2. 브라우저에서 http://localhost:8501 접속")
        print("  3. 홈 페이지에서 최신 회차 확인 (1205회)")
        print("  4. '데이터 탐색' 메뉴에서 새 데이터 반영 확인")
    else:
        print("❌ 테스트 실패")
    print("="*60)
