import sys
import os

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import LottoDataLoader
from prediction_model import LottoPredictionModel
from recommendation_system import LottoRecommendationSystem

def test_tuning_logic():
    print("🔧 튜닝(Semi-Auto) 기능 로직 테스트")
    print("=" * 60)

    # 1. 설정 및 모델 초기화
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_path = os.path.join(project_root, "Data", "645_251227.csv")

    print("1. 데이터 로딩 및 모델 학습 중...")
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()

    model = LottoPredictionModel(loader)
    model.train_all_patterns()

    recommender = LottoRecommendationSystem(model)

    # 2. 테스트용 조합 생성 (랜덤)
    print("\n2. 테스트용 조합 생성")
    test_combo = recommender.generate_random(1)[0]
    initial_score = recommender._calculate_combination_score(test_combo)
    
    print(f"   🎲 현재 조합: {test_combo}")
    print(f"   📊 현재 점수: {initial_score:.1f}")

    # 3. 교체 후보 추천 테스트
    remove_num = test_combo[0] # 첫 번째 번호를 교체 시도
    print(f"\n3. 교체 시뮬레이션: {remove_num}번 제거 후 대안 찾기")
    
    candidates = recommender.get_swap_candidates(test_combo, remove_num, top_n=3)
    
    if candidates:
        print(f"   ✅ {len(candidates)}개의 교체 후보 발견:")
        for i, cand in enumerate(candidates, 1):
            print(f"      [{i}] {cand['number']}번으로 교체")
            print(f"          → 예상 점수: {cand['new_score']:.1f} (변화: {cand['diff']:+.1f})")
            
            # 검증
            new_combo = sorted([n for n in test_combo if n != remove_num] + [cand['number']])
            
            # 유효성 및 제약조건 재확인
            is_valid = recommender._is_valid_combination(new_combo)
            is_safe = recommender._check_phase3_constraints(new_combo)
            
            if is_valid and is_safe:
                print(f"          ✅ 유효성 및 Phase 3 필터 통과")
            else:
                print(f"          ❌ 유효성 검사 실패 (Valid: {is_valid}, Safe: {is_safe})")
    else:
        print("   ⚠️ 적절한 교체 후보가 없습니다. (현재 조합이 이미 최적이거나 제약조건이 엄격함)")

if __name__ == "__main__":
    test_tuning_logic()