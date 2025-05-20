import geopandas as gpd
import matplotlib.pyplot as plt

# 設定 GeoJSON 檔案路徑
geojson_path = 'C:/Users/User/Documents/GitHub/cycu_oop_11022219/20250520/鄉(鎮、市、區)界線1140318'

# 指定圖層名稱
gdf = gpd.read_file(geojson_path, layer='TOWN_MOI_1140318')

# 列出所有縣市名稱，確認台北市的名稱
print(gdf['COUNTYNAME'].unique())

# 篩選台北市、新北市、基隆市和桃園市
target_cities = ['臺北市', '新北市', '基隆市', '桃園市']  # 根據實際名稱更新
filtered_gdf = gdf[gdf['COUNTYNAME'].isin(target_cities)]

# 繪製地圖
plt.figure(figsize=(10, 10))
filtered_gdf.plot(ax=plt.gca(), edgecolor='black', color='lightblue', alpha=0.7)

# 添加標題和標籤
plt.title('台北市、新北市、基隆市、桃園市的鄉鎮市區界圖', fontsize=16)
plt.xlabel('經度', fontsize=12)
plt.ylabel('緯度', fontsize=12)

# 顯示地圖
plt.tight_layout()
plt.show()