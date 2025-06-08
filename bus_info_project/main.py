import sys
import requests
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

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

def main():
    print("🚌 歡迎使用台北市公車即時站牌查詢")
    # 取得 route_id 與 route_name 對照表
    route_list = taipei_route_list()
    df_route = route_list.parse_route_list()
    route_id = input("請輸入路線ID（如 0161000900）：").strip()
    direction = input("請輸入方向（go 或 come）：").strip()
    if direction not in ["go", "come"]:
        print("❌ 方向只能是 go 或 come")
        return

    # 自動查 route_name
    row = df_route[df_route["route_id"] == route_id]
    if row.empty:
        print("❌ 查無此路線ID")
        return
    route_name = row.iloc[0]["route_name"]

    try:
        route_info = taipei_route_info(route_id, direction=direction)
        df = route_info.parse_route_info()
        stops = df["stop_name"].tolist()
        print("所有站名：")
        print("、".join(stops))
        start = input("請輸入出發站名：").strip()
        end = input("請輸入到達站名：").strip()
        if start not in stops or end not in stops:
            print("❌ 站名輸入錯誤")
            return
        start_idx = stops.index(start)
        end_idx = stops.index(end)
        if start_idx > end_idx:
            print("❌ 出發站應在到達站之前")
            return
        print(f"\n經過站名與預估到站時間（路線：{route_name}）：")
        for stop in stops[start_idx:end_idx+1]:
            eta = get_eta(route_name, stop)
            print(f"{stop}：{eta}")
    except Exception as e:
        print(f"❌ 查詢失敗：{e}")

if __name__ == "__main__":
    main()