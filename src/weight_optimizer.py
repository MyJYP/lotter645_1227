"""
로또 645 가중치 최적화기
Random Search + 정밀 Grid Search로 최적 가중치 탐색
"""
import random
import json
from datetime import datetime
from pathlib import Path


class WeightOptimizer:
    """가중치 최적화기"""

    def __init__(self, backtester, strategy='score', match_threshold=3):
        """
        Args:
            backtester: BacktestingSystem 인스턴스
            strategy: 추천 전략 ('score', 'hybrid', 등)
            match_threshold: 일치 기준 (3 또는 4, 기본값 3)
        """
        self.backtester = backtester
        self.strategy = strategy
        self.match_threshold = match_threshold

        # 탐색 범위
        self.weight_ranges = {
            'freq_weight': (10, 50),
            'trend_weight': (10, 50),
            'absence_weight': (5, 40),
            'hotness_weight': (5, 40)
        }

        self.optimization_history = []

    def random_weights(self):
        """무작위 가중치 생성"""
        return {
            key: random.uniform(min_val, max_val)
            for key, (min_val, max_val) in self.weight_ranges.items()
        }

    def evaluate_weights(self, weights, rounds, n_combinations=10):
        """가중치 평가

        Args:
            weights: 가중치 딕셔너리
            rounds: 백테스팅할 회차 리스트
            n_combinations: 추천 조합 개수

        Returns:
            float: {threshold}개 이상 일치율 (%)
        """
        results = self.backtester.backtest_multiple_rounds(
            rounds, weights, self.strategy, n_combinations,
            seed=42, use_cache=True
        )

        metrics = self.backtester.calculate_metrics(results)
        rate_key = f'rate_{self.match_threshold}plus'
        return metrics[rate_key]

    def random_search(self, rounds, n_trials=30, n_combinations=10):
        """Random Search 최적화

        Args:
            rounds: 백테스팅할 회차 리스트
            n_trials: 시도 횟수 (기본 30)
            n_combinations: 추천 조합 개수

        Returns:
            (best_weights, best_score): 최적 가중치 및 점수
        """
        print(f"\n🔍 Random Search 시작 (시도: {n_trials})")
        print("="*70)

        best_weights = None
        best_score = 0.0

        for trial in range(n_trials):
            weights = self.random_weights()

            print(f"\n[{trial+1}/{n_trials}] 평가 중...")
            print(f"  가중치: freq={weights['freq_weight']:.1f}, "
                  f"trend={weights['trend_weight']:.1f}, "
                  f"absence={weights['absence_weight']:.1f}, "
                  f"hotness={weights['hotness_weight']:.1f}")

            score = self.evaluate_weights(weights, rounds, n_combinations)

            print(f"  → {self.match_threshold}개 이상 일치율: {score:.2f}%")

            if score > best_score:
                best_score = score
                best_weights = weights.copy()
                print(f"  ✨ 신기록! {best_score:.2f}%")

            self.optimization_history.append({
                'trial': trial + 1,
                'weights': weights,
                'score': score
            })

        print(f"\n" + "="*70)
        print(f"✅ Random Search 완료")
        print(f"최고 점수: {best_score:.2f}%")
        print(f"최적 가중치: freq={best_weights['freq_weight']:.1f}, "
              f"trend={best_weights['trend_weight']:.1f}, "
              f"absence={best_weights['absence_weight']:.1f}, "
              f"hotness={best_weights['hotness_weight']:.1f}")

        return best_weights, best_score

    def grid_search_refined(self, base_weights, rounds, step=2.0, n_combinations=10):
        """정밀 Grid Search (기준 가중치 주변 탐색)

        Args:
            base_weights: 기준 가중치
            rounds: 백테스팅할 회차 리스트
            step: 탐색 간격 (기본 2.0)
            n_combinations: 추천 조합 개수

        Returns:
            (best_weights, best_score): 최적 가중치 및 점수
        """
        print(f"\n🔬 정밀 탐색 시작 (±{step*2})")
        print("="*70)

        best_weights = base_weights.copy()
        best_score = self.evaluate_weights(base_weights, rounds, n_combinations)

        print(f"기준 점수: {best_score:.2f}%\n")

        # 각 가중치를 개별적으로 조정
        for key in base_weights.keys():
            print(f"\n{key} 최적화...")

            for delta in [-step*2, -step, step, step*2]:
                test_weights = base_weights.copy()
                test_weights[key] += delta

                # 범위 체크
                min_val, max_val = self.weight_ranges[key]
                if not (min_val <= test_weights[key] <= max_val):
                    continue

                score = self.evaluate_weights(test_weights, rounds, n_combinations)
                print(f"  {key}={test_weights[key]:.1f}: {score:.2f}%", end="")

                if score > best_score:
                    best_score = score
                    best_weights = test_weights.copy()
                    print(f"  ✨ 개선!")
                else:
                    print()

        print(f"\n" + "="*70)
        print(f"✅ 정밀 탐색 완료")
        print(f"최종 점수: {best_score:.2f}%")
        print(f"최적 가중치: freq={best_weights['freq_weight']:.1f}, "
              f"trend={best_weights['trend_weight']:.1f}, "
              f"absence={best_weights['absence_weight']:.1f}, "
              f"hotness={best_weights['hotness_weight']:.1f}")

        return best_weights, best_score

    def fine_tune_weights(self, base_weights, rounds, n_trials=20, n_combinations=10, step=3.0):
        """가중치 미세 조정 (Fine-tuning) - Phase 3

        기존 가중치 주변을 무작위로 탐색하여 최적값 보정
        
        Args:
            base_weights: 기준 가중치
            rounds: 백테스팅할 회차 리스트
            n_trials: 시도 횟수 (기본 20)
            n_combinations: 추천 조합 개수
            step: 변동 범위 (±step)

        Returns:
            (best_weights, best_score): 최적 가중치 및 점수
        """
        print(f"\n🔧 가중치 미세 조정 시작 (시도: {n_trials}회, 범위: ±{step})")
        print("="*70)
        
        best_weights = base_weights.copy()
        best_score = self.evaluate_weights(base_weights, rounds, n_combinations)
        
        print(f"기준 점수: {best_score:.2f}%")
        
        for i in range(n_trials):
            # 현재 최적 가중치 주변에서 무작위 변동
            test_weights = best_weights.copy()
            
            # 모든 가중치를 소폭 조정 (Local Perturbation)
            for key in test_weights.keys():
                delta = random.uniform(-step, step)
                test_weights[key] += delta
                
                # 범위 체크
                min_val, max_val = self.weight_ranges[key]
                test_weights[key] = max(min_val, min(test_weights[key], max_val))
            
            score = self.evaluate_weights(test_weights, rounds, n_combinations)
            
            if score > best_score:
                print(f"[{i+1}/{n_trials}] {score:.2f}% (개선됨!)")
                best_score = score
                best_weights = test_weights
            else:
                if (i+1) % 5 == 0:
                    print(f"[{i+1}/{n_trials}] {score:.2f}%")
                    
        print(f"\n" + "="*70)
        print(f"✅ 미세 조정 완료")
        print(f"최종 점수: {best_score:.2f}%")
        
        return best_weights, best_score

    def optimize(self, rounds, n_random_trials=30, refine=True, n_combinations=10):
        """전체 최적화 프로세스

        Args:
            rounds: 백테스팅할 회차 리스트
            n_random_trials: Random Search 시도 횟수
            refine: 정밀 Grid Search 수행 여부
            n_combinations: 추천 조합 개수

        Returns:
            (best_weights, best_score): 최적 가중치 및 점수
        """
        print("\n" + "="*70)
        print("🚀 가중치 최적화 시작")
        print("="*70)
        print(f"전략: {self.strategy}")
        print(f"학습 회차: {len(rounds)}회 ({rounds[0]}회 ~ {rounds[-1]}회)")
        print(f"Random Search: {n_random_trials}회")
        print(f"정밀 탐색: {'Yes' if refine else 'No'}")

        # 1단계: Random Search
        best_weights, best_score = self.random_search(
            rounds, n_random_trials, n_combinations
        )

        # 2단계: 정밀 Grid Search (옵션)
        if refine:
            best_weights, best_score = self.grid_search_refined(
                best_weights, rounds, step=2.0, n_combinations=n_combinations
            )

        # 저장
        self.save_optimal_weights(best_weights, best_score)

        print("\n" + "="*70)
        print("🎉 최적화 완료!")
        print("="*70)

        return best_weights, best_score

    def save_optimal_weights(self, weights, score):
        """최적 가중치 저장 (이중 저장: 히스토리 + 최신)

        Args:
            weights: 최적 가중치
            score: 점수 ({threshold}개 이상 일치율)
        """
        now = datetime.now()
        result = {
            'timestamp': now.isoformat(),
            'strategy': self.strategy,
            'match_threshold': self.match_threshold,
            'weights': weights,
            'score': score,
            'optimization_history': self.optimization_history
        }

        # 1. 타임스탬프 파일명으로 히스토리 저장 (로컬에만 유지)
        timestamp_str = now.strftime('%Y-%m-%d_%H-%M-%S')
        history_file = self.backtester.cache_dir / f"optimal_weights_{self.strategy}_{self.match_threshold}plus_{timestamp_str}.json"

        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 히스토리 저장: {history_file.name}")

        # 2. 고정 파일명으로 최신 버전 저장 (배포용, 기준 포함)
        latest_file = self.backtester.cache_dir / f"optimal_weights_{self.strategy}_{self.match_threshold}plus.json"

        with open(latest_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"✓ 최신 버전 저장: {latest_file.name} (배포용)")

    def load_optimal_weights(self):
        """저장된 최적 가중치 로드

        Returns:
            dict or None: 최적 가중치 데이터
        """
        weights_file = self.backtester.cache_dir / f"optimal_weights_{self.strategy}_{self.match_threshold}plus.json"

        if not weights_file.exists():
            print(f"⚠️ 최적 가중치 파일 없음: {weights_file}")
            return None

        with open(weights_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        print(f"✓ 최적 가중치 로드:")
        print(f"  타임스탬프: {data['timestamp']}")
        print(f"  전략: {data['strategy']}")
        print(f"  기준: {data.get('match_threshold', self.match_threshold)}개 이상")
        print(f"  점수: {data['score']:.2f}%")
        print(f"  가중치: {data['weights']}")

        return data


def main():
    """테스트용 메인 함수"""
    from backtesting_system import BacktestingSystem

    data_path = "../Data/645_251227.csv"

    # 백테스팅 시스템 초기화
    backtester = BacktestingSystem(data_path)

    # 학습 데이터: 651~1105회 (455회)
    # 검증 데이터: 1106~1205회 (100회)
    trainable_rounds = backtester.get_trainable_rounds(min_train_rounds=50)
    train_rounds = [r for r in trainable_rounds if r < 1106]

    # 테스트: 최근 50회만 (빠른 테스트)
    train_rounds = train_rounds[-50:]

    print(f"\n학습 회차: {len(train_rounds)}회 ({train_rounds[0]}회 ~ {train_rounds[-1]}회)")

    # 최적화기 초기화
    optimizer = WeightOptimizer(backtester, strategy='score')

    # 최적화 실행 (테스트: 10번만)
    best_weights, best_score = optimizer.optimize(
        train_rounds,
        n_random_trials=10,
        refine=True,
        n_combinations=10
    )

    print(f"\n최종 결과:")
    print(f"  최적 가중치: {best_weights}")
    print(f"  3개 이상 일치율: {best_score:.2f}%")


if __name__ == "__main__":
    main()
