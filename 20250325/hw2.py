import pandas as pd
import matplotlib.pyplot as plt

# 讀取 CSV 檔案，假設檔案是 utf-8 編碼
file_path = r'C:\Users\User\Documents\GitHub\cycu_oop_11022219\ExchangeRate@202503251854.csv'
data = pd.read_csv(file_path, encoding='utf-8')

# 檢查資料的前幾行
print(data.head())

# 重新命名欄位，去除重複欄位
data.columns = ['資料日期', '幣別', '匯率_買入_標題', '買入', '匯率_賣出_標題', '賣出']

# 清理資料：只保留有用的列，並將「資料日期」轉換為日期格式
data = data[['資料日期', '買入', '賣出']]

# 將資料日期轉換為 datetime 格式
data['資料日期'] = pd.to_datetime(data['資料日期'].astype(str), format='%Y%m%d')

# 設定支持中文的字型（根據系統更改字型）
plt.rcParams['font.family'] = 'Microsoft YaHei'  # 或者 'SimHei'

# 繪製圖表
plt.figure(figsize=(10, 6))

# 繪製「買入」和「賣出」匯率的兩條線
plt.plot(data['資料日期'], data['買入'], marker='o', linestyle='-', color='b', label='Buy Rate (買入)')
plt.plot(data['資料日期'], data['賣出'], marker='o', linestyle='-', color='r', label='Sell Rate (賣出)')

# 圖表標題和軸標籤
plt.title('USD to TWD Exchange Rate (Buy and Sell Rates)')
plt.xlabel('Date')
plt.ylabel('Exchange Rate (TWD per USD)')

# 顯示圖例
plt.legend()

# 格式化日期顯示
plt.xticks(rotation=45)

# 顯示網格
plt.grid(True)

# 自動調整圖表佈局
plt.tight_layout()

# 顯示圖表
plt.show()