# SoulMatch Bot 🤖💬

Bot Telegram để kết nối người dùng trò chuyện ẩn danh ngẫu nhiên với hệ thống bảo vệ toàn diện.

## ✨ Tính năng

- 🔍 **Kết nối thông minh**: Tìm kiếm dựa trên giới tính và sở thích
- 💬 **Trò chuyện ẩn danh**: Chat 1-1 hoàn toàn bảo mật
- �️ **Bảo vệ trẻ em**: Xác thực tuổi 18+ và lọc nội dung
- ⚡ **Phản ứng nhanh**: Kết nối tức thì, dễ sử dụng
- 🔄 **Linh hoạt**: Tìm người mới, thay đổi sở thích

## 🛡️ An toàn & Bảo vệ

### Xác thực tuổi bắt buộc

- ✅ Yêu cầu xác nhận 18+ trước khi sử dụng
- ⚖️ Cảnh báo pháp lý rõ ràng về trách nhiệm
- 🚫 Từ chối dịch vụ cho người chưa đủ tuổi

### Hệ thống lọc nội dung

- 🤖 Phát hiện tự động ngôn ngữ của trẻ em
- � Phân tích hành vi nghi ngờ
- ⚡ Xử lý vi phạm tức thì

### Tuân thủ pháp luật

- 🇻🇳 Luật Trẻ em Việt Nam 2016
- 🌍 Tiêu chuẩn quốc tế COPPA, GDPR
- 📋 Chính sách riêng tư nghiêm ngặt

## 🚀 Cách sử dụng

1. **Bắt đầu**: `/start` - Đăng ký và xác thực tuổi
2. **Thiết lập hồ sơ**: Chọn giới tính và sở thích
3. **Tìm kiếm**: `/find` - Kết nối với người phù hợp
4. **Trò chuyện**: Nhắn tin tự nhiên
5. **Kết thúc**: `/stop` - Dừng và tìm người mới

## 🛠️ Công nghệ

- **Python 3.11+** - Core runtime
- **aiogram 3.15.0** - Telegram Bot framework
- **python-dotenv** - Environment management
- **Railway** - Cloud deployment platform
- **Smart Matching** - Thuật toán ghép đôi thông minh

## 📦 Cài đặt local

### Yêu cầu

- Python 3.11+
- Telegram Bot Token (từ @BotFather)

### Bước 1: Clone repository

```bash
git clone <repository-url>
cd souldmatch
```

### Bước 2: Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình environment

Tạo file `.env`:

```
TOKEN=your_telegram_bot_token_here
```

### Bước 4: Chạy bot

```bash
python bot.py
```

Hoặc dùng file batch:

```bash
run_bot.bat
```

## 🌐 Deploy lên Railway

Xem hướng dẫn chi tiết trong [DEPLOY.md](DEPLOY.md)

### Nhanh chóng:

1. Fork/clone repository này
2. Tạo project mới trên [Railway](https://railway.app)
3. Kết nối với GitHub repository
4. Thêm environment variable `TOKEN`
5. Deploy!

## 📁 Cấu trúc project

```
souldmatch/
├── bot.py              # Main bot code
├── requirements.txt    # Python dependencies
├── Procfile           # Railway/Heroku deployment
├── runtime.txt        # Python version
├── railway.json       # Railway configuration
├── .env               # Environment variables (local)
├── .gitignore         # Git ignore rules
├── README.md          # Project documentation
├── DEPLOY.md          # Deployment guide
└── run_bot.bat        # Windows batch file
```

## 🔧 Cấu hình

### Environment Variables

- `TOKEN`: Telegram Bot Token (bắt buộc)

### Bot Commands

- `/start` - Bắt đầu và hiển thị hướng dẫn
- `/find` - Tìm kiếm người trò chuyện
- `/stop` - Kết thúc cuộc trò chuyện hiện tại

## 🐛 Troubleshooting

### Bot không phản hồi:

- Kiểm tra TOKEN có đúng không
- Đảm bảo bot đã được start với BotFather
- Xem logs để tìm lỗi

### Lỗi khi cài đặt:

- Cập nhật pip: `pip install --upgrade pip`
- Dùng Python 3.11+ thay vì 3.13 nếu có lỗi build

### Deployment issues:

- Kiểm tra Procfile và requirements.txt
- Đảm bảo environment variables đã được set
- Xem logs trên Railway dashboard

## 📚 Tài liệu

- **[CHILD_PROTECTION.md](./CHILD_PROTECTION.md)** - Hệ thống bảo vệ trẻ em
- **[DEPLOY.md](./DEPLOY.md)** - Hướng dẫn deployment và pháp lý

## ⚖️ Lưu ý pháp lý

- 🔞 **Chỉ dành cho người từ 18 tuổi trở lên**
- 📋 Tuân thủ Luật Trẻ em Việt Nam 2016
- 🛡️ Bảo vệ dữ liệu theo GDPR và luật Việt Nam
- 📞 Báo cáo vi phạm: safety@soulmatch.vn

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

Dự án này được bảo vệ bởi luật sở hữu trí tuệ. Việc sử dụng phải tuân thủ các điều khoản và điều kiện.

---

**⚠️ Cảnh báo**: Dự án này chỉ dành cho mục đích giáo dục và phát triển. Việc triển khai thương mại cần tuân thủ đầy đủ quy định pháp luật về bảo vệ trẻ em và quyền riêng tư.

## 📝 License

MIT License - Xem file LICENSE để biết thêm chi tiết.

## 🤝 Contributing

1. Fork repository
2. Tạo feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Tạo Pull Request

## 📞 Support

Nếu gặp vấn đề, tạo issue trên GitHub hoặc liên hệ qua Telegram.

---

Made with ❤️ for anonymous conversations
