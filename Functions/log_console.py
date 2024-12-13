import asyncio
import aiohttp
from playwright.async_api import Page
from openpyxl import Workbook
import time
import json

async def fetch_error_code(url, line_number, column_number):
    try:
        if not url.startswith('http'):
            return "Invalid URL format"

        # Disable SSL certificate verification
        connector = aiohttp.TCPConnector(ssl=False)

        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url) as response:
                if response.status == 200:
                    code = await response.text()
                    lines = code.splitlines()
                    if int(line_number) <= len(lines):
                        error_line = lines[int(line_number) - 1]
                        return error_line[max(0, int(column_number) - 5000):int(column_number) + 5000]  # Capture a snippet of 10,000 characters around the error
                    else:
                        return "Line number exceeds the content length"
                else:
                    return f"Failed to fetch code: HTTP {response.status}"
    except Exception as e:
        return f"Error fetching code: {str(e)}"

async def log_console(page: Page, output_file: str):
    # Create a new Excel workbook and sheet
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Console Logs"

    # Write headers to the sheet
    headers = ["Action", "Message Type", "Message Text", "Location URL", "Line Number", "Column Number", "Timestamp", "Error Code"]
    sheet.append(headers)

    # Initialize a variable to keep track of the current action
    current_action_label = "unknown"

    async def handle_console_message(msg):
        if msg.type in ["error", "warning"]:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            location = msg.location or {}
            location_url = location.get('url', '')
            line_number = location.get('lineNumber', 0)
            column_number = location.get('columnNumber', 0)
            if 'Custom Error Log:' in msg.text or 'Custom Unhandled Rejection:' in msg.text:
                try:
                    error_details = json.loads(msg.text.split(':', 1)[1].strip())
                    error_code = error_details.get('error') or error_details.get('reason')
                    row = [current_action_label, msg.type, error_details.get('message'), error_details.get('source'), error_details.get('lineno'), error_details.get('colno'), timestamp, error_code]
                except json.JSONDecodeError:
                    row = [current_action_label, msg.type, msg.text, location_url, line_number, column_number, timestamp, "Error parsing custom log"]
            else:
                row = [current_action_label, msg.type, msg.text, location_url, line_number, column_number, timestamp, "N/A"]
            sheet.append(row)

    # Function to update the action label
    async def update_action_label(label):
        nonlocal current_action_label
        current_action_label = label

    # Add the event listener to log console messages
    page.on("console", lambda msg: asyncio.create_task(handle_console_message(msg)))

    # Function to save the workbook periodically
    async def save_workbook_periodically():
        while True:
            workbook.save(output_file)
            await asyncio.sleep(10)  # Save every 10 seconds

    # Start the periodic saving
    asyncio.create_task(save_workbook_periodically())

    # Inject a script to catch errors and log them with additional details
    await page.evaluate("""
        window.addEventListener('error', event => {
            console.error('Custom Error Log:', JSON.stringify({
                message: event.message,
                source: event.filename,
                lineno: event.lineno,
                colno: event.colno,
                error: event.error ? event.error.toString() : ''
            }));
        });

        window.addEventListener('unhandledrejection', event => {
            console.error('Custom Unhandled Rejection:', JSON.stringify({
                reason: event.reason ? event.reason.toString() : ''
            }));
        });
    """)

    return update_action_label
