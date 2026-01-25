"""
로또 645 당첨 결과 텍스트 파싱 모듈
동행복권 사이트에서 복사한 텍스트를 자동으로 파싱하여 데이터 추출
"""
import re


class LottoTextParser:
    """로또 당첨 결과 텍스트 파싱 클래스"""

    def __init__(self):
        pass

    def extract_round(self, text):
        """
        회차 번호 추출
        예: "제 1205회 추첨 결과" → 1205
        """
        pattern = r"제\s*(\d+)\s*회"
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
        return None

    def extract_date(self, text):
        """
        추첨 날짜 추출
        예: "2026.01.03 추첨" → "2026.01.03"
        """
        pattern = r"(\d{4}\.\d{2}\.\d{2})\s*추첨"
        match = re.search(pattern, text)
        if match:
            return match.group(1)
        return None

    def extract_winning_numbers(self, text):
        """
        당첨번호 6개 추출

        텍스트에서 "당첨번호" 다음에 나오는 숫자 6개를 추출
        """
        # 방법 1: 당첨번호 섹션에서 1~45 범위의 숫자 6개 찾기
        pattern = r"당첨번호\s*((?:\d+\s*){6})"
        match = re.search(pattern, text)

        if match:
            numbers_text = match.group(1)
            numbers = [int(n) for n in re.findall(r'\d+', numbers_text)]
            # 1~45 범위의 숫자만 필터링
            numbers = [n for n in numbers if 1 <= n <= 45]
            if len(numbers) >= 6:
                return sorted(numbers[:6])

        # 방법 2: 보너스번호 앞의 숫자들 (더 정확)
        # "8\n16\n28\n30\n31\n44\n+\n보너스번호" 패턴
        pattern2 = r"당첨번호\s*(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*\+?\s*보너스"
        match2 = re.search(pattern2, text, re.DOTALL)

        if match2:
            numbers = [int(match2.group(i)) for i in range(1, 7)]
            return sorted(numbers)

        return None

    def extract_bonus(self, text):
        """
        보너스 번호 추출
        예: "보너스번호\n2" → 2
        """
        # 보너스번호 다음의 숫자
        pattern = r"보너스번호\s*(\d+)"
        match = re.search(pattern, text)
        if match:
            bonus = int(match.group(1))
            if 1 <= bonus <= 45:
                return bonus
        return None

    def extract_prize_winners(self, text, rank):
        """
        특정 등수의 당첨자 수 추출

        Args:
            text: 전체 텍스트
            rank: 등수 (1~5)

        Returns:
            int: 당첨자 수
        """
        # "1등\n32,263,862,630원\n10\n" 패턴
        # 또는 "1등 ... 10 3,226,386,263원" 패턴

        # 패턴: {rank}등 다음에 나오는 숫자들 중에서 당첨자 수 찾기
        # 보통 당첨금보다 작은 숫자

        pattern = rf"{rank}등[^\d]*(\d{{1,3}}(?:,\d{{3}})*원)[^\d]*(\d{{1,3}}(?:,\d{{3}})*)"
        match = re.search(pattern, text)

        if match:
            # 두 번째 그룹이 당첨자 수 (쉼표 제거)
            winners_str = match.group(2).replace(',', '')
            return int(winners_str)

        # 대안 패턴: 표 형식
        # "당첨게임 수" 컬럼에서 찾기
        pattern2 = rf"{rank}등.*?당첨게임\s+수[^\d]*(\d{{1,3}}(?:,\d{{3}})*)"
        match2 = re.search(pattern2, text, re.DOTALL)

        if match2:
            winners_str = match2.group(1).replace(',', '')
            return int(winners_str)

        return 0

    def extract_total_prize(self, text, rank):
        """
        특정 등수의 총 당첨금 추출

        Args:
            text: 전체 텍스트
            rank: 등수 (1~5)

        Returns:
            int: 총 당첨금 (원 단위)
        """
        # "1등\n32,263,862,630원" 패턴
        pattern = rf"{rank}등[^\d]*(\d{{1,3}}(?:,\d{{3}})+)원"
        match = re.search(pattern, text)

        if match:
            prize_str = match.group(1).replace(',', '')
            return int(prize_str)

        # 대안: "등위별 총 당첨금" 컬럼
        pattern2 = rf"{rank}등.*?등위별\s+총\s+당첨금[^\d]*(\d{{1,3}}(?:,\d{{3}})+)원"
        match2 = re.search(pattern2, text, re.DOTALL)

        if match2:
            prize_str = match2.group(1).replace(',', '')
            return int(prize_str)

        return 0

    def parse(self, text):
        """
        전체 텍스트 파싱하여 딕셔너리 반환

        Args:
            text: 동행복권 사이트에서 복사한 텍스트

        Returns:
            dict: 파싱된 데이터
            {
                '회차': 1205,
                '일자': '2026.01.03',
                '당첨번호': [1, 4, 16, 23, 31, 41],
                '보너스번호': 2,
                '1등 당첨자수': 10,
                '1등 당첨액': 32263862630,
                ...
            }
        """
        result = {}

        # 회차 추출
        round_num = self.extract_round(text)
        if round_num:
            result['회차'] = round_num

        # 날짜 추출
        date = self.extract_date(text)
        if date:
            result['일자'] = date

        # 당첨번호 추출
        numbers = self.extract_winning_numbers(text)
        if numbers:
            result['당첨번호'] = numbers

        # 보너스 번호 추출
        bonus = self.extract_bonus(text)
        if bonus:
            result['보너스번호'] = bonus

        # 1~5등 당첨자 수 및 당첨금 추출
        for rank in range(1, 6):
            winners = self.extract_prize_winners(text, rank)
            prize = self.extract_total_prize(text, rank)

            result[f'{rank}등 당첨자수'] = winners
            result[f'{rank}등 당첨액'] = prize

        return result

    def validate_parsed_data(self, data):
        """
        파싱된 데이터 검증

        Returns:
            tuple: (is_valid, error_messages)
        """
        errors = []

        # 필수 필드 확인
        required_fields = ['회차', '일자', '당첨번호', '보너스번호']
        for field in required_fields:
            if field not in data or data[field] is None:
                errors.append(f"❌ {field} 정보를 찾을 수 없습니다")

        # 당첨번호 개수 확인
        if '당첨번호' in data and data['당첨번호']:
            if len(data['당첨번호']) != 6:
                errors.append(f"❌ 당첨번호가 {len(data['당첨번호'])}개입니다 (6개 필요)")

        # 보너스 번호 범위 확인
        if '보너스번호' in data and data['보너스번호']:
            if not (1 <= data['보너스번호'] <= 45):
                errors.append(f"❌ 보너스 번호 범위 오류: {data['보너스번호']}")

        # 당첨번호와 보너스 중복 확인
        if '당첨번호' in data and '보너스번호' in data:
            if data['보너스번호'] in data['당첨번호']:
                errors.append("❌ 보너스 번호가 당첨번호와 중복됩니다")

        return len(errors) == 0, errors


