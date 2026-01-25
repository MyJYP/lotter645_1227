"""
연속 번호 상세 분석 모듈
"""
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import platform

# 한글 폰트 설정 (크로스 플랫폼)
system = platform.system()
if system == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
elif system == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
else:  # Linux
    plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False


class ConsecutiveNumberAnalysis:
    """연속 번호 분석 클래스"""

    def __init__(self, data_loader):
        """
        Args:
            data_loader: LottoDataLoader 인스턴스
        """
        self.loader = data_loader
        self.df = data_loader.df
        self.numbers_df = data_loader.numbers_df
        self.output_dir = Path('output/charts')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def find_consecutive_groups(self, numbers):
        """당첨번호에서 연속 번호 그룹 찾기"""
        sorted_nums = sorted(numbers)
        groups = []
        current_group = [sorted_nums[0]]

        for i in range(1, len(sorted_nums)):
            if sorted_nums[i] == sorted_nums[i-1] + 1:
                current_group.append(sorted_nums[i])
            else:
                if len(current_group) >= 2:
                    groups.append(current_group[:])
                current_group = [sorted_nums[i]]

        # 마지막 그룹 처리
        if len(current_group) >= 2:
            groups.append(current_group)

        return groups

    def analyze_consecutive_patterns(self):
        """연속 번호 패턴 상세 분석"""
        print("\n" + "="*70)
        print("연속 번호 패턴 상세 분석")
        print("="*70)

        consecutive_data = []

        # 연속 번호 길이별 카운트
        length_counter = Counter()

        # 구체적인 연속 번호 조합 카운트
        specific_combos = defaultdict(int)

        for idx, row in self.numbers_df.iterrows():
            round_num = row['회차']
            date = row['일자']
            nums = row['당첨번호']

            groups = self.find_consecutive_groups(nums)

            if groups:
                for group in groups:
                    length = len(group)
                    length_counter[length] += 1

                    # 구체적인 조합 저장
                    combo_str = '-'.join(map(str, group))
                    specific_combos[combo_str] += 1

                    consecutive_data.append({
                        '회차': round_num,
                        '일자': date,
                        '연속길이': length,
                        '연속번호': combo_str,
                        '전체번호': nums
                    })
            else:
                consecutive_data.append({
                    '회차': round_num,
                    '일자': date,
                    '연속길이': 0,
                    '연속번호': '없음',
                    '전체번호': nums
                })

        self.consecutive_df = pd.DataFrame(consecutive_data)

        # 결과 출력
        print("\n1. 연속 번호 길이별 출현 빈도:")
        print("="*70)

        total_rounds = len(self.numbers_df)

        print(f"\n총 회차 수: {total_rounds}회\n")

        # 연속 없음
        no_consecutive = len(self.consecutive_df[self.consecutive_df['연속길이'] == 0])
        print(f"연속 번호 없음: {no_consecutive}회 ({no_consecutive/total_rounds*100:.2f}%)")

        # 연속 길이별
        for length in sorted([k for k in length_counter.keys() if k >= 2]):
            count = length_counter[length]
            print(f"연속 {length}개: {count}회 ({count/total_rounds*100:.2f}%)")

        # 가장 많이 나온 연속 번호 조합
        print("\n\n2. 가장 많이 나온 연속 번호 조합 TOP 20:")
        print("="*70)

        sorted_combos = sorted(specific_combos.items(), key=lambda x: x[1], reverse=True)[:20]

        combo_df = pd.DataFrame(sorted_combos, columns=['연속번호', '출현횟수'])
        combo_df['출현율(%)'] = (combo_df['출현횟수'] / total_rounds * 100).round(2)

        print("\n" + combo_df.to_string(index=False))

        # 연속 길이별 조합
        print("\n\n3. 연속 길이별 상위 조합:")
        print("="*70)

        for length in [2, 3, 4, 5, 6]:
            length_combos = {k: v for k, v in specific_combos.items() if len(k.split('-')) == length}

            if length_combos:
                print(f"\n▶ 연속 {length}개:")
                sorted_length = sorted(length_combos.items(), key=lambda x: x[1], reverse=True)[:10]

                for combo, count in sorted_length:
                    print(f"  {combo}: {count}회 ({count/total_rounds*100:.2f}%)")

        return length_counter, specific_combos

    def analyze_patterns_by_section(self):
        """구간별 연속 번호 패턴 분석"""
        print("\n\n4. 구간별 연속 번호 출현 패턴:")
        print("="*70)

        section_patterns = {
            '저구간 (1-15)': [],
            '중구간 (16-30)': [],
            '고구간 (31-45)': []
        }

        for idx, row in self.numbers_df.iterrows():
            nums = row['당첨번호']
            groups = self.find_consecutive_groups(nums)

            for group in groups:
                if all(1 <= n <= 15 for n in group):
                    section_patterns['저구간 (1-15)'].append('-'.join(map(str, group)))
                elif all(16 <= n <= 30 for n in group):
                    section_patterns['중구간 (16-30)'].append('-'.join(map(str, group)))
                elif all(31 <= n <= 45 for n in group):
                    section_patterns['고구간 (31-45)'].append('-'.join(map(str, group)))

        for section, combos in section_patterns.items():
            print(f"\n{section}:")
            if combos:
                counter = Counter(combos)
                top_5 = counter.most_common(5)
                for combo, count in top_5:
                    print(f"  {combo}: {count}회")
            else:
                print("  없음")

    def find_interesting_cases(self):
        """특이 케이스 찾기"""
        print("\n\n5. 특이 케이스:")
        print("="*70)

        # 연속 4개 이상
        long_consecutive = self.consecutive_df[self.consecutive_df['연속길이'] >= 4]

        if len(long_consecutive) > 0:
            print(f"\n▶ 연속 4개 이상 출현 회차 ({len(long_consecutive)}회):")
            for idx, row in long_consecutive.iterrows():
                print(f"  {int(row['회차'])}회차 ({row['일자'].strftime('%Y.%m.%d')}): {row['연속번호']} (전체: {row['전체번호']})")
        else:
            print("\n▶ 연속 4개 이상: 없음")

        # 여러 개의 연속 그룹이 있는 경우
        print("\n▶ 여러 연속 그룹이 동시 출현한 회차:")

        multi_group_count = 0
        for idx, row in self.numbers_df.iterrows():
            groups = self.find_consecutive_groups(row['당첨번호'])
            if len(groups) >= 2:
                multi_group_count += 1
                if multi_group_count <= 10:  # 상위 10개만 출력
                    group_strs = ['-'.join(map(str, g)) for g in groups]
                    print(f"  {int(row['회차'])}회차: {', '.join(group_strs)} (전체: {row['당첨번호']})")

        print(f"\n  총 {multi_group_count}회 발생")

    def plot_consecutive_distribution(self, length_counter):
        """연속 번호 길이별 분포 차트"""
        print("\n📊 연속 번호 길이별 분포 차트 생성 중...")

        # 데이터 준비
        total_rounds = len(self.numbers_df)
        no_consecutive = len(self.consecutive_df[self.consecutive_df['연속길이'] == 0])

        lengths = ['없음'] + [f'{i}개' for i in sorted([k for k in length_counter.keys() if k >= 2])]
        counts = [no_consecutive] + [length_counter[i] for i in sorted([k for k in length_counter.keys() if k >= 2])]
        percentages = [c / total_rounds * 100 for c in counts]

        # 그래프 생성
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # 막대 그래프
        colors = ['lightgray'] + plt.cm.viridis(np.linspace(0, 1, len(lengths)-1)).tolist()
        bars = ax1.bar(lengths, counts, color=colors, alpha=0.8, edgecolor='black')

        ax1.set_xlabel('연속 번호 길이', fontsize=12, fontweight='bold')
        ax1.set_ylabel('출현 횟수', fontsize=12, fontweight='bold')
        ax1.set_title('연속 번호 길이별 출현 빈도', fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3, axis='y')

        # 막대 위에 숫자 표시
        for bar, count, pct in zip(bars, counts, percentages):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{count}\n({pct:.1f}%)',
                    ha='center', va='bottom', fontsize=10)

        # 파이 차트
        ax2.pie(counts, labels=lengths, autopct='%1.1f%%', startangle=90,
                colors=colors, textprops={'fontsize': 11, 'fontweight': 'bold'})
        ax2.set_title('연속 번호 길이별 비율', fontsize=14, fontweight='bold')

        plt.tight_layout()

        filename = self.output_dir / 'consecutive_distribution.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_consecutive_trend(self):
        """연속 번호 출현 추이 차트"""
        print("📊 연속 번호 출현 추이 차트 생성 중...")

        # 최근 200회차 데이터
        recent_data = self.consecutive_df.head(200).copy()
        recent_data = recent_data.sort_values('회차')

        fig, ax = plt.subplots(figsize=(16, 6))

        # 연속 길이별 색상
        colors = {0: 'lightgray', 2: 'skyblue', 3: 'orange', 4: 'red', 5: 'purple', 6: 'darkred'}

        for idx, row in recent_data.iterrows():
            length = row['연속길이']
            color = colors.get(length, 'black')
            ax.scatter(row['회차'], length, c=color, s=50, alpha=0.7, edgecolors='black', linewidth=0.5)

        ax.set_xlabel('회차', fontsize=12, fontweight='bold')
        ax.set_ylabel('연속 번호 개수', fontsize=12, fontweight='bold')
        ax.set_title('최근 200회차 연속 번호 출현 추이', fontsize=14, fontweight='bold')
        ax.set_yticks(range(0, 7))
        ax.set_yticklabels(['없음', '1개', '2개', '3개', '4개', '5개', '6개'])
        ax.grid(True, alpha=0.3)

        # 범례
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='lightgray', label='연속 없음'),
            Patch(facecolor='skyblue', label='연속 2개'),
            Patch(facecolor='orange', label='연속 3개'),
            Patch(facecolor='red', label='연속 4개'),
            Patch(facecolor='purple', label='연속 5개'),
            Patch(facecolor='darkred', label='연속 6개')
        ]
        ax.legend(handles=legend_elements, loc='upper right')

        plt.tight_layout()

        filename = self.output_dir / 'consecutive_trend.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def plot_top_consecutive_combos(self, specific_combos):
        """가장 많이 나온 연속 조합 차트"""
        print("📊 연속 번호 조합 TOP 20 차트 생성 중...")

        sorted_combos = sorted(specific_combos.items(), key=lambda x: x[1], reverse=True)[:20]

        combos = [c[0] for c in sorted_combos]
        counts = [c[1] for c in sorted_combos]

        fig, ax = plt.subplots(figsize=(14, 8))

        bars = ax.barh(range(len(combos)), counts, color='steelblue', alpha=0.8, edgecolor='black')

        ax.set_yticks(range(len(combos)))
        ax.set_yticklabels(combos, fontsize=10)
        ax.set_xlabel('출현 횟수', fontsize=12, fontweight='bold')
        ax.set_ylabel('연속 번호 조합', fontsize=12, fontweight='bold')
        ax.set_title('가장 많이 나온 연속 번호 조합 TOP 20', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')

        # 막대 끝에 숫자 표시
        for i, (bar, count) in enumerate(zip(bars, counts)):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2.,
                   f' {count}회',
                   ha='left', va='center', fontsize=9)

        plt.tight_layout()

        filename = self.output_dir / 'consecutive_top_combos.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

        print(f"✓ 저장 완료: {filename}")

    def run_all(self):
        """모든 연속 번호 분석 실행"""
        print("\n\n" + "🔢 "*20)
        print("연속 번호 상세 분석 시작")
        print("🔢 "*20)

        length_counter, specific_combos = self.analyze_consecutive_patterns()
        self.analyze_patterns_by_section()
        self.find_interesting_cases()

        # 시각화
        self.plot_consecutive_distribution(length_counter)
        self.plot_consecutive_trend()
        self.plot_top_consecutive_combos(specific_combos)

        print("\n\n" + "✅ "*20)
        print("연속 번호 분석 완료")
        print("✅ "*20 + "\n")


def main():
    """메인 실행"""
    from data_loader import LottoDataLoader

    data_path = "../Data/645_251227.csv"

    print("데이터 로딩 중...")
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()

    # 연속 번호 분석 실행
    analysis = ConsecutiveNumberAnalysis(loader)
    analysis.run_all()


if __name__ == "__main__":
    main()
