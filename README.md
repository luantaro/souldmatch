# SoulMatch Bot 🤖💬

Bot Telegram để kết nối người dùng trò chuyện ẩn danh ngẫu nhiên.

## ✨ Tính năng

- 🔍 Tìm kiếm người trò chuyện ngẫu nhiên
- 💬 Trò chuyện ẩn danh 1-1
- 🚫 Kết thúc cuộc trò chuyện bất cứ lúc nào
- 🔄 Tìm kiếm người mới sau khi kết thúc

## 🚀 Cách sử dụng

1. **Bắt đầu**: `/start` - Chào mừng và hướng dẫn
2. **Tìm kiếm**: `/find` - Tìm người để trò chuyện
3. **Trò chuyện**: Gõ tin nhắn bình thường
4. **Kết thúc**: `/stop` - Dừng cuộc trò chuyện

## 🛠️ Công nghệ

- **Python 3.11+**
- **aiogram 3.15.0** - Telegram Bot framework
- **python-dotenv** - Environment variables
- **Railway** - Cloud deployment

## 📦 Cài đặt local

### Yêu cầu

- Python 3.11+
- Telegram Bot Token

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
