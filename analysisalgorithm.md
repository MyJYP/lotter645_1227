# 로또 645 분석 및 추천 시스템 알고리즘 문서

**작성일**: 2025-12-31
**프로젝트**: 로또 645 데이터 분석 및 번호 추천 시스템
**데이터 범위**: 601회차 ~ 1203회차 (총 603회차)

---

## 📋 목차

1. [데이터 로드 및 전처리](#1-데이터-로드-및-전처리)
2. [기본 통계 분석](#2-기본-통계-분석)
3. [시계열 분석](#3-시계열-분석)
4. [조합 패턴 분석](#4-조합-패턴-분석)
5. [연속 번호 분석](#5-연속-번호-분석)
6. [그리드 패턴 분석](#6-그리드-패턴-분석)
7. [머신러닝 예측 모델](#7-머신러닝-예측-모델)
8. [번호 추천 시스템](#8-번호-추천-시스템)

---

## 1. 데이터 로드 및 전처리

### 1.1 데이터 로딩 알고리즘

**파일**: `data_loader.py`

#### 알고리즘 설명

CSV 파일에서 로또 데이터를 읽고 전처리하는 과정입니다.

**단계:**
1. **인코딩 처리**: UTF-8-SIG 우선, 실패 시 CP949로 대체
2. **헤더 처리**: 첫 번째 행(깨진 헤더) 건너뛰고 두 번째 행을 헤더로 사용
3. **숫자 변환**: 쉼표 제거 후 float 타입으로 변환
4. **날짜 변환**: 문자열을 datetime 타입으로 변환
5. **결측치 제거**: 회차 컬럼에 결측치가 있는 행 제거

```python
try:
    df = pd.read_csv(path, encoding='utf-8-sig', skiprows=1)
except UnicodeDecodeError:
    df = pd.read_csv(path, encoding='cp949', skiprows=1)

# 숫자 컬럼 전처리
df[col] = df[col].astype(str).str.replace(',', '').astype(float)

# 날짜 변환
df['일자'] = pd.to_datetime(df['일자'], errors='coerce')
```

### 1.2 번호 추출 알고리즘

**목적**: 당첨번호를 구조화된 형태로 추출

**알고리즘:**
- 각 회차에서 당첨번호 6개와 보너스번호 1개 추출
- 정렬된 리스트로 변환하여 저장

```python
winning_numbers = sorted([
    int(row['당첨번호#1']), int(row['당첨번호#2']),
    int(row['당첨번호#3']), int(row['당첨번호#4']),
    int(row['당첨번호#5']), int(row['당첨번호#6'])
])
bonus_number = int(row['당첨번호#7'])
```

---

## 2. 기본 통계 분석

### 2.1 번호별 출현 빈도 분석

**파일**: `basic_stats.py`

#### 알고리즘: 빈도 계산 (Frequency Counting)

**사용 도구**: `collections.Counter`

**단계:**
1. 모든 회차의 당첨번호를 1차원 리스트로 평탄화
2. Counter를 사용하여 각 번호(1-45)의 출현 횟수 계산
3. 출현율 계산: `출현율 = (출현횟수 / 총 회차 수) × 100`

**복잡도**: O(n), n = 총 회차 수 × 6

```python
all_numbers = []
for _, row in numbers_df.iterrows():
    all_numbers.extend(row['당첨번호'])

frequency = Counter(all_numbers)  # {번호: 출현횟수}
출현율 = (출현횟수 / 총회차수) × 100
```

### 2.2 구간별 분석 알고리즘

**알고리즘**: 범위 기반 필터링

**구간 정의:**
- 저구간: 1 ≤ n ≤ 15
- 중구간: 16 ≤ n ≤ 30
- 고구간: 31 ≤ n ≤ 45

**수식:**
```
비율 = (구간 출현 횟수 / 전체 출현 횟수) × 100
```

**구현:**
```python
low = [n for n in all_numbers if 1 <= n <= 15]
mid = [n for n in all_numbers if 16 <= n <= 30]
high = [n for n in all_numbers if 31 <= n <= 45]

구간_비율 = len(구간) / len(all_numbers) × 100
```

### 2.3 홀짝 분석 알고리즘

**알고리즘**: 모듈로 연산 (Modulo Operation)

**수식:**
```
홀수: n % 2 == 1
짝수: n % 2 == 0
```

**회차별 홀짝 분포:**
```python
for _, row in numbers_df.iterrows():
    nums = row['당첨번호']
    odd_count = sum(1 for n in nums if n % 2 == 1)
    even_count = 6 - odd_count
```

### 2.4 연속 번호 검출 알고리즘

**알고리즘**: 순차 비교 (Sequential Comparison)

**단계:**
1. 당첨번호를 오름차순 정렬
2. 인접한 두 번호의 차이가 1인지 확인
3. 연속 쌍의 개수 카운트

**수식:**
```
연속 검출: nums[i+1] - nums[i] == 1
```

**구현:**
```python
nums = sorted(row['당첨번호'])
consecutive = 0

for i in range(len(nums) - 1):
    if nums[i+1] - nums[i] == 1:
        consecutive += 1
```

**복잡도**: O(n log n) (정렬) + O(n) (비교) = O(n log n)

### 2.5 합계 분석 알고리즘

**통계량 계산:**

**평균 (Mean):**
```
μ = Σ(당첨번호 합계) / 총 회차 수
```

**표준편차 (Standard Deviation):**
```
σ = √[Σ(x - μ)² / n]
```

**사분위수 (Quartiles):**
- Q1 (25th percentile)
- Q2 (50th percentile, Median)
- Q3 (75th percentile)

**구현:**
```python
sums = [sum(row['당첨번호']) for _, row in numbers_df.iterrows()]

평균 = np.mean(sums)
중앙값 = np.median(sums)
표준편차 = np.std(sums)
최소값 = min(sums)
최대값 = max(sums)
```

---

## 3. 시계열 분석

### 3.1 핫넘버/콜드넘버 분석

**파일**: `time_series.py`

#### 알고리즘: 윈도우 기반 빈도 분석

**파라미터:**
- `recent_rounds`: 최근 N회차 (기본값: 50 또는 100)
- `top_n`: 상위/하위 N개 번호 (기본값: 10)

**단계:**
1. 최근 N회차 데이터 슬라이싱
2. 해당 기간 내 번호별 출현 빈도 계산
3. 빈도 기준 내림차순/오름차순 정렬

**수식:**
```
핫넘버 출현율 = (최근 N회차 출현횟수 / N) × 100
콜드넘버: 출현율이 가장 낮은 번호
```

**구현:**
```python
recent_data = numbers_df.head(recent_rounds)

all_numbers = []
for _, row in recent_data.iterrows():
    all_numbers.extend(row['당첨번호'])

frequency = Counter(all_numbers)

# 핫넘버: 가장 많이 출현
hot_numbers = frequency.most_common(top_n)

# 콜드넘버: 가장 적게 출현
cold_numbers = frequency.most_common()[-top_n:]
```

**복잡도**: O(N × 6), N = recent_rounds

### 3.2 출현 간격 분석 알고리즘

**목적**: 특정 번호의 평균 출현 간격 및 미출현 기간 계산

**알고리즘:**

1. **출현 회차 수집:**
```python
appearance_rounds = []
for idx, row in numbers_df.iterrows():
    if number in row['당첨번호'] or number == row['보너스번호']:
        appearance_rounds.append(row['회차'])
```

2. **간격 계산:**
```python
intervals = []
for i in range(len(appearance_rounds) - 1):
    interval = appearance_rounds[i] - appearance_rounds[i+1]
    intervals.append(interval)
```

3. **통계량 계산:**
```
평균 간격 = mean(intervals)
최소 간격 = min(intervals)
최대 간격 = max(intervals)
표준편차 = std(intervals)
미출현 기간 = 현재 회차 - 최근 출현 회차
```

### 3.3 이동 평균 빈도 분석 (Rolling Frequency)

**알고리즘**: 슬라이딩 윈도우 (Sliding Window)

**파라미터:**
- `window_size`: 윈도우 크기 (기본값: 100회)
- `step`: 윈도우 이동 간격 (기본값: 10회)

**단계:**
1. 전체 데이터를 윈도우 크기로 슬라이싱
2. 각 윈도우에서 번호별 출현 빈도 계산
3. 최신 윈도우와 과거 윈도우의 평균 비교

**트렌드 변화 계산:**
```
트렌드_변화 = 최근_평균 - 과거_평균

최근_평균 = mean(최근 3개 윈도우의 빈도)
과거_평균 = mean(마지막 3개 윈도우의 빈도)
```

**구현:**
```python
for i in range(0, total_rounds - window_size + 1, step):
    window_data = numbers_df.iloc[i:i+window_size]

    # 윈도우 내 번호별 빈도
    all_numbers = []
    for _, row in window_data.iterrows():
        all_numbers.extend(row['당첨번호'])

    frequency = Counter(all_numbers)

    for num in range(1, 46):
        trends[num].append(frequency.get(num, 0))
```

**복잡도**: O((n/step) × window_size × 6)

---

## 4. 조합 패턴 분석

### 4.1 번호 쌍/트리플 빈도 분석

**파일**: `pattern_analysis.py`

#### 알고리즘: 조합 생성 및 빈도 계산 (Combinations)

**사용 도구**: `itertools.combinations`

**2개 조합 (Pairs):**
```python
from itertools import combinations

all_pairs = []
for _, row in numbers_df.iterrows():
    nums = row['당첨번호']
    pairs = list(combinations(sorted(nums), 2))  # C(6,2) = 15개
    all_pairs.extend(pairs)

pair_freq = Counter(all_pairs)
top_pairs = pair_freq.most_common(top_n)
```

**조합 수학:**
```
C(6, 2) = 6! / (2! × 4!) = 15개의 쌍/회차
C(6, 3) = 6! / (3! × 3!) = 20개의 트리플/회차

총 쌍 개수 = 603회차 × 15 = 9,045개
```

**복잡도**: O(n × C(6,k)), k=2 또는 3

### 4.2 동반 출현 분석 알고리즘

**목적**: 특정 번호와 자주 함께 나오는 번호 찾기

**알고리즘:**
1. 목표 번호가 포함된 회차 필터링
2. 해당 회차의 다른 번호들 수집
3. 빈도 계산 및 정렬

**수식:**
```
동반율 = (동반 출현 횟수 / 목표 번호 총 출현 횟수) × 100
```

**구현:**
```python
companion_numbers = []

for _, row in numbers_df.iterrows():
    nums = row['당첨번호']
    if target_number in nums:
        # 목표 번호를 제외한 나머지 번호
        companion_numbers.extend([n for n in nums if n != target_number])

companion_freq = Counter(companion_numbers)
```

### 4.3 AC값 (복잡도) 분석

**알고리즘**: 차이값 고유 개수 계산

**AC값 정의:**
```
AC값 = |{|nums[i] - nums[j]| : 0 ≤ i < j < 6}| - 5
```

**의미:**
- AC값이 클수록 번호가 고르게 분포
- AC값이 작을수록 번호가 군집

**단계:**
1. 6개 번호의 모든 쌍 조합 생성 (C(6,2) = 15개)
2. 각 쌍의 차이값 절댓값 계산
3. 고유한 차이값 개수 계산
4. AC값 = 고유 개수 - 5

**구현:**
```python
nums = sorted(row['당첨번호'])

differences = set()
for i in range(len(nums)):
    for j in range(i+1, len(nums)):
        diff = abs(nums[i] - nums[j])
        differences.add(diff)

ac_value = len(differences) - 5
```

**예시:**
- 번호: [1, 2, 3, 4, 5, 6]
- 차이값: {1, 2, 3, 4, 5} (5개)
- AC값: 5 - 5 = 0 (매우 군집)

- 번호: [3, 12, 19, 27, 33, 41]
- 차이값: {6, 8, 9, 14, 15, 16, 22, 24, 30, 38} (10개)
- AC값: 10 - 5 = 5 (고르게 분포)

**복잡도**: O(n²), n=6 (고정)

### 4.4 구간 패턴 분석

**알고리즘**: 구간별 개수 조합

**패턴 형식:** `저-중-고`

**예시:**
- `2-2-2`: 저구간 2개, 중구간 2개, 고구간 2개
- `3-1-2`: 저구간 3개, 중구간 1개, 고구간 2개

**구현:**
```python
for _, row in numbers_df.iterrows():
    nums = row['당첨번호']

    low = sum(1 for n in nums if 1 <= n <= 15)
    mid = sum(1 for n in nums if 16 <= n <= 30)
    high = sum(1 for n in nums if 31 <= n <= 45)

    pattern = f"{low}-{mid}-{high}"
    patterns.append(pattern)

pattern_dist = Counter(patterns)
```

---

## 5. 연속 번호 분석

### 5.1 연속 그룹 탐지 알고리즘

**파일**: `consecutive_analysis.py`

#### 알고리즘: 연속 시퀀스 찾기 (Consecutive Sequence Detection)

**단계:**
1. 당첨번호를 오름차순 정렬
2. 인접 번호 비교하여 차이가 1인 경우 그룹에 추가
3. 차이가 1이 아니면 현재 그룹 종료 및 새 그룹 시작
4. 2개 이상의 번호를 포함하는 그룹만 반환

**알고리즘 수식:**
```
연속 조건: nums[i] == nums[i-1] + 1
```

**구현:**
```python
def find_consecutive_groups(numbers):
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
```

**예시:**
- 입력: [3, 17, 18, 19, 25, 40]
- 출력: [[17, 18, 19]]
- 설명: 17-18-19가 3개 연속

**복잡도**: O(n log n) (정렬) + O(n) (그룹 탐지) = O(n log n)

### 5.2 연속 길이별 통계 알고리즘

**통계 항목:**
1. **연속 없음**: 연속 번호가 없는 회차
2. **연속 2개**: 2개 연속 (예: 6-7)
3. **연속 3개**: 3개 연속 (예: 17-18-19)
4. **연속 4개 이상**: 4개 이상 연속 (매우 희귀)

**비율 계산:**
```
연속_비율 = (연속 N개 출현 회차 수 / 총 회차 수) × 100
```

**구현:**
```python
length_counter = Counter()

for _, row in numbers_df.iterrows():
    groups = find_consecutive_groups(row['당첨번호'])

    for group in groups:
        length = len(group)
        length_counter[length] += 1
```

### 5.3 구간별 연속 패턴 분석

**알고리즘**: 구간 필터링 후 연속 검출

**조건:**
- 저구간 연속: 모든 번호가 1 ≤ n ≤ 15
- 중구간 연속: 모든 번호가 16 ≤ n ≤ 30
- 고구간 연속: 모든 번호가 31 ≤ n ≤ 45

**구현:**
```python
for group in consecutive_groups:
    if all(1 <= n <= 15 for n in group):
        section = '저구간'
    elif all(16 <= n <= 30 for n in group):
        section = '중구간'
    elif all(31 <= n <= 45 for n in group):
        section = '고구간'
    else:
        section = '혼합'  # 구간을 넘는 연속
```

---

## 6. 그리드 패턴 분석

### 6.1 7×7 그리드 매핑 알고리즘

**파일**: `grid_pattern_analysis.py`

#### 알고리즘: 2차원 좌표 매핑

**그리드 구조:**
```
번호 1-7   : Row 0, Col 0-6
번호 8-14  : Row 1, Col 0-6
번호 15-21 : Row 2, Col 0-6
...
번호 43-45 : Row 6, Col 0-2
```

**번호 → 좌표 변환:**
```
row = (number - 1) // 7
col = (number - 1) % 7
```

**좌표 → 번호 변환:**
```
number = row × 7 + col + 1
```

**구현:**
```python
number_to_position = {}
number = 1
for row in range(7):
    for col in range(7):
        if number <= 45:
            number_to_position[number] = (row, col)
            number += 1
```

### 6.2 그리드 구역 분류 알고리즘

**구역 정의:**

1. **모서리 (Corner)**: 4칸
   - (0,0), (0,6), (6,0), (6,6)

2. **가장자리 (Edge)**: 20칸
   - row=0 or row=6 or col=0 or col=6 (모서리 제외)

3. **중간 영역 (Middle)**: 12칸
   - 가장자리도 중앙부도 아닌 영역

4. **중앙부 (Center)**: 9칸
   - 2 ≤ row ≤ 4 and 2 ≤ col ≤ 4

**알고리즘:**
```python
def get_zone(row, col):
    if (row, col) in [(0,0), (0,6), (6,0), (6,6)]:
        return "corner"
    elif row == 0 or row == 6 or col == 0 or col == 6:
        return "edge"
    elif 2 <= row <= 4 and 2 <= col <= 4:
        return "center"
    else:
        return "middle"
```

### 6.3 위치별 출현 빈도 히트맵

**알고리즘**: 2차원 배열 카운팅

**단계:**
1. 7×7 배열 초기화 (모든 값 0)
2. 각 회차의 당첨번호를 좌표로 변환
3. 해당 좌표의 카운트 증가

**구현:**
```python
position_heatmap = np.zeros((7, 7))

for _, row in numbers_df.iterrows():
    winning_numbers = row['당첨번호']
    for num in winning_numbers:
        r, c = get_position(num)
        position_heatmap[r, c] += 1
```

**결과 해석:**
- 높은 값: 자주 나오는 위치
- 낮은 값: 드물게 나오는 위치

### 6.4 공간적 군집도 분석 (Spatial Clustering)

**알고리즘**: 맨해튼 거리 (Manhattan Distance)

**맨해튼 거리 정의:**
```
distance(i, j) = |row_i - row_j| + |col_i - col_j|
```

**단계:**
1. 6개 당첨번호의 모든 쌍 조합 생성 (C(6,2) = 15개)
2. 각 쌍의 맨해튼 거리 계산
3. 평균 거리 계산

**수식:**
```
평균_거리 = (Σ distance(i,j)) / C(6,2)

여기서 0 ≤ i < j < 6
```

**구현:**
```python
def calculate_spatial_distance(numbers):
    distances = []

    for i in range(len(numbers)):
        for j in range(i+1, len(numbers)):
            pos1 = number_to_position[numbers[i]]
            pos2 = number_to_position[numbers[j]]

            # 맨해튼 거리
            dist = abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
            distances.append(dist)

    return np.mean(distances)
```

**해석:**
- 평균 거리 2.0~3.0: 매우 군집 (번호들이 가까움)
- 평균 거리 4.0~5.5: 적절한 분산
- 평균 거리 6.0 이상: 매우 분산 (번호들이 멀리 떨어짐)

### 6.5 기하학적 패턴 분석

**알고리즘**: 대각선 및 라인 검출

#### 6.5.1 주 대각선 (Main Diagonal)

**조건:**
```
row == col
```

**해당 번호:** 1, 9, 17, 25, 33, 41 (6개)

#### 6.5.2 반대 대각선 (Anti-Diagonal)

**조건:**
```
row + col == 6
```

**해당 번호:** 7, 13, 19, 25, 31, 37, 43 (7개)

#### 6.5.3 같은 줄 패턴

**가로줄 검출:**
```python
horizontal_counts = defaultdict(int)

for num in winning_numbers:
    row, col = get_position(num)
    horizontal_counts[row] += 1

# 같은 줄에 3개 이상?
for row, count in horizontal_counts.items():
    if count >= 3:
        print(f"Row {row}: {count}개")
```

**세로줄 검출:**
```python
vertical_counts = defaultdict(int)

for num in winning_numbers:
    row, col = get_position(num)
    vertical_counts[col] += 1

if count >= 3:
    print(f"Col {col}: {count}개")
```

---

## 7. 머신러닝 예측 모델

### 7.1 특징 추출 알고리즘

**파일**: `prediction_model.py`

#### 번호별 특징 벡터 생성

**특징 리스트 (9개):**

1. **전체 출현 빈도** (total_frequency)
```
freq(n) = count(n in all_winning_numbers)
```

2. **최근 100회차 출현 빈도** (recent_100_frequency)
```
recent_freq_100(n) = count(n in last_100_rounds)
```

3. **최근 50회차 출현 빈도** (recent_50_frequency)
```
recent_freq_50(n) = count(n in last_50_rounds)
```

4. **부재 기간** (absence_length)
```
absence(n) = 현재_회차 - 마지막_출현_회차
```

5. **평균 출현 간격** (avg_interval)
```
intervals = [appearance[i] - appearance[i+1] for i in range(len-1)]
avg_interval = mean(intervals)
```

6. **출현 간격 표준편차** (std_interval)
```
std_interval = std(intervals)
```

7. **구간** (section)
```
section = {
    0  if 1 ≤ n ≤ 15   (저구간)
    1  if 16 ≤ n ≤ 30  (중구간)
    2  if 31 ≤ n ≤ 45  (고구간)
}
```

8. **홀짝** (odd_even)
```
odd_even = n % 2
```

9. **핫넘버 점수** (hotness_score)
```
hotness = (recent_50_freq / (absence + 1)) × 100
```

**특징 벡터:**
```
features[n] = [total_freq, recent_100, recent_50, absence,
               avg_interval, std_interval, section, odd_even, hotness]
```

### 7.2 종합 점수 계산 알고리즘

**점수 구성 (총 100점):**

1. **빈도 점수** (0-30점)
```
freq_score = min((total_frequency / 100) × 30, 30)
```

2. **최근 트렌드 점수** (0-30점)
```
trend_score = (recent_50_frequency / 50) × 30
```

3. **부재 기간 점수** (0-20점)
```
absence_score = min((absence_length / 20) × 20, 20)
```
- 오래 안 나올수록 높은 점수 (회귀 법칙 반영)

4. **핫넘버 점수** (0-20점)
```
hotness_score = min((hotness / 10) × 20, 20)
```

**총점 계산:**
```
total_score = freq_score + trend_score + absence_score + hotness_score

최대 100점
```

**구현:**
```python
def calculate_number_scores():
    scores = {}

    for num in range(1, 46):
        features = number_features[num]

        # 1. 빈도 점수
        freq_score = min(features['total_frequency'] / 100 * 30, 30)

        # 2. 트렌드 점수
        trend_score = features['recent_50_frequency'] / 50 * 30

        # 3. 부재 기간 점수
        absence_score = min(features['absence_length'] / 20 * 20, 20)

        # 4. 핫넘버 점수
        hotness_score = min(features['hotness_score'] / 10 * 20, 20)

        total = freq_score + trend_score + absence_score + hotness_score

        scores[num] = {
            'total_score': total,
            'freq_score': freq_score,
            'trend_score': trend_score,
            'absence_score': absence_score,
            'hotness_score': hotness_score
        }

    return scores
```

### 7.3 패턴 학습 알고리즘

#### 7.3.1 연속 번호 패턴 학습

**출현 확률 계산:**
```
P(연속 번호) = (연속 번호 포함 회차 수) / (총 회차 수)
```

**인기 연속 쌍 추출:**
```python
consecutive_pairs = defaultdict(int)

for _, row in numbers_df.iterrows():
    nums = sorted(row['당첨번호'])

    for i in range(len(nums)-1):
        if nums[i+1] == nums[i] + 1:
            pair = (nums[i], nums[i+1])
            consecutive_pairs[pair] += 1
```

#### 7.3.2 구간 패턴 학습

**가장 흔한 구간 분포:**
```python
section_patterns = []

for _, row in numbers_df.iterrows():
    nums = row['당첨번호']

    low = sum(1 for n in nums if 1 <= n <= 15)
    mid = sum(1 for n in nums if 16 <= n <= 30)
    high = sum(1 for n in nums if 31 <= n <= 45)

    section_patterns.append((low, mid, high))

most_common = Counter(section_patterns).most_common(10)
```

#### 7.3.3 홀짝 패턴 학습

**가장 흔한 홀짝 분포:**
```python
odd_even_patterns = []

for _, row in numbers_df.iterrows():
    nums = row['당첨번호']
    odd = sum(1 for n in nums if n % 2 == 1)
    even = 6 - odd

    odd_even_patterns.append((odd, even))

most_common_odd_even = Counter(odd_even_patterns).most_common(5)
```

#### 7.3.4 합계 패턴 학습

**통계량:**
```python
sums = [sum(row['당첨번호']) for _, row in numbers_df.iterrows()]

sum_patterns = {
    'mean': np.mean(sums),           # 평균
    'std': np.std(sums),             # 표준편차
    'median': np.median(sums),       # 중앙값
    'q1': np.percentile(sums, 25),   # 1사분위수
    'q3': np.percentile(sums, 75)    # 3사분위수
}
```

### 7.4 확률 가중치 계산

**알고리즘**: 점수 기반 정규화

**수식:**
```
weight(n) = score(n) / Σ score(i)
            i=1 to 45

where Σ weight(n) = 1
      n=1 to 45
```

**구현:**
```python
def get_probability_weights():
    weights = {}
    total_score = sum(score['total_score'] for score in number_scores.values())

    for num, score in number_scores.items():
        weights[num] = score['total_score'] / total_score

    return weights
```

---

## 8. 번호 추천 시스템

### 8.1 점수 기반 추천 알고리즘

**파일**: `recommendation_system.py`

#### 알고리즘: 상위 번호 샘플링 + 점수 최적화

**단계:**

1. **후보 번호 선정:**
```python
top_numbers = get_top_numbers(use_top)  # 상위 20개
```

2. **조합 생성 (Monte Carlo):**
```python
for attempt in range(max_attempts):
    selected = random.sample(top_numbers, 6)

    if is_valid_combination(selected):
        combinations_list.append(tuple(sorted(selected)))
```

3. **점수 계산 및 정렬:**
```python
scored_combos = []
for combo in combinations_list:
    score = calculate_combination_score(combo)
    scored_combos.append((combo, score))

scored_combos.sort(key=lambda x: x[1], reverse=True)
```

**복잡도**: O(max_attempts × 검증_비용)

### 8.2 확률 가중치 기반 추천

**알고리즘**: 가중치 샘플링 (Weighted Sampling)

**NumPy의 가중치 샘플링:**
```python
weights = get_probability_weights()
numbers = list(range(1, 46))
probabilities = [weights[n] for n in numbers]

# 중복 없이 6개 선택
selected = np.random.choice(
    numbers,
    size=6,
    replace=False,
    p=probabilities
)
```

**가중치 정규화:**
```
P(n) = weight(n) / Σ weight(i)
       i=1 to 45

Σ P(i) = 1
i=1 to 45
```

### 8.3 패턴 기반 추천 알고리즘

**목표:** 역사적으로 가장 흔한 패턴에 맞춰 번호 생성

**단계:**

1. **목표 패턴 설정:**
```python
# 가장 흔한 구간 분포
section_pattern = most_common_section[0]  # 예: (2, 2, 2)

# 가장 흔한 홀짝 분포
odd_even_pattern = most_common_odd_even[0]  # 예: (3, 3)
```

2. **구간별 번호 풀 생성:**
```python
top_numbers = get_top_numbers(30)

low_pool = [n for n in top_numbers if 1 <= n <= 15]
mid_pool = [n for n in top_numbers if 16 <= n <= 30]
high_pool = [n for n in top_numbers if 31 <= n <= 45]
```

3. **패턴 맞춤 샘플링:**
```python
selected = []

# 구간 패턴에 맞춰 선택
selected.extend(random.sample(low_pool, section_pattern[0]))
selected.extend(random.sample(mid_pool, section_pattern[1]))
selected.extend(random.sample(high_pool, section_pattern[2]))

# 홀짝 패턴 검증
odd_count = sum(1 for n in selected if n % 2 == 1)
if abs(odd_count - odd_even_pattern[0]) <= 1:  # 오차 허용
    accept(selected)
```

### 8.4 그리드 패턴 기반 추천 알고리즘

**목표:** 그리드 구역 분포 최적화

**그리드 가중치:**
```python
grid_weights = {
    'middle': 1.46,   # 중간 영역 (출현율 가장 높음)
    'center': 1.09,   # 중앙부
    'edge': 0.91,     # 가장자리
    'corner': 0.83    # 모서리 (출현율 가장 낮음)
}
```

**추천 전략:**

1. **중간 영역 우선 선택 (3-4개):**
```python
middle_numbers = [16, 17, 18, 19, 20, 23, 24, 25, 26, 27, 31, 32, 33, 34]
middle_pool = [n for n in middle_numbers if n in top_numbers[:30]]

num_middle = random.choice([3, 4])
selected.extend(random.sample(middle_pool, num_middle))
```

2. **반대 대각선 활용 (1-2개):**
```python
anti_diagonal = [7, 13, 19, 25, 31, 37, 43]
anti_diag_pool = [n for n in anti_diagonal if n not in selected]

num_anti_diag = random.choice([1, 2])
selected.extend(random.sample(anti_diag_pool, num_anti_diag))
```

3. **나머지 채우기 (모서리 제외):**
```python
corner = [1, 7, 43, 45]
remaining_pool = [n for n in top_numbers
                  if n not in selected and n not in corner]

while len(selected) < 6:
    selected.append(random.choice(remaining_pool))
```

4. **평균 거리 검증:**
```python
avg_distance = calculate_spatial_distance(selected)

if 3.5 <= avg_distance <= 6.0:
    accept(selected)
```

### 8.5 그리드 점수 계산 알고리즘

**점수 구성:**

1. **위치 가중치 점수:**
```python
score = 0
for num in numbers:
    zone = get_grid_zone(num)
    weight = grid_weights[zone]
    score += weight * 10
```

2. **중간 영역 보너스:**
```python
middle_count = sum(1 for n in numbers if n in middle_zone)

if 3 <= middle_count <= 4:
    score += 20  # 보너스
```

3. **반대 대각선 보너스:**
```python
anti_diag_count = sum(1 for n in numbers if n in anti_diagonal)

if 1 <= anti_diag_count <= 2:
    score += 15  # 보너스
```

4. **모서리 페널티:**
```python
corner_count = sum(1 for n in numbers if n in corner)

if corner_count >= 2:
    score -= 15  # 감점
```

5. **공간적 군집도 보너스:**
```python
avg_distance = calculate_spatial_distance(numbers)

if 4.0 <= avg_distance <= 5.5:
    score += 20  # 적절한 분산
elif avg_distance < 3.0 or avg_distance > 6.0:
    score -= 10  # 너무 군집/분산
```

### 8.6 조합 점수 계산 알고리즘 (통합)

**전체 점수 구성:**

1. **개별 번호 점수 합:**
```python
score = sum(number_scores[num]['total_score'] for num in numbers)
```

2. **연속 번호 보너스:**
```python
has_consecutive = check_consecutive(numbers)
if has_consecutive:
    score += 10
```

3. **구간 균형 보너스:**
```python
low, mid, high = count_sections(numbers)

if 1 <= low <= 3 and 1 <= mid <= 3 and 1 <= high <= 3:
    score += 15
```

4. **홀짝 균형 보너스:**
```python
odd = sum(1 for n in numbers if n % 2 == 1)

if 2 <= odd <= 4:
    score += 10
```

5. **합계 범위 보너스:**
```python
total = sum(numbers)
mean = sum_patterns['mean']
std = sum_patterns['std']

if mean - std <= total <= mean + std:
    score += 10
```

6. **그리드 패턴 보너스 (가중치 50%):**
```python
grid_score = calculate_grid_score(numbers)
score += grid_score * 0.5
```

**최종 점수:**
```
final_score = base_score + pattern_bonuses + grid_bonus
```

### 8.7 하이브리드 추천 알고리즘

**알고리즘**: 다중 전략 통합 (Ensemble)

**단계:**

1. **각 전략에서 후보 생성:**
```python
score_combos = generate_by_score(n=2)
prob_combos = generate_by_probability(n=2)
pattern_combos = generate_by_pattern(n=2)
grid_combos = generate_grid_based(n=2)
```

2. **중복 제거:**
```python
all_combos = []
for combo in score_combos + prob_combos + pattern_combos + grid_combos:
    sorted_combo = tuple(sorted(combo))
    if sorted_combo not in all_combos:
        all_combos.append(sorted_combo)
```

3. **재점수 계산 및 정렬:**
```python
scored = []
for combo in all_combos:
    score = calculate_combination_score(combo)
    scored.append((combo, score))

scored.sort(key=lambda x: x[1], reverse=True)
```

4. **상위 N개 선정:**
```python
final_recommendations = scored[:n_combinations]
```

**장점:**
- 다양한 전략의 장점 결합
- 과적합 방지
- 높은 품질의 조합 생성

### 8.8 검증 알고리즘

**기본 검증:**
```python
def is_valid_combination(numbers):
    # 1. 개수 확인
    if len(numbers) != 6:
        return False

    # 2. 범위 확인
    if any(n < 1 or n > 45 for n in numbers):
        return False

    # 3. 중복 확인
    if len(set(numbers)) != 6:
        return False

    return True
```

**엄격한 검증 (strict=True):**
```python
def is_valid_combination_strict(numbers):
    if not is_valid_combination(numbers):
        return False

    # 4. 구간 분포 확인
    low, mid, high = count_sections(numbers)
    if max(low, mid, high) > 4:  # 한 구간에 5개 이상 제외
        return False

    # 5. 홀짝 비율 확인
    odd = sum(1 for n in numbers if n % 2 == 1)
    if odd == 0 or odd == 6:  # 0:6 또는 6:0 제외
        return False

    # 6. 연속 4개 이상 제외
    consecutive_count = 0
    sorted_nums = sorted(numbers)
    for i in range(len(sorted_nums)-1):
        if sorted_nums[i+1] == sorted_nums[i] + 1:
            consecutive_count += 1
            if consecutive_count >= 3:  # 4개 연속
                return False
        else:
            consecutive_count = 0

    return True
```

---

## 9. 복잡도 분석 요약

### 시간 복잡도

| 알고리즘 | 복잡도 | 설명 |
|---------|--------|------|
| 데이터 로딩 | O(n) | n = 총 행 수 |
| 번호별 빈도 분석 | O(n × 6) | n = 회차 수 |
| 번호 쌍 빈도 | O(n × C(6,2)) | C(6,2) = 15 |
| 연속 그룹 탐지 | O(n log n) | 정렬 포함 |
| 그리드 매핑 | O(1) | 수식 계산 |
| 특징 추출 | O(45 × n) | 45개 번호 × n회차 |
| 조합 생성 (Monte Carlo) | O(attempts) | 시도 횟수 |
| 조합 점수 계산 | O(1) | 고정 크기 |

### 공간 복잡도

| 자료구조 | 복잡도 | 설명 |
|---------|--------|------|
| 전체 데이터 | O(n × m) | n=회차, m=컬럼 수 |
| 번호 빈도 맵 | O(45) | 고정 크기 |
| 조합 리스트 | O(k) | k=생성 조합 수 |
| 그리드 히트맵 | O(49) | 7×7 고정 |
| 특징 벡터 | O(45 × 9) | 45개 번호 × 9개 특징 |

---

## 10. 주요 수학 공식 요약

### 통계량

**평균 (Mean):**
```
μ = (Σ x_i) / n
```

**표준편차 (Standard Deviation):**
```
σ = √[(Σ (x_i - μ)²) / n]
```

**분산 (Variance):**
```
σ² = (Σ (x_i - μ)²) / n
```

### 확률

**출현율:**
```
P(번호 n) = (출현 횟수) / (총 회차 수)
```

**가중치 정규화:**
```
w_i' = w_i / (Σ w_j)
           j=1 to 45
```

### 거리 함수

**맨해튼 거리:**
```
d(i, j) = |x_i - x_j| + |y_i - y_j|
```

**유클리드 거리:**
```
d(i, j) = √[(x_i - x_j)² + (y_i - y_j)²]
```

### 조합론

**조합 (Combinations):**
```
C(n, k) = n! / (k! × (n-k)!)

C(6, 2) = 15
C(6, 3) = 20
C(45, 6) = 8,145,060
```

---

## 11. 알고리즘 최적화 전략

### 11.1 캐싱 (Caching)

**적용 대상:**
- 특징 추출 결과
- 패턴 학습 결과
- 점수 계산 결과

**구현:**
```python
@functools.lru_cache(maxsize=128)
def get_number_features(number):
    # 계산 비용이 높은 특징 추출
    return features
```

### 11.2 벡터화 (Vectorization)

**NumPy 활용:**
```python
# 비효율적
sums = []
for _, row in df.iterrows():
    sums.append(sum(row['당첨번호']))

# 효율적
sums = df['당첨번호'].apply(sum).values
```

### 11.3 조기 종료 (Early Termination)

**조합 생성 시:**
```python
max_attempts = 10000
attempts = 0

while len(combinations) < n and attempts < max_attempts:
    # 생성 시도
    attempts += 1

    if attempts >= max_attempts:
        break  # 무한 루프 방지
```

### 11.4 인덱싱 (Indexing)

**딕셔너리 활용:**
```python
# O(n) 탐색 대신 O(1) 접근
number_to_position = {num: (row, col) for ...}
position = number_to_position[num]  # O(1)
```

---

## 12. 알고리즘 검증 방법

### 12.1 단위 테스트

```python
def test_consecutive_detection():
    # 테스트 케이스
    assert find_consecutive_groups([1,2,3,10,15]) == [[1,2,3]]
    assert find_consecutive_groups([5,10,15,20,25,30]) == []
    assert find_consecutive_groups([6,7,18,19,20,40]) == [[6,7], [18,19,20]]
```

### 12.2 통계적 검증

**카이제곱 검정 (Chi-Square Test):**
```python
from scipy.stats import chisquare

observed = [빈도 데이터]
expected = [기대 빈도]

statistic, p_value = chisquare(observed, expected)

if p_value < 0.05:
    print("통계적으로 유의한 차이")
```

### 12.3 교차 검증

**시계열 분할:**
```python
# 최근 100회를 테스트 세트로
train_data = numbers_df.iloc[100:]
test_data = numbers_df.iloc[:100]

# 모델 학습
model.train(train_data)

# 예측 성능 평가
accuracy = evaluate(model, test_data)
```

---

## 13. 참고 문헌 및 이론적 배경

### 13.1 확률론

- **큰 수의 법칙 (Law of Large Numbers)**: 시행 횟수가 증가하면 표본 평균이 기댓값에 수렴
- **회귀의 오류 (Gambler's Fallacy)**: 과거 사건이 미래 독립 사건에 영향을 주지 않음

### 13.2 통계 분석

- **기술 통계 (Descriptive Statistics)**: 평균, 중앙값, 표준편차
- **추론 통계 (Inferential Statistics)**: 패턴 인식 및 예측

### 13.3 머신러닝

- **특징 공학 (Feature Engineering)**: 원시 데이터에서 의미 있는 특징 추출
- **앙상블 방법 (Ensemble Methods)**: 여러 모델 결합으로 성능 향상

### 13.4 조합 최적화

- **몬테카를로 방법 (Monte Carlo Method)**: 무작위 샘플링을 통한 근사 해 탐색
- **탐욕 알고리즘 (Greedy Algorithm)**: 각 단계에서 최선의 선택

---

## 14. 결론

본 로또 645 분석 및 추천 시스템은 다음과 같은 다층적 알고리즘을 활용합니다:

1. **데이터 처리**: 효율적인 전처리 및 구조화
2. **통계 분석**: 빈도, 분포, 패턴 인식
3. **시계열 분석**: 트렌드 및 주기성 파악
4. **공간 분석**: 그리드 패턴 및 군집도 분석
5. **머신러닝**: 특징 추출 및 점수 계산
6. **최적화**: 다중 전략 통합 및 검증

모든 알고리즘은 **과거 데이터 기반 패턴 분석**을 목적으로 하며, **로또의 독립 시행 특성**으로 인해 미래 결과를 보장하지 않습니다. 본 시스템은 **교육 및 데이터 분석 학습**을 위한 프로젝트입니다.

---

**문서 버전**: 1.0
**최종 업데이트**: 2025-12-31
**작성자**: Claude AI (Anthropic)
