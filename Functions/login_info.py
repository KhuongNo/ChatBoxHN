from playwright.async_api import Page

async def login_info(page: Page, username: str, password: str):
    await page.get_by_label("Log Out").click()
    await page.get_by_placeholder("Username").fill(username)
    await page.get_by_placeholder("Password").fill(password)
    await page.get_by_placeholder("Password").press("Enter")
