async def response(page, record):

    response_selector = 'div[style*="display: inline-block"][style*="background-color: white"]'
    initial_responses = await page.query_selector_all(response_selector)
    initial_count = len(initial_responses)
    await page.get_by_placeholder("Nhập tin nhắn...").fill(record["data"])
    await page.get_by_placeholder("Nhập tin nhắn...").press("Enter")
    await page.wait_for_function(
        f"document.querySelectorAll('{response_selector}').length > {initial_count}"
    )

    # Lấy tất cả phản hồi hiện tại
    responses = await page.query_selector_all(response_selector)

    # Bỏ qua phản hồi cũ, chỉ lấy phản hồi mới
    new_responses = responses[initial_count:]  # Lấy các phản hồi mới từ index `initial_count`
    latest_response = await new_responses[-1].inner_text() if new_responses else "No response found"

    # In ra câu hỏi và phản hồi (có thể bỏ qua nếu không cần thiết)
    print(f"Câu hỏi: {record['data']}")
    print(f"Phản hồi: {latest_response}")

    # Trả về phản hồi để sử dụng ở hàm gọi
    return latest_response
