import asyncio
from playwright.async_api import async_playwright

async def run():
    base_url = "https://www.bcsw.com.tw/category.php?type=1&arem1=1594&arem=125"
    page_urls = []  # 儲存每一頁的實際網址
    seen_pages = set()  # 防止重複

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await page.goto(base_url)
        await page.wait_for_timeout(2000)

        page_count = 1
        while True:
            print(f"📄 處理第 {page_count} 頁...")

            # 記錄目前頁面網址（加上 #分頁號碼）
            current_url = f"{base_url}#{page_count}"
            if current_url not in seen_pages:
                page_urls.append(current_url)
                seen_pages.add(current_url)

            # 嘗試找下一頁按鈕
            next_img = await page.query_selector('img[src*="all_page_next.gif"]')
            if not next_img:
                print("✅ 沒有下一頁了")
                break

            next_a = await next_img.evaluate_handle("node => node.closest('a')")
            if next_a:
                await next_a.click()
                await page.wait_for_timeout(2500)
                page_count += 1
            else:
                print("⚠️ 找不到下一頁按鈕")
                break

        await browser.close()

    # 顯示結果
    print(f"\n🧭 所有商品頁面網址如下：")
    for i, url in enumerate(page_urls, 1):
        print(f"{i}. {url}")

asyncio.run(run())
