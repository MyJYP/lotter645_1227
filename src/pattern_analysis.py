"""
조합 패턴 분석 모듈
"""
import pandas as pd
import numpy as np
from collections import Counter
from itertools import combinations


class PatternAnalysis:
    """조합 패턴 분석 클래스"""

    def __init__(self, data_loader):
        """
        Args:
            data_loader: LottoDataLoader 인스턴스
        """
        self.loader = data_loader
        self.df = data_loader.df
        self.numbers_df = data_loader.numbers_df

    def pair_frequency(self, top_n=20):
        """2개 번호 조합 빈도 분석"""
        print("\n" + "="*60)
        print(f"1. 2개 번호 조합 빈도 TOP {top_n}")
        print("="*60)

        all_pairs = []

        for _, row in self.numbers_df.iterrows():
            nums = row['당첨번호']
            pairs = list(combinations(sorted(nums), 2))
            all_pairs.extend(pairs)

        pair_freq = Counter(all_pairs)
        top_pairs = pair_freq.most_common(top_n)

        pair_df = pd.DataFrame(
            [(f"{p[0]}, {p[1]}", count) for p, count in top_pairs],
            columns=['번호쌍', '출현횟수']
        )

        pair_df['출현율(%)'] = (pair_df['출현횟수'] / len(self.numbers_df) * 100).round(2)

        print("\n" + pair_df.to_string(index=False))

        return pair_df

    def triplet_frequency(self, top_n=15):
        """3개 번호 조합 빈도 분석"""
        print("\n" + "="*60)
        print(f"2. 3개 번호 조합 빈도 TOP {top_n}")
        print("="*60)

        all_triplets = []

        for _, row in self.numbers_df.iterrows():
            nums = row['당첨번호']
            triplets = list(combinations(sorted(nums), 3))
            all_triplets.extend(triplets)

        triplet_freq = Counter(all_triplets)
        top_triplets = triplet_freq.most_common(top_n)

        triplet_df = pd.DataFrame(
            [(f"{t[0]}, {t[1]}, {t[2]}", count) for t, count in top_triplets],
            columns=['번호조합', '출현횟수']
        )

        triplet_df['출현율(%)'] = (triplet_df['출현횟수'] / len(self.numbers_df) * 100).round(2)

        print("\n" + triplet_df.to_string(index=False))

        return triplet_df

    def number_correlation(self, target_number, top_n=10):
        """특정 번호와 자주 함께 나오는 번호 분석"""
        print("\n" + "="*60)
        print(f"3. 번호 {target_number}와 동반 출현 번호 TOP {top_n}")
        print("="*60)

        companion_numbers = []

        for _, row in self.numbers_df.iterrows():
            nums = row['당첨번호']
            if target_number in nums:
                companion_numbers.extend([n for n in nums if n != target_number])

        if not companion_numbers:
            print(f"\n번호 {target_number}의 출현 기록이 없습니다.")
            return None

        companion_freq = Counter(companion_numbers)
        top_companions = companion_freq.most_common(top_n)

        # 번호 target_number의 총 출현 횟수
        target_count = sum(1 for _, row in self.numbers_df.iterrows() if target_number in row['당첨번호'])

        companion_df = pd.DataFrame(
            top_companions,
            columns=['번호', '동반출현횟수']
        )

        companion_df['동반율(%)'] = (companion_df['동반출현횟수'] / target_count * 100).round(2)

        print(f"\n번호 {target_number} 총 출현: {target_count}회\n")
        print(companion_df.to_string(index=False))

        return companion_df

    def sum_distribution_detail(self):
        """당첨번호 합계의 상세 분포"""
        print("\n" + "="*60)
        print("4. 당첨번호 합계 상세 분포")
        print("="*60)

        sums = []
        for _, row in self.numbers_df.iterrows():
            total = sum(row['당첨번호'])
            sums.append(total)

        # 10 단위로 구간 나누기
        bins = list(range(20, 281, 10))
        sum_series = pd.Series(sums)
        sum_bins = pd.cut(sum_series, bins=bins)
        sum_dist = sum_bins.value_counts().sort_index()

        sum_dist_df = pd.DataFrame({
            '합계구간': [str(interval) for interval in sum_dist.index],
            '회차수': sum_dist.values,
            '비율(%)': (sum_dist.values / len(sums) * 100).round(2)
        })

        print("\n" + sum_dist_df.to_string(index=False))

        return sum_dist_df

    def ac_value_analysis(self):
        """AC값 (복잡도) 분석"""
        print("\n" + "="*60)
        print("5. AC값 (복잡도) 분석")
        print("="*60)
        print("AC값: 당첨번호 간의 차이값의 고유한 개수 - 5")
        print("AC값이 클수록 번호가 고르게 분포됨\n")

        ac_values = []

        for _, row in self.numbers_df.iterrows():
            nums = sorted(row['당첨번호'])

            # 모든 차이값 계산
            differences = set()
            for i in range(len(nums)):
                for j in range(i+1, len(nums)):
                    differences.add(abs(nums[i] - nums[j]))

            ac_value = len(differences) - 5
            ac_values.append(ac_value)

        ac_dist = Counter(ac_values)
        ac_df = pd.DataFrame(
            sorted(ac_dist.items()),
            columns=['AC값', '회차수']
        )

        ac_df['비율(%)'] = (ac_df['회차수'] / len(ac_values) * 100).round(2)

        print(ac_df.to_string(index=False))

        ac_stats = {
            '평균 AC값': round(np.mean(ac_values), 2),
            '최소 AC값': min(ac_values),
            '최대 AC값': max(ac_values),
            '표준편차': round(np.std(ac_values), 2)
        }

        print("\n\nAC값 통계:")
        stats_df = pd.DataFrame([ac_stats])
        print(stats_df.to_string(index=False))

        return ac_df, stats_df

    def section_pattern_analysis(self):
        """구간별 조합 패턴 분석"""
        print("\n" + "="*60)
        print("6. 구간별 조합 패턴 분석")
        print("="*60)
        print("저구간(1-15), 중구간(16-30), 고구간(31-45) 개수 조합\n")

        patterns = []

        for _, row in self.numbers_df.iterrows():
            nums = row['당첨번호']

            low = sum(1 for n in nums if 1 <= n <= 15)
            mid = sum(1 for n in nums if 16 <= n <= 30)
            high = sum(1 for n in nums if 31 <= n <= 45)

            pattern = f"{low}-{mid}-{high}"
            patterns.append(pattern)

        pattern_dist = Counter(patterns)
        pattern_df = pd.DataFrame(
            sorted(pattern_dist.items(), key=lambda x: x[1], reverse=True),
            columns=['패턴(저-중-고)', '회차수']
        )

        pattern_df['비율(%)'] = (pattern_df['회차수'] / len(patterns) * 100).round(2)

        print(pattern_df.head(15).to_string(index=False))

        return pattern_df

    def analyze_consecutive_sequences(self):
        """연속 번호 패턴 분석 (2연속, 3연속 등)"""
        print("\n" + "="*60)
        print("7. 연속 번호 패턴 분석")
        print("="*60)
        
        seq_counts = {2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
        total_rounds = len(self.numbers_df)
        
        for _, row in self.numbers_df.iterrows():
            nums = sorted(row['당첨번호'])
            # Find sequences
            current_seq = 1
            for i in range(len(nums)-1):
                if nums[i+1] == nums[i] + 1:
                    current_seq += 1
                else:
                    if current_seq >= 2:
                        if current_seq in seq_counts:
                            seq_counts[current_seq] += 1
                    current_seq = 1
            if current_seq >= 2:
                if current_seq in seq_counts:
                    seq_counts[current_seq] += 1
                
        # DataFrame creation
        seq_df = pd.DataFrame([
            {'연속길이': k, '출현횟수': v, '비율(%)': round(v/total_rounds*100, 2)}
            for k, v in seq_counts.items() if v > 0
        ])
        seq_df = seq_df.sort_values('연속길이')
        
        print(seq_df.to_string(index=False))
        return seq_df

    def analyze_compatibility(self):
        """궁합수(친한 번호) 및 상극수(안 친한 번호) 분석"""
        print("\n" + "="*60)
        print("8. 궁합수 및 상극수 분석")
        print("="*60)
        
        # Calculate all pair frequencies
        all_pairs = []
        for _, row in self.numbers_df.iterrows():
            nums = row['당첨번호']
            all_pairs.extend(list(combinations(sorted(nums), 2)))
            
        pair_counts = Counter(all_pairs)
        
        # Best pairs (Gung-hap)
        best_pairs = pair_counts.most_common(10)
        print("\n🔥 최고의 궁합수 (자주 같이 나오는 쌍):")
        for pair, count in best_pairs:
            print(f"  {pair}: {count}회")
            
        # Worst pairs (Sang-geuk) - Pairs that never appeared
        all_possible_pairs = set(combinations(range(1, 46), 2))
        appeared_pairs = set(pair_counts.keys())
        never_appeared = list(all_possible_pairs - appeared_pairs)
        
        print(f"\n❄️ 최악의 상극수 (한 번도 같이 안 나온 쌍): 총 {len(never_appeared)}개")
        if never_appeared:
            print(f"  예시: {never_appeared[:5]} ...")
            
        return pair_counts, never_appeared

    def analyze_prime_composite(self):
        """소수/합성수 비율 분석"""
        print("\n" + "="*60)
        print("9. 소수/합성수 비율 분석")
        print("="*60)
        
        # 1~45 사이의 소수
        primes = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43}
        
        prime_counts = []
        for _, row in self.numbers_df.iterrows():
            nums = row['당첨번호']
            count = sum(1 for n in nums if n in primes)
            prime_counts.append(count)
            
        dist = Counter(prime_counts)
        total = len(prime_counts)
        
        df = pd.DataFrame([
            {'소수개수': k, '합성수개수': 6-k, '출현횟수': v, '비율(%)': round(v/total*100, 2)}
            for k, v in sorted(dist.items())
        ])
        
        print(df.to_string(index=False))
        return df

    def run_all(self):
        """모든 패턴 분석 실행"""
        print("\n\n" + "🔍 "*20)
        print("조합 패턴 분석 시작")
        print("🔍 "*20 + "\n")

        pair_df = self.pair_frequency(top_n=20)
        triplet_df = self.triplet_frequency(top_n=15)
        sum_dist = self.sum_distribution_detail()
        ac_df, ac_stats = self.ac_value_analysis()
        section_pattern = self.section_pattern_analysis()
        consecutive_df = self.analyze_consecutive_sequences()
        pair_counts, never_appeared = self.analyze_compatibility()
        prime_df = self.analyze_prime_composite()

        print("\n\n" + "✅ "*20)
        print("조합 패턴 분석 완료")
        print("✅ "*20 + "\n")

        return {
            'pairs': pair_df,
            'triplets': triplet_df,
            'sum_distribution': sum_dist,
            'ac_distribution': ac_df,
            'ac_stats': ac_stats,
            'section_pattern': section_pattern,
            'consecutive_pattern': consecutive_df,
            'compatibility': {'pair_counts': pair_counts, 'never_appeared': never_appeared},
            'prime_pattern': prime_df
        }


if __name__ == "__main__":
    from data_loader import LottoDataLoader

    # 데이터 로드
    print("📊 데이터 로드 중...")
    data_path = "../Data/645_251227.csv"
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()

    # 패턴 분석 실행
    analyzer = PatternAnalysis(loader)
    analyzer.run_all()
