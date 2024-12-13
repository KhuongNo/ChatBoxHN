import asyncio
import os
from Functions.take_screenshot_for_transaction import take_screenshot2

async def search_transaction(page, extracted_data, index, file_type, custom_text):
    await page.get_by_label("TD - Tìm kiếm lịch sử giao dịch", exact=True).click()
    frame = page.frame_locator("iframe[title=\"Coach\"]")
    
    await frame.get_by_role("textbox", name="Lựa chọn").click()
    await frame.get_by_role("option", name="Đề xuất CTD CN").click()
    
    # Use the extracted data in the placeholder
    input_field = frame.get_by_placeholder("Nhập mã giao dịch")
    await input_field.click()
    await input_field.fill(extracted_data)
    
    await frame.get_by_role("button", name=" Tìm kiếm").click()
    await frame.get_by_role("button", name="!").click()
    await asyncio.sleep(7)
    # Take a screenshot after performing the search with the specified filename
    screenshot_path = await take_screenshot2(page, "Search transaction completed", index, file_type, custom_text)
    print(f"Screenshot saved to {screenshot_path}")
