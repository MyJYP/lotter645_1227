import sys
import os
import pandas as pd
from itertools import combinations

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import LottoDataLoader
from prediction_model import LottoPredictionModel
from recommendation_system import LottoRecommendationSystem

def test_phase3_logic():
    print("🧪 Phase 3 필터링(제외수/상극수) 로직 테스트")
    print("=" * 60)

    # 1. 설정 및 모델 초기화
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_path = os.path.join(project_root, "Data", "645_251227.csv")

    print("1. 데이터 로딩 및 모델 초기화 중...")
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()

    model = LottoPredictionModel(loader)
    model.train_all_patterns()

    recommender = LottoRecommendationSystem(model)

    # 2. 필터 데이터 확인
    print("\n2. 필터링 기준 데이터 확인")
    print(f"   🔥 과열 번호 (최근 10회 4회 이상 출현): {sorted(list(recommender.overheated_numbers))}")
    print(f"   ❄️ 상극수 조합 (역대 동반 출현 0회) 개수: {len(recommender.never_appeared_set):,}개")
    
    # 3. 제약 조건 단위 테스트 (강제 위반 시도)
    print("\n3. 제약 조건 단위 테스트 (강제 위반 시도)")
    
    # Case A: 과열 번호 포함 테스트
    if recommender.overheated_numbers:
        bad_num = list(recommender.overheated_numbers)[0]
        # 과열 번호 1개 + 나머지 정상 번호 5개
        candidates = [n for n in range(1, 46) if n != bad_num]
        bad_combo = [bad_num] + candidates[:5]
        
        print(f"   [Test 1] 과열 번호({bad_num}) 포함 조합: {bad_combo}")
        is_valid = recommender._check_phase3_constraints(bad_combo)
        if not is_valid:
            print("   👉 결과: ✅ 필터링 성공 (제외됨)")
        else:
            print("   👉 결과: ❌ 필터링 실패 (통과됨)")
    else:
        print("   ⚠️ 과열 번호가 없어서 Test 1 건너뜀")

    # Case B: 4연속 번호 테스트
    consecutive_combo = [1, 2, 3, 4, 10, 20]
    print(f"   [Test 2] 4연속 번호(1-2-3-4) 포함 조합: {consecutive_combo}")
    is_valid = recommender._check_phase3_constraints(consecutive_combo)
    if not is_valid:
        print("   👉 결과: ✅ 필터링 성공 (제외됨)")
    else:
        print("   👉 결과: ❌ 필터링 실패 (통과됨)")

    # 4. 통합 추천 테스트
    print("\n4. 통합 추천 테스트 (Best Only 모드)")
    print("   generate_by_score(best_only=True) 실행 중...")
    
    # 점수 기반 최적 추천 실행 (Phase 3 적용됨)
    results = recommender.generate_by_score(n_combinations=1, best_only=True)
    best_combo = results[0]
    
    print(f"   🏆 추천된 최적 조합: {best_combo}")
    
    # 결과 검증
    # 1. 과열 번호 포함 여부
    has_overheated = any(n in recommender.overheated_numbers for n in best_combo)
    
    # 2. 4연속 번호 여부
    sorted_c = sorted(best_combo)
    cons_cnt = 0
    max_cons = 0
    for i in range(len(sorted_c)-1):
        if sorted_c[i+1] == sorted_c[i] + 1:
            cons_cnt += 1
            if cons_cnt >= 3: max_cons = 3 # 차이가 1인 횟수가 3번이면 4개 연속
        else:
            cons_cnt = 0
            
    if not has_overheated and max_cons < 3:
        print(f"   ✅ 최종 검증 통과: 과열번호 없음, 4연속 없음")
    else:
        print(f"   ❌ 최종 검증 실패: 과열번호포함={has_overheated}, 4연속존재={max_cons>=3}")

if __name__ == "__main__":
    test_phase3_logic()