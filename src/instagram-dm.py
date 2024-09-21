import asyncio, json, random
from playwright.async_api import async_playwright

insta_username = "username"
insta_password = "password"

async def send_insta_DM(influencers):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = False)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            viewport={'width': 1280, 'height': 800},
            accept_downloads=True
        )
        context.set_default_timeout(100000)

        # Navigate to Etsy domain first
        page = await context.new_page()
        await page.goto("https://www.instagram.com")
        await asyncio.sleep(random.uniform(1, 2))

        # Load cookies from the JSON file
        with open(f'./instagram.json', 'r') as cookies_file:
            cookies = json.load(cookies_file)
            await context.add_cookies(cookies)
        await asyncio.sleep(random.uniform(1, 2))
        await page.reload()
        # await page.pause()

        for influencer in influencers:
            await page.goto(f"https://www.instagram.com/{influencer}/")
            if await page.locator("button", name="Message").count() == 0:
                print(f"{influencer} - No message option. Skipping")
                continue
            await page.get_by_role("button", name="Message").click()
            await page.get_by_role("paragraph").click()
            message = influencers[influencer]
            await page.get_by_label("Message", exact=True).fill(message)
            print(f"Sending message to {influencer}")
            asyncio.sleep(10)

        # ---------------------
        context.close()
        browser.close()

asyncio.run(send_insta_DM())