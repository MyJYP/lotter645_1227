"""
상극수 페널티 및 궁합수 보너스 점수 반영 테스트
"""
import sys
import os

# 모듈 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import LottoDataLoader
from prediction_model import LottoPredictionModel
from recommendation_system import LottoRecommendationSystem
from pattern_analysis import PatternAnalysis

def test_compatibility_score():
    print("="*70)
    print("🧪 상극수/궁합수 점수 반영 테스트")
    print("="*70)

    # 1. 데이터 로드 및 모델 초기화
    print("\n1. 데이터 로드 및 모델 초기화...")
    # 상위 디렉토리의 Data 폴더 참조
    data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Data", "645_251227.csv")
    
    if not os.path.exists(data_path):
        print(f"❌ 데이터 파일을 찾을 수 없습니다: {data_path}")
        return
        
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()

    model = LottoPredictionModel(loader)
    model.train_all_patterns()

    recommender = LottoRecommendationSystem(model)
    
    # 2. 상극수 확인
    print("\n2. 상극수(한 번도 같이 안 나온 쌍) 확인...")
    analyzer = PatternAnalysis(loader)
    _, never_appeared = analyzer.analyze_compatibility()
    
    if not never_appeared:
        print("⚠️ 상극수가 없습니다. 테스트를 진행할 수 없습니다.")
        return

    # 테스트용 상극수 쌍 선택 (첫 번째 것 사용)
    bad_pair = list(never_appeared)[0]
    print(f"  👉 테스트용 상극수 쌍: {bad_pair}")
    
    # 3. 테스트 조합 생성
    # 상극수 쌍을 포함하는 조합 생성
    # 나머지 번호는 1부터 채우되 중복되지 않게 설정
    combo_with_bad_pair = list(bad_pair)
    candidate = 1
    while len(combo_with_bad_pair) < 6:
        if candidate not in combo_with_bad_pair:
            combo_with_bad_pair.append(candidate)
        candidate += 1
    
    combo_with_bad_pair = sorted(combo_with_bad_pair)
    print(f"  👉 상극수 포함 조합: {combo_with_bad_pair}")

    # 4. 점수 계산 (상극수 포함)
    score_bad = recommender._calculate_combination_score(combo_with_bad_pair)
    print(f"  👉 점수 (상극수 포함): {score_bad:.2f}점")
    
    # 5. 비교군: 상극수 중 하나를 다른 숫자로 변경하여 페널티 제거
    # bad_pair[1]을 다른 숫자로 변경 (기존에 없는 숫자이면서 또다른 상극수를 만들지 않는 숫자)
    combo_good = combo_with_bad_pair.copy()
    original_num = bad_pair[1]
    
    # 대체할 숫자 찾기 (단순하게 45부터 내려오면서 찾음)
    new_num = 45
    while True:
        # 이미 조합에 있거나, bad_pair[0]과 또다른 상극수 관계라면 패스
        is_another_bad = (min(bad_pair[0], new_num), max(bad_pair[0], new_num)) in recommender.never_appeared_set
        if new_num not in combo_good and not is_another_bad:
            break
        new_num -= 1
    
    # 숫자 교체
    if original_num in combo_good:
        idx = combo_good.index(original_num)
        combo_good[idx] = new_num
    
    combo_good = sorted(combo_good)
    print(f"  👉 상극수 제거 조합: {combo_good} (상극수 {bad_pair} 중 {original_num} -> {new_num} 교체)")
    
    # 6. 점수 계산 (상극수 제거)
    score_good = recommender._calculate_combination_score(combo_good)
    print(f"  👉 점수 (상극수 제거): {score_good:.2f}점")
    
    # 7. 결과 분석
    diff = score_good - score_bad
    print("\n3. 결과 분석")
    print(f"  점수 차이: {diff:.2f}점")
    
    # 개별 번호 점수 차이를 감안하더라도 
    print("  ⚠️ 점수 차이가 예상보다 작습니다. 상세 로직 확인이 필요합니다.")
        
    # 상세 점수 분해 (디버깅용)
    print("\n[참고] 상극수 포함 조합 상세 점수:")
    base_score = sum(model.number_scores[n]['total_score'] for n in combo_with_bad_pair)
    print(f"  기본 점수 합(개별 번호 점수): {base_score:.2f}")
    print(f"  최종 점수: {score_bad:.2f}")
    print(f"  패턴 보너스/페널티 합계: {score_bad - base_score:.2f}")
    print(f"  (예상 페널티: -10점)")

if __name__ == "__main__":
    test_compatibility_score()