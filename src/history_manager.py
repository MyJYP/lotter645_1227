import pandas as pd
import os
from datetime import datetime

class HistoryManager:
    """고정 모드 이력 관리 클래스"""
    
    def __init__(self):
        # 프로젝트 루트 경로 계산 (src 상위 폴더)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        self.file_path = os.path.join(project_root, "Data", "fixed_mode_history.csv")
        
        self.columns = ['round', 'date', 'strategy', 'numbers', 'memo']
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """파일이 없으면 생성"""
        if not os.path.exists(self.file_path):
            # Data 폴더가 없으면 생성 (혹시 모를 상황 대비)
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            
            df = pd.DataFrame(columns=self.columns)
            df.to_csv(self.file_path, index=False, encoding='utf-8-sig')

    def save_history(self, round_num, strategy, numbers, memo=""):
        """
        고정 모드 이력 저장
        
        Args:
            round_num (int): 회차
            strategy (str): 사용된 전략
            numbers (list or str): 번호 리스트 또는 문자열
            memo (str): 사용자 메모
            
        Returns:
            bool: 성공 여부
        """
        try:
            # 번호 리스트를 문자열로 변환
            if isinstance(numbers, list):
                numbers_str = ', '.join(map(str, sorted(numbers)))
            else:
                numbers_str = str(numbers)

            new_data = {
                'round': round_num,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'strategy': strategy,
                'numbers': numbers_str,
                'memo': memo
            }

            # 기존 데이터 로드
            if os.path.exists(self.file_path):
                df = pd.read_csv(self.file_path, encoding='utf-8-sig')
            else:
                df = pd.DataFrame(columns=self.columns)
            
            # 새 데이터 추가
            new_row = pd.DataFrame([new_data])
            df = pd.concat([df, new_row], ignore_index=True)
            
            # 저장
            df.to_csv(self.file_path, index=False, encoding='utf-8-sig')
            return True
            
        except Exception as e:
            print(f"Error saving history: {e}")
            return False

    def load_history(self):
        """
        저장된 이력 불러오기
        
        Returns:
            DataFrame: 이력 데이터 (최신순 정렬)
        """
        try:
            if os.path.exists(self.file_path):
                df = pd.read_csv(self.file_path, encoding='utf-8-sig')
                # 날짜 기준 내림차순 정렬
                if not df.empty and 'date' in df.columns:
                    df = df.sort_values(by='date', ascending=False)
                return df
            return pd.DataFrame(columns=self.columns)
        except Exception as e:
            print(f"Error loading history: {e}")
            return pd.DataFrame(columns=self.columns)

    def delete_history(self, index):
        """
        특정 이력 삭제
        
        Args:
            index (int): 삭제할 행의 인덱스 (DataFrame index)
            
        Returns:
            bool: 성공 여부
        """
        try:
            if os.path.exists(self.file_path):
                df = pd.read_csv(self.file_path, encoding='utf-8-sig')
                if index in df.index:
                    df = df.drop(index)
                    df.to_csv(self.file_path, index=False, encoding='utf-8-sig')
                    return True
            return False
        except Exception as e:
            print(f"Error deleting history: {e}")
            return False