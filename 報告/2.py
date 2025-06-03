from playwright.sync_api import sync_playwright
import pandas as pd

def fetch_bus_arrival_times(url):
    """
    使用 Playwright 抓取公車到站時間。
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)  # 等待頁面載入

        # 抓取到站時間的 HTML 元素
        bus_data = []
        rows = page.query_selector_all("div.bus-arrival-row")  # 替換為正確的 CSS 選擇器
        for row in rows:
            bus_number = row.query_selector("span.bus-number").inner_text()
            arrival_time = row.query_selector("span.arrival-time").inner_text()
            bus_data.append({"bus_number": bus_number, "arrival_time": arrival_time})

        browser.close()

    # 將資料轉換為 DataFrame
    df = pd.DataFrame(bus_data)
    return df

if __name__ == "__main__":
    url = "https://example.com/bus-arrival"  # 替換為目標網站的 URL
    bus_arrival_df = fetch_bus_arrival_times(url)
    print(bus_arrival_df)
    bus_arrival_df.to_excel("bus_arrival_times.xlsx", index=False)