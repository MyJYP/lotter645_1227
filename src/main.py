"""
로또 645 데이터 분석 메인 실행 스크립트
"""
import sys
from pathlib import Path

# 모듈 import
from data_loader import LottoDataLoader
from basic_stats import BasicStats
from time_series import TimeSeriesAnalysis
from pattern_analysis import PatternAnalysis
from prize_analysis import PrizeAnalysis
from visualization import LottoVisualization


def print_banner():
    """배너 출력"""
    banner = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║            🎰  로또 645 데이터 종합 분석 시스템  🎰            ║
    ║                                                               ║
    ║              Lotto 645 Comprehensive Analysis                 ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_menu():
    """메뉴 출력"""
    menu = """
    ═══════════════════════════════════════════════════════════════
    분석 메뉴
    ═══════════════════════════════════════════════════════════════

    1. 전체 분석 실행 (기본 통계 + 시계열 + 패턴 + 당첨금 + 시각화)
    2. 기본 통계 분석만
    3. 시계열 분석만
    4. 조합 패턴 분석만
    5. 당첨금 분석만
    6. 시각화만
    7. 특정 번호 분석
    8. 종료

    ═══════════════════════════════════════════════════════════════
    """
    print(menu)


def run_full_analysis(loader):
    """전체 분석 실행"""
    print("\n" + "="*70)
    print("전체 분석을 시작합니다...")
    print("="*70)

    # 1. 기본 통계
    basic = BasicStats(loader)
    basic_results = basic.run_all()

    # 2. 시계열 분석
    timeseries = TimeSeriesAnalysis(loader)
    ts_results = timeseries.run_all()

    # 3. 패턴 분석
    pattern = PatternAnalysis(loader)
    pattern_results = pattern.run_all()

    # 4. 당첨금 분석
    prize = PrizeAnalysis(loader)
    prize_results = prize.run_all()

    # 5. 시각화
    viz = LottoVisualization(loader)
    viz.plot_all()

    print("\n\n" + "🎉 "*30)
    print("모든 분석이 완료되었습니다!")
    print("🎉 "*30)
    print("\n결과물:")
    print("  - 콘솔 출력: 각종 통계 및 분석 결과")
    print("  - output/charts/: 시각화 차트 이미지 파일들")


def run_basic_stats(loader):
    """기본 통계 분석만 실행"""
    basic = BasicStats(loader)
    basic.run_all()


def run_time_series(loader):
    """시계열 분석만 실행"""
    timeseries = TimeSeriesAnalysis(loader)
    timeseries.run_all()


def run_pattern_analysis(loader):
    """패턴 분석만 실행"""
    pattern = PatternAnalysis(loader)
    pattern.run_all()


def run_prize_analysis(loader):
    """당첨금 분석만 실행"""
    prize = PrizeAnalysis(loader)
    prize.run_all()


def run_visualization(loader):
    """시각화만 실행"""
    viz = LottoVisualization(loader)
    viz.plot_all()


def analyze_specific_number(loader):
    """특정 번호 상세 분석"""
    try:
        number = int(input("\n분석할 번호를 입력하세요 (1-45): "))

        if number < 1 or number > 45:
            print("❌ 1부터 45 사이의 번호를 입력해주세요.")
            return

        print(f"\n{'='*70}")
        print(f"번호 {number} 상세 분석")
        print(f"{'='*70}")

        # 시계열 분석에서 번호 출현 간격 분석
        timeseries = TimeSeriesAnalysis(loader)
        timeseries.number_appearance_interval(number)

        # 패턴 분석에서 동반 출현 번호 분석
        pattern = PatternAnalysis(loader)
        pattern.number_correlation(number, top_n=10)

    except ValueError:
        print("❌ 올바른 숫자를 입력해주세요.")
    except Exception as e:
        print(f"❌ 오류 발생: {e}")


def main():
    """메인 함수"""
    # 배너 출력
    print_banner()

    # 데이터 파일 경로
    data_path = Path(__file__).parent.parent / "Data" / "645_251227.csv"

    if not data_path.exists():
        print(f"❌ 데이터 파일을 찾을 수 없습니다: {data_path}")
        print("Data/645_251227.csv 파일이 존재하는지 확인해주세요.")
        sys.exit(1)

    # 데이터 로드
    print("\n📂 데이터를 로딩합니다...\n")
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()
    loader.get_summary()

    # 메뉴 루프
    while True:
        print_menu()

        try:
            choice = input("선택하세요 (1-8): ").strip()

            if choice == '1':
                run_full_analysis(loader)
            elif choice == '2':
                run_basic_stats(loader)
            elif choice == '3':
                run_time_series(loader)
            elif choice == '4':
                run_pattern_analysis(loader)
            elif choice == '5':
                run_prize_analysis(loader)
            elif choice == '6':
                run_visualization(loader)
            elif choice == '7':
                analyze_specific_number(loader)
            elif choice == '8':
                print("\n👋 프로그램을 종료합니다. 감사합니다!\n")
                break
            else:
                print("\n❌ 1부터 8 사이의 숫자를 입력해주세요.\n")

        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.\n")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}\n")

        input("\n\nEnter를 눌러 계속...")


if __name__ == "__main__":
    main()
