import asyncio
from playwright.async_api import async_playwright

async def run():
    page_urls = [
        "https://www.bcsw.com.tw/category.php?type=1&arem=125&arem1=1594#1",
        "https://www.bcsw.com.tw/category.php?type=1&arem=125&arem1=1594#2",
        "https://www.bcsw.com.tw/category.php?type=1&arem=125&arem1=1594#3",
        "https://www.bcsw.com.tw/category.php?type=1&arem=125&arem1=1594#4"
    ]

    all_links = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        for i, url in enumerate(page_urls, 1):
            print(f"📄 正在處理第 {i} 頁：{url}")
            await page.goto(url)
            await page.wait_for_timeout(1500)

            # 抓取所有 <a> 元素
            anchors = await page.query_selector_all('a')
            for a in anchors:
                href = await a.get_attribute('href')
                if href and "/product/" in href and "category_sn=1594" in href:
                    full_url = f"https://www.bcsw.com.tw{href}" if href.startswith("/") else href
                    all_links.add(full_url)

        await browser.close()

    # 輸出所有擷取結果
    print(f"\n🎯 共擷取商品連結數量：{len(all_links)} 筆")
    for i, link in enumerate(sorted(all_links), 1):
        print(f"{i}. {link}")

asyncio.run(run())
