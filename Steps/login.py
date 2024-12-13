import asyncio


async def login(page):
    await page.get_by_placeholder("Username").fill("thamdt@hpt.vn")
    await page.get_by_placeholder("Password").fill("123456")
    await page.get_by_role("button", name="Login").click()
    await asyncio.sleep(5)
    # await page.goto("http://10.4.18.152:3001/dashboard")
    # await page.get_by_role("button", name="wechat").click()
    # await page.get_by_role("button", name="Bắt đầu").click()
    
