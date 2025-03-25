import requests
from bs4 import BeautifulSoup

# 定義目標網站的 URL
url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

# 定義一個函數來抓取並解析網頁資料
def fetch_data():
    # 發送 GET 請求來取得網頁內容
    response = requests.get(url)

    # 檢查回應是否成功
    if response.status_code == 200:
        # 解析 HTML 內容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 你可以根據網頁結構提取你想要的資料
        # 例如，抓取網頁中的所有表格資料
        tables = soup.find_all('table')
        if tables:
            for table in tables:
                rows = table.find_all('tr')
                for row in rows:
                    cols = row.find_all('td')
                    cols = [ele.text.strip() for ele in cols]
                    print(cols)  # 輸出每一行的資料
        else:
            print("無法找到表格資料")

    else:
        print(f"無法成功訪問網站，狀態碼: {response.status_code}")

# 提供一個終端機界面來讓用戶查詢
def terminal_interface():
    print("歡迎使用查詢系統！")
    while True:
        print("\n請輸入 'q' 退出程序，或者輸入任何其他關鍵字來查詢資料：")
        query = input("查詢：")
        if query.lower() == 'q':
            print("退出查詢系統。")
            break
        else:
            print("正在查詢資料...")
            fetch_data()

# 主程式
if __name__ == "__main__":
    terminal_interface()
