import sys
import requests
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# 匯入 taipei_route_info, taipei_route_list
sys.path.append(str(Path(__file__).resolve().parent.parent / "20250513" / "src" / "m11022219"))
from ebus_taipei import taipei_route_info, taipei_route_list

def get_eta(route_name, stop_name):
    # 台北市公車即時到站資料 PTX API
    url = f"https://tdx.transportdata.tw/api/basic/v2/Bus/EstimatedTimeOfArrival/City/Taipei/{route_name}?$format=JSON"
    try:
        resp = requests.get(url)
        data = resp.json()
        for item in data:
            if item.get("StopName", {}).get("Zh_tw") == stop_name:
                sec = item.get("EstimateTime")
                if sec is None:
                    return "尚未發車或無資料"
                elif sec < 60:
                    return "進站中"
                else:
                    return f"{sec//60} 分 {sec%60} 秒"
        return "查無即時資料"
    except Exception:
        return "查詢失敗"

def get_eta_by_web(route_name, stop_name):
    df = pd.read_csv("HW2.csv", dtype=str)
    print("CSV 欄位名稱：", df.columns.tolist())  # 新增這行
    # 這裡 route_id 改為 route_name
    # 你需要先查 route_name 對應的 route_id，這裡假設 HW2.csv 有這個對照
    # 先查 route_id
    row = df[df['route_name'] == route_name].iloc[0]
    route_id = row['route_name']
    url = f"https://ebus.gov.taipei/EBus/VsSimpleMap?routeid={route_name}&gb=0"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)
        html = page.content()
        browser.close()
    soup = BeautifulSoup(html, "html.parser")
    for stop_div in soup.select("div.stop-info"):
        name_tag = stop_div.select_one(".stop-name")
        eta_tag = stop_div.select_one(".eta")
        if name_tag and name_tag.text.strip() == stop_name:
            return eta_tag.text.strip() if eta_tag else "查無即時資料"
    return "查無即時資料"

def main():
    df = pd.read_csv("HW2.csv", dtype=str)
    start = input("請輸入出發站名：").strip()
    end = input("請輸入到達站名：").strip()

    matched = []
    for (route_name, direction_text), group in df.groupby(['route_name', 'direction_text']):
        stops = group.sort_values('stop_number')['stop_name'].tolist()
        if start in stops and end in stops:
            if stops.index(start) < stops.index(end):
                matched.append((route_name, direction_text, stops))

    if not matched:
        print("❌ 查無同時經過這兩站的公車路線")
        return

    for route_name, direction_text, stops in matched:
        start_idx = stops.index(start)
        end_idx = stops.index(end)
        print(f"\n路線：{route_name}（{direction_text}）")
        for stop in stops[start_idx:end_idx+1]:
            eta = get_eta_by_web(route_name, stop)
            print(f"{stop}：{eta}")

if __name__ == "__main__":
    main()