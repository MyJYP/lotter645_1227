"""
이미지 생성 속도 테스트
"""
import time
from batch_generate_tickets import generate_recent_tickets

print("⏱️  10개 회차 생성 속도 테스트...")
print("="*70)

start_time = time.time()

# 10개 생성
generate_recent_tickets(10)

elapsed_time = time.time() - start_time

print(f"\n⏱️  10개 생성 소요 시간: {elapsed_time:.2f}초")
print(f"📊 1개당 평균: {elapsed_time/10:.2f}초")
print(f"⏱️  100개 예상 시간: {elapsed_time*10:.2f}초 ({elapsed_time*10/60:.1f}분)")
