import requests
import pandas as pd
import time
import os

def get_steam_reviews(app_id, target_count=2000):
    """
    특정 게임(app_id)의 스팀 리뷰를 수집하여 데이터프레임으로 반환합니다.
    """
    url = f"https://store.steampowered.com/appreviews/{app_id}?json=1"
    reviews_data = []
    cursor = '*' 
    
    while len(reviews_data) < target_count:
        params = {
            'filter': 'recent',     
            'language': 'english',  
            'num_per_page': 100,    
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
        cursor = data['cursor']
        
        # 진행 상황을 터미널에 표시
        if len(reviews_data) % 500 == 0:
            print(f"  ... {len(reviews_data)}개 수집 완료 ...")
            
        time.sleep(1) # 서버 부하 방지
        
    df = pd.DataFrame(reviews_data[:target_count])
    
    if not df.empty:
        # 플레이타임을 시간 단위로 변환
        df['playtime_forever'] = df['author'].apply(lambda x: x.get('playtime_forever', 0) / 60) 
        df = df[['voted_up', 'review', 'playtime_forever']]
        
    return df

# 분석할 6개 게임의 App ID 딕셔너리
target_games = {
    # 오픈월드 RPG
    "Elden_Ring": 1245620,
    "Witcher_3": 292030,
    "Cyberpunk_2077": 1091500,
    
    # 전술/경쟁 FPS
    "PUBG": 578080,
    "CS2": 730,
    "R6_Siege": 359550
}

# 데이터를 깔끔하게 모아둘 폴더 생성
os.makedirs("data", exist_ok=True)

print("=== 다중 게임 스팀 리뷰 수집 시작 (목표: 각 2000개) ===\n")

# 딕셔너리를 돌면서 각 게임의 데이터를 순차적으로 수집 및 저장
for game_name, app_id in target_games.items():
    print(f"[{game_name}] (App ID: {app_id}) 리뷰 수집 중...")
    
    # 각 게임당 2000개의 최신 리뷰를 수집
    df = get_steam_reviews(app_id, target_count=2000) 
    
    if not df.empty:
        file_path = f"data/{game_name}_reviews.csv"
        df.to_csv(file_path, index=False, encoding="utf-8-sig")
        print(f"  -> 수집 완료! ({len(df)}개 리뷰 저장됨: {file_path})\n")
    else:
        print(f"  -> 수집된 데이터가 없습니다.\n")

print("=== 모든 게임의 데이터 수집이 완료되었습니다! ===")