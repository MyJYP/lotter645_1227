# 백테스팅 3개/4개 기준 동시 지원 계획서

## 📋 개요

현재 3개 기준만 지원하는 백테스팅 시스템을 **3개 기준과 4개 기준을 동시에 제공**하도록 확장하는 계획서입니다.

---

## ✅ 구현 방안

### 방안 1: 서브 탭 방식 (권장) ⭐

**"📊 백테스팅 결과" 탭 내부에 서브 탭 추가**

```
📊 백테스팅 결과
  ├─ 📈 3개 이상 일치 (5등 기준)
  └─ 🎯 4개 이상 일치 (4등 기준)
```

**장점:**
- 기존 구조 유지
- 사용자가 쉽게 비교 가능
- UI가 깔끔함

**단점:**
- 탭이 한 단계 더 깊어짐

---

### 방안 2: 섹션 분리 방식

**각 탭 내부에 섹션으로 구분**

```
📊 백테스팅 결과
  ├─ 📈 3개 이상 일치 결과
  └─ 🎯 4개 이상 일치 결과
```

**장점:**
- 한 화면에서 비교 가능
- 스크롤만으로 확인

**단점:**
- 화면이 길어질 수 있음

---

### 방안 3: 기준 선택 드롭다운

**탭 상단에 기준 선택 옵션 추가**

```
📊 백테스팅 결과
  [기준 선택: 3개 이상 ▼] [4개 이상 ▼]
```

**장점:**
- 가장 간단한 구현
- 동적 전환 가능

**단점:**
- 두 기준을 동시에 비교하기 어려움

---

## 🎯 권장 방안: 서브 탭 방식

**구조:**
```
🔬 백테스팅 결과 (메인 페이지)
  ├─ 📊 백테스팅 결과 (Tab 1)
  │    ├─ 📈 3개 이상 일치 (서브 탭 1)
  │    └─ 🎯 4개 이상 일치 (서브 탭 2)
  ├─ ⚙️ 가중치 최적화 (Tab 2)
  │    ├─ 📈 3개 기준 최적화 (서브 탭 1)
  │    └─ 🎯 4개 기준 최적화 (서브 탭 2)
  └─ 🚀 실시간 재학습 (Tab 3)
       ├─ 📈 3개 기준 재학습 (서브 탭 1)
       └─ 🎯 4개 기준 재학습 (서브 탭 2)
```

---

## 📝 상세 구현 계획

### 1단계: 백테스팅 시스템 확장

**파일**: `src/backtesting_system.py`

#### 1.1 `__init__` 메서드에 `match_threshold` 파라미터 추가

```python
def __init__(self, data_path, cache_dir="Data/backtesting_cache", match_threshold=3):
    """
    Args:
        match_threshold: 일치 기준 (3 또는 4, 기본값 3)
    """
    self.match_threshold = match_threshold
    # ... 기존 코드
```

#### 1.2 `backtest_single_round()` 메서드 수정

```python
def backtest_single_round(self, target_round, weights, strategy='score',
                          n_combinations=10, seed=42):
    # ... 기존 코드
    
    # 동적으로 기준 적용
    has_match = max_match >= self.match_threshold
    
    return {
        'round': target_round,
        'predicted': predicted,
        'actual': actual,
        'matches': matches,
        'max_match': max_match,
        f'has_{self.match_threshold}plus': has_match  # 동적 키
    }
```

#### 1.3 `calculate_metrics()` 메서드 수정

```python
def calculate_metrics(self, results):
    # ... 기존 코드
    
    # 동적으로 기준 적용
    threshold_key = f'has_{self.match_threshold}plus'
    count_match = sum(1 for r in results if r.get(threshold_key, False))
    rate_match = count_match / total_rounds * 100
    
    return {
        'total_rounds': total_rounds,
        f'count_{self.match_threshold}plus': count_match,
        f'rate_{self.match_threshold}plus': rate_match,
        'avg_match': avg_match,
        'max_match_overall': max(r['max_match'] for r in results),
        'match_distribution': match_counts,
        'match_threshold': self.match_threshold  # 기준 정보 포함
    }
```

#### 1.4 `print_metrics()` 메서드 수정

```python
def print_metrics(self, metrics):
    threshold = metrics.get('match_threshold', 3)
    count_key = f'count_{threshold}plus'
    rate_key = f'rate_{threshold}plus'
    
    print(f"\n⭐ {threshold}개 이상 일치율: {metrics[rate_key]:.2f}% ({metrics[count_key]}회)")
    
    # 무작위 기준선 (3개: 1.87%, 4개: 0.15%)
    baseline = 1.87 if threshold == 3 else 0.15
    improvement = metrics[rate_key] - baseline
    # ... 기존 코드
```

---

### 2단계: 가중치 최적화기 확장

**파일**: `src/weight_optimizer.py`

