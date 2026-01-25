"""
그리드 패턴 기반 추천 시스템 테스트
"""
from data_loader import LottoDataLoader
from prediction_model import LottoPredictionModel
from recommendation_system import LottoRecommendationSystem

print("="*70)
print("🎨 그리드 패턴 기반 추천 시스템 테스트")
print("="*70)

# 데이터 로드
print("\n📊 데이터 로드 중...")
data_path = "../Data/645_251227.csv"
loader = LottoDataLoader(data_path)
loader.load_data()
loader.preprocess()
loader.extract_numbers()

# 예측 모델 학습
print("\n🤖 예측 모델 학습 중...")
model = LottoPredictionModel(loader)
model.train_all_patterns()

# 추천 시스템 초기화
print("\n🎯 추천 시스템 초기화...")
recommender = LottoRecommendationSystem(model)

# 그리드 패턴 기반 추천 테스트
print("\n" + "="*70)
print("🧪 TEST 1: 그리드 패턴 기반 추천")
print("="*70)

results = recommender.generate_grid_based(n_combinations=5, seed=None)

print("\n✅ 생성된 번호 조합:")
for i, combo in enumerate(results, 1):
    print(f"\n🎰 조합 {i}: {combo}")

    # 상세 분석
    middle_count = sum(1 for n in combo if n in recommender.grid_zones['middle'])
    anti_diag_count = sum(1 for n in combo if n in recommender.grid_zones['anti_diagonal'])
    corner_count = sum(1 for n in combo if n in recommender.grid_zones['corner'])
    avg_distance = recommender._calculate_spatial_distance(combo)
    grid_score = recommender._calculate_grid_score(combo)

    print(f"   - 중간 영역: {middle_count}개")
    print(f"   - 반대 대각선: {anti_diag_count}개")
    print(f"   - 모서리: {corner_count}개")
    print(f"   - 평균 거리: {avg_distance:.2f}")
    print(f"   - 그리드 점수: {grid_score:.1f}")

# 하이브리드 전략 테스트 (그리드 포함)
print("\n" + "="*70)
print("🧪 TEST 2: 하이브리드 전략 (그리드 패턴 포함)")
print("="*70)

results_hybrid = recommender.generate_hybrid(n_combinations=5, seed=None)

print("\n" + "="*70)
print("✅ 모든 테스트 완료!")
print("="*70)
