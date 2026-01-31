"""
로또 645 데이터 자동 업데이트 모듈
- 웹 크롤링을 통한 자동 업데이트
- 수동 입력 데이터 검증 및 업데이트
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pathlib import Path
from datetime import datetime
import re


class DataUpdater:
    """로또 데이터 업데이트 클래스"""

    def __init__(self, csv_path):
        """
        Args:
            csv_path: CSV 파일 경로
        """
        self.csv_path = Path(csv_path)
        self.base_url = "https://www.dhlottery.co.kr/gameResult.do?method=byWin"

    def get_current_latest_round(self):
        """현재 CSV 파일의 최신 회차 반환"""
        try:
            df = pd.read_csv(self.csv_path, encoding='utf-8-sig', skiprows=1)
            latest_round = int(df['회차'].max())
            return latest_round
        except Exception as e:
            print(f"CSV 파일 읽기 오류: {e}")
            return None

    def fetch_latest_draw_from_web(self, round_num=None):
        """
        웹에서 최신 회차 데이터 수집

        Args:
            round_num: 특정 회차 번호 (None이면 최신 회차)

        Returns:
            dict: 수집된 데이터 또는 None (실패 시)
        """
        try:
            # URL 구성
            if round_num:
                url = f"{self.base_url}&drwNo={round_num}"
            else:
                url = self.base_url

            # HTTP 요청
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()

            # HTML 파싱
            soup = BeautifulSoup(response.text, 'lxml')

            # 데이터 추출 (실제 HTML 구조에 맞게 수정 필요)
            draw_data = self._parse_draw_page(soup)

            return draw_data

        except requests.exceptions.RequestException as e:
            print(f"웹 요청 오류: {e}")
            return None
        except Exception as e:
            print(f"파싱 오류: {e}")
            return None

    def _parse_draw_page(self, soup):
        """
        HTML에서 당첨 정보 파싱 (동행복권 데스크탑 사이트 기준)
        """
        try:
            # 회차 추출
            # <div class="win_result"><h4><strong>1000회</strong> 당첨결과</h4>...</div>
            round_element = soup.select_one('div.win_result h4 strong')
            if not round_element:
                return None
            round_text = round_element.text
            round_num = int(re.search(r'(\d+)', round_text).group(1))

            # 날짜 추출
            # <p class="desc">(2022년 01월 29일 추첨)</p>
            date_element = soup.select_one('div.win_result p.desc')
            date_text = date_element.text
            date_match = re.search(r'(\d{4})년\s*(\d{1,2})월\s*(\d{1,2})일', date_text)
            if date_match:
                date_str = f"{date_match.group(1)}.{date_match.group(2).zfill(2)}.{date_match.group(3).zfill(2)}"
            else:
                date_str = datetime.now().strftime('%Y.%m.%d')

            # 당첨번호 추출
            # <div class="num win"> ... <span class="ball_645 lrg ball1">2</span> ... </div>
            numbers = []
            number_spans = soup.select('div.num.win p span.ball_645')
            for span in number_spans:
                numbers.append(int(span.text))

            # 보너스 번호
            # <div class="num bonus"> ... <span class="ball_645 lrg ball2">19</span> ... </div>
            bonus_span = soup.select_one('div.num.bonus p span.ball_645')
            bonus = int(bonus_span.text)

            # 당첨금 정보 (1~5등)
            prize_data = {}
            try:
                # 테이블 파싱: <table class="tbl_data">
                table = soup.select_one('table.tbl_data')
                if table:
                    rows = table.select('tbody tr')
                    for i, row in enumerate(rows):
                        if i >= 5: break # 1~5등까지만
                        cols = row.select('td')
                        # cols[0]: 등위(텍스트), cols[1]: 총당첨금, cols[2]: 당첨자수, cols[3]: 1인당 당첨금
                        if len(cols) >= 4:
                            winners = int(re.sub(r'[^\d]', '', cols[2].text))
                            amount = int(re.sub(r'[^\d]', '', cols[3].text)) # 1인당 당첨금 사용
                            prize_data[f'{i+1}등 당첨자수'] = winners
                            prize_data[f'{i+1}등 당첨액'] = amount
            except Exception as e:
                print(f"당첨금 파싱 오류 (기본값 사용): {e}")
                for rank in range(1, 6):
                    prize_data[f'{rank}등 당첨자수'] = 0
                    prize_data[f'{rank}등 당첨액'] = 0

            return {
                '회차': round_num,
                '일자': date_str,
                '당첨번호': numbers,
                '보너스번호': bonus,
                **prize_data
            }

        except Exception as e:
            print(f"파싱 상세 오류: {e}")
            return None

    def validate_draw_data(self, data):
        """
        수집/입력된 데이터 검증

        Args:
            data: dict 형태의 회차 데이터

        Returns:
            tuple: (is_valid, error_message)
        """
        # 1. 필수 필드 확인
        required_fields = ['회차', '일자', '당첨번호', '보너스번호']
        for field in required_fields:
            if field not in data or data[field] is None:
                return False, f"필수 필드 누락: {field}"

        # 2. 회차 번호 유효성
        round_num = data['회차']
        if not isinstance(round_num, int) or round_num < 1:
            return False, f"잘못된 회차 번호: {round_num}"

        # 3. 당첨번호 검증
        numbers = data['당첨번호']

        # 개수 확인
        if len(numbers) != 6:
            return False, f"당첨번호는 6개여야 합니다 (현재: {len(numbers)}개)"

        # 범위 확인
        for num in numbers:
            if not (1 <= num <= 45):
                return False, f"번호 범위 오류: {num} (1-45 범위)"

        # 중복 확인
        if len(set(numbers)) != 6:
            return False, "당첨번호에 중복이 있습니다"

        # 4. 보너스 번호 검증
        bonus = data['보너스번호']
        if not (1 <= bonus <= 45):
            return False, f"보너스 번호 범위 오류: {bonus} (1-45 범위)"

        if bonus in numbers:
            return False, "보너스 번호가 당첨번호와 중복됩니다"

        # 5. 당첨금 검증 (있는 경우)
        for rank in range(1, 6):
            prize_key = f'{rank}등 당첨액'
            if prize_key in data:
                prize = data[prize_key]
                if prize is not None and prize < 0:
                    return False, f"{prize_key}이(가) 음수입니다"

        return True, ""

    def create_backup(self):
        """CSV 파일 백업 생성"""
        if not self.csv_path.exists():
            return None

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir = self.csv_path.parent / 'backups'
        backup_dir.mkdir(exist_ok=True)

        backup_path = backup_dir / f"{self.csv_path.stem}_backup_{timestamp}.csv"

        import shutil
        shutil.copy2(self.csv_path, backup_path)

        return backup_path

    def update_csv_with_new_draw(self, draw_data):
        """
        CSV 파일에 신규 회차 추가

        Args:
            draw_data: dict 형태의 회차 데이터

        Returns:
            tuple: (success, message)
        """
        try:
            # 1. 데이터 검증
            is_valid, error_msg = self.validate_draw_data(draw_data)
            if not is_valid:
                return False, f"데이터 검증 실패: {error_msg}"

            # 2. 현재 CSV 로드
            df_existing = pd.read_csv(self.csv_path, encoding='utf-8-sig', skiprows=1)

            # 3. 중복 회차 확인
            if draw_data['회차'] in df_existing['회차'].values:
                return False, f"{draw_data['회차']}회는 이미 존재합니다"

            # 4. 백업 생성
            backup_path = self.create_backup()

            # 5. 새 행 데이터 생성
            new_row = {
                'year': int(str(draw_data['일자'])[:4]) if isinstance(draw_data['일자'], str) else datetime.now().year,
                '회차': draw_data['회차'],
                '일자': draw_data['일자'],
                '1등 당첨자수': draw_data.get('1등 당첨자수', 0),
                '1등 당첨액': draw_data.get('1등 당첨액', 0),
                '2등 당첨자수': draw_data.get('2등 당첨자수', 0),
                '2등 당첨액': draw_data.get('2등 당첨액', 0),
                '3등 당첨자수': draw_data.get('3등 당첨자수', 0),
                '3등 당첨액': draw_data.get('3등 당첨액', 0),
                '4등 당첨자수': draw_data.get('4등 당첨자수', 0),
                '4등 당첨액': draw_data.get('4등 당첨액', 0),
                '5등 당첨자수': draw_data.get('5등 당첨자수', 0),
                '5등 당첨액': draw_data.get('5등 당첨액', 0),
                '당첨번호#1': draw_data['당첨번호'][0],
                '당첨번호#2': draw_data['당첨번호'][1],
                '당첨번호#3': draw_data['당첨번호'][2],
                '당첨번호#4': draw_data['당첨번호'][3],
                '당첨번호#5': draw_data['당첨번호'][4],
                '당첨번호#6': draw_data['당첨번호'][5],
                '당첨번호#7': draw_data['보너스번호']
            }

            # 6. 데이터프레임에 추가
            df_new = pd.DataFrame([new_row])
            df_updated = pd.concat([df_new, df_existing], ignore_index=True)

            # 7. 회차 기준 내림차순 정렬 (최신이 위로)
            df_updated = df_updated.sort_values('회차', ascending=False)

            # 8. CSV 저장
            # 첫 번째 행 헤더 유지
            with open(self.csv_path, 'w', encoding='utf-8-sig') as f:
                f.write("회차,당첨번호,,,,,,,,,,,,,,,,,,,\n")
                df_updated.to_csv(f, index=False, header=True)

            message = f"✓ {draw_data['회차']}회 데이터가 추가되었습니다"
            if backup_path:
                message += f"\n백업: {backup_path.name}"

            return True, message

        except Exception as e:
            return False, f"CSV 업데이트 실패: {str(e)}"


def main():
    """테스트용 메인 함수"""
    csv_path = "../Data/645_251227.csv"
    updater = DataUpdater(csv_path)

    # 현재 최신 회차 확인
    latest_round = updater.get_current_latest_round()
    print(f"현재 최신 회차: {latest_round}회")

    # 테스트: 수동 데이터 검증
    test_data = {
        '회차': 1205,
        '일자': '2026.01.03',
        '당첨번호': [1, 4, 16, 23, 31, 41],
        '보너스번호': 2,
        '1등 당첨자수': 10,
        '1등 당첨액': 32263862630,
        '2등 당첨자수': 97,
        '2등 당첨액': 5377310527,
        '3등 당첨자수': 3486,
        '3등 당첨액': 5377311870,
        '4등 당첨자수': 174740,
        '4등 당첨액': 8737000000,
        '5등 당첨자수': 2915978,
        '5등 당첨액': 14579890000
    }

    is_valid, msg = updater.validate_draw_data(test_data)
    print(f"\n데이터 검증: {is_valid}")
    if not is_valid:
        print(f"오류: {msg}")


if __name__ == "__main__":
    main()
