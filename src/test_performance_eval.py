import sys
import os
import pandas as pd

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import LottoDataLoader
from prediction_model import LottoPredictionModel

def test_performance_evaluation():
    print("🧪 모델 성능 검증(Evaluation) 기능 테스트")
    print("=" * 60)

    # 1. 데이터 로드
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_path = os.path.join(project_root, "Data", "645_251227.csv")
    
    if not os.path.exists(data_path):
        print(f"❌ 데이터 파일을 찾을 수 없습니다: {data_path}")
        return

    print("1. 데이터 로딩 및 모델 학습 중...")
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()
    
    model = LottoPredictionModel(loader)
    model.train_all_patterns()
    
    # 메서드 존재 여부 확인 (안전장치)
    if not hasattr(model, 'evaluate_recent_performance'):
        print("\n❌ 오류: LottoPredictionModel에 'evaluate_recent_performance' 메서드가 없습니다.")
        print("   src/prediction_model.py 파일이 업데이트되었는지 확인해주세요.")
        return

    # 2. 성능 평가 메서드 호출
    print("\n2. evaluate_recent_performance(10) 호출")
    try:
        perf = model.evaluate_recent_performance(n_rounds=10)
        
        # 3. 결과 검증
        print("\n3. 반환 데이터 구조 검증")
        required_keys = ['avg_match', 'roi', 'total_prize', 'details']
        missing_keys = [k for k in required_keys if k not in perf]
        
        if missing_keys:
            print(f"   ❌ 실패: 필수 키 누락 ({missing_keys})")
            return
            
        print(f"   ✅ 필수 키 존재 확인: {list(perf.keys())}")
        
        print("\n4. 데이터 값 확인")
        print(f"   - 평균 당첨 개수: {perf['avg_match']:.2f}개")
        print(f"   - 가상 수익률(ROI): {perf['roi']:.2f}%")
        print(f"   - 총 당첨금: {perf['total_prize']:,}원")
        print(f"   - 상세 데이터 개수: {len(perf['details'])}개")
            
        print("\n🎉 테스트 성공! 모델 성능 평가 기능이 정상 작동합니다.")
        
    except Exception as e:
        print(f"\n❌ 테스트 중 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_performance_evaluation()