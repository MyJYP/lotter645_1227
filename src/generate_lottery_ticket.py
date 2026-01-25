"""
로또 복권 용지 이미지 생성 (당첨번호 마킹)
"""
from PIL import Image, ImageDraw, ImageFont
import os
import platform

def create_lottery_ticket(round_num, date, winning_numbers, output_path):
    """
    로또 복권 용지 이미지 생성

    Args:
        round_num: 회차 번호
        date: 날짜 (YYYYMMDD)
        winning_numbers: 당첨번호 리스트 [n1, n2, n3, n4, n5, n6]
        output_path: 저장 경로
    """
    # 이미지 크기 (복권 용지 비율)
    width = 400
    height = 900

    # 배경 흰색
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # 색상 정의
    header_color = '#E53935'  # 빨간색
    number_color = '#333333'  # 어두운 회색
    mark_color = '#1E88E5'    # 파란색
    grid_color = '#CCCCCC'    # 연한 회색

    # 헤더 그리기
    draw.rectangle([0, 0, width, 50], fill=header_color)

    try:
        # 폰트 로드 (크로스 플랫폼)
        system = platform.system()
        if system == 'Darwin':  # macOS
            font_path = "/System/Library/Fonts/Helvetica.ttc"
        elif system == 'Windows':
            font_path = "C:/Windows/Fonts/arial.ttf"
        else:  # Linux
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

        title_font = ImageFont.truetype(font_path, 24)
        header_font = ImageFont.truetype(font_path, 18)
        number_font = ImageFont.truetype(font_path, 14)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        number_font = ImageFont.load_default()

    # 헤더 텍스트
    draw.text((20, 15), "A", fill='white', font=title_font)
    draw.text((70, 18), f"{round_num}회", fill='white', font=header_font)

    # 게임 A 영역 (하나만)
    start_y = 70

    # 번호 그리드 (7x7 레이아웃, 1-45번 + 빈칸)
    rows = 7
    cols = 7
    cell_width = 50
    cell_height = 50
    start_x = 20

    number = 1
    for row in range(rows):
        for col in range(cols):
            if number > 45:
                break

            x = start_x + col * cell_width
            y = start_y + row * cell_height

            # 셀 테두리
            draw.rectangle(
                [x, y, x + cell_width, y + cell_height],
                outline=grid_color,
                width=1
            )

            # 번호 텍스트
            text = str(number)
            # 텍스트 중앙 정렬을 위한 계산
            bbox = draw.textbbox((0, 0), text, font=number_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x + (cell_width - text_width) // 2
            text_y = y + (cell_height - text_height) // 2

            # 당첨번호면 마킹
            if number in winning_numbers:
                # 채운 원
                circle_padding = 8
                draw.ellipse(
                    [x + circle_padding, y + circle_padding,
                     x + cell_width - circle_padding, y + cell_height - circle_padding],
                    fill=mark_color,
                    outline=mark_color,
                    width=2
                )
                # 흰색 텍스트
                draw.text((text_x, text_y), text, fill='white', font=number_font)
            else:
                # 일반 텍스트
                draw.text((text_x, text_y), text, fill=number_color, font=number_font)

            number += 1

    # 하단 정보
    info_y = start_y + rows * cell_height + 20
    draw.text((20, info_y), f"회차: {round_num}회", fill=number_color, font=number_font)
    draw.text((20, info_y + 25), f"날짜: {date[:4]}.{date[4:6]}.{date[6:]}",
              fill=number_color, font=number_font)
    draw.text((20, info_y + 50), f"당첨번호: {', '.join(map(str, sorted(winning_numbers)))}",
              fill=header_color, font=number_font)

    # 저장
    img.save(output_path, 'PNG', quality=95)
    print(f"✅ 이미지 생성: {output_path}")
    return output_path


def create_lottery_ticket_enhanced(round_num, date, winning_numbers, bonus_number, output_path):
    """
    향상된 로또 복권 용지 이미지 생성 (실제 용지와 유사)
    """
    # 이미지 크기
    width = 500
    height = 1000

    # 배경
    img = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(img)

    # 색상
    header_bg = '#D32F2F'
    mark_fill = '#1976D2'
    mark_outline = '#0D47A1'
    text_color = '#212121'
    grid_color = '#BDBDBD'

    try:
        # 폰트 로드 (크로스 플랫폼)
        system = platform.system()
        if system == 'Darwin':  # macOS
            font_path = "/System/Library/Fonts/Helvetica.ttc"
        elif system == 'Windows':
            font_path = "C:/Windows/Fonts/arial.ttf"
        else:  # Linux
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

        title_font = ImageFont.truetype(font_path, 28)
        header_font = ImageFont.truetype(font_path, 20)
        number_font = ImageFont.truetype(font_path, 16)
        small_font = ImageFont.truetype(font_path, 12)
    except:
        # Fallback to default font
        title_font = ImageFont.load_default()
        header_font = ImageFont.load_default()
        number_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    # 헤더
    draw.rectangle([0, 0, width, 60], fill=header_bg)
    draw.text((30, 18), "A", fill='white', font=title_font)
    draw.text((100, 20), f"{round_num}회", fill='white', font=header_font)

    # 안내 텍스트
    draw.text((20, 75), "아래 번호 중 6개를 선택하세요", fill=text_color, font=small_font)

    # 번호 그리드
    start_y = 110
    start_x = 30
    cell_size = 60
    cols = 7
    rows = 7

    number = 1
    for row in range(rows):
        for col in range(cols):
            if number > 45:
                break

            x = start_x + col * cell_size
            y = start_y + row * cell_size

            # 테두리
            draw.rectangle(
                [x, y, x + cell_size - 2, y + cell_size - 2],
                outline=grid_color,
                width=2
            )

            # 번호
            text = str(number)
            bbox = draw.textbbox((0, 0), text, font=number_font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_x = x + (cell_size - text_width) // 2
            text_y = y + (cell_size - text_height) // 2

            # 당첨번호 마킹
            if number in winning_numbers:
                # 채워진 원
                padding = 10
                draw.ellipse(
                    [x + padding, y + padding,
                     x + cell_size - padding - 2, y + cell_size - padding - 2],
                    fill=mark_fill,
                    outline=mark_outline,
                    width=3
                )
                draw.text((text_x, text_y), text, fill='white', font=number_font)
            else:
                draw.text((text_x, text_y), text, fill=text_color, font=number_font)

            number += 1

    # 하단 정보
    info_y = start_y + rows * cell_size + 30

    # 구분선
    draw.line([20, info_y - 10, width - 20, info_y - 10], fill=grid_color, width=2)

    # 회차 및 날짜
    draw.text((30, info_y), f"제 {round_num}회", fill=text_color, font=header_font)
    draw.text((30, info_y + 35), f"추첨일: {date[:4]}년 {date[4:6]}월 {date[6:]}일",
              fill=text_color, font=number_font)

    # 당첨번호 표시
    draw.text((30, info_y + 70), "당첨번호", fill=header_bg, font=header_font)

    winning_text = "  ".join(map(str, sorted(winning_numbers)))
    draw.text((30, info_y + 100), winning_text, fill=mark_fill, font=title_font)

    if bonus_number:
        draw.text((30, info_y + 140), f"보너스: {bonus_number}", fill=text_color, font=number_font)

    # 저장
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, 'PNG', quality=95, dpi=(300, 300))
    print(f"✅ 이미지 저장: {output_path}")
    return output_path


if __name__ == "__main__":
    # 1204회차 테스트
    round_num = 1204
    date = "20251227"
    winning_numbers = [8, 16, 28, 30, 31, 44]
    bonus_number = 27

    output_path = f"../images/{round_num}_{date}.png"

    create_lottery_ticket_enhanced(round_num, date, winning_numbers, bonus_number, output_path)

    print(f"\n📁 생성된 이미지: {output_path}")
