# Hướng dẫn chạy SoulMatch Bot

## Yêu cầu
- Python 3.7+ đã cài đặt
- Token bot Telegram (đã có trong file .env)

## Cách chạy

1. Mở Command Prompt hoặc PowerShell
2. Chuyển đến thư mục dự án:
   ```
   cd d:\1project\souldmatch
   ```

3. Cài đặt dependencies:
   ```
   pip install -r requirements.txt
   ```
   
   Hoặc cài từng package:
   ```
   pip install aiogram==2.25.1 python-dotenv==1.0.0
   ```

4. Chạy bot:
   ```
   python bot.py
   ```

## Nếu gặp lỗi "Python was not found"

1. Cài đặt Python từ https://www.python.org/downloads/
2. Hoặc chạy lệnh `python` trong cmd để cài từ Microsoft Store
3. Đảm bảo check "Add Python to PATH" khi cài đặt

## Cách sử dụng bot

1. Tìm bot trên Telegram bằng username
2. Gõ `/start` để bắt đầu
3. Gõ `/find` để tìm người trò chuyện
4. Gõ `/stop` để kết thúc trò chuyện

## Tính năng
- Kết nối 2 người dùng ngẫu nhiên để trò chuyện ẩn danh
- Chuyển tiếp tin nhắn giữa 2 người
- Quản lý trạng thái kết nối
