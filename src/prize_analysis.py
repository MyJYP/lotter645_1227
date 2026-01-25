"""
당첨금 분석 모듈
"""
import pandas as pd
import numpy as np


class PrizeAnalysis:
    """당첨금 분석 클래스"""

    def __init__(self, data_loader):
        """
        Args:
            data_loader: LottoDataLoader 인스턴스
        """
        self.loader = data_loader
        self.df = data_loader.df
        self.numbers_df = data_loader.numbers_df

    def first_prize_stats(self):
        """1등 당첨금 통계"""
        print("\n" + "="*60)
        print("1. 1등 당첨금 통계")
        print("="*60)

        first_prize = self.df['1등 당첨액']

        stats = {
            '평균 당첨금': f"{int(first_prize.mean()):,}원",
            '중앙값': f"{int(first_prize.median()):,}원",
            '최소 당첨금': f"{int(first_prize.min()):,}원",
            '최대 당첨금': f"{int(first_prize.max()):,}원",
            '표준편차': f"{int(first_prize.std()):,}원"
        }

        stats_df = pd.DataFrame([stats])
        print("\n" + stats_df.to_string(index=False))

        # 최고 당첨금 회차
        max_idx = first_prize.idxmax()
        max_round = self.df.loc[max_idx]

        print(f"\n\n최고 당첨금 회차:")
        print(f"  회차: {int(max_round['회차'])}회")
        print(f"  날짜: {max_round['일자'].strftime('%Y.%m.%d')}")
        print(f"  당첨금: {int(max_round['1등 당첨액']):,}원")
        print(f"  당첨자 수: {int(max_round['1등 당첨자수'])}명")

        return stats_df

    def prize_by_year(self):
        """연도별 1등 당첨금 추이"""
        print("\n" + "="*60)
        print("2. 연도별 1등 당첨금 추이")
        print("="*60)

        df_copy = self.df.copy()
        df_copy['연도'] = df_copy['일자'].dt.year

        yearly_stats = df_copy.groupby('연도').agg({
            '1등 당첨액': ['mean', 'max', 'min', 'count']
        }).round(0)

        yearly_stats.columns = ['평균', '최대', '최소', '회차수']

        # 정수로 변환하고 천단위 구분
        for col in ['평균', '최대', '최소']:
            yearly_stats[col] = yearly_stats[col].astype(int)

        yearly_stats['회차수'] = yearly_stats['회차수'].astype(int)

        print("\n" + yearly_stats.to_string())

        return yearly_stats

    def winner_count_analysis(self):
        """1등 당첨자 수 분석"""
        print("\n" + "="*60)
        print("3. 1등 당첨자 수 분석")
        print("="*60)

        winner_counts = self.df['1등 당첨자수']

        stats = {
            '평균 당첨자': f"{winner_counts.mean():.1f}명",
            '중앙값': f"{int(winner_counts.median())}명",
            '최소': f"{int(winner_counts.min())}명",
            '최대': f"{int(winner_counts.max())}명"
        }

        stats_df = pd.DataFrame([stats])
        print("\n" + stats_df.to_string(index=False))

        # 당첨자 수 분포
        print("\n\n당첨자 수 구간별 분포:")
        bins = [0, 5, 10, 15, 20, 30, 100]
        labels = ['1-5명', '6-10명', '11-15명', '16-20명', '21-30명', '31명 이상']

        winner_bins = pd.cut(winner_counts, bins=bins, labels=labels)
        winner_dist = winner_bins.value_counts().sort_index()

        dist_df = pd.DataFrame({
            '당첨자수구간': winner_dist.index,
            '회차수': winner_dist.values,
            '비율(%)': (winner_dist.values / len(winner_counts) * 100).round(2)
        })

        print(dist_df.to_string(index=False))

        return stats_df, dist_df

    def prize_vs_winners_correlation(self):
        """당첨금과 당첨자 수의 관계"""
        print("\n" + "="*60)
        print("4. 당첨금과 당첨자 수의 상관관계")
        print("="*60)

        correlation = self.df['1등 당첨액'].corr(self.df['1등 당첨자수'])

        print(f"\n상관계수: {correlation:.4f}")

        if correlation < -0.7:
            print("해석: 강한 음의 상관관계 (당첨자가 많을수록 당첨금 감소)")
        elif correlation < -0.3:
            print("해석: 중간 정도의 음의 상관관계")
        elif correlation < 0.3:
            print("해석: 약한 상관관계")
        elif correlation < 0.7:
            print("해석: 중간 정도의 양의 상관관계")
        else:
            print("해석: 강한 양의 상관관계")

        # 당첨자 수별 평균 당첨금
        print("\n\n당첨자 수 구간별 평균 당첨금:")

        df_copy = self.df.copy()
        bins = [0, 5, 10, 15, 20, 30, 100]
        labels = ['1-5명', '6-10명', '11-15명', '16-20명', '21-30명', '31명 이상']

        df_copy['당첨자구간'] = pd.cut(df_copy['1등 당첨자수'], bins=bins, labels=labels)

        avg_prize_by_winners = df_copy.groupby('당첨자구간')['1등 당첨액'].mean().round(0)

        result_df = pd.DataFrame({
            '당첨자구간': avg_prize_by_winners.index,
            '평균당첨금': [f"{int(v):,}원" for v in avg_prize_by_winners.values]
        })

        print(result_df.to_string(index=False))

        return correlation, result_df

    def total_sales_estimation(self):
        """총 판매액 추정 (1등 당첨금 기반)"""
        print("\n" + "="*60)
        print("5. 총 판매액 및 환원율 추정")
        print("="*60)
        print("※ 1등 총 당첨금 = 판매액 × 50% × 75% (대략)")
        print("   (전체 당첨금의 50%, 그 중 1등 배분율 75% 가정)\n")

        # 1등 총 당첨금
        self.df['1등총당첨금'] = self.df['1등 당첨액'] * self.df['1등 당첨자수']

        # 판매액 추정 (역산)
        estimated_multiplier = 1 / (0.5 * 0.75)
        self.df['추정판매액'] = self.df['1등총당첨금'] * estimated_multiplier

        recent_10 = self.df.head(10)

        print("최근 10회차 추정 판매액:")
        display_df = recent_10[['회차', '일자', '1등총당첨금', '추정판매액']].copy()
        display_df['일자'] = display_df['일자'].dt.strftime('%Y.%m.%d')
        display_df['1등총당첨금'] = display_df['1등총당첨금'].apply(lambda x: f"{int(x):,}원")
        display_df['추정판매액'] = display_df['추정판매액'].apply(lambda x: f"{int(x):,}원")

        print("\n" + display_df.to_string(index=False))

        avg_sales = self.df['추정판매액'].mean()
        print(f"\n\n전체 평균 추정 판매액: {int(avg_sales):,}원")

        return display_df

    def run_all(self):
        """모든 당첨금 분석 실행"""
        print("\n\n" + "💰 "*20)
        print("당첨금 분석 시작")
        print("💰 "*20 + "\n")

        first_stats = self.first_prize_stats()
        yearly = self.prize_by_year()
        winner_stats, winner_dist = self.winner_count_analysis()
        correlation, corr_df = self.prize_vs_winners_correlation()
        sales = self.total_sales_estimation()

        print("\n\n" + "✅ "*20)
        print("당첨금 분석 완료")
        print("✅ "*20 + "\n")

        return {
            'first_prize_stats': first_stats,
            'yearly_stats': yearly,
            'winner_stats': winner_stats,
            'winner_distribution': winner_dist,
            'correlation': correlation,
            'correlation_df': corr_df,
            'sales_estimation': sales
        }
