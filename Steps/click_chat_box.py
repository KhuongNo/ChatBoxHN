import asyncio


async def click_chat_box(page):
    await page.get_by_role("button", name="wechat").click()
    await page.get_by_role("button", name="Bắt đầu").click()
    
