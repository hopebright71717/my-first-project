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
"https://www.bcsw.com.tw/product/ASG-16090?category_sn=1594",
"https://www.bcsw.com.tw/product/ASG-16724?category_sn=1594",
"https://www.bcsw.com.tw/product/ASG-19592?category_sn=1594",
"https://www.bcsw.com.tw/product/ASG-19593?category_sn=1594",
"https://www.bcsw.com.tw/product/ASG-19923?category_sn=1594",
"https://www.bcsw.com.tw/product/ASG-19924?category_sn=1594",
"https://www.bcsw.com.tw/product/ASG715BK?category_sn=1594",
"https://www.bcsw.com.tw/product/E5000145?category_sn=1594",
"https://www.bcsw.com.tw/product/EMGARK17BK?category_sn=1594",
"https://www.bcsw.com.tw/product/F4C1103A?category_sn=1594",
"https://www.bcsw.com.tw/product/F4C1103B?category_sn=1594",
"https://www.bcsw.com.tw/product/FS0001?category_sn=1594",
"https://www.bcsw.com.tw/product/FS0002?category_sn=1594",
"https://www.bcsw.com.tw/product/FSA1000?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC0317B25?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC0317B37?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC0317S37?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC0725B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1001B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1001C?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002B2?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002B4?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002B6?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002BR2?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002BR6?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002BRW2?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002BRW4?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002BRW6?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002BW2?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002BW4?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1002BW6?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1203B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1204B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1205B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1206B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1206BL?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1207B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1208B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1209B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1210B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1312B01?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1312B02?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1312B03?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1312C01?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1312C02?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1312C03?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1501B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1501BA?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1501BB?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1502B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1503B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1504B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1505B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1505C?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1506B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1507B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1508B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1509B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1510B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1611B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC1612B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC2021B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSC654K?category_sn=1594",
"https://www.bcsw.com.tw/product/FSCLM1B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSCLPB2?category_sn=1594",
"https://www.bcsw.com.tw/product/FSCLSP100B?category_sn=1594",
"https://www.bcsw.com.tw/product/FSGSMK23?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCLKC02?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCS1911B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCS1911BW?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCS1911O?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSCZP09?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSCZP09T?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSCZP09TBR?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSCZP09TTR?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP01B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP01E2?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP02B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP05B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP06B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP07B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP08B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP09?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP13B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP13C?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP13G?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP15B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP16T?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP17B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP17T?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP18B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP18T?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSKP21B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSM9A1B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSM9A1BW?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSM9A1O?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSM9B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSM9IAB?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSM9IABW?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSM9VEB?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSMK21?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSMK2?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSSP01B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSSP01BS?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCSSP01U?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCTCZP09B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCTCZP09T?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCTCZP09U?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCTKP13FT?category_sn=1594",
"https://www.bcsw.com.tw/product/KJCTSP01B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJGSKP19B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJGSKP21B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJTCKP07B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJUCKP13G?category_sn=1594",
"https://www.bcsw.com.tw/product/KJUCKP17B?category_sn=1594",
"https://www.bcsw.com.tw/product/KJVCKP07B?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKC40DN?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKC43DN?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKC44DN?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKC46HN?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKC47HN?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKC48HN?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKC55?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKC66?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKC67?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKC68?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB07?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB15?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB18?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB19?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB202?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB23?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB41?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB44?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB46?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB48?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB51?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB51S?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB54?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB74?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB76?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB76WB?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB76WS?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB77?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB77WB?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB77WBS?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB88?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKCB89?category_sn=1594",
"https://www.bcsw.com.tw/product/KWCKMB15?category_sn=1594",
"https://www.bcsw.com.tw/product/LSC6904MB?category_sn=1594",
"https://www.bcsw.com.tw/product/OCKP07B?category_sn=1594",
"https://www.bcsw.com.tw/product/RACKJ-CZP09?category_sn=1594",
"https://www.bcsw.com.tw/product/UD-102LA?category_sn=1594",
"https://www.bcsw.com.tw/product/UD-102LB?category_sn=1594",
"https://www.bcsw.com.tw/product/UD-102LS?category_sn=1594",
"https://www.bcsw.com.tw/product/UD-102P-BA?category_sn=1594",
"https://www.bcsw.com.tw/product/UD-102P-BB?category_sn=1594",
"https://www.bcsw.com.tw/product/UD-102P-BS?category_sn=1594",
"https://www.bcsw.com.tw/product/UD-102P-SB?category_sn=1594",
"https://www.bcsw.com.tw/product/UD-801R?category_sn=1594",
"https://www.bcsw.com.tw/product/UD-802R?category_sn=1594",
"https://www.bcsw.com.tw/product/UDSP-100-A?category_sn=1594",
"https://www.bcsw.com.tw/product/UDSP-100-B?category_sn=1594",
"https://www.bcsw.com.tw/product/UDSP-100-S?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CB01?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CB03?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN01?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN02?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN03?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN05?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN08?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN09?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN10?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN11?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN12?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN13?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN14?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN15?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN17?category_sn=1594",
"https://www.bcsw.com.tw/product/UM45CN18?category_sn=1594",
"https://www.bcsw.com.tw/product/UMCS1911?category_sn=1594",
"https://www.bcsw.com.tw/product/UMCSMOS17Z?category_sn=1594",
"https://www.bcsw.com.tw/product/UMCSMOS19Z?category_sn=1594",
"https://www.bcsw.com.tw/product/UMGSMOS17?category_sn=1594",
"https://www.bcsw.com.tw/product/UMGSMOS17CT?category_sn=1594",
"https://www.bcsw.com.tw/product/UMGSMOS17T?category_sn=1594",
"https://www.bcsw.com.tw/product/UMT4E112?category_sn=1594",
"https://www.bcsw.com.tw/product/UMT4E112BU?category_sn=1594",
"https://www.bcsw.com.tw/product/UMT4E123?category_sn=1594",
"https://www.bcsw.com.tw/product/WEE017CB?category_sn=1594",
"https://www.bcsw.com.tw/product/WEXC001?category_sn=1594",
"https://www.bcsw.com.tw/product/WEXC002?category_sn=1594",
"https://www.bcsw.com.tw/product/WEXC004?category_sn=1594",
"https://www.bcsw.com.tw/product/WEXC005?category_sn=1594",
"https://www.bcsw.com.tw/product/WEXC006?category_sn=1594",
"https://www.bcsw.com.tw/product/WG301B?category_sn=1594",
"https://www.bcsw.com.tw/product/WG792B?category_sn=1594",
"https://www.bcsw.com.tw/product/WGGUNS0049?category_sn=1594",
"https://www.bcsw.com.tw/product/WGPG1058?category_sn=1594",
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
