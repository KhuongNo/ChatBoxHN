import os

async def take_screenshot2(page, error_message, index, file_type, custom_text):
    custom_path = "D:\\PythonTest\\Capture2"
    
    if file_type not in ["LSGD", "CVCT"]:
        raise ValueError("Invalid file_type provided. Use 'LSGD' or 'CVCT'.")
    
    filename = f"{file_type}_{custom_text}_Testcase_{index}.png"
    screenshot_path = os.path.join(custom_path, filename)
    
    # Ensure the directory exists
    if not os.path.exists(custom_path):
        os.makedirs(custom_path)
    
    # Save the screenshot
    await page.screenshot(path=screenshot_path)
    
    return screenshot_path
