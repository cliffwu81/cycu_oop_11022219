import requests
import json
from datetime import datetime

# PTX API 認證資訊
APP_ID = '你的AppID'
APP_KEY = '你的AppKey'

# 設定 API 請求的標頭
def get_headers():
    from hashlib import sha1
    import hmac
    import base64
    from datetime import datetime

    x_date = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    hashed = hmac.new(
        APP_KEY.encode('utf-8'),
        ('x-date: ' + x_date).encode('utf-8'),
        sha1
    ).digest()
    signature = base64.b64encode(hashed).decode()
    authorization = f'hmac username="{APP_ID}", algorithm="hmac-sha1", headers="x-date", signature="{signature}"'

    return {
        'Authorization': authorization,
        'x-date': x_date,
        'Accept-Encoding': 'gzip'
    }

# 抓取公車站牌資訊
def fetch_bus_stops():
    url = 'https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/Taipei?$format=JSON'
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        stops = response.json()
        print(f"共抓取到 {len(stops)} 筆站牌資料")
        return stops
    else:
        print(f"無法取得站牌資料，狀態碼: {response.status_code}")
        return []

# 抓取公車路線資訊
def fetch_bus_routes():
    url = 'https://ptx.transportdata.tw/MOTC/v2/Bus/Route/City/Taipei?$format=JSON'
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        routes = response.json()
        print(f"共抓取到 {len(routes)} 筆路線資料")
        return routes
    else:
        print(f"無法取得路線資料，狀態碼: {response.status_code}")
        return []

# 抓取即時到站時間
def fetch_bus_arrival_times():
    url = 'https://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/City/Taipei?$format=JSON'
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        arrivals = response.json()
        print(f"共抓取到 {len(arrivals)} 筆即時到站資料")
        return arrivals
    else:
        print(f"無法取得即時到站資料，狀態碼: {response.status_code}")
        return []

# 主程式
if __name__ == '__main__':
    print("正在抓取站牌資訊...")
    stops = fetch_bus_stops()

    print("正在抓取路線資訊...")
    routes = fetch_bus_routes()

    print("正在抓取即時到站時間...")
    arrivals = fetch_bus_arrival_times()

    # 將資料儲存為 JSON 檔案
    with open('bus_stops.json', 'w', encoding='utf-8') as f:
        json.dump(stops, f, ensure_ascii=False, indent=4)

    with open('bus_routes.json', 'w', encoding='utf-8') as f:
        json.dump(routes, f, ensure_ascii=False, indent=4)

    with open('bus_arrivals.json', 'w', encoding='utf-8') as f:
        json.dump(arrivals, f, ensure_ascii=False, indent=4)

    print("資料已儲存為 JSON 檔案")