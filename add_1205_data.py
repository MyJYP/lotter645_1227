"""
1205회 데이터를 수동으로 추가하는 스크립트
"""
import sys
sys.path.append('src')

from data_updater import DataUpdater

# 1205회 데이터 (제공받은 정보)
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
    csv_path = "Data/645_251227.csv"
    updater = DataUpdater(csv_path)

    print("="*60)
    print("1205회 데이터 추가 스크립트")
    print("="*60)

    # 현재 최신 회차 확인
    current_latest = updater.get_current_latest_round()
    print(f"\n현재 최신 회차: {current_latest}회")

    # 데이터 검증
    print("\n데이터 검증 중...")
    is_valid, error_msg = updater.validate_draw_data(draw_data_1205)

    if not is_valid:
        print(f"❌ 검증 실패: {error_msg}")
        return

    print("✓ 데이터 검증 통과")

    # 사용자 확인
    print(f"\n추가할 데이터:")
    print(f"  회차: {draw_data_1205['회차']}")
    print(f"  일자: {draw_data_1205['일자']}")
    print(f"  당첨번호: {draw_data_1205['당첨번호']}")
    print(f"  보너스: {draw_data_1205['보너스번호']}")
    print(f"  1등: {draw_data_1205['1등 당첨자수']}명 / {draw_data_1205['1등 당첨액']:,}원")

    confirm = input("\n진행하시겠습니까? (y/n): ")

    if confirm.lower() != 'y':
        print("취소되었습니다.")
        return

    # CSV 업데이트
    print("\nCSV 파일 업데이트 중...")
    success, message = updater.update_csv_with_new_draw(draw_data_1205)

    if success:
        print(f"\n✅ {message}")
        print("\n완료! 웹 앱을 새로고침하여 확인하세요.")
    else:
        print(f"\n❌ {message}")


if __name__ == "__main__":
    main()
