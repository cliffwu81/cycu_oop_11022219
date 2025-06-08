import math

def calculate_quadrilateral_area(a, b, c, d, diagonal):
    """
    計算凸四邊形的面積

    :param a: 第一邊長
    :param b: 第二邊長
    :param c: 第三邊長
    :param d: 第四邊長
    :param diagonal: 對角線長
    :return: 四邊形的面積
    """
    # 使用 Brahmagupta 公式計算凸四邊形面積
    s = (a + b + c + d) / 2  # 半周長
    area = math.sqrt((s - a) * (s - b) * (s - c) * (s - d) - (a * c + b * d - diagonal ** 2) ** 2 / 16)
    return area

# 主程式
if __name__ == "__main__":
    print("請輸入四邊形的四邊長及對角線長：")
    a = float(input("第一邊長: "))
    b = float(input("第二邊長: "))
    c = float(input("第三邊長: "))
    d = float(input("第四邊長: "))
    diagonal = float(input("對角線長: "))
    
    try:
        area = calculate_quadrilateral_area(a, b, c, d, diagonal)
        print(f"四邊形的面積為: {area:.2f}")
    except ValueError:
        print("輸入的邊長或對角線長無法構成有效的四邊形。")