def main():
    """테스트용 메인 함수"""

    # 테스트 텍스트 (사용자 제공)
    test_text = """제 1205회 추첨 결과
2026.01.03 추첨
당첨번호
1
4
16
23
31
41
+
보너스번호
2
당첨번호
보너스번호
순위
등위별 총 당첨금
당첨게임 수
1게임당 당첨금
당첨기준
비고
1등
32,263,862,630원
10
3,226,386,263원
6개번호 일치
2등
5,377,310,527원
97
55,436,191원
5개번호 일치 + 보너스번호 일치
3등
5,377,311,870원
3,486
1,542,545원
5개번호 일치
4등
8,737,000,000원
174,740
50,000원
4개번호 일치
5등
14,579,890,000원
2,915,978
5,000원
3개번호 일치"""

    parser = LottoTextParser()

    print("="*60)
    print("🧪 로또 텍스트 파싱 테스트")
    print("="*60)

    result = parser.parse(test_text)

    print("\n📋 파싱 결과:")
    print("-"*60)
    for key, value in result.items():
        if '당첨액' in key:
            print(f"{key}: {value:,}원")
        else:
            print(f"{key}: {value}")

    print("\n✅ 검증:")
    is_valid, errors = parser.validate_parsed_data(result)
    if is_valid:
        print("✓ 모든 데이터가 정상입니다")
    else:
        print("검증 오류:")
        for error in errors:
            print(f"  {error}")


if __name__ == "__main__":
    main()
