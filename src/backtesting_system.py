"""
로또 645 백테스팅 시스템
과거 데이터로 예측 후 실제 당첨번호와 비교하여 알고리즘 성능 검증
"""
import os
import json
import numpy as np
from pathlib import Path
from tqdm import tqdm
from collections import defaultdict
from data_loader import LottoDataLoader
from prediction_model import LottoPredictionModel
from recommendation_system import LottoRecommendationSystem


class BacktestingSystem:
    """백테스팅 엔진"""

    def __init__(self, data_path, cache_dir="Data/backtesting_cache"):
        """
        Args:
            data_path: CSV 데이터 파일 경로
            cache_dir: 캐시 디렉토리 경로
        """
        self.data_path = data_path
        self.cache_dir = Path(cache_dir)

        # 전체 데이터 로드 (정답 확인용)
        print("전체 데이터 로딩 중...")
        self.full_loader = LottoDataLoader(data_path)
        self.full_loader.load_data()
        self.full_loader.preprocess()
        self.full_loader.extract_numbers()

        # 캐시 디렉토리 생성
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        print(f"✓ 백테스팅 시스템 초기화 완료 (총 {len(self.full_loader.df)}회차)")

    def get_trainable_rounds(self, min_train_rounds=50):
        """백테스팅 가능한 회차 범위 결정

        Args:
            min_train_rounds: 최소 학습 데이터 회차 수 (기본 50)

        Returns:
            list: 백테스팅할 회차 리스트
        """
        all_rounds = sorted(self.full_loader.df['회차'].unique())

        # 최소 회차: 최초 회차 + 최소 학습 회차
        min_round = int(all_rounds[0])
        trainable_rounds = [int(r) for r in all_rounds
                           if r >= min_round + min_train_rounds]

        print(f"백테스팅 가능 범위: {trainable_rounds[0]}회 ~ {trainable_rounds[-1]}회")
        print(f"  (총 {len(trainable_rounds)}회, 최소 학습: {min_train_rounds}회)")

        return trainable_rounds

    def backtest_single_round(self, target_round, weights, strategy='score',
                              n_combinations=10, seed=42):
        """단일 회차 백테스팅

        프로세스:
        1. target_round - 1까지 데이터 로드
        2. 모델 학습
        3. 번호 추천
        4. 실제 당첨번호와 비교

        Args:
            target_round: 목표 회차
            weights: 가중치 딕셔너리
            strategy: 추천 전략 ('score', 'hybrid', 등)
            n_combinations: 추천 조합 개수
            seed: 랜덤 시드

        Returns:
            dict: {
                'round': 회차,
                'predicted': [추천 조합들],
                'actual': [실제 당첨번호],
                'matches': [각 조합의 일치 개수],
                'max_match': 최대 일치 개수,
                'has_3plus': 3개 이상 일치 여부
            }
        """
        # 1. 직전 회차까지 로드
        train_loader = LottoDataLoader(self.data_path)
        train_loader.load_data_until_round(target_round - 1)

        # 2. 모델 학습
        model = LottoPredictionModel(train_loader, weights=weights)
        model.train_all_patterns()

        # 3. 추천
        recommender = LottoRecommendationSystem(model)

        if strategy == 'score':
            predicted = recommender.generate_by_score(n_combinations, seed=seed)
        elif strategy == 'probability':
            predicted = recommender.generate_by_probability(n_combinations, seed=seed)
        elif strategy == 'pattern':
            predicted = recommender.generate_by_pattern(n_combinations, seed=seed)
        elif strategy == 'hybrid':
            predicted = recommender.generate_hybrid(n_combinations, seed=seed)
        else:
            predicted = recommender.generate_by_score(n_combinations, seed=seed)

        # 4. 실제 당첨번호
        actual = self.full_loader.get_round_data(target_round)

        # 5. 일치 개수 계산
        matches = [len(set(combo) & set(actual)) for combo in predicted]
        max_match = max(matches)
        has_3plus = max_match >= 3

        return {
            'round': target_round,
            'predicted': predicted,
            'actual': actual,
            'matches': matches,
            'max_match': max_match,
            'has_3plus': has_3plus
        }

    def backtest_multiple_rounds(self, rounds, weights, strategy='score',
                                  n_combinations=10, seed=42, use_cache=True):
        """여러 회차 백테스팅 (캐싱 지원)

        Args:
            rounds: 백테스팅할 회차 리스트
            weights: 가중치 딕셔너리
            strategy: 추천 전략
            n_combinations: 추천 조합 개수
            seed: 랜덤 시드
            use_cache: 캐시 사용 여부

        Returns:
            list: 백테스팅 결과 리스트
        """
        results = []

        # 캐시 키 생성
        cache_key = f"{strategy}_w{weights['freq_weight']:.0f}-{weights['trend_weight']:.0f}-{weights['absence_weight']:.0f}-{weights['hotness_weight']:.0f}"
        cache_file = self.cache_dir / f"{cache_key}.json"

        # 캐시 로드
        cached_rounds = set()
        if use_cache and cache_file.exists():
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)

            cached_rounds = {r['round'] for r in cached_data}
            remaining_rounds = [r for r in rounds if r not in cached_rounds]

            results.extend(cached_data)
            print(f"✓ 캐시: {len(cached_data)}회, 신규: {len(remaining_rounds)}회")
            rounds = remaining_rounds

        # 신규 계산
        if rounds:
            for target_round in tqdm(rounds, desc="백테스팅"):
                result = self.backtest_single_round(
                    target_round, weights, strategy, n_combinations, seed
                )
                results.append(result)

            # 캐시 저장
            if use_cache:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, ensure_ascii=False, indent=2)

        # 회차 순으로 정렬
        results.sort(key=lambda x: x['round'])

        return results

    def calculate_metrics(self, results):
        """백테스팅 결과 메트릭 계산

        Args:
            results: 백테스팅 결과 리스트

        Returns:
            dict: {
                'total_rounds': 전체 회차,
                'count_3plus': 3개 이상 일치 회차 수,
                'rate_3plus': 3개 이상 일치율 (%),
                'avg_match': 평균 일치 개수,
                'max_match_overall': 최고 일치 개수,
                'match_distribution': {0:..., 1:..., ...}
            }
        """
        total_rounds = len(results)

        if total_rounds == 0:
            return {
                'total_rounds': 0,
                'count_3plus': 0,
                'rate_3plus': 0.0,
                'avg_match': 0.0,
                'max_match_overall': 0,
                'match_distribution': {}
            }

        # 일치 개수별 통계
        match_counts = {i: 0 for i in range(7)}
        for r in results:
            match_counts[r['max_match']] += 1

        # 핵심 메트릭: 3개 이상 일치율
        count_3plus = sum(1 for r in results if r['has_3plus'])
        rate_3plus = count_3plus / total_rounds * 100

        # 평균 일치
        avg_match = np.mean([r['max_match'] for r in results])

        return {
            'total_rounds': total_rounds,
            'count_3plus': count_3plus,
            'rate_3plus': rate_3plus,
            'avg_match': avg_match,
            'max_match_overall': max(r['max_match'] for r in results),
            'match_distribution': match_counts
        }

    def print_metrics(self, metrics):
        """메트릭 출력"""
        print("\n" + "="*70)
        print("📊 백테스팅 결과")
        print("="*70)
        print(f"전체 회차: {metrics['total_rounds']}회")
        print(f"\n⭐ 3개 이상 일치율: {metrics['rate_3plus']:.2f}% ({metrics['count_3plus']}회)")
        print(f"평균 일치 개수: {metrics['avg_match']:.2f}개")
        print(f"최고 일치 개수: {metrics['max_match_overall']}개")

        print(f"\n일치 개수별 분포:")
        for i in range(7):
            count = metrics['match_distribution'][i]
            rate = count / metrics['total_rounds'] * 100 if metrics['total_rounds'] > 0 else 0
            bar = "█" * int(rate / 2)
            print(f"  {i}개: {count:3d}회 ({rate:5.2f}%) {bar}")

        # 무작위 기준선과 비교
        baseline = 1.87
        improvement = metrics['rate_3plus'] - baseline
        print(f"\n📈 개선도:")
        print(f"  무작위 기준선: {baseline:.2f}%")
        print(f"  현재 성능: {metrics['rate_3plus']:.2f}%")
        print(f"  차이: {improvement:+.2f}%p")

        if metrics['rate_3plus'] > baseline:
            print(f"  ✅ 무작위 대비 개선!")
        elif metrics['rate_3plus'] == baseline:
            print(f"  ⚠️ 무작위와 동일")
        else:
            print(f"  ❌ 무작위보다 낮음")

        print("="*70 + "\n")


