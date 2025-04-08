# -*- coding: utf-8 -*-
import pandas as pd
import re
from playwright.sync_api import sync_playwright
import sqlite3
from bs4 import BeautifulSoup
import csv
import os


class BusRouteInfo:
    def __init__(self, routeid: str, direction: str = 'go'):
        self.rid = routeid
        self.content = None
        self.url = f'https://ebus.gov.taipei/Route/StopsOfRoute?routeid={routeid}'

        if direction not in ['go', 'come']:
            raise ValueError("Direction must be 'go' or 'come'")

        self.direction = direction

        self._fetch_content()
    

    def _fetch_content(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(self.url)
            
            if self.direction == 'come':
                page.click('a.stationlist-come-go-gray.stationlist-come')
            
            page.wait_for_timeout(3000)  # wait for 3 seconds
            self.content = page.content()
            browser.close()

        # 確保資料目錄存在
        os.makedirs("data", exist_ok=True)

        # 將渲染後的 HTML 寫入檔案
        with open(f"data/ebus_taipei_{self.rid}.html", "w", encoding="utf-8") as file:
            file.write(self.content)

    def parse_and_save_to_csv(self):
        """
        解析 HTML 資料，提取站點資訊，並儲存為 CSV 檔案。
        """
        if not self.content:
            print("尚未抓取到內容，請檢查網頁是否正確加載。")
            return

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(self.content, 'html.parser')

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
        output_file = f"data/bus_route_{self.rid}_{self.direction}.csv"
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["arrival_info", "stop_number", "stop_name", "stop_id", "latitude", "longitude"])
            writer.writerows(bus_data)

        print(f"資料已成功儲存至 {output_file}")


# 主程式
if __name__ == "__main__":
    route_id = input("請輸入公車代碼 (例如 '0100000A00'): ")
    direction = input("請輸入方向 ('go' 或 'come')，預設為 'go': ") or 'go'

    try:
        bus_route = BusRouteInfo(routeid=route_id, direction=direction)
        bus_route.parse_and_save_to_csv()
    except Exception as e:
        print(f"發生錯誤: {e}")