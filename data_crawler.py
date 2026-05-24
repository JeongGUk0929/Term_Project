import requests
import pandas as pd
import time
import os

"""특정 게임의 스팀 리뷰를 수집하여 데이터프레임으로 반환합니다."""
def get_steam_reviews(app_id, target_count=2000):
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"
    reviews_data = []
    cursor = '*' 
    
    # 목표 개수만큼 API 반복 요청
    while len(reviews_data) < target_count:
        params = {
            'filter': 'recent',     # 최신순
            'language': 'english',  # 영어 리뷰만
            'num_per_page': 100,    # 한 번에 100개씩
            'cursor': cursor
        }
        
        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(f"  [에러] API 요청 실패 (상태 코드: {response.status_code})")
            break
            
        data = response.json()
        if 'reviews' not in data or not data['reviews']:
            break
            
        reviews_data.extend(data['reviews'])
        cursor = data['cursor'] # 다음 페이지 커서 업데이트
        
        # 진행 상황 출력 (500개 단위)
        if len(reviews_data) % 500 == 0:
            print(f"  ... {len(reviews_data)}개 수집 완료 ...")
            
        time.sleep(1) # 서버 부하 방지
        
    df = pd.DataFrame(reviews_data[:target_count])
    
    if not df.empty:
        # 플레이타임을 시간 단위로 변환하고 핵심 컬럼 3개만 추출
        df['playtime_forever'] = df['author'].apply(lambda x: x.get('playtime_forever', 0) / 60) 
        df = df[['voted_up', 'review', 'playtime_forever']]
        
    return df

# --- 메인 실행부 ---

target_games = {
    "Elden_Ring": 1245620, "Witcher_3": 292030, "Cyberpunk_2077": 1091500, # RPG
    "PUBG": 578080, "CS2": 730, "R6_Siege": 359550 # FPS
}

os.makedirs("data", exist_ok=True) # 저장 폴더 생성
print("=== 다중 게임 스팀 리뷰 수집 시작 (목표: 각 2000개) ===\n")

for game_name, app_id in target_games.items():
    print(f"[{game_name}] (App ID: {app_id}) 리뷰 수집 중...")
    
    df = get_steam_reviews(app_id, target_count=2000) 
    
    if not df.empty:
        file_path = f"data/{game_name}_reviews.csv"
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"  -> 수집 완료! ({len(df)}개 리뷰 저장됨: {file_path})\n")
    else:
        print(f"  -> 수집된 데이터가 없습니다.\n")