import asyncio
import os
import re
import requests
from playwright.async_api import async_playwright

# ✅ 儲存根目錄（可修改）
BASE_DIR = r"C:/Users/hopeb/Documents/露天API-專案/玩具槍.BB槍/CO2手槍"

# ✅ 商品網址列表（來自你提供的 200 筆）
URL_LIST = [
    "https://www.bcsw.com.tw/product/%20UMGSMOS17G?category_sn=1594",
    "https://www.bcsw.com.tw/product/20ASG-16090?category_sn=1594",
    "https://www.bcsw.com.tw/product/ASG-16724?category_sn=1594",
    "https://www.bcsw.com.tw/product/ASG-19592?category_sn=1594",
    "https://www.bcsw.com.tw/product/ASG-19593?category_sn=1594",
    "https://www.bcsw.com.tw/product/ASG-19923?category_sn=1594",
    "https://www.bcsw.com.tw/product/ASG-19924?category_sn=1594",
    "https://www.bcsw.com.tw/product/ASG715BK?category_sn=1594",
    "https://www.bcsw.com.tw/product/E5000145?category_sn=1594",
    "https://www.bcsw.com.tw/product/EMGARK17BK?category_sn=1594",
    # （老師只貼了前10筆，實際版本你貼上完整的200筆網址）
]

# 🔧 儲存文字檔
def save_text(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip())

# 🔧 儲存圖片（不壓縮）
def download_image(url, path):
    try:
        if url.startswith("//"):
            url = "https:" + url
        elif url.startswith("/"):
            url = "https://www.bcsw.com.tw" + url
        response = requests.get(url)
        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
    except Exception as e:
        print(f"⚠️ 下載圖片失敗：{url}\n錯誤：{e}")

# ✅ 單一商品頁擷取
async def scrape_bcs_product(page, url):
    try:
        await page.goto(url, timeout=30000)
        await page.wait_for_timeout(1000)

        # 商品名稱
        await page.wait_for_selector(".product_name.name h1", timeout=5000)
        title = await page.inner_text(".product_name.name h1")
        title = title.strip().replace("【BCS】", "【甲武】")

        # 建立資料夾
        folder_name = re.sub(r'[\\/:*?"<>|]', '', title)
        folder_path = os.path.join(BASE_DIR, folder_name)
        img_dir = os.path.join(folder_path, "圖片")
        os.makedirs(img_dir, exist_ok=True)

        # 商品編號 & 價格
        sn = await page.inner_text(".data-item.number .context")
        price = await page.inner_text("#product_price3_id .digital")

        save_text(os.path.join(folder_path, "商品名稱.txt"), title)
        save_text(os.path.join(folder_path, "商品編號.txt"), sn)
        save_text(os.path.join(folder_path, "商品價格.txt"), price)

        # 主圖
        main_img_url = await page.get_attribute("img[data-zoom-image]", "data-zoom-image")
        if main_img_url:
            download_image(main_img_url, os.path.join(img_dir, "主圖.jpg"))

        # 商品介紹（HTML格式）
        await page.click("#product_module_0")
        await page.wait_for_selector("#ajax_box_product_context_id", timeout=5000)
        await page.wait_for_timeout(1000)
        desc_html = await page.inner_html("#ajax_box_product_context_id")
        save_text(os.path.join(folder_path, "商品介紹.html"), desc_html)

        # 商品介紹圖片
        img_urls = re.findall(r'<img[^>]+src="([^"]+)"', desc_html)
        for i, img_url in enumerate(img_urls):
            download_image(img_url, os.path.join(img_dir, f"intro_{i+1}.jpg"))

        print(f"✅ 擷取完成：{title}")

    except Exception as e:
        print(f"❌ 擷取失敗：{url}\n錯誤訊息：{e}")

# ✅ 批次爬蟲任務
async def scrape_all_products():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        for i, url in enumerate(URL_LIST, 1):
            print(f"\n🚀 第 {i} 筆：開始擷取 {url}")
            await scrape_bcs_product(page, url)
            await page.wait_for_timeout(3000)  # 等待3秒再繼續

        await browser.close()
        print("\n🎉 所有商品擷取完畢！")

# ✅ 程式進入點
if __name__ == "__main__":
    asyncio.run(scrape_all_products())
