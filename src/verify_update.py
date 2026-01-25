"""
업데이트된 데이터 검증 스크립트
"""
import sys
sys.path.append('src')

from data_loader import LottoDataLoader

def main():
    print("="*60)
    print("📊 업데이트된 데이터 검증")
    print("="*60)

    # 데이터 로드
    loader = LottoDataLoader("./../Data/645_251227.csv")
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()

    # 요약 정보
    loader.get_summary()

    # 최신 5개 회차 확인
    print("\n최신 5개 회차:")
    print("-" * 60)
    for idx, row in loader.numbers_df.head(5).iterrows():
        print(f"{int(row['회차'])}회 ({row['일자'].strftime('%Y.%m.%d')})")
        print(f"  당첨번호: {row['당첨번호']}")
        print(f"  보너스: {row['보너스번호']}")
        print()

    # 1205회 상세 확인
    print("\n" + "="*60)
    print("🎯 1205회 데이터 상세 확인")
    print("="*60)

    round_1205 = loader.numbers_df[loader.numbers_df['회차'] == 1205].iloc[0]

    print(f"\n회차: {int(round_1205['회차'])}")
    print(f"일자: {round_1205['일자'].strftime('%Y.%m.%d')}")
    print(f"당첨번호: {round_1205['당첨번호']}")
    print(f"보너스번호: {round_1205['보너스번호']}")

    # 원본 DataFrame에서 당첨금 정보 확인
    round_1205_full = loader.df[loader.df['회차'] == 1205].iloc[0]

    print(f"\n💰 당첨금 정보:")
    print(f"  1등: {int(round_1205_full['1등 당첨자수'])}명 / {int(round_1205_full['1등 당첨액']):,}원")
    print(f"  2등: {int(round_1205_full['2등 당첨자수'])}명 / {int(round_1205_full['2등 당첨액']):,}원")
    print(f"  3등: {int(round_1205_full['3등 당첨자수'])}명 / {int(round_1205_full['3등 당첨액']):,}원")
    print(f"  4등: {int(round_1205_full['4등 당첨자수'])}명 / {int(round_1205_full['4등 당첨액']):,}원")
    print(f"  5등: {int(round_1205_full['5등 당첨자수'])}명 / {int(round_1205_full['5등 당첨액']):,}원")

    # 기본 통계
    print(f"\n📈 기본 통계:")
    print(f"  합계: {sum(round_1205['당첨번호'])}")
    print(f"  홀수: {sum(1 for n in round_1205['당첨번호'] if n % 2 == 1)}개")
    print(f"  짝수: {sum(1 for n in round_1205['당첨번호'] if n % 2 == 0)}개")

    print("\n" + "="*60)
    print("✅ 데이터 검증 완료!")
    print("="*60)


if __name__ == "__main__":
    main()
