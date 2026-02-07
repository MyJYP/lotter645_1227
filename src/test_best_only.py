import sys
import os

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import LottoDataLoader
from prediction_model import LottoPredictionModel
from recommendation_system import LottoRecommendationSystem

def test_best_only():
    print("🚀 Best Only (결정론적 추천) 모드 테스트 시작")
    print("=" * 60)
    
    # 데이터 로드
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data", "645_251227.csv")
    
    print("1. 데이터 로딩 및 모델 학습 중...")
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()
    
    model = LottoPredictionModel(loader)
    model.train_all_patterns()
    
    recommender = LottoRecommendationSystem(model)
    
    strategies = [
        ('score', recommender.generate_by_score),
        ('probability', recommender.generate_by_probability),
        ('pattern', recommender.generate_by_pattern),
        ('grid', recommender.generate_grid_based),
        ('image', recommender.generate_image_based),
        ('consecutive', recommender.generate_with_consecutive),
        ('safe', recommender.generate_safe_strategy),
        ('hybrid', recommender.generate_hybrid)
    ]
    
    print("\n2. 전략별 비교 테스트 (Best Only vs Random Seed)")
    print("-" * 60)
    print(f"{'전략':<15} | {'모드':<10} | {'조합':<30} | {'점수':<5}")
    print("-" * 60)
    
    for name, func in strategies:
        # 1. Best Only 모드 (결정론적 최적해)
        try:
            results_best = func(n_combinations=1, best_only=True)
            combo_best = results_best[0]
            score_best = recommender._calculate_combination_score(combo_best)
            
            print(f"{name:<15} | {'Best':<10} | {str(combo_best):<30} | {score_best:.1f}")
        except Exception as e:
            print(f"{name:<15} | {'Best':<10} | ERROR: {str(e)}")

        # 2. Random Seed 모드 (기존 방식)
        try:
            seed = 42
            results_random = func(n_combinations=1, seed=seed, best_only=False)
            combo_random = results_random[0]
            score_random = recommender._calculate_combination_score(combo_random)
            
            print(f"{name:<15} | {'Random':<10} | {str(combo_random):<30} | {score_random:.1f}")
        except Exception as e:
            print(f"{name:<15} | {'Random':<10} | ERROR: {str(e)}")
            
        # 비교
        if score_best > score_random:
            print(f"   ✅ Best Only가 {score_best - score_random:.1f}점 더 높음")
        elif score_best == score_random:
            print(f"   ⚠️ 점수 동일 (최적해가 우연히 같거나 탐색 범위 제한)")
        else:
            print(f"   ❌ Random이 더 높음 (탐색 로직 점검 필요)")
        print("-" * 60)

if __name__ == "__main__":
    test_best_only()