"""
시각화 모듈
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter
import platform

# 한글 폰트 설정 (크로스 플랫폼)
system = platform.system()
if system == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
elif system == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:  # Linux
    plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지


class LottoVisualization:
    """로또 데이터 시각화 클래스"""

    def __init__(self, data_loader, output_dir='output/charts'):
        """
        Args:
            data_loader: LottoDataLoader 인스턴스
            output_dir: 차트 저장 디렉토리
        """
        self.loader = data_loader
        self.df = data_loader.df
        self.numbers_df = data_loader.numbers_df
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # 스타일 설정
        sns.set_style("whitegrid")
        sns.set_palette("husl")

    def plot_number_frequency(self, include_bonus=False):
        """번호별 출현 빈도 막대 그래프"""
        print("📊 번호별 출현 빈도 차트 생성 중...")

        all_numbers = self.loader.get_all_numbers_flat(include_bonus=include_bonus)
        frequency = Counter(all_numbers)

        # 모든 번호 1-45 초기화
        all_45_numbers = {i: 0 for i in range(1, 46)}
        all_45_numbers.update(frequency)

        numbers = sorted(all_45_numbers.keys())
        counts = [all_45_numbers[n] for n in numbers]

        # 그래프 생성
        fig, ax = plt.subplots(figsize=(16, 6))

        bars = ax.bar(numbers, counts, color='steelblue', alpha=0.8, edgecolor='black')

        # 평균선 추가
        avg_count = np.mean(counts)
        ax.axhline(y=avg_count, color='red', linestyle='--', linewidth=2, label=f'평균: {avg_count:.1f}')

        # 최다/최소 출현 번호 강조
        max_count = max(counts)
        min_count = min(counts)

        for i, (num, count) in enumerate(zip(numbers, counts)):
            if count == max_count:
                bars[i].set_color('darkgreen')
            elif count == min_count:
                bars[i].set_color('darkred')

        ax.set_xlabel('번호', fontsize=12, fontweight='bold')
        ax.set_ylabel('출현 횟수', fontsize=12, fontweight='bold')
        ax.set_title('로또 645 번호별 출현 빈도', fontsize=14, fontweight='bold')
        ax.set_xticks(numbers)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = self.output_dir / 'number_frequency.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_section_distribution(self):
        """구간별 출현 분포 파이 차트"""
        print("📊 구간별 분포 차트 생성 중...")

        all_numbers = self.loader.get_all_numbers_flat(include_bonus=False)

        low = len([n for n in all_numbers if 1 <= n <= 15])
        mid = len([n for n in all_numbers if 16 <= n <= 30])
        high = len([n for n in all_numbers if 31 <= n <= 45])

        labels = ['저구간 (1-15)', '중구간 (16-30)', '고구간 (31-45)']
        sizes = [low, mid, high]
        colors = ['#ff9999', '#66b3ff', '#99ff99']
        explode = (0.05, 0.05, 0.05)

        fig, ax = plt.subplots(figsize=(10, 8))

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=explode,
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(14)

        ax.set_title('구간별 번호 출현 분포', fontsize=14, fontweight='bold')

        plt.tight_layout()

        filename = self.output_dir / 'section_distribution.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_odd_even_distribution(self):
        """홀짝 분포 파이 차트"""
        print("📊 홀짝 분포 차트 생성 중...")

        all_numbers = self.loader.get_all_numbers_flat(include_bonus=False)

        odd = len([n for n in all_numbers if n % 2 == 1])
        even = len([n for n in all_numbers if n % 2 == 0])

        labels = ['홀수', '짝수']
        sizes = [odd, even]
        colors = ['#ff6b6b', '#4ecdc4']
        explode = (0.05, 0.05)

        fig, ax = plt.subplots(figsize=(10, 8))

        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            colors=colors,
            autopct='%1.1f%%',
            startangle=90,
            explode=explode,
            textprops={'fontsize': 12, 'fontweight': 'bold'}
        )

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(14)

        ax.set_title('홀수/짝수 출현 분포', fontsize=14, fontweight='bold')

        plt.tight_layout()

        filename = self.output_dir / 'odd_even_distribution.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_sum_distribution(self):
        """당첨번호 합계 분포 히스토그램"""
        print("📊 당첨번호 합계 분포 차트 생성 중...")

        sums = []
        for _, row in self.numbers_df.iterrows():
            total = sum(row['당첨번호'])
            sums.append(total)

        fig, ax = plt.subplots(figsize=(12, 6))

        n, bins, patches = ax.hist(sums, bins=30, color='skyblue', edgecolor='black', alpha=0.7)

        # 평균, 중앙값 선 추가
        mean_sum = np.mean(sums)
        median_sum = np.median(sums)

        ax.axvline(mean_sum, color='red', linestyle='--', linewidth=2, label=f'평균: {mean_sum:.1f}')
        ax.axvline(median_sum, color='green', linestyle='--', linewidth=2, label=f'중앙값: {median_sum:.1f}')

        ax.set_xlabel('당첨번호 합계', fontsize=12, fontweight='bold')
        ax.set_ylabel('회차 수', fontsize=12, fontweight='bold')
        ax.set_title('당첨번호 합계 분포', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = self.output_dir / 'sum_distribution.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_first_prize_trend(self):
        """1등 당첨금 추이 라인 차트"""
        print("📊 1등 당첨금 추이 차트 생성 중...")

        df_sorted = self.df.sort_values('회차')

        fig, ax = plt.subplots(figsize=(16, 6))

        ax.plot(df_sorted['회차'], df_sorted['1등 당첨액'] / 1e8,
                color='darkblue', linewidth=1.5, alpha=0.7)

        # 평균선
        avg_prize = df_sorted['1등 당첨액'].mean()
        ax.axhline(y=avg_prize / 1e8, color='red', linestyle='--',
                   linewidth=2, label=f'평균: {avg_prize/1e8:.1f}억원')

        ax.set_xlabel('회차', fontsize=12, fontweight='bold')
        ax.set_ylabel('1등 당첨금 (억원)', fontsize=12, fontweight='bold')
        ax.set_title('로또 645 1등 당첨금 추이', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = self.output_dir / 'first_prize_trend.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_heatmap(self):
        """번호 출현 히트맵 (시기별)"""
        print("📊 번호 출현 히트맵 생성 중...")

        # 최근 100회차를 10회차씩 나누어 분석
        recent_100 = self.numbers_df.head(100)

        heatmap_data = []

        for i in range(0, 100, 10):
            segment = recent_100.iloc[i:i+10]
            all_numbers = []

            for _, row in segment.iterrows():
                all_numbers.extend(row['당첨번호'])

            frequency = Counter(all_numbers)

            # 1-45 모든 번호 초기화
            row_data = [frequency.get(n, 0) for n in range(1, 46)]
            heatmap_data.append(row_data)

        # DataFrame으로 변환
        heatmap_df = pd.DataFrame(
            heatmap_data,
            columns=list(range(1, 46)),
            index=[f'{i+1}-{i+10}회' for i in range(0, 100, 10)]
        )

        fig, ax = plt.subplots(figsize=(20, 8))

        sns.heatmap(
            heatmap_df,
            cmap='YlOrRd',
            annot=True,
            fmt='d',
            cbar_kws={'label': '출현 횟수'},
            linewidths=0.5,
            ax=ax
        )

        ax.set_title('최근 100회차 번호 출현 히트맵 (10회차 단위)', fontsize=14, fontweight='bold')
        ax.set_xlabel('번호', fontsize=12, fontweight='bold')
        ax.set_ylabel('회차 구간', fontsize=12, fontweight='bold')

        plt.tight_layout()

        filename = self.output_dir / 'number_heatmap.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_hot_cold_comparison(self):
        """최근 50회/100회 핫넘버 콜드넘버 비교 차트"""
        print("📊 핫넘버/콜드넘버 비교 차트 생성 중...")

        from collections import Counter

        # 최근 50회
        recent_50 = self.numbers_df.head(50)
        numbers_50 = []
        for _, row in recent_50.iterrows():
            numbers_50.extend(row['당첨번호'])
        freq_50 = Counter(numbers_50)

        # 최근 100회
        recent_100 = self.numbers_df.head(100)
        numbers_100 = []
        for _, row in recent_100.iterrows():
            numbers_100.extend(row['당첨번호'])
        freq_100 = Counter(numbers_100)

        # 전체 기간
        all_numbers = self.loader.get_all_numbers_flat(include_bonus=False)
        freq_all = Counter(all_numbers)

        # 1-45번 모든 번호 초기화
        all_45 = list(range(1, 46))

        freq_50_list = [freq_50.get(n, 0) for n in all_45]
        freq_100_list = [freq_100.get(n, 0) for n in all_45]
        freq_all_list = [freq_all.get(n, 0) for n in all_45]

        # 그래프 생성 (3개의 서브플롯)
        fig, axes = plt.subplots(3, 1, figsize=(16, 12))

        # 최근 50회
        axes[0].bar(all_45, freq_50_list, color='coral', alpha=0.8, edgecolor='black')
        axes[0].axhline(y=np.mean(freq_50_list), color='red', linestyle='--', linewidth=2, label=f'평균: {np.mean(freq_50_list):.1f}')
        axes[0].set_title('최근 50회차 번호 출현 빈도', fontsize=12, fontweight='bold')
        axes[0].set_ylabel('출현 횟수', fontsize=10)
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # 최근 100회
        axes[1].bar(all_45, freq_100_list, color='skyblue', alpha=0.8, edgecolor='black')
        axes[1].axhline(y=np.mean(freq_100_list), color='red', linestyle='--', linewidth=2, label=f'평균: {np.mean(freq_100_list):.1f}')
        axes[1].set_title('최근 100회차 번호 출현 빈도', fontsize=12, fontweight='bold')
        axes[1].set_ylabel('출현 횟수', fontsize=10)
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        # 전체 기간
        axes[2].bar(all_45, freq_all_list, color='lightgreen', alpha=0.8, edgecolor='black')
        axes[2].axhline(y=np.mean(freq_all_list), color='red', linestyle='--', linewidth=2, label=f'평균: {np.mean(freq_all_list):.1f}')
        axes[2].set_title('전체 기간 번호 출현 빈도', fontsize=12, fontweight='bold')
        axes[2].set_xlabel('번호', fontsize=10)
        axes[2].set_ylabel('출현 횟수', fontsize=10)
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)

        plt.tight_layout()

        filename = self.output_dir / 'hot_cold_comparison.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_number_interval(self):
        """번호별 평균 출현 간격 차트"""
        print("📊 번호별 평균 출현 간격 차트 생성 중...")

        # 각 번호의 평균 출현 간격 계산
        avg_intervals = {}

        for num in range(1, 46):
            appearance_rounds = []
            for idx, row in self.numbers_df.iterrows():
                if num in row['당첨번호']:
                    appearance_rounds.append(row['회차'])

            if len(appearance_rounds) > 1:
                intervals = []
                for i in range(len(appearance_rounds) - 1):
                    intervals.append(appearance_rounds[i] - appearance_rounds[i+1])
                avg_intervals[num] = np.mean(intervals)
            else:
                avg_intervals[num] = 0

        numbers = sorted(avg_intervals.keys())
        intervals = [avg_intervals[n] for n in numbers]

        fig, ax = plt.subplots(figsize=(16, 6))

        bars = ax.bar(numbers, intervals, color='teal', alpha=0.7, edgecolor='black')

        # 전체 평균선
        avg_interval = np.mean([v for v in intervals if v > 0])
        ax.axhline(y=avg_interval, color='red', linestyle='--', linewidth=2, label=f'평균 간격: {avg_interval:.1f}회')

        ax.set_xlabel('번호', fontsize=12, fontweight='bold')
        ax.set_ylabel('평균 출현 간격 (회차)', fontsize=12, fontweight='bold')
        ax.set_title('번호별 평균 출현 간격', fontsize=14, fontweight='bold')
        ax.set_xticks(numbers)
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = self.output_dir / 'number_interval.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_missing_periods(self):
        """미출현 기간 차트"""
        print("📊 미출현 기간 차트 생성 중...")

        current_round = self.numbers_df.iloc[0]['회차']
        missing_periods = {}

        for num in range(1, 46):
            last_appearance = None
            for idx, row in self.numbers_df.iterrows():
                if num in row['당첨번호']:
                    last_appearance = row['회차']
                    break

            if last_appearance:
                missing_periods[num] = int(current_round - last_appearance)
            else:
                missing_periods[num] = int(current_round)

        # 정렬
        sorted_periods = sorted(missing_periods.items(), key=lambda x: x[1], reverse=True)

        numbers = [x[0] for x in sorted_periods]
        periods = [x[1] for x in sorted_periods]

        fig, ax = plt.subplots(figsize=(16, 8))

        colors = ['darkred' if p > 20 else 'orange' if p > 10 else 'skyblue' for p in periods]
        bars = ax.bar(range(45), periods, color=colors, alpha=0.8, edgecolor='black')

        ax.set_xlabel('번호', fontsize=12, fontweight='bold')
        ax.set_ylabel('미출현 기간 (회차)', fontsize=12, fontweight='bold')
        ax.set_title('번호별 미출현 기간 (최근 출현 이후 경과 회차)', fontsize=14, fontweight='bold')
        ax.set_xticks(range(45))
        ax.set_xticklabels(numbers, rotation=0, fontsize=8)
        ax.grid(True, alpha=0.3, axis='y')

        # 범례 추가
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='darkred', alpha=0.8, label='20회 이상'),
            Patch(facecolor='orange', alpha=0.8, label='10-20회'),
            Patch(facecolor='skyblue', alpha=0.8, label='10회 미만')
        ]
        ax.legend(handles=legend_elements)

        plt.tight_layout()

        filename = self.output_dir / 'missing_periods.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_pair_correlation_heatmap(self):
        """번호 쌍 동반 출현 히트맵"""
        print("📊 번호 쌍 동반 출현 히트맵 생성 중...")

        # 동반 출현 매트릭스 생성
        co_occurrence = np.zeros((45, 45))

        for _, row in self.numbers_df.iterrows():
            nums = row['당첨번호']
            for i, n1 in enumerate(nums):
                for j, n2 in enumerate(nums):
                    if i < j:  # 중복 방지
                        co_occurrence[n1-1][n2-1] += 1
                        co_occurrence[n2-1][n1-1] += 1

        fig, ax = plt.subplots(figsize=(18, 16))

        sns.heatmap(
            co_occurrence,
            cmap='YlOrRd',
            cbar_kws={'label': '동반 출현 횟수'},
            linewidths=0,
            ax=ax,
            square=True
        )

        ax.set_title('번호 간 동반 출현 히트맵', fontsize=14, fontweight='bold')
        ax.set_xlabel('번호', fontsize=12, fontweight='bold')
        ax.set_ylabel('번호', fontsize=12, fontweight='bold')

        # 축 레이블 설정
        ax.set_xticks(np.arange(0.5, 45.5, 5))
        ax.set_yticks(np.arange(0.5, 45.5, 5))
        ax.set_xticklabels(range(1, 46, 5))
        ax.set_yticklabels(range(1, 46, 5))

        plt.tight_layout()

        filename = self.output_dir / 'pair_correlation_heatmap.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_prize_vs_winners(self):
        """당첨금과 당첨자 수의 관계 산점도"""
        print("📊 당첨금-당첨자 수 관계 차트 생성 중...")

        fig, ax = plt.subplots(figsize=(12, 8))

        # 산점도
        ax.scatter(
            self.df['1등 당첨자수'],
            self.df['1등 당첨액'] / 1e8,  # 억 단위
            alpha=0.6,
            s=50,
            c='steelblue',
            edgecolors='black',
            linewidth=0.5
        )

        # 추세선 추가
        z = np.polyfit(self.df['1등 당첨자수'], self.df['1등 당첨액'] / 1e8, 1)
        p = np.poly1d(z)
        ax.plot(
            sorted(self.df['1등 당첨자수']),
            p(sorted(self.df['1등 당첨자수'])),
            "r--",
            linewidth=2,
            label='추세선'
        )

        # 상관계수 표시
        corr = self.df['1등 당첨액'].corr(self.df['1등 당첨자수'])
        ax.text(
            0.05, 0.95,
            f'상관계수: {corr:.3f}',
            transform=ax.transAxes,
            fontsize=12,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        )

        ax.set_xlabel('1등 당첨자 수 (명)', fontsize=12, fontweight='bold')
        ax.set_ylabel('1등 당첨금 (억원)', fontsize=12, fontweight='bold')
        ax.set_title('1등 당첨자 수와 당첨금의 관계', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)

        plt.tight_layout()

        filename = self.output_dir / 'prize_vs_winners.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_yearly_prize_boxplot(self):
        """연도별 당첨금 박스플롯"""
        print("📊 연도별 당첨금 분포 차트 생성 중...")

        df_copy = self.df.copy()
        df_copy['연도'] = df_copy['일자'].dt.year
        df_copy['당첨금_억'] = df_copy['1등 당첨액'] / 1e8

        fig, ax = plt.subplots(figsize=(14, 8))

        # 박스플롯
        years = sorted(df_copy['연도'].unique())
        data_by_year = [df_copy[df_copy['연도'] == year]['당첨금_억'].values for year in years]

        bp = ax.boxplot(
            data_by_year,
            labels=years,
            patch_artist=True,
            notch=True,
            showmeans=True
        )

        # 박스 색상 설정
        colors = plt.cm.viridis(np.linspace(0, 1, len(years)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(0.7)

        ax.set_xlabel('연도', fontsize=12, fontweight='bold')
        ax.set_ylabel('1등 당첨금 (억원)', fontsize=12, fontweight='bold')
        ax.set_title('연도별 1등 당첨금 분포', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        filename = self.output_dir / 'yearly_prize_boxplot.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_all(self):
        """모든 시각화 차트 생성"""
        print("\n\n" + "🎨 "*20)
        print("시각화 시작")
        print("🎨 "*20 + "\n")

        # 기본 통계 차트
        self.plot_number_frequency(include_bonus=False)
        self.plot_section_distribution()
        self.plot_odd_even_distribution()
        self.plot_sum_distribution()
        self.plot_heatmap()

        # 시계열 분석 차트
        self.plot_hot_cold_comparison()
        self.plot_number_interval()
        self.plot_missing_periods()

        # 조합 패턴 분석 차트
        self.plot_pair_correlation_heatmap()

        # 당첨금 분석 차트
        self.plot_first_prize_trend()
        self.plot_prize_vs_winners()
        self.plot_yearly_prize_boxplot()

        print("\n\n" + "✅ "*20)
        print("시각화 완료")
        print("✅ "*20 + "\n")

        print(f"모든 차트가 '{self.output_dir}' 디렉토리에 저장되었습니다.")
