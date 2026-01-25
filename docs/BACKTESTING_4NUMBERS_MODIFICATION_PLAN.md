# 백테스팅 4개 번호 수정 계획서

## 📋 개요

현재 백테스팅 시스템은 **3개 이상 일치율**을 기준으로 성능을 평가하고 있습니다.
이를 **4개 이상 일치율**로 변경하는 수정 계획서입니다.

---

## ✅ 수정 가능 여부

**✅ 수정 가능합니다.**

현재 코드 구조상 3개 기준이 하드코딩되어 있지만, 모든 관련 부분을 체계적으로 수정하면 4개 기준으로 변경 가능합니다.

---

## 🔍 현재 상태 분석

### 영향받는 파일 목록

1. **`src/backtesting_system.py`** (핵심 로직)
   - `backtest_single_round()`: `has_3plus` 계산
   - `calculate_metrics()`: `count_3plus`, `rate_3plus` 계산`
   - `print_metrics()`: "3개 이상 일치율" 출력

2. **`src/weight_optimizer.py`** (최적화)
   - `evaluate_weights()`: `rate_3plus` 반환
   - 주석 및 출력 메시지

3. **`src/web_app.py`** (웹 UI)
   - 백테스팅 페이지 설명 텍스트
   - 메트릭 표시
   - 차트 및 테이블 레이블

4. **`src/recommendation_system.py`** (추천 시스템)
   - 최적 가중치 로드 시 출력 메시지

---

## 📝 상세 수정 계획

### 1단계: 백테스팅 시스템 핵심 로직 수정

**파일**: `src/backtesting_system.py`

#### 1.1 `backtest_single_round()` 메서드 수정

**위치**: Line 61-125

**변경 사항**:
```python
# 변경 전
has_3plus = max_match >= 3

return {
    ...
    'has_3plus': has_3plus
}

# 변경 후
has_4plus = max_match >= 4

return {
    ...
    'has_4plus': has_4plus
}
```

#### 1.2 `calculate_metrics()` 메서드 수정

**위치**: Line 179-226

**변경 사항**:
```python
# 변경 전
'count_3plus': 3개 이상 일치 회차 수,
'rate_3plus': 3개 이상 일치율 (%),

count_3plus = sum(1 for r in results if r['has_3plus'])
rate_3plus = count_3plus / total_rounds * 100

return {
    ...
    'count_3plus': count_3plus,
    'rate_3plus': rate_3plus,
    ...
}

# 변경 후
'count_4plus': 4개 이상 일치 회차 수,
'rate_4plus': 4개 이상 일치율 (%),

count_4plus = sum(1 for r in results if r['has_4plus'])
rate_4plus = count_4plus / total_rounds * 100

return {
    ...
    'count_4plus': count_4plus,
    'rate_4plus': rate_4plus,
    ...
}
```

#### 1.3 `print_metrics()` 메서드 수정

**위치**: Line 228-260

**변경 사항**:
```python
# 변경 전
print(f"\n⭐ 3개 이상 일치율: {metrics['rate_3plus']:.2f}% ({metrics['count_3plus']}회)")

baseline = 1.87  # 무작위 기준선 (3개 이상)
improvement = metrics['rate_3plus'] - baseline

# 변경 후
print(f"\n⭐ 4개 이상 일치율: {metrics['rate_4plus']:.2f}% ({metrics['count_4plus']}회)")

baseline = 0.15  # 무작위 기준선 (4개 이상, 약 0.15%)
improvement = metrics['rate_4plus'] - baseline
```

**참고**: 무작위 기준선 계산
- 3개 이상: 약 1.87%
- 4개 이상: 약 0.15% (C(6,4) * C(39,2) / C(45,6) ≈ 0.15%)

---

### 2단계: 가중치 최적화기 수정

**파일**: `src/weight_optimizer.py`

#### 2.1 `evaluate_weights()` 메서드 수정

**위치**: Line 40-57

**변경 사항**:
```python
# 변경 전
Returns:
    float: 3개 이상 일치율 (%)

return metrics['rate_3plus']

# 변경 후
Returns:
    float: 4개 이상 일치율 (%)

return metrics['rate_4plus']
```

#### 2.2 출력 메시지 수정

**위치**: Line 87, 102, 128, 155 등

**변경 사항**:
- "3개 이상 일치율" → "4개 이상 일치율"
- 모든 관련 주석 및 출력 메시지 업데이트

---

### 3단계: 웹 애플리케이션 UI 수정

**파일**: `src/web_app.py`

#### 3.1 백테스팅 페이지 설명 수정

**위치**: Line 2024-2031

**변경 사항**:
```python
# 변경 전
- **기준**: 3개 이상 일치율 (4등 당첨 기준)
- **무작위 기준선**: 1.87%

# 변경 후
- **기준**: 4개 이상 일치율 (3등 당첨 기준)
- **무작위 기준선**: 0.15%
```

#### 3.2 메트릭 표시 수정

**위치**: Line 2059, 2063, 2124, 2142, 2159, 2293 등

**변경 사항**:
```python
# 변경 전
st.metric("3개 이상 일치율", f"{data['score']:.2f}%")

# 변경 후
st.metric("4개 이상 일치율", f"{data['score']:.2f}%")
```

#### 3.3 가중치 최적화 탭 설명 수정

**위치**: Line 2139-2142, 2159

**변경 사항**:
```python
# 변경 전
- 3개 이상 일치율을 극대화하는 가중치 발견
4. 3개 이상 일치율 기준으로 최적 가중치 선택

