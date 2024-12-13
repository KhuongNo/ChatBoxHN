import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

async def log_task_in_jira(jira_url, jira_username, jira_password, task_title, task_description, screenshot_path):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        try:
            await page.goto(jira_url, timeout=100000)
            await page.fill('input#login-form-username', jira_username)
            await page.fill('input#login-form-password', jira_password)
            async with page.expect_navigation():
                await page.click('input#login-form-submit')

            await page.goto(f'{jira_url.replace("login.jsp", "")}/secure/CreateIssue!default.jspa')
            await page.get_by_label("Project Required").fill("P. Kiểm thử phần mềm - HAS (PKTPMH)")
            await page.get_by_label("Issue Type Required").fill("Bug")
            await page.get_by_role("button", name="Next").click()
            await page.fill('input#summary', task_title)
            await page.get_by_role("button", name="Assign to me").click()
            await page.locator("#components-multi-select span").click()
            await page.get_by_role("link", name="Auto Log Jira").click()

            current_date = datetime.now().strftime("%d/%b/%y").lstrip('0').replace(' 0', ' ')
            await page.get_by_label("Due Date (d/MMM/yy) Required").fill(current_date)

            await page.fill('textarea#description', task_description)
            await page.get_by_label("Môi trường thực hiện kiểm th").select_option("10306")
            await page.locator("#customfield_10100-single-select span").click()
            await page.get_by_role("link", name="Test auto upload Jira - (").click()

            await page.set_input_files('input[type="file"]', screenshot_path)
            await asyncio.sleep(5)
            await page.get_by_title("Press Alt+s to submit this").click(timeout=100000)
            print('Task created successfully!')
            await context.close()
            await browser.close()
        except Exception as e:
            print(f'Failed to log issue in Jira: {e}')
            await context.close()
            await browser.close()
