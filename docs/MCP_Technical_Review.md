# 📋 기술 검토서: 로또 645 서비스의 MCP 서버 구현

**작성일:** 2026년 2월 8일  
**작성자:** Gemini Code Assist  
**대상 프로젝트:** 로또 645 분석 및 추천 시스템 (기존 Streamlit 기반)

---

## 1. 개요 (Executive Summary)

본 문서는 현재 Python(Streamlit, Pandas) 기반으로 운영 중인 로또 645 분석 서비스를 **Model Context Protocol (MCP)** 서버로 구현 가능한지 기술적으로 검토한 결과입니다.

**결론:**  
기존의 데이터 처리 로직(Pandas)과 분석 알고리즘(NumPy, 통계 로직)이 모듈화되어 있어 **MCP 서버로의 전환 및 확장이 매우 용이**합니다. 이를 통해 AI 에이전트가 직접 로또 데이터를 실시간으로 조회하고, 사용자의 자연어 요청에 따라 복잡한 분석을 수행할 수 있습니다.

---

## 2. 기존 아키텍처 vs MCP 아키텍처 비교

| 구분            | 기존 (Streamlit Web App)    | 변경/확장 (MCP Server)                                     |
| :-------------- | :-------------------------- | :--------------------------------------------------------- |
| **사용자**      | 사람 (웹 브라우저 클릭)     | AI 모델 (Claude, Cursor 등)                                |
| **인터페이스**  | 버튼, 슬라이더, 차트 (GUI)  | Tools, Resources, Prompts (Protocol)                       |
| **데이터 접근** | 화면에 렌더링된 결과 확인   | `lotto://history` 리소스를 통해 원본 데이터 직접 독해      |
| **기능 실행**   | 버튼 클릭 시 함수 실행      | AI가 판단하여 적절한 Tool(`calculate_hot_numbers` 등) 호출 |
| **보안**        | `secrets.toml` 및 세션 관리 | MCP 프로토콜 내 인증 및 로컬 실행 환경                     |

---

## 3. MCP 구현 상세 전략

MCP는 크게 **Resources(데이터)**, **Tools(기능)**, **Prompts(템플릿)** 세 가지 요소로 구성됩니다. 기존 코드를 다음과 같이 매핑할 수 있습니다.

### 3.1 Resources (데이터 제공)

- **URI:** `lotto://history/latest`
- **설명:** `Data/645_251227.csv` 파일을 읽어 텍스트나 JSON 형태로 AI에게 제공합니다.
- **구현:** 기존 `pd.read_csv()` 코드를 재사용하여, AI가 "최근 당첨 번호 보여줘"라고 할 때 파일 내용을 직접 컨텍스트로 주입합니다.
- **장점:** 에피소드 9에서 구현한 '파일 수정 시간 감지(Caching)' 로직을 그대로 적용하여, 데이터가 업데이트되면 AI도 즉시 최신 데이터를 알게 됩니다.

### 3.2 Tools (기능 실행)

기존의 분석 함수들을 AI가 호출할 수 있는 도구로 래핑합니다.

1.  **`analyze_numbers`**:
    - 기능: 특정 번호의 출현 빈도, 최근 출현일, 핫/콜드 여부 분석.
    - 입력: 숫자 (1~45).
    - 기존 코드: `Counter` 및 필터링 로직 재사용.

2.  **`generate_recommendation`**:
    - 기능: 7가지 전략(가중치, 패턴, 하이브리드 등) 중 하나를 선택하여 번호 생성.
    - 입력: 전략 이름 (string), 생성 개수 (int).
    - 기존 코드: 에피소드 5의 `generate_access_code` 및 추천 알고리즘 재사용.

3.  **`verify_premium_access`**:
    - 기능: 에피소드 10의 `PREM-****-****` 코드 검증.
    - 입력: 액세스 코드.
    - 동작: 코드가 유효하면 'VIP 전용 분석 툴' 사용 권한을 부여하거나, 숨겨진 분석 결과를 반환.

### 3.3 Prompts (대화 템플릿)

- **`analyze_this_week`**: "이번 주 로또 번호 분석해줘"라는 요청이 들어오면, 자동으로 최근 5회차 데이터와 핫넘버 분석 도구를 실행하도록 유도하는 프롬프트 템플릿 제공.

---

## 4. 기술적 타당성 검토 (Feasibility)

### ✅ 긍정적 요소 (Pros)

1.  **Python 호환성:** MCP SDK는 Python을 완벽하게 지원하며, 기존 프로젝트의 `pandas`, `numpy` 의존성을 그대로 사용할 수 있습니다.
2.  **로직 재사용:** UI 코드(`st.write`, `st.sidebar`)만 제거하면 핵심 로직(Business Logic)은 100% 재사용 가능합니다.
3.  **자연어 인터페이스:** "지난달에 가장 많이 나온 번호랑 짝수 패턴이 일치하는 거 추천해줘" 같은 복잡한 자연어 명령을 AI가 해석하고, 적절한 함수를 연쇄적으로 호출하여 처리할 수 있습니다.

### ⚠️ 고려 사항 (Cons)

1.  **시각화:** Streamlit의 `Plotly` 차트는 인터랙티브하지만, MCP는 텍스트나 이미지(Base64)로 결과를 반환해야 합니다. 차트 대신 요약된 통계 텍스트를 반환하거나, 차트 이미지를 생성하여 전달하는 방식으로 변경이 필요합니다.
2.  **상태 관리:** Streamlit의 `Session State`와 달리 MCP 서버는 기본적으로 Stateless(상태 없음)를 지향하므로, VIP 인증 상태 등을 관리하려면 별도의 토큰 방식이나 매 요청마다 코드를 확인하는 방식이 필요합니다.

---

## 5. 구현 예시 코드 (Python MCP SDK)

```python
from mcp.server.fastmcp import FastMCP
import pandas as pd
import random

# MCP 서버 초기화
mcp = FastMCP("Lotto645-Analysis")

# 데이터 로드 (기존 로직 활용)
def load_data():
    return pd.read_csv("Data/645_251227.csv")

@mcp.resource("lotto://history")
def get_lotto_history() -> str:
    """전체 로또 당첨 기록을 CSV 텍스트로 반환"""
    df = load_data()
    return df.to_csv(index=False)

@mcp.tool()
def recommend_numbers(strategy: str = "random") -> list[int]:
    """
    전략에 따라 로또 번호 6개를 추천합니다.
    Args:
        strategy: 'random', 'hot', 'cold', 'hybrid' 중 하나
    """
    if strategy == "random":
        return sorted(random.sample(range(1, 46), 6))
    # ... 기존 에피소드 5의 로직 구현 ...
    return []

if __name__ == "__main__":
    mcp.run()
```

---

## 6. 결론 및 제언

로또 645 분석 서비스는 **데이터(CSV)**와 **명확한 규칙(함수)**을 가지고 있어 MCP 서버로 구현하기에 **매우 적합한 프로젝트**입니다.

**추천 진행 단계:**

1.  **Core 분리:** `app.py`에 섞여 있는 분석 로직을 `lotto_engine.py`와 같은 별도 모듈로 분리합니다.
2.  **MCP 서버 구축:** `mcp` 라이브러리를 설치하고 위 예시처럼 Tools를 등록합니다.
3.  **Claude Desktop 연동:** 로컬에서 MCP 서버를 띄우고 Claude Desktop 설정 파일에 추가하여, AI와 대화하며 로또 분석을 테스트합니다.

이 전환을 통해 단순한 웹 대시보드를 넘어, **"대화형 AI 로또 분석가"**를 만들 수 있습니다.