#### 2.1 `__init__` 메서드에 `match_threshold` 추가

```python
def __init__(self, backtester, strategy='score', match_threshold=3):
    """
    Args:
        match_threshold: 일치 기준 (3 또는 4)
    """
    self.backtester = backtester
    self.strategy = strategy
    self.match_threshold = match_threshold
    # ... 기존 코드
```

#### 2.2 `evaluate_weights()` 메서드 수정

```python
def evaluate_weights(self, weights, rounds, n_combinations=10):
    results = self.backtester.backtest_multiple_rounds(
        rounds, weights, self.strategy, n_combinations,
        seed=42, use_cache=True
    )
    
    metrics = self.backtester.calculate_metrics(results)
    rate_key = f'rate_{self.match_threshold}plus'
    return metrics[rate_key]
```

#### 2.3 저장 파일명에 기준 포함

```python
def save_optimal_weights(self, weights, score):
    # 파일명에 기준 포함
    filename = f"optimal_weights_{self.strategy}_{self.match_threshold}plus.json"
    latest_file = self.backtester.cache_dir / filename
    # ... 기존 코드
```

---

### 3단계: 웹 UI 수정

**파일**: `src/web_app.py`

#### 3.1 백테스팅 결과 탭에 서브 탭 추가

```python
# Tab 1: 백테스팅 결과 표시
with tab1:
    st.header("백테스팅 결과")
    
    # 서브 탭 추가
    sub_tab1, sub_tab2 = st.tabs([
        "📈 3개 이상 일치 (5등 기준)",
        "🎯 4개 이상 일치 (4등 기준)"
    ])
    
    # 서브 탭 1: 3개 기준
    with sub_tab1:
        display_backtesting_results(loader, match_threshold=3, cache_dir=cache_dir)
    
    # 서브 탭 2: 4개 기준
    with sub_tab2:
        display_backtesting_results(loader, match_threshold=4, cache_dir=cache_dir)
```

#### 3.2 결과 표시 함수 분리

```python
def display_backtesting_results(loader, match_threshold, cache_dir):
    """백테스팅 결과 표시 (재사용 가능한 함수)"""
    weights_file = cache_dir / f"optimal_weights_score_{match_threshold}plus.json"
    
    if not weights_file.exists():
        st.info(f"아직 {match_threshold}개 기준 백테스팅을 실행하지 않았습니다.")
        return
    
    # 최적 가중치 로드
    with open(weights_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 기준에 따른 설명
    if match_threshold == 3:
        st.info("📈 **3개 이상 일치 기준** (5등 당첨 기준, 무작위: 1.87%)")
    else:
        st.info("🎯 **4개 이상 일치 기준** (4등 당첨 기준, 무작위: 0.15%)")
    
    # 메트릭 표시
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(f"{match_threshold}개 이상 일치율", f"{data['score']:.2f}%")
    # ... 기존 코드
```

#### 3.3 가중치 최적화 탭에 서브 탭 추가

```python
# Tab 2: 가중치 최적화 실행
with tab2:
    st.header("⚙️ 가중치 최적화")
    
    # 프리미엄 접근 권한 확인
    if not check_premium_access():
        show_premium_unlock_ui()
        return
    
    # 서브 탭 추가
    sub_tab1, sub_tab2 = st.tabs([
        "📈 3개 기준 최적화",
        "🎯 4개 기준 최적화"
    ])
    
    # 서브 탭 1: 3개 기준
    with sub_tab1:
        display_optimization_ui(loader, match_threshold=3, cache_dir=cache_dir)
    
    # 서브 탭 2: 4개 기준
    with sub_tab2:
        display_optimization_ui(loader, match_threshold=4, cache_dir=cache_dir)
```

#### 3.4 최적화 UI 함수 분리

```python
def display_optimization_ui(loader, match_threshold, cache_dir):
    """가중치 최적화 UI (재사용 가능한 함수)"""
    st.info(f"""
    💡 **{match_threshold}개 기준 최적화 프로세스**:
    1. Random Search: 무작위로 가중치 조합을 시도하여 최적점 탐색
    2. 정밀 Grid Search (옵션): 최적점 주변을 정밀 탐색
    3. 백테스팅: 각 가중치로 과거 데이터 예측 후 실제와 비교
    4. {match_threshold}개 이상 일치율 기준으로 최적 가중치 선택
    """)
    
    # ... 기존 최적화 UI 코드
    # 백테스팅 시스템 초기화 시 match_threshold 전달
    backtester = BacktestingSystem(data_path, cache_dir=str(cache_dir), 
                                   match_threshold=match_threshold)
    optimizer = WeightOptimizer(backtester, strategy='score', 
                                match_threshold=match_threshold)
    # ... 기존 코드
```

#### 3.5 실시간 재학습 탭에 서브 탭 추가

