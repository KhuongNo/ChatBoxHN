import asyncio
from Functions.take_screenshot_for_transaction import take_screenshot2


async def search_workList(page, index, file_type, custom_text):

    await page.get_by_label("Main Menu").click()
    await page.get_by_label("Công việc của tôi", exact=True).click()
    await page.get_by_label("Main Menu").click()
    await asyncio.sleep(10)
    screenshot_path = await take_screenshot2(page, "Search WorkList complete", index, file_type,custom_text)
    print(f"Screenshot saved to {screenshot_path}")