# 변경 후
- 4개 이상 일치율을 극대화하는 가중치 발견
4. 4개 이상 일치율 기준으로 최적 가중치 선택
```

#### 3.4 차트 및 테이블 레이블 수정

**위치**: Line 2124, 2125 등

**변경 사항**:
- 모든 차트의 "3개 이상" → "4개 이상"으로 변경
- 기준선 주석도 업데이트

---

### 4단계: 추천 시스템 수정

**파일**: `src/recommendation_system.py`

#### 4.1 최적 가중치 로드 메시지 수정

**위치**: Line 627 (추정)

**변경 사항**:
```python
# 변경 전
print(f"  최적 가중치 로드 (3개 이상 일치율: {data['score']:.2f}%)")

# 변경 후
print(f"  최적 가중치 로드 (4개 이상 일치율: {data['score']:.2f}%)")
```

---

## ⚠️ 주의사항

### 1. 무작위 기준선 변경

**3개 기준**: 약 1.87%
**4개 기준**: 약 0.15%

4개 기준은 훨씬 더 엄격한 기준이므로:
- 성능 지표가 크게 낮아질 수 있음
- 무작위 대비 개선도 측정이 더 어려움
- 하지만 더 의미 있는 성능 평가 가능 (3등 당첨 기준)

### 2. 기존 최적 가중치 파일

기존에 저장된 `optimal_weights_score.json` 파일은 3개 기준으로 최적화된 것이므로:
- **새로 최적화를 실행해야 함**
- 기존 파일은 히스토리로 보관하거나 삭제 가능

### 3. 캐시 파일

백테스팅 캐시 파일(`backtesting_cache/*.json`)도 3개 기준으로 생성되었으므로:
- **캐시를 삭제하고 재생성하는 것을 권장**
- 또는 캐시 키에 버전 정보를 추가하여 구분

### 4. 테스트 필요

수정 후 다음을 테스트해야 함:
- 백테스팅 단일 회차 테스트
- 여러 회차 백테스팅 테스트
- 가중치 최적화 실행 테스트
- 웹 UI 표시 확인

---

## 📊 예상 변경 결과

### 성능 지표 변화

| 항목 | 3개 기준 | 4개 기준 | 변화 |
|------|---------|---------|------|
| 무작위 기준선 | 1.87% | 0.15% | -92% |
| 예상 일치율 | 2-5% | 0.2-1% | -80% |
| 평가 엄격도 | 보통 | 매우 엄격 | ↑ |

### 장점

1. **더 의미 있는 평가**: 3등 당첨 기준으로 실제 당첨에 가까운 평가
2. **엄격한 검증**: 더 높은 품질의 알고리즘만 통과
3. **실용성 향상**: 실제 당첨 가능성에 더 가까운 지표

### 단점

1. **낮은 성공률**: 일치율이 크게 낮아져서 개선도 측정이 어려울 수 있음
2. **최적화 어려움**: 더 엄격한 기준으로 최적화가 어려울 수 있음
3. **사용자 혼란**: 기존 사용자가 낮은 수치에 당황할 수 있음

---

## 🚀 구현 순서

1. **백테스팅 시스템 수정** (`backtesting_system.py`)
   - 가장 핵심적인 변경
   - 모든 다른 모듈이 의존하는 부분

2. **가중치 최적화기 수정** (`weight_optimizer.py`)
   - 백테스팅 시스템에 의존

3. **웹 UI 수정** (`web_app.py`)
   - 사용자에게 보이는 부분

4. **추천 시스템 수정** (`recommendation_system.py`)
   - 부가적인 출력 메시지

5. **테스트 및 검증**
   - 단위 테스트
   - 통합 테스트
   - UI 확인

---

## 📝 체크리스트

### 코드 수정
- [ ] `backtesting_system.py`: `has_3plus` → `has_4plus`
- [ ] `backtesting_system.py`: `count_3plus` → `count_4plus`
- [ ] `backtesting_system.py`: `rate_3plus` → `rate_4plus`
- [ ] `backtesting_system.py`: 무작위 기준선 1.87% → 0.15%
- [ ] `weight_optimizer.py`: `rate_3plus` → `rate_4plus`
- [ ] `weight_optimizer.py`: 모든 출력 메시지 업데이트
- [ ] `web_app.py`: 모든 UI 텍스트 "3개" → "4개"
- [ ] `web_app.py`: 무작위 기준선 업데이트
- [ ] `recommendation_system.py`: 출력 메시지 업데이트

### 테스트
- [ ] 단일 회차 백테스팅 테스트
- [ ] 여러 회차 백테스팅 테스트
- [ ] 가중치 최적화 실행 테스트
- [ ] 웹 UI 표시 확인
- [ ] 캐시 동작 확인

### 문서화
- [ ] README.md 업데이트 (선택)
- [ ] 주석 업데이트
- [ ] 변경 이력 기록

---

## 💡 추가 고려사항

### 옵션 1: 설정 가능한 기준

3개/4개를 선택할 수 있도록 설정 옵션 추가:
```python
class BacktestingSystem:
    def __init__(self, data_path, cache_dir="Data/backtesting_cache", 
                 match_threshold=4):  # 기본값 4개
        self.match_threshold = match_threshold
```

### 옵션 2: 다중 기준 지원

3개, 4개, 5개 등 여러 기준을 동시에 평가:
```python
return {
    'rate_3plus': ...,
    'rate_4plus': ...,
    'rate_5plus': ...,
}
```

---

## 📅 예상 소요 시간

- **코드 수정**: 1-2시간
- **테스트**: 1-2시간
- **문서화**: 30분
- **총 예상 시간**: 3-4시간

---

## ✅ 결론

**4개 번호 기준으로 수정 가능하며, 위 계획서에 따라 체계적으로 수정하면 됩니다.**

다만, 4개 기준은 훨씬 엄격하므로 성능 지표가 크게 낮아질 수 있음을 인지하고 진행해야 합니다.

