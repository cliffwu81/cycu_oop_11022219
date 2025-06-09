import pandas as pd
import asyncio
from playwright.async_api import async_playwright

def find_routes_by_stops(from_stop, to_stop):
    df = pd.read_csv("HW2.csv", dtype=str)
    # 找出同時有出發站和到達站的路線
    routes_from = set(df[df['stop_name'] == from_stop]['route_name'])
    routes_to = set(df[df['stop_name'] == to_stop]['route_name'])
    routes = list(routes_from & routes_to)
    return routes

async def open_route_web(route_name, from_stop, to_stop):
    url = f"https://ebus.gov.taipei/EBus/VsSimpleMap?routeid={route_name}&gb=0"
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto(url)
        print(f"已開啟 {url}，請手動查詢「{from_stop}」到「{to_stop}」的站牌資訊。")
        input("請查詢完畢後按 Enter 關閉瀏覽器...")
        await browser.close()

def main():
    from_stop = input("請輸入出發站名稱: ")
    to_stop = input("請輸入到達站名稱: ")
    routes = find_routes_by_stops(from_stop, to_stop)
    if not routes:
        print("查無同時經過這兩站的公車路線。")
        return
    print(f"同時經過「{from_stop}」和「{to_stop}」的公車路線有：{', '.join(routes)}")
    route_name = input("請輸入你想查詢即時資訊的公車路線名稱：")
    if route_name not in routes:
        print("你輸入的路線不在查詢結果中。")
        return
    asyncio.run(open_route_web(route_name, from_stop, to_stop))

if __name__ == "__main__":
    main()