from datetime import datetime
from playwright.async_api import Page

async def take_screenshot(page: Page, error_message: str, index: int):
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"D:\\PythonTest\\Capture\\error_{index}_{current_time}.png"
    await page.screenshot(path=screenshot_path)
    print(f"Error: {error_message}")
    print(f"Screenshot saved to {screenshot_path}")
    return screenshot_path
