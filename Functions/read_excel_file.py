import openpyxl

def read_excel_file(file_path: str):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    data = []
    
    for row in sheet.iter_rows(min_row=2, values_only=True):  # Bắt đầu từ dòng thứ 2 để bỏ qua header
        if row[0] is None:  # Kiểm tra nếu giá trị trong cột đầu tiên là None
            break  # Dừng khi gặp dòng có giá trị None trong cột đầu tiên
        data.append({
            "IsRefresh": str(row[1]) if row[1] is not None else "",
            "data": str(row[2]) if row[2] is not None else "",
            "query": str(row[5]) if row[5] is not None else ""  # Lấy câu query từ cột thứ 5 (index 4)
        })
    
    return data 
