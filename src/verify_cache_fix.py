"""
웹 앱 캐싱 수정 검증 스크립트
- 데이터 로더가 최신 회차를 읽는지 확인
- 예측 모델과 추천 시스템이 최신 데이터를 사용하는지 확인
"""
import sys
import os

sys.path.append('src')

from data_loader import LottoDataLoader
from prediction_model import LottoPredictionModel
from recommendation_system import LottoRecommendationSystem

def main():
    print("=" * 60)
    print("🧪 웹 앱 캐싱 수정 검증")
    print("=" * 60)

    # 현재 파일 위치 기준으로 Data 폴더 경로 계산 (웹 앱과 동일한 방식)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "Data", "645_251227.csv")

    print(f"\n[1단계] 데이터 로드 (경로: {data_path})")
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()

    # 최신 회차 확인
    latest_round = int(loader.df['회차'].max())
    latest_date = loader.df['일자'].iloc[0]
    total_rounds = len(loader.df)

    print(f"  ✓ 총 회차 수: {total_rounds}회")
    print(f"  ✓ 최신 회차: {latest_round}회 ({latest_date.strftime('%Y.%m.%d')})")

    if latest_round == 1205:
        print("  ✅ 최신 회차가 1205회로 정상 표시됩니다!")
    else:
        print(f"  ❌ 경고: 최신 회차가 {latest_round}회입니다. 1205회가 아닙니다.")
        return False

    # 최신 회차 데이터 확인
    latest_row = loader.numbers_df.iloc[0]
    print(f"\n  당첨번호: {latest_row['당첨번호']}")
    print(f"  보너스: {latest_row['보너스번호']}")

    print(f"\n[2단계] 예측 모델 검증")
    model = LottoPredictionModel(loader)
    model.train_all_patterns()

    # 모델이 사용하는 데이터 확인
    model_total_rounds = len(model.loader.df)
    model_latest_round = int(model.loader.df['회차'].max())

    print(f"  ✓ 모델이 사용하는 총 회차: {model_total_rounds}회")
    print(f"  ✓ 모델이 사용하는 최신 회차: {model_latest_round}회")

    if model_latest_round == 1205:
        print("  ✅ 예측 모델이 1205회 데이터를 사용합니다!")
    else:
        print(f"  ❌ 경고: 예측 모델이 {model_latest_round}회 데이터를 사용합니다.")
        return False

    # 상위 번호 확인
    top_numbers = model.get_top_numbers(10)
    print(f"\n  상위 10개 번호 (점수 기반):")
    print(f"  {top_numbers[:10]}")

    print(f"\n[3단계] 추천 시스템 검증")
    recommender = LottoRecommendationSystem(model)

    # 추천 시스템이 사용하는 데이터 확인
    rec_total_rounds = len(recommender.model.loader.df)
    rec_latest_round = int(recommender.model.loader.df['회차'].max())

    print(f"  ✓ 추천 시스템이 사용하는 총 회차: {rec_total_rounds}회")
    print(f"  ✓ 추천 시스템이 사용하는 최신 회차: {rec_latest_round}회")

    if rec_latest_round == 1205:
        print("  ✅ 추천 시스템이 1205회 데이터를 사용합니다!")
    else:
        print(f"  ❌ 경고: 추천 시스템이 {rec_latest_round}회 데이터를 사용합니다.")
        return False

    # 샘플 번호 생성 (1개) - 함수 내에서 이미 출력됨
    print(f"\n  샘플 추천 번호 생성 테스트:")
    recommender.generate_hybrid(1)

    print("\n" + "=" * 60)
    print("✅ 모든 검증 통과!")
    print("=" * 60)
    print("\n📝 검증 결과:")
    print("  1. 데이터 로더: 최신 회차 1205회 사용 ✓")
    print("  2. 예측 모델: 최신 회차 1205회 사용 ✓")
    print("  3. 추천 시스템: 최신 회차 1205회 사용 ✓")
    print("\n🌐 웹 앱 확인:")
    print("  - URL: http://localhost:8502")
    print("  - 홈 페이지에서 '최신 회차: 1205회' 표시 확인")
    print("  - 데이터 탐색 > 최근 10회 당첨번호에서 1205회 확인")
    print("  - 번호 추천 > 추천 번호 생성 시 최신 데이터 사용 확인")

    return True


if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ 검증 실패!")
        sys.exit(1)
