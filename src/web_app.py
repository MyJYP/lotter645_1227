"""
로또 645 데이터 분석 및 번호 추천 웹 애플리케이션
Streamlit 기반 인터랙티브 대시보드
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import sys
import os

# 모듈 import를 위한 경로 설정
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_loader import LottoDataLoader
from basic_stats import BasicStats
from time_series import TimeSeriesAnalysis
from pattern_analysis import PatternAnalysis
from prediction_model import LottoPredictionModel
from recommendation_system import LottoRecommendationSystem
from grid_pattern_analysis import GridPatternAnalysis
from image_pattern_analysis import ImagePatternAnalysis
from core_number_system import CoreNumberSystem
from text_lottery_ticket import create_lottery_ticket_compact, create_lottery_grid_simple


# 페이지 설정
st.set_page_config(
    page_title="로또 645 분석 & 추천",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 캐시 데이터 로딩
@st.cache_data
def load_lotto_data():
    """데이터 로드 및 캐싱"""
    data_path = "../Data/645_251227.csv"
    loader = LottoDataLoader(data_path)
    loader.load_data()
    loader.preprocess()
    loader.extract_numbers()
    return loader

@st.cache_resource
def load_prediction_model(_loader):
    """예측 모델 로드 및 학습 (캐싱)"""
    model = LottoPredictionModel(_loader)
    model.train_all_patterns()
    return model

@st.cache_resource
def load_recommender(_model, _version="v3.1"):
    """추천 시스템 로드 (캐싱) - v3.1: seed 파라미터 추가"""
    return LottoRecommendationSystem(_model)

@st.cache_resource
def load_core_system(_model, _recommender, _version="v1.0"):
    """코어 번호 시스템 로드 (캐싱)"""
    return CoreNumberSystem(_model, _recommender)


# 사이드바
def sidebar(loader):
    """사이드바 메뉴"""
    st.sidebar.title("🎰 로또 645")
    st.sidebar.markdown("---")

    menu = st.sidebar.radio(
        "메뉴 선택",
        ["🏠 홈", "📊 데이터 탐색", "🎯 번호 추천", "🔍 번호 분석", "🤖 예측 모델", "🎨 그리드 패턴", "🖼️ 이미지 패턴", "🎲 번호 테마"]
    )

    st.sidebar.markdown("---")

    # 동적으로 데이터 정보 가져오기
    min_round = int(loader.df['회차'].min())
    max_round = int(loader.df['회차'].max())
    total_rounds = len(loader.df)
    min_date = loader.df['일자'].iloc[-1]  # 가장 오래된 데이터 (마지막 행)
    max_date = loader.df['일자'].iloc[0]   # 가장 최근 데이터 (첫 행)

    st.sidebar.info(
        f"""
        **데이터 정보**
        - 기간: {min_round}회~{max_round}회
        - 회차: 총 {total_rounds}회
        - 날짜: {min_date} ~ {max_date}
        """
    )

    st.sidebar.markdown("---")
    st.sidebar.warning(
        """
        ⚠️ **주의사항**

        로또는 독립 시행이므로 과거 데이터가
        미래 결과를 보장하지 않습니다.

        본 서비스는 통계 분석 및
        교육 목적입니다.
        """
    )

    return menu


# 홈 페이지
def home_page(loader):
    """홈 페이지"""
    st.title("🎰 로또 645 데이터 분석 & 번호 추천 시스템")

    # 동적으로 데이터 범위 가져오기
    min_round = int(loader.df['회차'].min())
    max_round = int(loader.df['회차'].max())
    total_rounds = len(loader.df)
    min_date = loader.df['일자'].iloc[-1]  # 가장 오래된 데이터 (마지막 행)
    max_date = loader.df['일자'].iloc[0]   # 가장 최근 데이터 (첫 행)

    st.markdown(f"""
    ## 📋 프로젝트 개요

    로또 645의 **{min_round}회차부터 {max_round}회차까지 ({min_date} ~ {max_date})** 총 {total_rounds}회차의
    당첨 데이터를 분석하고, 머신러닝과 확률론적 접근을 통해 번호를 추천하는 시스템입니다.

    ### ✨ 주요 기능

    - **📊 데이터 탐색**: 기본 통계, 시계열 분석, 패턴 분석
    - **🎯 번호 추천**: 8가지 전략 기반 번호 추천
    - **🔍 번호 분석**: 특정 번호의 상세 분석
    - **🤖 예측 모델**: 머신러닝 기반 번호 점수 및 인사이트
    - **🎨 그리드 패턴**: 복권 용지 7x7 그리드 공간 분석
    - **🖼️ 이미지 패턴**: 복권 용지 이미지 시각적 패턴 분석
    - **🎲 번호 테마**: 코어 번호, 고정 번호, 신뢰도 점수 ⭐ NEW

    ### 🎯 추천 전략 (8가지)

    1. **하이브리드 추천** ⭐ - 5가지 전략을 결합한 최고 품질
    2. **점수 기반 추천** - 번호별 종합 점수로 선정
    3. **확률 가중치 추천** - 통계적 확률 기반 샘플링
    4. **패턴 기반 추천** - 빈출 패턴 활용
    5. **그리드 패턴 추천** - 7x7 그리드 공간 분석
    6. **이미지 패턴 추천** - 복권 용지 시각적 밀도/균형 ⭐ NEW
    7. **연속 번호 추천** - 연속 번호 포함 (56% 확률)
    8. **무작위 추천** - 순수 랜덤 (대조군)

    ### 🎲 번호 테마 (3가지 특별 추천) ⭐ NEW

    1. **⭐ 코어 번호**: 가장 확신하는 핵심 3-4개 추출
       - 신뢰도 85% 이상 최상위 번호
       - 코어 포함 조합 생성
       - 과거 매칭 분석 제공

    2. **🔒 고정 번호**: 사용자 선택 + 최적 조합
       - 개인 선호 번호 고정 (1-5개)
       - 보완 번호 자동 추천
       - 동반 출현 빈도 기반

    3. **📊 신뢰도 점수**: 전체 번호(1-45) 신뢰도 확인
       - S등급 (90%+), A등급 (80%+), B등급 (70%+), C등급
       - 종합 점수 기반 정규화
       - 순위 및 등급 제공
    """)

    # 데이터 요약
    st.markdown("---")
    st.subheader("📈 데이터 요약")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("총 회차", f"{len(loader.df):,}회")

    with col2:
        avg_prize = loader.df['1등 당첨액'].mean()
        st.metric("평균 1등 당첨금", f"{avg_prize/100000000:.1f}억원")

    with col3:
        all_numbers = loader.get_all_numbers_flat(include_bonus=False)
        most_common = Counter(all_numbers).most_common(1)[0]
        st.metric("최다 출현 번호", f"{most_common[0]}번 ({most_common[1]}회)")

    with col4:
        latest_round = loader.df['회차'].iloc[0]
        st.metric("최신 회차", f"{latest_round}회")

    # 최근 당첨번호
    st.markdown("---")
    st.subheader("🎲 최근 당첨번호 (최근 10회)")

    recent_df = loader.numbers_df.head(10)[['회차', '일자', '당첨번호', '보너스번호']].copy()
    recent_df['당첨번호'] = recent_df['당첨번호'].apply(lambda x: ', '.join(map(str, sorted(x))))
    recent_df = recent_df.rename(columns={'보너스번호': '보너스'})

    st.dataframe(recent_df, use_container_width=True, hide_index=True)


# 데이터 탐색 페이지
def data_exploration_page(loader):
    """데이터 탐색 페이지"""
    st.title("📊 데이터 탐색")

    tab1, tab2, tab3 = st.tabs(["기본 통계", "시계열 분석", "패턴 분석"])

    with tab1:
        st.subheader("📈 번호별 출현 빈도")

        all_numbers = loader.get_all_numbers_flat(include_bonus=False)
        frequency = Counter(all_numbers)

        freq_df = pd.DataFrame([
            {'번호': num, '출현횟수': frequency.get(num, 0),
             '출현율(%)': frequency.get(num, 0) / len(loader.df) * 100}
            for num in range(1, 46)
        ])

        # Plotly 차트
        fig = px.bar(freq_df, x='번호', y='출현횟수',
                     title='번호별 출현 빈도',
                     color='출현횟수',
                     color_continuous_scale='Blues')
        fig.add_hline(y=freq_df['출현횟수'].mean(),
                      line_dash="dash",
                      annotation_text="평균",
                      line_color="red")
        st.plotly_chart(fig, use_container_width=True)

        # 구간별 분석
        st.subheader("📊 구간별 분포")

        low = sum(1 for n in all_numbers if 1 <= n <= 15)
        mid = sum(1 for n in all_numbers if 16 <= n <= 30)
        high = sum(1 for n in all_numbers if 31 <= n <= 45)

        section_df = pd.DataFrame({
            '구간': ['저구간(1-15)', '중구간(16-30)', '고구간(31-45)'],
            '출현횟수': [low, mid, high],
            '비율(%)': [low/(low+mid+high)*100, mid/(low+mid+high)*100, high/(low+mid+high)*100]
        })

        fig = px.pie(section_df, values='출현횟수', names='구간',
                     title='구간별 분포',
                     color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1'])
        st.plotly_chart(fig, use_container_width=True)

        # 홀짝 분석
        st.subheader("🔢 홀수/짝수 분포")

        odd = sum(1 for n in all_numbers if n % 2 == 1)
        even = len(all_numbers) - odd

        odd_even_df = pd.DataFrame({
            '구분': ['홀수', '짝수'],
            '출현횟수': [odd, even],
            '비율(%)': [odd/(odd+even)*100, even/(odd+even)*100]
        })

        fig = px.pie(odd_even_df, values='출현횟수', names='구분',
                     title='홀수/짝수 분포',
                     color_discrete_sequence=['#F38181', '#95E1D3'])
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("📈 최근 트렌드 분석")

        # 최근 50회 핫넘버
        recent_50_numbers = []
        for _, row in loader.numbers_df.head(50).iterrows():
            recent_50_numbers.extend(row['당첨번호'])

        recent_freq = Counter(recent_50_numbers)
        hot_numbers = recent_freq.most_common(10)
        cold_numbers = sorted(recent_freq.items(), key=lambda x: x[1])[:10]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 🔥 핫넘버 TOP 10 (최근 50회)")
            hot_df = pd.DataFrame(hot_numbers, columns=['번호', '출현횟수'])
            hot_df['출현율(%)'] = (hot_df['출현횟수'] / 50 * 100).round(1)
            st.dataframe(hot_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("##### ❄️ 콜드넘버 TOP 10 (최근 50회)")
            cold_df = pd.DataFrame(cold_numbers, columns=['번호', '출현횟수'])
            cold_df['출현율(%)'] = (cold_df['출현횟수'] / 50 * 100).round(1)
            st.dataframe(cold_df, use_container_width=True, hide_index=True)

        # 미출현 기간
        st.subheader("⏱️ 번호별 미출현 기간")

        absence_data = []
        for num in range(1, 46):
            for idx, row in loader.numbers_df.iterrows():
                if num in row['당첨번호']:
                    absence_data.append({'번호': num, '미출현 기간': idx})
                    break
            else:
                absence_data.append({'번호': num, '미출현 기간': len(loader.numbers_df)})

        absence_df = pd.DataFrame(absence_data)
        absence_df = absence_df.sort_values('미출현 기간', ascending=False).head(15)

        fig = px.bar(absence_df, x='번호', y='미출현 기간',
                     title='장기 미출현 번호 TOP 15',
                     color='미출현 기간',
                     color_continuous_scale='Reds')
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("🔄 연속 번호 패턴")

        consecutive_stats = {'none': 0, 'pair': 0, 'triple': 0, 'quad': 0}

        for _, row in loader.numbers_df.iterrows():
            nums = sorted(row['당첨번호'])
            max_consecutive = 0
            current_consecutive = 1

            for i in range(len(nums)-1):
                if nums[i+1] == nums[i] + 1:
                    current_consecutive += 1
                    max_consecutive = max(max_consecutive, current_consecutive)
                else:
                    current_consecutive = 1

            if max_consecutive == 0:
                consecutive_stats['none'] += 1
            elif max_consecutive == 2:
                consecutive_stats['pair'] += 1
            elif max_consecutive == 3:
                consecutive_stats['triple'] += 1
            elif max_consecutive >= 4:
                consecutive_stats['quad'] += 1

        cons_df = pd.DataFrame({
            '패턴': ['연속 없음', '연속 2개', '연속 3개', '연속 4개 이상'],
            '출현횟수': [consecutive_stats['none'], consecutive_stats['pair'],
                         consecutive_stats['triple'], consecutive_stats['quad']],
        })
        cons_df['비율(%)'] = (cons_df['출현횟수'] / len(loader.df) * 100).round(2)

        fig = px.bar(cons_df, x='패턴', y='출현횟수',
                     title='연속 번호 패턴 분포',
                     color='출현횟수',
                     color_continuous_scale='Greens',
                     text='비율(%)')
        st.plotly_chart(fig, use_container_width=True)

        st.info("💡 **인사이트**: 연속 2개가 약 56%로 가장 흔한 패턴입니다!")


# 번호 추천 페이지
def recommendation_page(loader, model, recommender):
    """번호 추천 페이지"""
    st.title("🎯 번호 추천")

    st.markdown("""
    머신러닝과 통계적 패턴 분석을 기반으로 번호를 추천합니다.
    다양한 전략 중 원하는 방식을 선택하세요!
    """)

    # 설정
    col1, col2, col3 = st.columns([1, 2, 2])

    with col1:
        n_combinations = st.slider("추천 개수", min_value=1, max_value=10, value=5)

    with col2:
        strategy = st.selectbox(
            "추천 전략 선택",
            ["⭐ 하이브리드 (최고 품질)",
             "📊 점수 기반",
             "🎲 확률 가중치",
             "🔄 패턴 기반",
             "🎨 그리드 패턴 기반",
             "🖼️ 이미지 패턴 기반",
             "🔢 연속 번호 포함",
             "🎰 무작위 (대조군)"]
        )

    with col3:
        fixed_mode = st.checkbox(
            "🔒 고정 모드",
            value=False,
            help="고정 모드: 다음 회차(1204회)에 맞춰 항상 같은 번호 추천\n랜덤 모드: 매번 다른 번호 추천"
        )

        if fixed_mode:
            next_round = int(loader.df['회차'].max()) + 1
            st.caption(f"📌 다음 회차({next_round}회)용 고정 번호")
        else:
            st.caption("🎲 매번 새로운 번호")

    if st.button("🎯 번호 추천 받기", type="primary", use_container_width=True):
        with st.spinner("번호 생성 중..."):
            # 시드 설정 (고정 모드일 경우) - 다음 회차 번호를 시드로 사용
            next_round = int(loader.df['회차'].max()) + 1
            seed = next_round if fixed_mode else None

            # 전략에 따라 추천
            if "하이브리드" in strategy:
                results = recommender.generate_hybrid(n_combinations, seed=seed)
                st.success("⭐ 하이브리드 전략으로 최고 품질의 번호를 추천했습니다!")
            elif "점수" in strategy:
                results = recommender.generate_by_score(n_combinations, seed=seed)
                st.success("📊 점수 기반으로 상위 번호들을 선정했습니다!")
            elif "확률" in strategy:
                results = recommender.generate_by_probability(n_combinations, seed=seed)
                st.success("🎲 확률 가중치 기반으로 번호를 생성했습니다!")
            elif "패턴" in strategy and "그리드" not in strategy:
                results = recommender.generate_by_pattern(n_combinations, seed=seed)
                st.success("🔄 빈출 패턴을 활용하여 번호를 생성했습니다!")
            elif "그리드" in strategy:
                results = recommender.generate_grid_based(n_combinations, seed=seed)
                st.success("🎨 그리드 패턴 분석을 기반으로 번호를 생성했습니다!")
            elif "이미지" in strategy:
                results = recommender.generate_image_based(n_combinations, seed=seed)
                st.success("🖼️ 이미지 패턴 분석을 기반으로 번호를 생성했습니다!")
            elif "연속" in strategy:
                results = recommender.generate_with_consecutive(n_combinations, seed=seed)
                st.success("🔢 연속 번호를 포함한 번호를 생성했습니다!")
            else:
                results = recommender.generate_random(n_combinations, seed=seed)
                st.success("🎰 무작위로 번호를 생성했습니다 (대조군)")

            # 모드 정보 표시
            if fixed_mode:
                st.info(f"🔒 **고정 모드**: 다음 회차({next_round}회)에 대해 항상 동일한 번호를 추천합니다.")

        # 결과 표시
        st.markdown("---")
        st.subheader("🎰 추천 번호")

        for i, combo in enumerate(results, 1):
            sorted_combo = sorted(combo)

            # 번호 분석
            odd = sum(1 for n in sorted_combo if n % 2 == 1)
            even = 6 - odd
            total = sum(sorted_combo)

            low = sum(1 for n in sorted_combo if 1 <= n <= 15)
            mid = sum(1 for n in sorted_combo if 16 <= n <= 30)
            high = sum(1 for n in sorted_combo if 31 <= n <= 45)

            # 연속 번호 찾기
            consecutive = []
            for j in range(len(sorted_combo)-1):
                if sorted_combo[j+1] == sorted_combo[j] + 1:
                    consecutive.append(f"{sorted_combo[j]}-{sorted_combo[j+1]}")

            # 표시
            col1, col2, col3 = st.columns([2, 2, 1])

            with col1:
                st.markdown(f"### 조합 #{i}")
                # 번호 버튼 형태로 표시
                cols = st.columns(6)
                for idx, num in enumerate(sorted_combo):
                    with cols[idx]:
                        # 구간별 색상
                        if 1 <= num <= 15:
                            st.markdown(f'<div style="background-color:#FF6B6B;color:white;padding:15px;border-radius:10px;text-align:center;font-size:20px;font-weight:bold;">{num}</div>', unsafe_allow_html=True)
                        elif 16 <= num <= 30:
                            st.markdown(f'<div style="background-color:#4ECDC4;color:white;padding:15px;border-radius:10px;text-align:center;font-size:20px;font-weight:bold;">{num}</div>', unsafe_allow_html=True)
                        else:
                            st.markdown(f'<div style="background-color:#45B7D1;color:white;padding:15px;border-radius:10px;text-align:center;font-size:20px;font-weight:bold;">{num}</div>', unsafe_allow_html=True)

            with col2:
                st.markdown("#### 📊 통계")
                st.write(f"**합계**: {total}")
                st.write(f"**홀/짝**: {odd}/{even}")
                st.write(f"**구간 분포**: 저{low} / 중{mid} / 고{high}")
                if consecutive:
                    st.write(f"**연속**: {', '.join(consecutive)}")
                else:
                    st.write("**연속**: 없음")

            with col3:
                st.markdown("#### 📋 용지")
                # 복권 용지 미리보기 (간단 버전)
                grid_html = create_lottery_grid_simple(sorted_combo)
                st.markdown(grid_html, unsafe_allow_html=True)

            st.markdown("---")

        # 전체 통계
        st.subheader("📈 추천 번호 통계")

        all_nums = [n for combo in results for n in combo]
        freq = Counter(all_nums)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("가장 많이 추천된 번호",
                     f"{freq.most_common(1)[0][0]}번 ({freq.most_common(1)[0][1]}회)")

        with col2:
            avg_sum = sum(sum(combo) for combo in results) / len(results)
            st.metric("평균 합계", f"{avg_sum:.1f}")

        with col3:
            has_consecutive = sum(1 for combo in results if any(
                sorted(combo)[i+1] == sorted(combo)[i] + 1
                for i in range(len(sorted(combo))-1)
            ))
            st.metric("연속 번호 포함 비율", f"{has_consecutive/len(results)*100:.0f}%")


# 번호 분석 페이지
def number_analysis_page(loader, model):
    """특정 번호 분석 페이지"""
    st.title("🔍 번호 분석")

    st.markdown("특정 번호의 상세한 통계와 특징을 분석합니다.")

    # 번호 선택
    selected_number = st.number_input(
        "분석할 번호를 선택하세요 (1-45)",
        min_value=1, max_value=45, value=7, step=1
    )

    if st.button("🔍 분석하기", type="primary"):
        # 번호 특징
        features = model.number_features[selected_number]
        scores = model.number_scores[selected_number]

        st.markdown(f"## 번호 {selected_number} 상세 분석")

        # 메트릭
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("총 출현 횟수", f"{features['total_frequency']}회")

        with col2:
            st.metric("최근 50회 출현", f"{features['recent_50_frequency']}회")

        with col3:
            st.metric("미출현 기간", f"{features['absence_length']}회차")

        with col4:
            st.metric("종합 점수", f"{scores['total_score']:.1f}점")

        # 점수 분해
        st.markdown("---")
        st.subheader("📊 점수 분해")

        score_df = pd.DataFrame({
            '항목': ['빈도 점수', '트렌드 점수', '부재 기간 점수', '핫넘버 점수'],
            '점수': [scores['freq_score'], scores['trend_score'],
                    scores['absence_score'], scores['hotness_score']]
        })

        fig = px.bar(score_df, x='항목', y='점수',
                     title=f'번호 {selected_number}의 점수 분해',
                     color='점수',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

        # 출현 이력
        st.markdown("---")
        st.subheader("📅 최근 출현 이력")

        appearance_history = []
        for idx, row in loader.numbers_df.iterrows():
            if selected_number in row['당첨번호']:
                appearance_history.append({
                    '회차': row['회차'],
                    '일자': row['일자'],
                    '당첨번호': ', '.join(map(str, sorted(row['당첨번호'])))
                })
                if len(appearance_history) >= 10:
                    break

        if appearance_history:
            history_df = pd.DataFrame(appearance_history)
            st.dataframe(history_df, use_container_width=True, hide_index=True)
        else:
            st.warning("출현 이력이 없습니다.")

        # 동반 출현 번호
        st.markdown("---")
        st.subheader("🤝 자주 함께 나온 번호 TOP 10")

        companion_counts = Counter()
        for _, row in loader.numbers_df.iterrows():
            if selected_number in row['당첨번호']:
                companions = [n for n in row['당첨번호'] if n != selected_number]
                companion_counts.update(companions)

        companion_df = pd.DataFrame(
            companion_counts.most_common(10),
            columns=['번호', '동반 출현 횟수']
        )
        companion_df['동반 출현율(%)'] = (
            companion_df['동반 출현 횟수'] / features['total_frequency'] * 100
        ).round(1)

        st.dataframe(companion_df, use_container_width=True, hide_index=True)


# 예측 모델 페이지
def prediction_model_page(loader, model):
    """예측 모델 인사이트 페이지"""
    st.title("🤖 예측 모델 인사이트")

    st.markdown("""
    머신러닝 모델이 학습한 패턴과 각 번호의 특징을 시각화합니다.
    """)

    # 상위 번호
    st.subheader("🏆 점수 기반 상위 20개 번호")

    top_numbers = model.get_top_numbers(20)
    top_scores = [(num, model.number_scores[num]['total_score']) for num in top_numbers]

    top_df = pd.DataFrame(top_scores, columns=['번호', '종합 점수'])

    fig = px.bar(top_df, x='번호', y='종합 점수',
                 title='번호별 종합 점수 TOP 20',
                 color='종합 점수',
                 color_continuous_scale='Viridis')
    st.plotly_chart(fig, use_container_width=True)

    # 패턴 분석
    st.markdown("---")
    st.subheader("🔄 학습된 패턴")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### 가장 흔한 구간 분포")
        section_patterns = model.patterns['section']['most_common'][:5]
        section_df = pd.DataFrame(
            section_patterns,
            columns=['패턴 (저/중/고)', '출현 횟수']
        )
        st.dataframe(section_df, use_container_width=True, hide_index=True)

    with col2:
        st.markdown("##### 가장 흔한 홀짝 분포")
        odd_even_patterns = model.patterns['odd_even']['most_common']
        odd_even_df = pd.DataFrame(
            odd_even_patterns,
            columns=['패턴 (홀/짝)', '출현 횟수']
        )
        st.dataframe(odd_even_df, use_container_width=True, hide_index=True)

    # 합계 통계
    st.markdown("---")
    st.subheader("➕ 당첨번호 합계 통계")

    sum_stats = model.patterns['sum']

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("평균", f"{sum_stats['mean']:.1f}")

    with col2:
        st.metric("중앙값", f"{sum_stats['median']:.1f}")

    with col3:
        st.metric("표준편차", f"{sum_stats['std']:.1f}")

    with col4:
        st.metric("범위", f"{sum_stats['min']:.0f}~{sum_stats['max']:.0f}")

    # 연속 번호 통계
    st.markdown("---")
    st.subheader("🔢 연속 번호 통계")

    consecutive_prob = model.patterns['consecutive']['has_consecutive_prob']

    st.info(f"💡 **연속 번호 출현 확률**: {consecutive_prob*100:.1f}% (전체 {len(loader.df)}회차 중)")

    # 인기 연속 쌍
    pair_freq = model.patterns['consecutive']['pair_frequency']
    top_pairs = sorted(pair_freq.items(), key=lambda x: x[1], reverse=True)[:10]

    pairs_df = pd.DataFrame([
        {'연속 쌍': f"{p[0]}-{p[1]}", '출현 횟수': count,
         '출현율(%)': count/len(loader.df)*100}
        for p, count in top_pairs
    ])

    st.markdown("##### 인기 연속 쌍 TOP 10")
    st.dataframe(pairs_df, use_container_width=True, hide_index=True)


# 그리드 패턴 분석 페이지
def grid_pattern_page(loader):
    """그리드 패턴 분석 페이지"""
    st.title("🎨 복권 용지 그리드 패턴 분석")

    st.markdown("""
    복권 용지의 **7x7 그리드 배치**를 기반으로 당첨번호의 공간적 분포를 분석합니다.
    숫자가 아닌 **위치**라는 새로운 관점에서 로또를 분석하는 독창적인 방법입니다.
    """)

    # 그리드 구조 설명
    st.markdown("---")
    st.subheader("📐 그리드 구조")

    st.code("""
    [ 1][ 2][ 3][ 4][ 5][ 6][ 7]
    [ 8][ 9][10][11][12][13][14]
    [15][16][17][18][19][20][21]
    [22][23][24][25][26][27][28]
    [29][30][31][32][33][34][35]
    [36][37][38][39][40][41][42]
    [43][44][45][  ][  ][  ][  ]
    """, language="text")

    # 분석 실행
    with st.spinner("그리드 패턴 분석 중..."):
        analyzer = GridPatternAnalysis(loader)

        # 1. 위치별 빈도 분석
        st.markdown("---")
        st.subheader("🔥 위치별 출현 빈도")

        position_heatmap = analyzer.analyze_position_frequency()

        # 히트맵 이미지 표시
        import matplotlib.pyplot as plt
        import seaborn as sns

        fig, ax = plt.subplots(figsize=(12, 10))
        sns.heatmap(
            position_heatmap,
            annot=True,
            fmt='.0f',
            cmap='YlOrRd',
            cbar_kws={'label': '출현 횟수'},
            linewidths=0.5,
            ax=ax
        )

        # 각 셀에 번호 표시
        for row in range(7):
            for col in range(7):
                number = analyzer.position_to_number.get((row, col))
                if number:
                    freq = int(position_heatmap[row, col])
                    ax.text(col + 0.5, row + 0.3, f'#{number}',
                           ha='center', va='center',
                           fontsize=8, color='blue', weight='bold')

        ax.set_title('로또 복권 용지 그리드 위치별 출현 빈도',
                     fontsize=14, weight='bold', pad=20)
        ax.set_xlabel('열 (Column)', fontsize=12)
        ax.set_ylabel('행 (Row)', fontsize=12)

        st.pyplot(fig)
        plt.close()

        # 통계
        valid_frequencies = []
        for pos, num in analyzer.position_to_number.items():
            r, c = pos
            freq = position_heatmap[r, c]
            valid_frequencies.append((freq, pos, num))

        valid_frequencies.sort(reverse=True)
        max_freq, max_pos, max_number = valid_frequencies[0]
        min_freq, min_pos, min_number = valid_frequencies[-1]
        avg_freq = np.mean([f[0] for f in valid_frequencies])

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🔥 최다 출현", f"#{max_number}", f"{int(max_freq)}회")
        with col2:
            st.metric("📊 평균 출현", "", f"{avg_freq:.1f}회")
        with col3:
            st.metric("❄️ 최소 출현", f"#{min_number}", f"{int(min_freq)}회")

        # 2. 구역별 분석
        st.markdown("---")
        st.subheader("🗺️ 구역별 분포")

        zone_counts = analyzer.analyze_zone_distribution()

        zone_names = {
            "corner": "모서리 (4칸)",
            "edge": "가장자리 (20칸)",
            "middle": "중간 (12칸)",
            "center": "중앙부 (9칸)"
        }

        zone_data = []
        total = sum(zone_counts.values())
        for zone in ["corner", "edge", "middle", "center"]:
            count = zone_counts[zone]
            cells = {"corner": 4, "edge": 20, "middle": 12, "center": 9}[zone]
            avg_per_cell = count / cells
            zone_data.append({
                '구역': zone_names[zone],
                '출현 횟수': count,
                '비율(%)': f"{(count/total)*100:.2f}",
                '1칸당 평균': f"{avg_per_cell:.1f}"
            })

        zone_df = pd.DataFrame(zone_data)
        st.dataframe(zone_df, use_container_width=True, hide_index=True)

        # 인사이트
        st.info("""
        💡 **핵심 인사이트**:
        - **중간 영역**이 1칸당 평균 출현 횟수가 가장 높습니다!
        - 모서리 4칸(1, 7, 43, 45번)은 상대적으로 출현율이 낮습니다.
        - 가장자리 20칸이 전체의 약 37%를 차지합니다.
        """)

        # 3. 기하학적 패턴
        st.markdown("---")
        st.subheader("📐 기하학적 패턴")

        pattern_stats = analyzer.analyze_geometric_patterns()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 대각선 패턴")
            main_diag_avg = np.mean(pattern_stats["diagonal_main"])
            anti_diag_avg = np.mean(pattern_stats["diagonal_anti"])

            diag_data = pd.DataFrame([
                {"대각선": "주 대각선 (↘)", "평균 출현": f"{main_diag_avg:.2f}개/회차"},
                {"대각선": "반대 대각선 (↙)", "평균 출현": f"{anti_diag_avg:.2f}개/회차"}
            ])
            st.dataframe(diag_data, use_container_width=True, hide_index=True)

            if anti_diag_avg > main_diag_avg:
                st.success(f"✅ 반대 대각선이 {anti_diag_avg - main_diag_avg:.2f}개 더 많이 나옵니다!")

        with col2:
            st.markdown("##### 같은 줄 패턴")
            h_total = sum(len(v) for v in pattern_stats["horizontal"].values())
            v_total = sum(len(v) for v in pattern_stats["vertical"].values())

            line_data = pd.DataFrame([
                {"패턴": "같은 가로줄 3개 이상", "발생 횟수": f"{h_total}회", "비율": f"{h_total/len(loader.df)*100:.1f}%"},
                {"패턴": "같은 세로줄 3개 이상", "발생 횟수": f"{v_total}회", "비율": f"{v_total/len(loader.df)*100:.1f}%"}
            ])
            st.dataframe(line_data, use_container_width=True, hide_index=True)

        # 4. 공간적 군집도
        st.markdown("---")
        st.subheader("🎯 공간적 군집도")

        clustering_scores = analyzer.analyze_spatial_clustering()

        avg_distances = [s['avg_distance'] for s in clustering_scores]

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("평균 거리", f"{np.mean(avg_distances):.2f}")
        with col2:
            st.metric("중앙값", f"{np.median(avg_distances):.2f}")
        with col3:
            st.metric("최소", f"{np.min(avg_distances):.2f}")
        with col4:
            st.metric("최대", f"{np.max(avg_distances):.2f}")

        st.markdown("**평균 거리**: 당첨번호들이 그리드 상에서 평균적으로 떨어져 있는 거리 (맨해튼 거리)")

        # 군집도 분포 차트
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=avg_distances,
            nbinsx=30,
            name='회차별 평균 거리',
            marker_color='skyblue'
        ))
        fig.add_vline(x=np.mean(avg_distances), line_dash="dash",
                     line_color="red",
                     annotation_text=f"평균: {np.mean(avg_distances):.2f}")
        fig.update_layout(
            title='회차별 번호 간 평균 거리 분포',
            xaxis_title='평균 거리',
            yaxis_title='빈도',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        # 5. 실전 활용 전략
        st.markdown("---")
        st.subheader("💡 실전 활용 전략")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### ✅ 추천 전략")
            st.success("""
            1. **중간 영역 집중**: 16-27, 31-34번 우선
            2. **반대 대각선 활용**: 7, 13, 19, 25, 31, 37, 43 중 1-2개
            3. **같은 줄 2-3개**: 한 가로줄에서 2-3개 선택
            4. **평균 거리 4-5**: 적절한 분산 유지
            """)

        with col2:
            st.markdown("##### ⚠️ 주의 전략")
            st.warning("""
            1. **모서리 번호 지양**: 1, 7, 43, 45번은 1개 이하
            2. **극단적 군집 피하기**: 너무 밀집된 패턴
            3. **같은 줄 4개 이상 피하기**: 매우 드묾
            4. **극단적 분산 피하기**: 너무 흩어진 패턴
            """)

        # 추천 번호 영역
        st.markdown("---")
        st.subheader("🎯 그리드 기반 추천 번호")

        middle_zone_numbers = [16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 31, 32, 33, 34]
        anti_diagonal_numbers = [7, 13, 19, 25, 31, 37, 43]

        st.markdown("##### 중간 영역 추천 번호 (1칸당 출현율 높음)")
        st.write(", ".join(map(str, middle_zone_numbers)))

        st.markdown("##### 반대 대각선 추천 번호 (출현율 높음)")
        st.write(", ".join(map(str, anti_diagonal_numbers)))

        st.info("""
        📌 **활용 팁**:
        - 중간 영역에서 3-4개 선택
        - 반대 대각선에서 1-2개 선택
        - 나머지는 가장자리에서 고르게 분산
        - 평균 거리 4.0~5.0 유지
        """)


# 이미지 패턴 분석 페이지
def image_pattern_page(loader):
    """이미지 패턴 분석 페이지"""
    st.title("🖼️ 복권 용지 이미지 패턴 분석")

    st.markdown("""
    생성된 복권용지 이미지들의 **시각적 패턴**을 분석합니다.
    번호 배치의 밀도, 균형, 대칭성 등을 분석하여 최적의 조합을 찾습니다.
    """)

    # 복권 용지 미리보기 (텍스트 기반)
    st.markdown("---")
    st.subheader("📁 복권 용지 미리보기")

    st.info(f"✅ 총 {len(loader.df)}개 회차의 복권 용지를 텍스트 그리드로 표시합니다.")

    # 최근 회차 미리보기
    st.markdown("##### 최근 복권 용지 (최근 3회)")

    recent_rounds = loader.numbers_df.head(3)

    cols = st.columns(3)
    for idx, (_, row) in enumerate(recent_rounds.iterrows()):
        with cols[idx]:
            round_num = int(row['회차'])
            date = row['일자'].strftime('%Y.%m.%d')
            winning = list(row['당첨번호'])
            bonus = row['보너스번호']

            # HTML 그리드 생성
            html = create_lottery_ticket_compact(round_num, date, winning, bonus)
            st.markdown(html, unsafe_allow_html=True)

    # 분석 실행
    st.markdown("---")
    st.subheader("📊 이미지 패턴 분석")

    with st.spinner("이미지 패턴 분석 중..."):
        analyzer = ImagePatternAnalysis(loader)

        # 1. 시각적 밀도 분석
        st.markdown("### 🎨 시각적 밀도 분석")
        st.markdown("복권용지 상에서 번호들이 얼마나 밀집되어 있는지 분석")

        density_df = analyzer.analyze_visual_density()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("평균 거리", f"{density_df['평균_거리'].mean():.2f}")
        with col2:
            st.metric("최소 (밀집)", f"{density_df['평균_거리'].min():.2f}")
        with col3:
            st.metric("최대 (분산)", f"{density_df['평균_거리'].max():.2f}")
        with col4:
            st.metric("표준편차", f"{density_df['평균_거리'].std():.2f}")

        # 밀도 분포 히스토그램
        import plotly.graph_objects as go
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=density_df['평균_거리'],
            nbinsx=30,
            name='평균 거리',
            marker_color='skyblue'
        ))
        fig.add_vline(x=density_df['평균_거리'].mean(), line_dash="dash",
                     line_color="red",
                     annotation_text=f"평균: {density_df['평균_거리'].mean():.2f}")
        fig.update_layout(
            title='회차별 번호 간 평균 거리 분포',
            xaxis_title='평균 거리',
            yaxis_title='빈도',
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

        # 가장 밀집/분산된 회차
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 🔥 가장 밀집된 회차 TOP 5")
            top_dense = density_df.nsmallest(5, '평균_거리')[['회차', '평균_거리']]
            st.dataframe(top_dense, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("##### 🌊 가장 분산된 회차 TOP 5")
            top_sparse = density_df.nlargest(5, '평균_거리')[['회차', '평균_거리']]
            st.dataframe(top_sparse, use_container_width=True, hide_index=True)

        # 2. 4분면 패턴 분석
        st.markdown("---")
        st.markdown("### 📐 4분면 패턴 분석")
        st.markdown("복권용지를 4등분하여 각 분면의 번호 분포 분석")

        st.code("""
        Q1 (왼쪽 위):    1-3, 8-10, 15-17
        Q2 (오른쪽 위):  4-7, 11-14, 18-21
        Q3 (왼쪽 아래):  22-24, 29-31, 36-38, 43-45
        Q4 (오른쪽 아래): 25-28, 32-35, 39-42
        """, language="text")

        quadrant_patterns = analyzer.analyze_quadrant_patterns()

        # 패턴 빈도 차트
        pattern_data = pd.DataFrame([
            {'패턴': pattern, '출현횟수': count, '비율(%)': count/len(loader.df)*100}
            for pattern, count in quadrant_patterns.most_common(10)
        ])

        fig = px.bar(pattern_data, x='패턴', y='출현횟수',
                     title='4분면 분포 패턴 TOP 10 (Q1-Q2-Q3-Q4)',
                     color='출현횟수',
                     color_continuous_scale='Viridis',
                     text='비율(%)')
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        st.plotly_chart(fig, use_container_width=True)

        # 3. 시각적 균형 분석
        st.markdown("---")
        st.markdown("### ⚖️ 시각적 균형 분석 (무게중심)")

        balance_df = analyzer.analyze_visual_balance()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("평균 무게중심",
                     f"({balance_df['중심_row'].mean():.2f}, {balance_df['중심_col'].mean():.2f})")
        with col2:
            st.metric("이상중심 (3, 3)", "")
        with col3:
            st.metric("평균 편차", f"{balance_df['이상중심_편차'].mean():.2f}")

        # 무게중심 분포 산점도
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=balance_df['중심_col'],
            y=balance_df['중심_row'],
            mode='markers',
            marker=dict(
                size=5,
                color=balance_df['이상중심_편차'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="편차")
            ),
            text=balance_df['회차'],
            hovertemplate='회차: %{text}<br>중심: (%{x:.2f}, %{y:.2f})<extra></extra>'
        ))
        # 이상적인 중심 표시
        fig.add_trace(go.Scatter(
            x=[3], y=[3],
            mode='markers',
            marker=dict(size=15, color='green', symbol='star'),
            name='이상적 중심 (3, 3)'
        ))
        fig.update_layout(
            title='회차별 무게중심 분포',
            xaxis_title='중심 열 (Column)',
            yaxis_title='중심 행 (Row)',
            showlegend=True,
            height=500
        )
        st.plotly_chart(fig, use_container_width=True)

        # 가장 균형잡힌 회차
        st.markdown("##### ⚖️ 가장 균형잡힌 회차 TOP 5")
        balanced = balance_df.nsmallest(5, '이상중심_편차')[['회차', '중심_row', '중심_col', '이상중심_편차']]
        st.dataframe(balanced, use_container_width=True, hide_index=True)

        # 4. 대칭 패턴 분석
        st.markdown("---")
        st.markdown("### 🔄 대칭 패턴 분석")

        symmetry_stats = analyzer.analyze_symmetry_patterns()

        symmetry_df = pd.DataFrame([
            {'패턴': pattern, '출현횟수': count, '비율(%)': count/len(loader.df)*100}
            for pattern, count in symmetry_stats.items()
        ])

        fig = px.pie(symmetry_df, values='출현횟수', names='패턴',
                     title='대칭 패턴 분포',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

        # 5. 실전 활용 전략
        st.markdown("---")
        st.markdown("### 💡 이미지 패턴 기반 실전 전략")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### ✅ 추천 전략")
            st.success("""
            1. **적절한 밀도**: 평균 거리 3.0~4.5 유지
            2. **4분면 균형**: 모든 분면에 최소 1개씩 분포
            3. **무게중심**: (3, 3)에 가깝게 (편차 1.5 이하)
            4. **좌우 대칭**: 좌우 번호 개수 차이 1개 이하
            """)

        with col2:
            st.markdown("##### ⚠️ 주의 전략")
            st.warning("""
            1. **극단적 밀집 피하기**: 평균 거리 2.0 이하
            2. **극단적 분산 피하기**: 평균 거리 6.0 이상
            3. **한쪽 편중 피하기**: 한 분면에 4개 이상
            4. **무게중심 불균형**: 편차 2.0 이상
            """)

        # 테스트 번호 조합 평가
        st.markdown("---")
        st.markdown("### 🧪 번호 조합 이미지 패턴 평가")

        test_numbers = st.multiselect(
            "6개의 번호를 선택하세요 (1-45)",
            options=list(range(1, 46)),
            default=[7, 12, 19, 27, 33, 41],
            max_selections=6
        )

        if len(test_numbers) == 6:
            score_data = analyzer.calculate_image_score(test_numbers)

            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("#### 📊 점수")
                st.metric("총점", f"{score_data['total_score']}점", "/ 100점")
                st.metric("시각적 밀도", f"{score_data['density_score']}점", "/ 25점")
                st.metric("4분면 균형", f"{score_data['quadrant_score']}점", "/ 25점")
                st.metric("무게중심 균형", f"{score_data['balance_score']}점", "/ 25점")
                st.metric("대칭성", f"{score_data['symmetry_score']}점", "/ 25점")

            with col2:
                st.markdown("#### 📋 상세 정보")
                st.write(f"**평균 거리**: {score_data['avg_distance']:.2f}")
                st.write(f"**4분면 분포**: {score_data['quadrants']}")
                st.write(f"**무게중심**: ({score_data['center'][0]:.2f}, {score_data['center'][1]:.2f})")
                st.write(f"**이상중심 편차**: {score_data['deviation']:.2f}")

                # 평가
                if score_data['total_score'] >= 80:
                    st.success("✅ 우수한 이미지 패턴입니다!")
                elif score_data['total_score'] >= 60:
                    st.info("ℹ️ 양호한 이미지 패턴입니다.")
                else:
                    st.warning("⚠️ 개선이 필요한 이미지 패턴입니다.")


# 번호 테마 페이지
def number_theme_page(loader, model, recommender):
    """번호 테마 페이지 (코어 번호, 고정 번호, 신뢰도)"""
    st.title("🎲 번호 테마")

    st.markdown("""
    **3가지 특별한 번호 추천 방식**을 제공합니다.
    - 코어 번호 (가장 확신하는 핵심 번호 3-4개)
    - 고정 번호 (사용자 선택 + 최적 조합)
    - 신뢰도 점수 (각 번호의 출현 확신도)
    """)

    # 코어 시스템 로드
    core_system = load_core_system(model, recommender)

    # 탭 구성
    tab1, tab2, tab3 = st.tabs(["⭐ 코어 번호", "🔒 고정 번호", "📊 신뢰도 점수"])

    # ========== 탭 1: 코어 번호 ==========
    with tab1:
        st.header("⭐ 코어 번호 추천")
        st.markdown("""
        **가장 확신하는 핵심 번호 3-4개**를 추출하여 조합을 생성합니다.
        - 신뢰도 85% 이상의 최상위 번호
        - 여러 전략의 점수를 종합한 결과
        - 코어 번호를 중심으로 다양한 조합 생성
        """)

        col1, col2 = st.columns([1, 2])

        with col1:
            n_core = st.slider("코어 번호 개수", min_value=3, max_value=5, value=4)
            min_confidence = st.slider("최소 신뢰도 (%)", min_value=70, max_value=95, value=85)

        with col2:
            n_combinations = st.slider("생성할 조합 개수", min_value=3, max_value=10, value=5)

        if st.button("⭐ 코어 번호 추출 및 조합 생성", type="primary", use_container_width=True):
            with st.spinner("코어 번호 추출 중..."):
                core_numbers, confidence_scores = core_system.get_core_numbers(
                    n_core=n_core,
                    min_confidence=min_confidence
                )

                st.markdown("---")
                st.subheader("🎯 추출된 코어 번호")

                # 코어 번호 표시
                cols = st.columns(len(core_numbers))
                for idx, num in enumerate(core_numbers):
                    with cols[idx]:
                        conf = confidence_scores[num]['confidence']
                        st.markdown(
                            f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'
                            f'color:white;padding:20px;border-radius:15px;text-align:center;'
                            f'box-shadow: 0 4px 6px rgba(0,0,0,0.1);">'
                            f'<div style="font-size:32px;font-weight:bold;margin-bottom:5px;">{num}</div>'
                            f'<div style="font-size:14px;opacity:0.9;">신뢰도 {conf:.1f}%</div>'
                            f'</div>',
                            unsafe_allow_html=True
                        )

                # 과거 데이터 분석
                st.markdown("---")
                st.subheader("📈 과거 데이터 분석")

                coverage = core_system.analyze_core_coverage(core_numbers)

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("코어 전체 포함", f"{coverage['all_matched']}회",
                             f"{coverage['all_matched_rate']:.1f}%")
                with col2:
                    partial_3plus = sum(
                        coverage['partial_matched'][i]['count']
                        for i in range(3, n_core + 1)
                    )
                    st.metric("3개 이상 포함", f"{partial_3plus}회")
                with col3:
                    st.metric("전혀 없음", f"{coverage['none_matched']}회",
                             f"{coverage['none_matched_rate']:.1f}%")
                with col4:
                    avg_match = sum(
                        i * coverage['partial_matched'][i]['count']
                        for i in range(n_core + 1)
                    ) / len(loader.df)
                    st.metric("평균 매칭 개수", f"{avg_match:.2f}개")

                # 부분 매칭 분포
                st.markdown("##### 📊 매칭 개수별 분포")
                match_data = pd.DataFrame([
                    {
                        '매칭 개수': f"{i}개",
                        '출현 횟수': coverage['partial_matched'][i]['count'],
                        '비율(%)': coverage['partial_matched'][i]['rate']
                    }
                    for i in range(n_core + 1)
                ])

                fig = px.bar(match_data, x='매칭 개수', y='출현 횟수',
                            title='코어 번호 매칭 개수별 분포',
                            color='비율(%)',
                            color_continuous_scale='Blues',
                            text='비율(%)')
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig, use_container_width=True)

                # 코어 번호 포함 조합 생성
                st.markdown("---")
                st.subheader("🎰 코어 번호 포함 추천 조합")

                core_combos = core_system.generate_with_core(
                    core_numbers,
                    n_combinations=n_combinations
                )

                for i, combo in enumerate(core_combos, 1):
                    st.markdown(f"### 조합 #{i}")

                    # 번호 표시
                    cols = st.columns(6)
                    for idx, num in enumerate(sorted(combo)):
                        with cols[idx]:
                            is_core = num in core_numbers
                            if is_core:
                                # 코어 번호 - 보라색 그라디언트
                                st.markdown(
                                    f'<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'
                                    f'color:white;padding:15px;border-radius:10px;text-align:center;'
                                    f'font-size:20px;font-weight:bold;box-shadow: 0 2px 4px rgba(0,0,0,0.2);">'
                                    f'{num}</div>',
                                    unsafe_allow_html=True
                                )
                            else:
                                # 일반 번호 - 구간별 색상
                                if 1 <= num <= 15:
                                    color = '#FF6B6B'
                                elif 16 <= num <= 30:
                                    color = '#4ECDC4'
                                else:
                                    color = '#45B7D1'

                                st.markdown(
                                    f'<div style="background-color:{color};color:white;'
                                    f'padding:15px;border-radius:10px;text-align:center;'
                                    f'font-size:20px;font-weight:bold;">{num}</div>',
                                    unsafe_allow_html=True
                                )

                    # 통계
                    st.caption(f"합계: {sum(combo)}, "
                              f"홀{sum(1 for n in combo if n % 2 == 1)}/짝{sum(1 for n in combo if n % 2 == 0)}")

                    st.markdown("---")

                # 인사이트
                st.info(f"""
                💡 **활용 팁**:
                - 코어 번호 {core_numbers}는 가장 높은 신뢰도를 가진 번호입니다.
                - 과거 {coverage['all_matched']}회({coverage['all_matched_rate']:.1f}%)에서 코어 번호가 모두 포함되었습니다.
                - 평균적으로 회차당 약 {avg_match:.1f}개의 코어 번호가 출현했습니다.
                """)

    # ========== 탭 2: 고정 번호 ==========
    with tab2:
        st.header("🔒 고정 번호 + 추천 조합")
        st.markdown("""
        **사용자가 선택한 번호를 고정**하고, 나머지를 최적으로 추천합니다.
        - 개인적으로 선호하는 번호 활용
        - 시스템이 최적의 보완 번호 추천
        - 고정 번호와 잘 어울리는 조합 생성
        """)

        st.markdown("### 🎯 고정할 번호 선택")

        # 번호 선택 UI
        fixed_numbers = st.multiselect(
            "고정할 번호를 선택하세요 (1-5개 권장)",
            options=list(range(1, 46)),
            default=[],
            max_selections=5,
            help="너무 많은 번호를 고정하면 조합의 다양성이 줄어듭니다."
        )

        if len(fixed_numbers) > 0:
            st.success(f"✅ 선택된 고정 번호: {sorted(fixed_numbers)}")

            # 보완 번호 추천
            st.markdown("---")
            st.subheader("💡 추천 보완 번호")
            st.markdown("고정 번호와 **자주 함께 나온** 번호들을 추천합니다.")

            complementary = core_system.get_complementary_numbers(fixed_numbers, top_n=12)

            # 보완 번호를 3줄로 표시
            for row in range(3):
                cols = st.columns(4)
                for col_idx in range(4):
                    idx = row * 4 + col_idx
                    if idx < len(complementary):
                        num, count, score, combined = complementary[idx]
                        with cols[col_idx]:
                            st.markdown(
                                f'<div style="background-color:#f8f9fa;border:2px solid #dee2e6;'
                                f'padding:12px;border-radius:8px;text-align:center;">'
                                f'<div style="font-size:24px;font-weight:bold;color:#495057;margin-bottom:5px;">{num}</div>'
                                f'<div style="font-size:11px;color:#6c757d;">동반 {count}회</div>'
                                f'<div style="font-size:11px;color:#6c757d;">점수 {score:.0f}</div>'
                                f'</div>',
                                unsafe_allow_html=True
                            )

            # 조합 생성 설정
            st.markdown("---")
            st.subheader("🎰 추천 조합 생성")

            n_combinations_fixed = st.slider(
                "생성할 조합 개수",
                min_value=3, max_value=10, value=5,
                key="n_combinations_fixed"
            )

            if st.button("🎲 고정 번호 포함 조합 생성", type="primary", use_container_width=True):
                with st.spinner("조합 생성 중..."):
                    fixed_combos = core_system.generate_with_fixed(
                        fixed_numbers,
                        n_combinations=n_combinations_fixed
                    )

                    st.markdown("---")

                    for i, combo in enumerate(fixed_combos, 1):
                        st.markdown(f"### 조합 #{i}")

                        # 번호 표시
                        cols = st.columns(6)
                        for idx, num in enumerate(sorted(combo)):
                            with cols[idx]:
                                is_fixed = num in fixed_numbers

                                if is_fixed:
                                    # 고정 번호 - 금색
                                    st.markdown(
                                        f'<div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'
                                        f'color:white;padding:15px;border-radius:10px;text-align:center;'
                                        f'font-size:20px;font-weight:bold;box-shadow: 0 2px 4px rgba(0,0,0,0.2);">'
                                        f'{num}</div>',
                                        unsafe_allow_html=True
                                    )
                                else:
                                    # 일반 번호
                                    if 1 <= num <= 15:
                                        color = '#FF6B6B'
                                    elif 16 <= num <= 30:
                                        color = '#4ECDC4'
                                    else:
                                        color = '#45B7D1'

                                    st.markdown(
                                        f'<div style="background-color:{color};color:white;'
                                        f'padding:15px;border-radius:10px;text-align:center;'
                                        f'font-size:20px;font-weight:bold;">{num}</div>',
                                        unsafe_allow_html=True
                                    )

                        # 통계
                        st.caption(f"합계: {sum(combo)}, "
                                  f"홀{sum(1 for n in combo if n % 2 == 1)}/짝{sum(1 for n in combo if n % 2 == 0)}")

                        st.markdown("---")

                    st.info(f"""
                    💡 **고정 번호 전략**:
                    - 선택한 {len(fixed_numbers)}개 번호를 모든 조합에 포함시켰습니다.
                    - 나머지 {6 - len(fixed_numbers)}개는 분석 기반 최적 번호로 채웠습니다.
                    - 보완 번호는 고정 번호와 자주 함께 출현한 번호들입니다.
                    """)

        else:
            st.warning("⚠️ 고정할 번호를 먼저 선택해주세요.")

    # ========== 탭 3: 신뢰도 점수 ==========
    with tab3:
        st.header("📊 번호별 신뢰도 점수")
        st.markdown("""
        **모든 번호(1-45)의 신뢰도**를 한눈에 확인하세요.
        - 신뢰도 = 종합 점수를 50%~100% 범위로 정규화
        - 여러 분석 전략의 결과를 통합
        - 높을수록 출현 가능성이 높다고 판단
        """)

        # 신뢰도 계산
        with st.spinner("신뢰도 점수 계산 중..."):
            confidence_scores = core_system.calculate_confidence_scores()

        # 정렬 옵션
        st.markdown("---")
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            sort_option = st.radio(
                "정렬 기준",
                ["신뢰도 높은 순", "신뢰도 낮은 순", "번호 순"],
                horizontal=True
            )

        with col2:
            view_option = st.radio(
                "보기 옵션",
                ["전체 (45개)", "상위 20개", "상위 10개"],
                horizontal=True
            )

        # 정렬
        if sort_option == "신뢰도 높은 순":
            sorted_numbers = sorted(confidence_scores.items(),
                                   key=lambda x: x[1]['confidence'],
                                   reverse=True)
        elif sort_option == "신뢰도 낮은 순":
            sorted_numbers = sorted(confidence_scores.items(),
                                   key=lambda x: x[1]['confidence'])
        else:
            sorted_numbers = sorted(confidence_scores.items(),
                                   key=lambda x: x[0])

        # 보기 개수
        if view_option == "상위 20개":
            display_count = 20
        elif view_option == "상위 10개":
            display_count = 10
        else:
            display_count = 45

        sorted_numbers = sorted_numbers[:display_count]

        # 신뢰도 차트
        st.markdown("---")
        st.subheader("📈 신뢰도 차트")

        chart_data = pd.DataFrame([
            {
                '번호': num,
                '신뢰도(%)': data['confidence'],
                '점수': data['score'],
                '순위': data['rank']
            }
            for num, data in sorted_numbers
        ])

        fig = px.bar(chart_data, x='번호', y='신뢰도(%)',
                     title=f'번호별 신뢰도 점수 ({view_option})',
                     color='신뢰도(%)',
                     color_continuous_scale='RdYlGn',
                     hover_data=['점수', '순위'])
        fig.add_hline(y=75, line_dash="dash", line_color="orange",
                     annotation_text="기준선 75%")
        st.plotly_chart(fig, use_container_width=True)

        # 신뢰도 등급별 분류
        st.markdown("---")
        st.subheader("🏆 신뢰도 등급별 분류")

        grade_s = [num for num, data in confidence_scores.items() if data['confidence'] >= 90]
        grade_a = [num for num, data in confidence_scores.items() if 80 <= data['confidence'] < 90]
        grade_b = [num for num, data in confidence_scores.items() if 70 <= data['confidence'] < 80]
        grade_c = [num for num, data in confidence_scores.items() if data['confidence'] < 70]

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("##### 🥇 S등급 (90% 이상)")
            if grade_s:
                st.success(f"{', '.join(map(str, sorted(grade_s)))} ({len(grade_s)}개)")
            else:
                st.info("해당 등급 없음")

            st.markdown("##### 🥈 A등급 (80~90%)")
            if grade_a:
                st.success(f"{', '.join(map(str, sorted(grade_a)))} ({len(grade_a)}개)")
            else:
                st.info("해당 등급 없음")

        with col2:
            st.markdown("##### 🥉 B등급 (70~80%)")
            if grade_b:
                st.info(f"{', '.join(map(str, sorted(grade_b)))} ({len(grade_b)}개)")
            else:
                st.info("해당 등급 없음")

            st.markdown("##### ⚪ C등급 (70% 미만)")
            if grade_c:
                st.warning(f"{', '.join(map(str, sorted(grade_c)))} ({len(grade_c)}개)")
            else:
                st.info("해당 등급 없음")

        # 상세 테이블
        st.markdown("---")
        st.subheader("📋 상세 신뢰도 테이블")

        table_data = pd.DataFrame([
            {
                '순위': data['rank'],
                '번호': num,
                '신뢰도(%)': f"{data['confidence']:.1f}%",
                '점수': f"{data['score']:.1f}",
                '등급': 'S' if data['confidence'] >= 90 else
                       'A' if data['confidence'] >= 80 else
                       'B' if data['confidence'] >= 70 else 'C'
            }
            for num, data in sorted_numbers
        ])

        st.dataframe(table_data, use_container_width=True, hide_index=True)

        # 활용 가이드
        st.markdown("---")
        st.info("""
        💡 **신뢰도 점수 활용 가이드**:
        - **S/A 등급**: 핵심 후보군, 코어 번호로 활용 권장
        - **B 등급**: 보조 번호로 활용 가능
        - **C 등급**: 신중하게 선택 (하지만 가끔 예상 밖의 번호가 나오기도 함)
        - 신뢰도가 높다고 반드시 나오는 것은 아니며, 통계적 확률을 나타냅니다.
        """)


# 메인 앱
def main():
    """메인 앱"""
    # 데이터 로드
    try:
        loader = load_lotto_data()
        model = load_prediction_model(loader)
        recommender = load_recommender(model, _version="v3.1")
    except Exception as e:
        st.error(f"❌ 데이터 로딩 오류: {str(e)}")
        st.stop()

    # 사이드바 메뉴
    menu = sidebar(loader)

    # 페이지 라우팅
    if menu == "🏠 홈":
        home_page(loader)
    elif menu == "📊 데이터 탐색":
        data_exploration_page(loader)
    elif menu == "🎯 번호 추천":
        recommendation_page(loader, model, recommender)
    elif menu == "🔍 번호 분석":
        number_analysis_page(loader, model)
    elif menu == "🤖 예측 모델":
        prediction_model_page(loader, model)
    elif menu == "🎨 그리드 패턴":
        grid_pattern_page(loader)
    elif menu == "🖼️ 이미지 패턴":
        image_pattern_page(loader)
    elif menu == "🎲 번호 테마":
        number_theme_page(loader, model, recommender)


if __name__ == "__main__":
    main()
