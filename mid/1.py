import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def plot_and_save_normal_pdf(mu, sigma, filename="normal_pdf.jpg"):
    """
    繪製常態分布的機率密度函數（PDF）並儲存為 JPG 圖檔

    :param mu: 常態分布的平均值 (mean)
    :param sigma: 常態分布的標準差 (standard deviation)
    :param filename: 儲存的圖檔名稱，預設為 "normal_pdf.jpg"
    """
    # 定義 x 軸範圍
    x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
    # 計算機率密度函數
    y = norm.pdf(x, mu, sigma)
    
    # 繪製圖形
    plt.figure(figsize=(8, 5))
    plt.plot(x, y, label=f'N({mu}, {sigma**2})', color='blue')
    plt.title('Normal Distribution PDF')
    plt.xlabel('x')
    plt.ylabel('Probability Density')
    plt.legend()
    plt.grid()
    
    # 顯示圖形
    plt.show()
    
    # 儲存圖檔
    plt.savefig(filename, format='jpg')
    plt.close()
    print(f"圖檔已儲存為 {filename}")

# 範例使用
plot_and_save_normal_pdf(0, 1.0)  # 繪製標準常態分布並儲存為 normal_pdf.jpg