import asyncpg  # Đây là thư viện để làm việc với PostgreSQL

async def run_query(query):
    conn = None
    try:
        # Sử dụng DSN hợp lệ để kết nối với PostgreSQL
        dsn = "postgresql://postgres:Hpt123456@10.4.18.143:54323/RMP"
        conn = await asyncpg.connect(dsn=dsn)  # Kết nối với cơ sở dữ liệu
        result = await conn.fetch(query)
        print(f"Query result: {result}")  # Thực thi câu truy vấn và trả về kết quả
        return result  # Trả về danh sách kết quả
    except Exception as e:
        print(f"Error running query: {e}")
        return None
    finally:
        if conn:
            await conn.close()  # Đảm bảo kết nối được đóng
