import os
import sys
import pandas as pd
import shutil

# 프로젝트 루트 경로 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_updater import DataUpdater

def test_smart_sync():
    print("🧪 스마트 데이터 동기화(Smart Data Sync) 기능 테스트")
    print("=" * 60)

    # 1. 테스트 환경 설정
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    original_csv = os.path.join(base_dir, "Data", "645_251227.csv")
    test_csv = os.path.join(base_dir, "Data", "test_smart_sync.csv")

    print(f"1. 테스트 환경 설정")
    print(f"   - 원본 데이터: {os.path.basename(original_csv)}")
    print(f"   - 테스트 파일: {os.path.basename(test_csv)}")

    # 원본 보호를 위해 복사본으로 테스트
    shutil.copy(original_csv, test_csv)
    
    try:
        # 2. '구버전 데이터' 상황 연출 (강제 롤백)
        # CSV를 읽어서 가장 최신 회차를 삭제함
        try:
            df = pd.read_csv(test_csv, encoding='utf-8-sig')
        except:
            df = pd.read_csv(test_csv, encoding='cp949')
            
        latest_round = int(df['회차'].max())
        target_round = latest_round  # 삭제하고 다시 가져올 목표 회차
        
        print(f"\n2. '구버전 데이터' 상황 연출 (시뮬레이션)")
        print(f"   - 현재 최신 회차: {latest_round}회")
        print(f"   - {target_round}회차 데이터를 삭제하여 과거 상태로 되돌립니다.")
        
        # 최신 회차 행 삭제
        df_outdated = df[df['회차'] != target_round]
        df_outdated.to_csv(test_csv, index=False, encoding='utf-8-sig')
        
        current_latest = int(df_outdated['회차'].max())
        print(f"   - 롤백 후 최신 회차: {current_latest}회")

        # 3. DataUpdater 실행 (핵심 기능 테스트)
        print(f"\n3. DataUpdater 실행 (자동 감지 및 업데이트)")
        updater = DataUpdater(test_csv)
        
        # 웹에서 삭제된 회차(target_round) 검색 시도
        print(f"   - 웹에서 {target_round}회차 데이터 검색 중...")
        draw_data = updater.fetch_latest_draw_from_web(target_round)
        
        if not draw_data:
            print(f"   ❌ 실패: 웹에서 {target_round}회차 데이터를 찾을 수 없습니다.")
            print("      (동행복권 사이트 접속 문제거나 아직 추첨 전일 수 있습니다.)")
            return

        print(f"   ✅ 성공: 데이터 발견!")
        print(f"      결과: {draw_data['회차']}회 ({draw_data['일자']}) - {draw_data['당첨번호']}")

        # CSV 업데이트 시도
        print(f"   - CSV 파일 업데이트(복구) 시도...")
        success, msg = updater.update_csv_with_new_draw(draw_data)
        
        if success:
            print(f"   ✅ 업데이트 성공: {msg}")
        else:
            print(f"   ❌ 업데이트 실패: {msg}")
            return

        # 4. 결과 검증
        print(f"\n4. 최종 결과 검증")
        df_new = pd.read_csv(test_csv, encoding='utf-8-sig')
        new_latest = int(df_new['회차'].max())
        
        if new_latest == target_round:
            print(f"   🎉 검증 통과: CSV 파일이 {new_latest}회차로 완벽하게 복구되었습니다.")
            print("   🚀 Phase 1 (스마트 데이터 동기화) 기능이 정상 작동합니다.")
        else:
            print(f"   ❌ 검증 실패: CSV 파일의 최신 회차가 {new_latest}회입니다. (기대값: {target_round})")

    except Exception as e:
        print(f"\n❌ 테스트 중 오류 발생: {e}")
    finally:
        # 테스트 파일 정리
        if os.path.exists(test_csv):
            os.remove(test_csv)
            print(f"\n🧹 임시 테스트 파일 삭제 완료")

if __name__ == "__main__":
    test_smart_sync()