```python
# Tab 3: 실시간 재학습
with tab3:
    st.header("🚀 실시간 재학습")
    
    # 프리미엄 접근 권한 확인
    if not check_premium_access():
        show_premium_unlock_ui()
        return
    
    # 서브 탭 추가
    sub_tab1, sub_tab2 = st.tabs([
        "📈 3개 기준 재학습",
        "🎯 4개 기준 재학습"
    ])
    
    # 서브 탭 1: 3개 기준
    with sub_tab1:
        display_retraining_ui(loader, match_threshold=3, cache_dir=cache_dir)
    
    # 서브 탭 2: 4개 기준
    with sub_tab2:
        display_retraining_ui(loader, match_threshold=4, cache_dir=cache_dir)
```

---

## 📊 파일 구조 변경

### 캐시 파일 구조

```
Data/backtesting_cache/
  ├─ optimal_weights_score_3plus.json      # 3개 기준 최적 가중치
  ├─ optimal_weights_score_4plus.json      # 4개 기준 최적 가중치
  ├─ score_w30-30-20-20_3plus.json        # 3개 기준 백테스팅 캐시
  └─ score_w30-30-20-20_4plus.json         # 4개 기준 백테스팅 캐시
```

### 캐시 키 생성 수정

```python
# backtesting_system.py
cache_key = f"{strategy}_w{weights['freq_weight']:.0f}-{weights['trend_weight']:.0f}-{weights['absence_weight']:.0f}-{weights['hotness_weight']:.0f}_{self.match_threshold}plus"
```

---

## ⚠️ 주의사항

### 1. 기존 데이터 호환성

- 기존 `optimal_weights_score.json` 파일은 3개 기준으로 간주
- 마이그레이션 스크립트로 이름 변경 권장

### 2. 캐시 무효화

- 3개 기준 캐시와 4개 기준 캐시는 별도로 관리
- 기준 변경 시 해당 기준의 캐시만 사용

### 3. 성능

- 두 기준을 동시에 실행하면 시간이 2배 소요될 수 있음
- 사용자가 선택적으로 실행하도록 UI 구성

---

## 🚀 구현 순서

1. **백테스팅 시스템 확장** (`backtesting_system.py`)
   - `match_threshold` 파라미터 추가
   - 동적 메트릭 계산

2. **가중치 최적화기 확장** (`weight_optimizer.py`)
   - `match_threshold` 파라미터 추가
   - 파일명에 기준 포함

3. **웹 UI 수정** (`web_app.py`)
   - 서브 탭 추가
   - 함수 분리 및 재사용

4. **테스트**
   - 3개 기준 테스트
   - 4개 기준 테스트
   - 동시 실행 테스트

---

## 📝 체크리스트

### 백테스팅 시스템
- [ ] `match_threshold` 파라미터 추가
- [ ] `backtest_single_round()` 동적 기준 적용
- [ ] `calculate_metrics()` 동적 메트릭 계산
- [ ] `print_metrics()` 동적 출력
- [ ] 캐시 키에 기준 포함

### 가중치 최적화기
- [ ] `match_threshold` 파라미터 추가
- [ ] 파일명에 기준 포함
- [ ] 출력 메시지 동적 변경

### 웹 UI
- [ ] 백테스팅 결과 탭에 서브 탭 추가
- [ ] 가중치 최적화 탭에 서브 탭 추가
- [ ] 실시간 재학습 탭에 서브 탭 추가
- [ ] 결과 표시 함수 분리
- [ ] 최적화 UI 함수 분리
- [ ] 재학습 UI 함수 분리

### 테스트
- [ ] 3개 기준 단위 테스트
- [ ] 4개 기준 단위 테스트
- [ ] 웹 UI 동작 확인
- [ ] 캐시 동작 확인

---

## 💡 추가 개선 사항

### 비교 기능 추가

두 기준을 한 화면에서 비교하는 기능:

```python
with st.expander("📊 3개 vs 4개 기준 비교"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("3개 기준")
        # 3개 기준 결과 표시
    
    with col2:
        st.subheader("4개 기준")
        # 4개 기준 결과 표시
```

---

## 📅 예상 소요 시간

- **백테스팅 시스템 확장**: 2-3시간
- **가중치 최적화기 확장**: 1-2시간
- **웹 UI 수정**: 3-4시간
- **테스트**: 2-3시간
- **총 예상 시간**: 8-12시간

---

## ✅ 결론

**3개 기준과 4개 기준을 동시에 제공하는 것이 가능하며, 서브 탭 방식으로 구현하는 것을 권장합니다.**

이 방식의 장점:
- 기존 기능 유지
- 사용자가 선택적으로 사용 가능
- 두 기준을 쉽게 비교 가능
- 확장성 좋음 (나중에 5개 기준 추가도 가능)

