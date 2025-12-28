"""
로또 645 번호 추천 시스템
다양한 전략으로 번호 조합 생성
"""
import numpy as np
import random
from collections import Counter
from itertools import combinations


class LottoRecommendationSystem:
    """로또 번호 추천 시스템"""

    def __init__(self, prediction_model):
        """
        Args:
            prediction_model: LottoPredictionModel 인스턴스
        """
        self.model = prediction_model
        self.loader = prediction_model.loader

        # 그리드 패턴 데이터 초기화 (7x7 그리드)
        self._init_grid_pattern_data()

        # 이미지 패턴 분석기 초기화
        from image_pattern_analysis import ImagePatternAnalysis
        self.image_analyzer = ImagePatternAnalysis(self.loader)

    def _init_grid_pattern_data(self):
        """그리드 패턴 관련 데이터 초기화"""
        # 번호를 그리드 좌표로 매핑 (1-45)
        self.number_to_position = {}
        number = 1
        for row in range(7):
            for col in range(7):
                if number <= 45:
                    self.number_to_position[number] = (row, col)
                    number += 1

        # 그리드 구역별 번호 정의
        self.grid_zones = {
            'corner': [1, 7, 43, 45],  # 모서리 (4칸)
            'middle': [16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 31, 32, 33, 34],  # 중간 (12칸)
            'center': [24, 25, 26, 31, 32, 33, 38, 39, 40],  # 중앙부 (9칸)
            'anti_diagonal': [7, 13, 19, 25, 31, 37, 43]  # 반대 대각선
        }

        # 그리드 가중치 (1칸당 평균 출현 기준)
        self.grid_weights = {
            'middle': 1.46,    # 108.3 / 74.0 = 1.46
            'center': 1.09,    # 80.7 / 74.0 = 1.09
            'edge': 0.91,      # 67.7 / 74.0 = 0.91
            'corner': 0.83     # 61.5 / 74.0 = 0.83
        }

    def _get_grid_zone(self, number):
        """번호가 속한 그리드 구역 반환"""
        if number in self.grid_zones['corner']:
            return 'corner'
        elif number in self.grid_zones['middle']:
            return 'middle'
        elif number in self.grid_zones['center']:
            return 'center'
        else:
            return 'edge'

    def _calculate_grid_score(self, numbers):
        """그리드 패턴 기반 점수 계산"""
        score = 0

        # 1. 위치 기반 가중치
        for num in numbers:
            zone = self._get_grid_zone(num)
            weight = self.grid_weights.get(zone, 1.0)
            score += weight * 10  # 기본 10점에 가중치 적용

        # 2. 중간 영역 보너스 (3-4개 권장)
        middle_count = sum(1 for n in numbers if n in self.grid_zones['middle'])
        if 3 <= middle_count <= 4:
            score += 20

        # 3. 반대 대각선 보너스 (1-2개 권장)
        anti_diag_count = sum(1 for n in numbers if n in self.grid_zones['anti_diagonal'])
        if 1 <= anti_diag_count <= 2:
            score += 15

        # 4. 모서리 페널티 (2개 이상이면 감점)
        corner_count = sum(1 for n in numbers if n in self.grid_zones['corner'])
        if corner_count >= 2:
            score -= 15

        # 5. 공간적 군집도 (평균 거리 4.0~5.5 권장)
        avg_distance = self._calculate_spatial_distance(numbers)
        if 4.0 <= avg_distance <= 5.5:
            score += 20
        elif avg_distance < 3.0 or avg_distance > 6.0:
            score -= 10  # 너무 밀집/분산되면 감점

        return score

    def _calculate_spatial_distance(self, numbers):
        """번호들 간의 평균 맨해튼 거리 계산"""
        distances = []
        nums = sorted(numbers)

        for i in range(len(nums)):
            for j in range(i+1, len(nums)):
                pos1 = self.number_to_position.get(nums[i])
                pos2 = self.number_to_position.get(nums[j])

                if pos1 and pos2:
                    # 맨해튼 거리
                    dist = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
                    distances.append(dist)

        return np.mean(distances) if distances else 0

    def _is_valid_combination(self, numbers, strict=False):
        """번호 조합이 유효한지 검증"""
        nums = sorted(numbers)

        # 1. 개수 확인
        if len(nums) != 6:
            return False

        # 2. 범위 확인
        if any(n < 1 or n > 45 for n in nums):
            return False

        # 3. 중복 확인
        if len(set(nums)) != 6:
            return False

        if not strict:
            return True

        # 엄격한 검증: 패턴 기반

        # 4. 구간 분포 확인 (한 구간에 5개 이상 X)
        low = sum(1 for n in nums if 1 <= n <= 15)
        mid = sum(1 for n in nums if 16 <= n <= 30)
        high = sum(1 for n in nums if 31 <= n <= 45)

        if max(low, mid, high) > 4:
            return False

        # 5. 홀짝 비율 확인 (0:6 또는 6:0 제외)
        odd = sum(1 for n in nums if n % 2 == 1)
        if odd == 0 or odd == 6:
            return False

        # 6. 연속 번호 체크 (4개 이상 연속 제외 - 극히 드뭄)
        consecutive_count = 0
        for i in range(len(nums)-1):
            if nums[i+1] == nums[i] + 1:
                consecutive_count += 1
                if consecutive_count >= 3:  # 4개 연속
                    return False
            else:
                consecutive_count = 0

        return True

    def _calculate_combination_score(self, numbers):
        """조합에 대한 점수 계산"""
        score = 0

        # 1. 개별 번호 점수 합
        for num in numbers:
            score += self.model.number_scores[num]['total_score']

        # 2. 패턴 보너스

        # 연속 번호 있으면 보너스 (56% 확률이므로)
        nums = sorted(numbers)
        has_consecutive = False
        for i in range(len(nums)-1):
            if nums[i+1] == nums[i] + 1:
                has_consecutive = True
                score += 10
                break

        # 구간 분포 보너스
        low = sum(1 for n in nums if 1 <= n <= 15)
        mid = sum(1 for n in nums if 16 <= n <= 30)
        high = sum(1 for n in nums if 31 <= n <= 45)

        # 균형잡힌 분포
        if 1 <= low <= 3 and 1 <= mid <= 3 and 1 <= high <= 3:
            score += 15

        # 홀짝 균형
        odd = sum(1 for n in nums if n % 2 == 1)
        if 2 <= odd <= 4:
            score += 10

        # 합계 범위
        total = sum(nums)
        mean = self.model.patterns['sum']['mean']
        std = self.model.patterns['sum']['std']

        if mean - std <= total <= mean + std:
            score += 10

        # 3. 그리드 패턴 보너스 (NEW)
        grid_score = self._calculate_grid_score(numbers)
        score += grid_score * 0.5  # 가중치 적용 (50%)

        # 4. 이미지 패턴 보너스 (NEW)
        image_score_data = self.image_analyzer.calculate_image_score(numbers)
        score += image_score_data['total_score'] * 0.3  # 가중치 적용 (30%)

        return score

    def generate_by_score(self, n_combinations=5, use_top=20, seed=None):
        """점수 기반 추천"""
        print(f"\n🎯 점수 기반 추천 (상위 {use_top}개 번호 활용)")

        # 시드 설정 (고정 모드)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        top_numbers = self.model.get_top_numbers(use_top)
        combinations_list = []

        # 상위 번호들로 가능한 조합 생성
        max_attempts = 10000
        attempts = 0

        while len(combinations_list) < n_combinations and attempts < max_attempts:
            # 상위 번호에서 가중치 샘플링
            selected = random.sample(top_numbers, 6)

            if self._is_valid_combination(selected):
                sorted_selected = tuple(sorted(selected))
                if sorted_selected not in combinations_list:
                    combinations_list.append(sorted_selected)

            attempts += 1

        # 점수 순으로 정렬
        scored_combos = []
        for combo in combinations_list:
            score = self._calculate_combination_score(combo)
            scored_combos.append((combo, score))

        scored_combos.sort(key=lambda x: x[1], reverse=True)

        results = [list(combo) for combo, _ in scored_combos[:n_combinations]]

        for i, (combo, score) in enumerate(scored_combos[:n_combinations], 1):
            print(f"  {i}. {list(combo)} (점수: {score:.1f})")

        return results

    def generate_by_probability(self, n_combinations=5, seed=None):
        """확률 가중치 기반 추천"""
        print(f"\n🎲 확률 가중치 기반 추천")

        # 시드 설정 (고정 모드)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        weights = self.model.get_probability_weights()
        numbers = list(range(1, 46))
        probabilities = [weights[n] for n in numbers]

        combinations_list = []
        max_attempts = 10000
        attempts = 0

        while len(combinations_list) < n_combinations and attempts < max_attempts:
            # 가중치 기반 샘플링
            selected = np.random.choice(numbers, size=6, replace=False, p=probabilities)

            if self._is_valid_combination(selected):
                sorted_selected = tuple(sorted(selected))
                if sorted_selected not in combinations_list:
                    combinations_list.append(sorted_selected)

            attempts += 1

        results = [list(combo) for combo in combinations_list[:n_combinations]]

        for i, combo in enumerate(results, 1):
            print(f"  {i}. {combo}")

        return results

    def generate_by_pattern(self, n_combinations=5, seed=None):
        """패턴 기반 추천 (연속, 구간, 홀짝 고려)"""
        print(f"\n🔄 패턴 기반 추천")

        # 시드 설정 (고정 모드)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # 가장 흔한 패턴 가져오기
        section_pattern = self.model.patterns['section']['most_common'][0][0]  # (저, 중, 고)
        odd_even_pattern = self.model.patterns['odd_even']['most_common'][0][0]  # (홀, 짝)

        print(f"  목표 구간 분포: 저{section_pattern[0]}/중{section_pattern[1]}/고{section_pattern[2]}")
        print(f"  목표 홀짝 분포: 홀{odd_even_pattern[0]}/짝{odd_even_pattern[1]}")

        combinations_list = []
        max_attempts = 10000
        attempts = 0

        top_numbers = self.model.get_top_numbers(30)  # 상위 30개에서 선택

        while len(combinations_list) < n_combinations and attempts < max_attempts:
            selected = []

            # 구간별로 번호 선택
            low_pool = [n for n in top_numbers if 1 <= n <= 15]
            mid_pool = [n for n in top_numbers if 16 <= n <= 30]
            high_pool = [n for n in top_numbers if 31 <= n <= 45]

            # 구간 패턴 맞추기
            if len(low_pool) >= section_pattern[0]:
                selected.extend(random.sample(low_pool, section_pattern[0]))
            if len(mid_pool) >= section_pattern[1]:
                selected.extend(random.sample(mid_pool, section_pattern[1]))
            if len(high_pool) >= section_pattern[2]:
                selected.extend(random.sample(high_pool, section_pattern[2]))

            # 부족하면 나머지 채우기
            while len(selected) < 6:
                remaining = [n for n in top_numbers if n not in selected]
                if remaining:
                    selected.append(random.choice(remaining))
                else:
                    break

            if len(selected) == 6 and self._is_valid_combination(selected):
                # 홀짝 패턴도 확인
                odd_count = sum(1 for n in selected if n % 2 == 1)
                if abs(odd_count - odd_even_pattern[0]) <= 1:  # 오차 1 허용
                    sorted_selected = tuple(sorted(selected))
                    if sorted_selected not in combinations_list:
                        combinations_list.append(sorted_selected)

            attempts += 1

        results = [list(combo) for combo in combinations_list[:n_combinations]]

        for i, combo in enumerate(results, 1):
            odd = sum(1 for n in combo if n % 2 == 1)
            low = sum(1 for n in combo if 1 <= n <= 15)
            mid = sum(1 for n in combo if 16 <= n <= 30)
            high = sum(1 for n in combo if 31 <= n <= 45)
            print(f"  {i}. {combo} [홀{odd}/짝{6-odd}, 저{low}/중{mid}/고{high}]")

        return results

    def generate_grid_based(self, n_combinations=5, seed=None):
        """그리드 패턴 기반 추천 (NEW)"""
        print(f"\n🎨 그리드 패턴 기반 추천")

        # 시드 설정 (고정 모드)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # 중간 영역 번호 우선 선택
        middle_numbers = self.grid_zones['middle']
        anti_diag_numbers = self.grid_zones['anti_diagonal']
        top_numbers = self.model.get_top_numbers(45)

        combinations_list = []
        max_attempts = 10000
        attempts = 0

        while len(combinations_list) < n_combinations and attempts < max_attempts:
            selected = []

            # 1. 중간 영역에서 3-4개 선택
            middle_pool = [n for n in middle_numbers if n in top_numbers[:30]]
            if len(middle_pool) >= 3:
                num_middle = random.choice([3, 4])
                selected.extend(random.sample(middle_pool, min(num_middle, len(middle_pool))))

            # 2. 반대 대각선에서 1-2개 선택
            anti_diag_pool = [n for n in anti_diag_numbers if n not in selected and n in top_numbers[:30]]
            if len(anti_diag_pool) >= 1:
                num_anti_diag = random.choice([1, 2])
                selected.extend(random.sample(anti_diag_pool, min(num_anti_diag, len(anti_diag_pool))))

            # 3. 나머지는 상위 번호에서 선택 (모서리 제외)
            remaining_pool = [n for n in top_numbers[:30]
                            if n not in selected and n not in self.grid_zones['corner']]

            while len(selected) < 6 and remaining_pool:
                selected.append(random.choice(remaining_pool))
                remaining_pool = [n for n in remaining_pool if n not in selected]

            if len(selected) == 6:
                # 평균 거리 검증 (4.0~5.5 권장)
                avg_distance = self._calculate_spatial_distance(selected)

                if 3.5 <= avg_distance <= 6.0:  # 약간 여유 있게
                    if self._is_valid_combination(selected):
                        sorted_selected = tuple(sorted(selected))
                        if sorted_selected not in combinations_list:
                            combinations_list.append(sorted_selected)

            attempts += 1

        # 그리드 점수로 정렬
        scored_combos = []
        for combo in combinations_list:
            grid_score = self._calculate_grid_score(combo)
            total_score = self._calculate_combination_score(combo)
            scored_combos.append((combo, grid_score, total_score))

        scored_combos.sort(key=lambda x: x[2], reverse=True)  # 총점으로 정렬

        results = [list(combo) for combo, _, _ in scored_combos[:n_combinations]]

        for i, (combo, grid_score, total_score) in enumerate(scored_combos[:n_combinations], 1):
            avg_dist = self._calculate_spatial_distance(combo)
            middle_count = sum(1 for n in combo if n in self.grid_zones['middle'])
            anti_diag_count = sum(1 for n in combo if n in self.grid_zones['anti_diagonal'])
            print(f"  {i}. {list(combo)} [그리드:{grid_score:.1f}, 총점:{total_score:.1f}, 평균거리:{avg_dist:.1f}, 중간:{middle_count}, 대각:{anti_diag_count}]")

        return results

    def generate_image_based(self, n_combinations=5, seed=None):
        """이미지 패턴 기반 추천 (NEW)"""
        print(f"\n🖼️  이미지 패턴 기반 추천")

        # 시드 설정 (고정 모드)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        combinations_list = []
        max_attempts = 10000
        attempts = 0

        top_numbers = self.model.get_top_numbers(35)

        print("  목표: 시각적 밀도 3.0~4.5, 4분면 균형, 무게중심 균형, 좌우 대칭")

        while len(combinations_list) < n_combinations and attempts < max_attempts:
            selected = random.sample(top_numbers, 6)

            if self._is_valid_combination(selected):
                # 이미지 패턴 점수 계산
                image_score_data = self.image_analyzer.calculate_image_score(selected)

                # 점수가 70점 이상이면 채택
                if image_score_data['total_score'] >= 70:
                    sorted_selected = tuple(sorted(selected))
                    if sorted_selected not in combinations_list:
                        combinations_list.append((sorted_selected, image_score_data))

            attempts += 1

        # 이미지 패턴 점수로 정렬
        combinations_list.sort(key=lambda x: x[1]['total_score'], reverse=True)

        results = [list(combo) for combo, _ in combinations_list[:n_combinations]]

        for i, (combo, score_data) in enumerate(combinations_list[:n_combinations], 1):
            quad = score_data['quadrants']
            quad_str = f"Q1:{quad['Q1']}, Q2:{quad['Q2']}, Q3:{quad['Q3']}, Q4:{quad['Q4']}"
            print(f"  {i}. {list(combo)} [이미지점수:{score_data['total_score']}점, "
                  f"거리:{score_data['avg_distance']:.1f}, {quad_str}]")

        return results

    def generate_hybrid(self, n_combinations=5, seed=None):
        """하이브리드 추천 (여러 전략 혼합)"""
        print(f"\n⭐ 하이브리드 추천 (최고 품질)")

        # 시드 설정 (고정 모드)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        all_combos = []

        # 각 전략에서 생성 (5가지 전략)
        score_combos = self.generate_by_score(n_combinations=2, use_top=15, seed=seed)
        prob_combos = self.generate_by_probability(n_combinations=2, seed=seed)
        pattern_combos = self.generate_by_pattern(n_combinations=2, seed=seed)
        grid_combos = self.generate_grid_based(n_combinations=2, seed=seed)
        image_combos = self.generate_image_based(n_combinations=2, seed=seed)  # NEW

        # 중복 제거하여 합치기
        for combo in score_combos + prob_combos + pattern_combos + grid_combos + image_combos:
            sorted_combo = tuple(sorted(combo))
            if sorted_combo not in all_combos:
                all_combos.append(sorted_combo)

        # 점수 계산하여 정렬
        scored = []
        for combo in all_combos:
            score = self._calculate_combination_score(combo)
            scored.append((combo, score))

        scored.sort(key=lambda x: x[1], reverse=True)

        results = [list(combo) for combo, _ in scored[:n_combinations]]

        print(f"\n최종 선정:")
        for i, (combo, score) in enumerate(scored[:n_combinations], 1):
            odd = sum(1 for n in combo if n % 2 == 1)
            total = sum(combo)
            print(f"  {i}. {list(combo)} (점수: {score:.1f}, 합: {total}, 홀{odd}/짝{6-odd})")

        return results

    def generate_with_consecutive(self, n_combinations=5, seed=None):
        """연속 번호 포함 추천 (56% 확률 반영)"""
        print(f"\n🔢 연속 번호 포함 추천")

        # 시드 설정 (고정 모드)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        # 가장 많이 나온 연속 쌍
        consecutive_pairs = self.model.patterns['consecutive']['pair_frequency']
        top_pairs = sorted(consecutive_pairs.items(), key=lambda x: x[1], reverse=True)[:10]

        print(f"  인기 연속 쌍 활용: {[f'{p[0]}-{p[1]}' for p, _ in top_pairs[:5]]}")

        combinations_list = []
        max_attempts = 10000
        attempts = 0

        top_numbers = self.model.get_top_numbers(30)

        while len(combinations_list) < n_combinations and attempts < max_attempts:
            # 인기 연속 쌍 중 하나 선택
            pair = random.choice(top_pairs)[0]
            selected = list(pair)

            # 나머지 4개 선택
            remaining = [n for n in top_numbers if n not in selected]
            if len(remaining) >= 4:
                selected.extend(random.sample(remaining, 4))

            if len(selected) == 6 and self._is_valid_combination(selected):
                sorted_selected = tuple(sorted(selected))
                if sorted_selected not in combinations_list:
                    combinations_list.append(sorted_selected)

            attempts += 1

        results = [list(combo) for combo in combinations_list[:n_combinations]]

        for i, combo in enumerate(results, 1):
            # 연속 쌍 찾기
            consecutive = []
            sorted_combo = sorted(combo)
            for j in range(len(sorted_combo)-1):
                if sorted_combo[j+1] == sorted_combo[j] + 1:
                    consecutive.append(f"{sorted_combo[j]}-{sorted_combo[j+1]}")

            print(f"  {i}. {combo} [연속: {', '.join(consecutive)}]")

        return results

    def generate_random(self, n_combinations=5, seed=None):
        """무작위 추천 (대조군)"""
        print(f"\n🎰 무작위 추천")

        # 시드 설정 (고정 모드)
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        combinations_list = []

        while len(combinations_list) < n_combinations:
            selected = random.sample(range(1, 46), 6)
            sorted_selected = tuple(sorted(selected))
            if sorted_selected not in combinations_list:
                combinations_list.append(sorted_selected)

        results = [list(combo) for combo in combinations_list]

        for i, combo in enumerate(results, 1):
            print(f"  {i}. {combo}")

        return results

    def generate_all_strategies(self, n_per_strategy=3, seed=None):
        """모든 전략으로 번호 생성"""
        print("\n" + "="*70)
        print("🎯 로또 645 번호 추천 시스템")
        print("="*70)

        results = {
            'hybrid': self.generate_hybrid(n_per_strategy, seed=seed),
            'score': self.generate_by_score(n_per_strategy, seed=seed),
            'probability': self.generate_by_probability(n_per_strategy, seed=seed),
            'pattern': self.generate_by_pattern(n_per_strategy, seed=seed),
            'grid': self.generate_grid_based(n_per_strategy, seed=seed),
            'image': self.generate_image_based(n_per_strategy, seed=seed),  # NEW
            'consecutive': self.generate_with_consecutive(n_per_strategy, seed=seed),
            'random': self.generate_random(n_per_strategy, seed=seed)
        }

        print("\n" + "="*70)
        print("✅ 추천 완료")
        print("="*70)

        return results


def main():
    """테스트용 메인 함수"""
    from data_loader import LottoDataLoader
    from prediction_model import LottoPredictionModel

    data_path = "../Data/645_251227.csv"

    print("데이터 로딩 및 모델 학습 중...")
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()

    model = LottoPredictionModel(loader)
    model.train_all_patterns()

    # 추천 시스템 실행
    recommender = LottoRecommendationSystem(model)
    recommendations = recommender.generate_all_strategies(n_per_strategy=3)

    print("\n\n📋 추천 요약:")
    print("="*70)
    for strategy, combos in recommendations.items():
        print(f"\n[{strategy.upper()}]")
        for i, combo in enumerate(combos, 1):
            print(f"  {i}. {combo}")


if __name__ == "__main__":
    main()
