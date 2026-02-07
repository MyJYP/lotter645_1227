import sys
import os
import pandas as pd

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from history_manager import HistoryManager

def test_history_manager():
    print("🧪 HistoryManager 모듈 테스트")
    print("=" * 60)

    # 1. 초기화
    print("1. 초기화 및 파일 확인")
    manager = HistoryManager()
    print(f"   📂 파일 경로: {manager.file_path}")
    
    if os.path.exists(manager.file_path):
        print("   ✅ 파일이 존재합니다.")
    else:
        print("   ❌ 파일이 생성되지 않았습니다.")

    # 2. 저장 테스트
    print("\n2. 이력 저장 테스트")
    test_round = 9999
    test_strategy = "Test_Strategy"
    test_numbers = [1, 2, 3, 4, 5, 6]
    test_memo = "테스트 메모입니다."
    
    success = manager.save_history(test_round, test_strategy, test_numbers, test_memo)
    if success:
        print(f"   ✅ 저장 성공: {test_round}회, {test_numbers}")
    else:
        print("   ❌ 저장 실패")

    # 3. 조회 테스트
    print("\n3. 이력 조회 테스트")
    df = manager.load_history()
    print(f"   📊 총 데이터 개수: {len(df)}")
    
    if not df.empty:
        # 최신 데이터 (방금 저장한 데이터) 확인
        # load_history는 날짜 내림차순 정렬하므로 첫 번째 행이 최신
        latest = df.iloc[0]
        print(f"   📝 최신 데이터: {latest['round']}회 - {latest['numbers']}")
        
        if latest['round'] == test_round and latest['strategy'] == test_strategy:
            print("   ✅ 데이터 무결성 확인 (일치함)")
            
            # 4. 삭제 테스트
            print("\n4. 이력 삭제 테스트")
            # DataFrame의 인덱스를 사용하여 삭제
            target_index = latest.name
            print(f"   🗑️ 삭제할 인덱스: {target_index}")
            
            del_success = manager.delete_history(target_index)
            if del_success:
                print("   ✅ 삭제 성공")
                
                # 삭제 확인
                df_after = manager.load_history()
                if len(df_after) == len(df) - 1:
                    print("   ✅ 데이터 개수 감소 확인")
                else:
                    print("   ⚠️ 데이터 개수가 갱신되지 않았습니다.")
            else:
                print("   ❌ 삭제 실패")
        else:
            print("   ⚠️ 최신 데이터가 방금 저장한 데이터와 다릅니다. (다른 프로세스가 개입했거나 정렬 문제)")
    else:
        print("   ❌ 데이터가 로드되지 않았습니다.")

    print("\n" + "=" * 60)
    print("테스트 종료")

if __name__ == "__main__":
    test_history_manager()