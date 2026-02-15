"""
Gemini와 MCP 서버 간의 연동을 테스트하기 위한 스크립트입니다.
이 스크립트는 Gemini API를 사용하여 자연어 요청을 처리하고,
필요한 경우 MCP 도구(Tool) 호출을 시뮬레이션하거나 실제 서버로 전달합니다.
"""

import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

# 환경 변수 로드 (.env 파일에서 GOOGLE_API_KEY 등을 로드)
load_dotenv()

# Gemini API 키 설정
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("⚠️ 경고: GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")
    print("  .env 파일을 생성하고 GOOGLE_API_KEY를 입력하거나 환경 변수로 설정해주세요.")

# Gemini 모델 설정
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# ------------------------------------------------------------------------------
# 1. MCP 도구 정의 (Gemini에게 알려줄 도구 명세)
# ------------------------------------------------------------------------------
# 실제 구현 시에는 MCP 서버에서 도구 목록을 조회하여 동적으로 생성해야 합니다.
# 여기서는 테스트를 위해 하드코딩된 스키마를 사용합니다.
lotto_tools = [
    {
        "name": "get_winning_numbers",
        "description": "특정 회차의 로또 당첨 번호와 보너스 번호를 조회합니다.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "round": {
                    "type": "INTEGER",
                    "description": "조회할 로또 회차 (예: 1000)"
                }
            },
            "required": ["round"]
        }
    },
    {
        "name": "recommend_lotto_numbers",
        "description": "다양한 전략을 사용하여 로또 번호를 추천합니다.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "strategy": {
                    "type": "STRING",
                    "description": "추천 전략 (hybrid, score, pattern, random 중 하나)",
                    "enum": ["hybrid", "score", "pattern", "random"]
                },
                "count": {
                    "type": "INTEGER",
                    "description": "생성할 게임 수 (기본값: 5)"
                }
            },
            "required": ["strategy"]
        }
    }
]

# ------------------------------------------------------------------------------
# 2. MCP 도구 실행 함수 (Mock & Bridge)
# ------------------------------------------------------------------------------
async def execute_mcp_tool(name: str, args: dict):
    """
    Gemini가 요청한 도구를 실제로 실행하는 함수입니다.
    추후 mcp 라이브러리를 사용하여 실제 로컬 MCP 서버와 통신하도록 구현해야 합니다.
    """
    print(f"\n🛠️  [MCP Client] 도구 실행 요청: {name}")
    print(f"    └─ 인자: {args}")

    # --- Mock 구현 (실제 서버 연결 전 테스트용) ---
    if name == "get_winning_numbers":
        # 가짜 데이터 반환
        round_num = args.get("round")
        return {
            "round": round_num,
            "winning_numbers": [1, 2, 3, 4, 5, 6],
            "bonus": 7,
            "date": "2024-01-01",
            "note": "이것은 테스트용 가짜 데이터입니다."
        }
    
    elif name == "recommend_lotto_numbers":
        strategy = args.get("strategy", "hybrid")
        count = int(args.get("count", 5))
        return {
            "strategy": strategy,
            "recommendations": [
                [1, 10, 20, 30, 40, 45] for _ in range(count)
            ],
            "note": f"{strategy} 전략으로 생성된 테스트 번호입니다."
        }
    
    return {"error": f"알 수 없는 도구입니다: {name}"}

# ------------------------------------------------------------------------------
# 3. 메인 테스트 로직
# ------------------------------------------------------------------------------
async def run_chat_session():
    if not GOOGLE_API_KEY:
        print("API 키가 없어 테스트를 종료합니다.")
        return

    # 모델 초기화 (도구 포함)
    tools_obj = genai.protos.Tool(function_declarations=lotto_tools)
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash', # 최신 모델 사용 권장
        tools=[tools_obj]
    )

    # 채팅 세션 시작 (자동 함수 호출 비활성화 - 수동 제어 테스트를 위해)
    chat = model.start_chat(enable_automatic_function_calling=False)

    print("🤖 Gemini 로또 분석 에이전트 테스트 시작 (종료하려면 'quit' 입력)")
    print("------------------------------------------------------------------")

    while True:
        try:
            user_input = input("\n👤 사용자: ")
        except EOFError:
            break
            
        if user_input.lower() in ['quit', 'exit', 'q']:
            break
        
        if not user_input.strip():
            continue

        try:
            # 1. 사용자 메시지 전송
            response = chat.send_message(user_input)
            
            # 2. 모델 응답 분석 (함수 호출 요청이 있는지 확인)
            if not response.candidates:
                print("⚠️ 모델이 응답하지 않았습니다 (Safety filter 등).")
                continue
                
            part = response.candidates[0].content.parts[0]
            
            if part.function_call:
                fc = part.function_call
                tool_name = fc.name
                tool_args = dict(fc.args)
                
                # 3. MCP 도구 실행 (Bridge)
                tool_result = await execute_mcp_tool(tool_name, tool_args)
                
                # 4. 실행 결과를 Gemini에게 전달
                # FunctionResponse 파트 생성
                function_response_part = content.Part(
                    function_response=content.FunctionResponse(
                        name=tool_name,
                        response={"result": tool_result}
                    )
                )
                
                # 결과와 함께 모델에 다시 요청
                final_response = chat.send_message(content.Content(parts=[function_response_part]))
                print(f"🤖 Gemini: {final_response.text}")
                
            else:
                # 일반 텍스트 응답
                print(f"🤖 Gemini: {response.text}")
                
        except Exception as e:
            print(f"❌ 에러 발생: {e}")

if __name__ == "__main__":
    asyncio.run(run_chat_session())