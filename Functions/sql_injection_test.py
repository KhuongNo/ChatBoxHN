from playwright.async_api import Page
import openpyxl
from openpyxl import Workbook
import asyncio

async def test_sql_injection(page: Page, url: str, input_selectors: list, sql_payloads: list, output_file: str):
    # Create a new Excel workbook and sheet
    workbook = Workbook()
    results_sheet = workbook.active
    results_sheet.title = "SQL Injection Test Results"

    # Write headers to the results sheet
    headers = ["URL", "Payload", "Input Field", "Result"]
    results_sheet.append(headers)

    # Loop through each SQL payload and input field
    for payload in sql_payloads:
        for selector in input_selectors:
            try:
                # Navigate to the URL
                await page.goto(url)

                # Find the input field and fill with the payload
                await page.fill(selector, payload)

                # Submit the form (assuming form submission via Enter key)
                await page.press(selector, "Enter")

                # Wait for response (adjust timeout as necessary)
                await page.wait_for_load_state('networkidle', timeout=10000)

                # Capture response body (or relevant part of the page that changes)
                response_body = await page.content()

                # Check for typical SQL error messages in the response
                sql_errors = ["syntax error", "unrecognized token", "SQL", "MySQL", "ORA-", "ODBC"]
                result = "No SQL error found"

                for error in sql_errors:
                    if error.lower() in response_body.lower():
                        result = f"SQL error found: {error}"
                        break

                # Append result to the sheet
                results_sheet.append([url, payload, selector, result])

            except Exception as e:
                # Handle exceptions and log as errors in the results
                results_sheet.append([url, payload, selector, f"Error: {e}"])

    # Save the workbook to the specified output file
    workbook.save(output_file)

