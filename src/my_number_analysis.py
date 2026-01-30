"""
나의 번호 분석 및 진단 모듈
사용자 번호의 당첨 이력 분석 및 알고리즘 기반 개선 제안
"""
import pandas as pd
import numpy as np
from collections import Counter

class MyNumberAnalyzer:
    def __init__(self, loader, model, recommender):
        """
        Args:
            loader: 데이터 로더
            model: 예측 모델 (점수 데이터 활용)
            recommender: 추천 시스템 (조합 점수 계산 활용)
        """
        self.loader = loader
        self.model = model
        self.recommender = recommender
        self.df = loader.df
        self.numbers_df = loader.numbers_df

    def analyze_history(self, my_numbers):
        """나의 번호 당첨 연대기 분석"""
        my_set = set(my_numbers)
        history = []
        
        total_prize = 0
        total_rounds = len(self.numbers_df)
        win_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 0: 0}
        
        # 전체 회차 순회하며 당첨 확인
        for _, row in self.numbers_df.iterrows():
            round_num = row['회차']
            date = row['일자']
            winning_numbers = set(row['당첨번호'])
            bonus = row['보너스번호']
            
            # 일치 개수 확인
            matched = my_set & winning_numbers
            match_count = len(matched)
            is_bonus = bonus in my_set
            
            # 등수 판별
            rank = 0
            prize = 0
            
            if match_count == 6:
                rank = 1
                prize = row['1등 당첨액']
            elif match_count == 5 and is_bonus:
                rank = 2
                prize = row['2등 당첨액']
            elif match_count == 5:
                rank = 3
                prize = row['3등 당첨액']
            elif match_count == 4:
                rank = 4
                prize = row['4등 당첨액']
            elif match_count == 3:
                rank = 5
                prize = row['5등 당첨액']
            
            if rank > 0:
                win_counts[rank] += 1
                total_prize += prize
                history.append({
                    'round': round_num,
                    'date': date,
                    'rank': rank,
                    'prize': prize,
                    'matched_count': match_count,
                    'matched_numbers': sorted(list(matched)),
                    'bonus_matched': is_bonus
                })
                
        # 가상 수익률 계산 (매주 1게임 1000원 구매 가정)
        total_cost = total_rounds * 1000
        profit_rate = ((total_prize - total_cost) / total_cost * 100) if total_cost > 0 else 0
        
        return {
            'history': sorted(history, key=lambda x: x['round'], reverse=True),
            'win_counts': win_counts,
            'total_prize': total_prize,
            'total_cost': total_cost,
            'profit_rate': profit_rate
        }

    def diagnose_and_boost(self, my_numbers):
        """번호 진단 및 확률 높이기 제안"""
        # 1. 현재 번호 조합 점수 계산 (기존 추천 시스템 로직 재사용)
        current_score = self.recommender._calculate_combination_score(my_numbers)
        
        # 2. 번호별 상세 점수 분석 (약점 찾기)
        details = []
        for num in my_numbers:
            # 모델에서 해당 번호의 점수 정보 가져오기
            scores = self.model.number_scores.get(num, {})
            details.append({
                'number': num,
                'total_score': scores.get('total_score', 0),
                'freq_score': scores.get('freq_score', 0),
                'trend_score': scores.get('trend_score', 0),
                'absence_score': scores.get('absence_score', 0)
            })
            
        # 3. 가장 약한 번호 식별 (점수 최하위)
        details.sort(key=lambda x: x['total_score'])
        weakest_num = details[0]['number']
        
        # 4. 교체 제안 (상위 번호 중 현재 조합에 없는 것)
        # 모델이 생각하는 상위 20개 번호 중 하나로 교체 시도
        top_numbers = self.model.get_top_numbers(20)
        recommendations = []
        
        for candidate in top_numbers:
            if candidate in my_numbers:
                continue
                
            # 교체 시뮬레이션: 약한 번호 빼고 후보 번호 넣기
            new_combo = [n for n in my_numbers if n != weakest_num] + [candidate]
            new_score = self.recommender._calculate_combination_score(new_combo)
            
            # 점수가 오르는 경우만 제안
            if new_score > current_score:
                recommendations.append({
                    'out': weakest_num,
                    'in': candidate,
                    'score_diff': new_score - current_score,
                    'new_score': new_score
                })
                
        # 점수 상승폭이 큰 순서대로 정렬
        recommendations.sort(key=lambda x: x['score_diff'], reverse=True)
        
        return {
            'current_score': current_score,
            'details': details,
            'weakest': weakest_num,
            'recommendations': recommendations[:3] # 상위 3개 제안
        }