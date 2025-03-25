import requests
from bs4 import BeautifulSoup

# 定義目標網站的 URL
url = "https://pda5284.gov.taipei/MQS/route.jsp?rid=10417"

# 發送 GET 請求來取得網頁內容
response = requests.get(url)

# 檢查回應是否成功
if response.status_code == 200:
    # 解析 HTML 內容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 在這裡，根據網站的結構提取你需要的資料
    # 假設你想要抓取網頁上的所有表格資料
    tables = soup.find_all('table')

    # 可以遍歷每個表格，並進一步提取資料
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            print(cols)  # 輸出每一行的資料

else:
    print(f"無法成功訪問網站，狀態碼: {response.status_code}")
