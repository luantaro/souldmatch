# Deploy SoulMatch Bot lên Railway

## Chuẩn bị

### 1. Tạo tài khoản Railway
- Truy cập https://railway.app/
- Đăng ký/đăng nhập bằng GitHub

### 2. Cài đặt Railway CLI (Tùy chọn)
```bash
npm install -g @railway/cli
```

## Phương pháp 1: Deploy qua GitHub (Khuyên dùng)

### Bước 1: Tạo repository GitHub
1. Tạo repository mới trên GitHub
2. Clone hoặc upload code lên repository

### Bước 2: Kết nối Railway với GitHub
1. Vào Railway Dashboard
2. Click "New Project"
3. Chọn "Deploy from GitHub repo"
4. Chọn repository của bạn

### Bước 3: Cấu hình Environment Variables
Trong Railway Dashboard:
1. Vào tab "Variables"
2. Thêm biến môi trường:
   - `TOKEN` = `8324524420:AAHmXRfwlQ2cCuz9kfNFQ380JAuUU3yzS38`

### Bước 4: Deploy
Railway sẽ tự động build và deploy bot.

## Phương pháp 2: Deploy trực tiếp qua Railway CLI

### Bước 1: Login Railway CLI
```bash
railway login
```

### Bước 2: Khởi tạo project
```bash
railway init
```

### Bước 3: Thêm environment variables
```bash
railway variables set TOKEN=8324524420:AAHmXRfwlQ2cCuz9kfNFQ380JAuUU3yzS38
```

### Bước 4: Deploy
```bash
railway up
```

## Kiểm tra deployment

1. Vào Railway Dashboard
2. Kiểm tra logs để đảm bảo bot khởi động thành công
3. Test bot trên Telegram

## Lưu ý quan trọng

- Bot sẽ chạy 24/7 trên Railway
- Railway cung cấp 500 giờ miễn phí mỗi tháng
- Logs có thể xem trực tiếp trên Dashboard
- Khi có thay đổi code, push lên GitHub để auto-deploy

## Files quan trọng đã tạo:

- `Procfile`: Định nghĩa lệnh chạy app
- `requirements.txt`: Dependencies Python  
- `runtime.txt`: Phiên bản Python
- `.gitignore`: Files bỏ qua khi commit
- `railway.json`: Cấu hình Railway (tùy chọn)

## Troubleshooting

### Bot không khởi động:
1. Kiểm tra logs trên Railway Dashboard
2. Đảm bảo TOKEN environment variable đã được set
3. Kiểm tra requirements.txt có đúng dependencies

### Bot bị crash:
1. Xem logs để tìm lỗi
2. Restart service trên Railway Dashboard
3. Kiểm tra code có lỗi syntax không
