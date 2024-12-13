from playwright.async_api import Page

async def capture_current_url(page: Page) -> str:
    return page.url
