"""
여러 회차의 복권 용지 이미지 일괄 생성
"""
from data_loader import LottoDataLoader
from generate_lottery_ticket import create_lottery_ticket_enhanced
import os

def generate_recent_tickets(n_recent=10):
    """최근 N회차의 복권 용지 이미지 생성"""

    # 데이터 로드
    data_path = "../Data/645_251227.csv"
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()

    print(f"\n{'='*70}")
    print(f"🎰 최근 {n_recent}회차 복권 용지 이미지 생성")
    print('='*70)

    # 최근 N회차 데이터
    recent_data = loader.numbers_df.head(n_recent)

    generated_files = []

    for idx, row in recent_data.iterrows():
        round_num = int(row['회차'])
        # 날짜를 문자열로 변환 (YYYYMMDD 형식)
        date_obj = row['일자']
        date_str = date_obj.strftime('%Y%m%d')
        winning_numbers = row['당첨번호']
        bonus_number = row['보너스번호']

        # 파일명 생성
        output_path = f"../images/{round_num}_{date_str}.png"

        try:
            # 이미지 생성
            create_lottery_ticket_enhanced(
                round_num,
                date_str,
                winning_numbers,
                bonus_number,
                output_path
            )
            generated_files.append(output_path)

        except Exception as e:
            print(f"❌ {round_num}회차 생성 실패: {str(e)}")

    print(f"\n{'='*70}")
    print(f"✅ 총 {len(generated_files)}개 이미지 생성 완료!")
    print('='*70)

    return generated_files


def generate_specific_rounds(round_numbers):
    """특정 회차들의 복권 용지 이미지 생성"""

    # 데이터 로드
    data_path = "../Data/645_251227.csv"
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()

    print(f"\n{'='*70}")
    print(f"🎰 지정된 {len(round_numbers)}개 회차 복권 용지 이미지 생성")
    print('='*70)

    generated_files = []

    for round_num in round_numbers:
        # 해당 회차 데이터 찾기
        round_data = loader.numbers_df[loader.numbers_df['회차'] == round_num]

        if round_data.empty:
            print(f"⚠️  {round_num}회차 데이터 없음")
            continue

        row = round_data.iloc[0]
        # 날짜를 문자열로 변환 (YYYYMMDD 형식)
        date_obj = row['일자']
        date_str = date_obj.strftime('%Y%m%d')
        winning_numbers = row['당첨번호']
        bonus_number = row['보너스번호']

        # 파일명 생성
        output_path = f"../images/{round_num}_{date_str}.png"

        try:
            # 이미지 생성
            create_lottery_ticket_enhanced(
                round_num,
                date_str,
                winning_numbers,
                bonus_number,
                output_path
            )
            generated_files.append(output_path)

        except Exception as e:
            print(f"❌ {round_num}회차 생성 실패: {str(e)}")

    print(f"\n{'='*70}")
    print(f"✅ 총 {len(generated_files)}개 이미지 생성 완료!")
    print('='*70)

    return generated_files


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "recent":
            # 최근 N회차 생성
            n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
            generate_recent_tickets(n)
        elif sys.argv[1] == "rounds":
            # 특정 회차들 생성
            rounds = [int(r) for r in sys.argv[2:]]
            generate_specific_rounds(rounds)
    else:
        # 기본: 최근 5회차 생성
        print("\n사용법:")
        print("  python batch_generate_tickets.py recent [개수]")
        print("  python batch_generate_tickets.py rounds [회차1] [회차2] ...")
        print("\n기본 실행: 최근 5회차 생성")

        generate_recent_tickets(5)
