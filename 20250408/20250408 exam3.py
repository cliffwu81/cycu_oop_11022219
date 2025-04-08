import requests
from bs4 import BeautifulSoup
import csv

def fetch_bus_route_data(route_id):
    """
    從臺北市公開網站抓取指定公車路線的站點資料，並輸出為 CSV 格式。
    
    :param route_id: 公車代碼 (例如 '0100000A00')
    """
    # 定義目標 URL
    url = f"https://ebus.gov.taipei/Route/StopsOfRoute?routeid={route_id}"
    
    try:
        # 發送 GET 請求
        response = requests.get(url)
        response.raise_for_status()  # 檢查請求是否成功
    except requests.RequestException as e:
        print(f"無法取得資料: {e}")
        return

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到包含站點資料的表格
    stops_table = soup.find('table', {'class': 'table'})  # 假設表格有 class="table"
    if not stops_table:
        print("無法找到站點資料表格")
        return

    # 解析表格中的資料
    rows = stops_table.find_all('tr')
    bus_data = []
    for row in rows[1:]:  # 跳過表頭
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
        arrival_info = cols[0].text.strip()
        stop_number = cols[1].text.strip()
        stop_name = cols[2].text.strip()
        stop_id = cols[3].text.strip()
        latitude = cols[4].text.strip()
        longitude = cols[5].text.strip()
        bus_data.append([arrival_info, stop_number, stop_name, stop_id, latitude, longitude])

    # 將資料寫入 CSV 檔案
    output_file = f"bus_route_{route_id}.csv"
    with open(output_file, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["arrival_info", "stop_number", "stop_name", "stop_id", "latitude", "longitude"])
        writer.writerows(bus_data)

    print(f"資料已成功儲存至 {output_file}")

# 主程式
if __name__ == "__main__":
    route_id = input("請輸入公車代碼 (例如 '0100000A00'): ")
    fetch_bus_route_data(route_id)