def main():
    """테스트용 메인 함수"""
    data_path = "../Data/645_251227.csv"

    # 백테스팅 시스템 초기화
    backtester = BacktestingSystem(data_path)

    # 백테스팅 가능 회차
    trainable_rounds = backtester.get_trainable_rounds(min_train_rounds=50)

    # 테스트: 최근 10회차만 (빠른 테스트)
    test_rounds = trainable_rounds[-10:]

    print(f"\n테스트 회차: {test_rounds}")

    # 기본 가중치로 백테스팅
    weights = {
        'freq_weight': 30.0,
        'trend_weight': 30.0,
        'absence_weight': 20.0,
        'hotness_weight': 20.0
    }

    print(f"\n테스트 가중치: {weights}")

    results = backtester.backtest_multiple_rounds(
        test_rounds, weights, strategy='score',
        n_combinations=10, seed=42, use_cache=True
    )

    # 메트릭 계산 및 출력
    metrics = backtester.calculate_metrics(results)
    backtester.print_metrics(metrics)

    # 상세 결과 출력 (최근 5회)
    print("\n상세 결과 (최근 5회):")
    for r in results[-5:]:
        print(f"\n{r['round']}회:")
        print(f"  실제: {r['actual']}")
        print(f"  예측: {r['predicted'][0]} (1st)")
        print(f"  일치: {r['matches'][0]}개 ({r['has_3plus'] and '✓ 3개 이상' or ''})")


if __name__ == "__main__":
    main()
