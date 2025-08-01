# bot.py
import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()

# Lưu trữ thông tin người dùng
users = {}
waiting_users = {
    'male_seeking_female': [],
    'male_seeking_male': [],
    'female_seeking_male': [],
    'female_seeking_female': [],
    'any_seeking_any': []
}
connections = {}

# Content filtering để phát hiện trẻ em
MINOR_KEYWORDS = [
    "học sinh", "lớp 12", "lớp 11", "lớp 10", "lớp 9", "trường", "học bài",
    "bài tập", "kiểm tra", "thi cử", "phụ huynh", "bố mẹ", "ba má", 
    "cấp 3", "cấp 2", "thcs", "thpt", "đại học sắp thi", "tốt nghiệp",
    "em mới", "em còn nhỏ", "tuổi teen", "chưa 18", "17 tuổi", "16 tuổi", "15 tuổi"
]

async def check_minor_behavior(message_text, user_id):
    """Phát hiện hành vi nghi ngờ trẻ em"""
    if not message_text:
        return False
        
    text_lower = message_text.lower()
    violations = 0
    
    for keyword in MINOR_KEYWORDS:
        if keyword in text_lower:
            violations += 1
    
    if violations >= 2:  # Nghi ngờ nếu match nhiều keyword
        await handle_minor_detection(user_id)
        return True
    
    return False

async def handle_minor_detection(user_id):
    """Xử lý khi phát hiện nghi ngờ trẻ em"""
    try:
        await bot.send_message(
            user_id,
            "🚫 **TÀI KHOẢN BỊ ĐÌNH CHỈ**\n\n"
            "⚠️ **Lý do:** Hệ thống phát hiện dấu hiệu bạn chưa đủ 18 tuổi\n\n"
            "📋 **Thông tin:**\n"
            "• SoulMatch chỉ dành cho người từ 18+ tuổi\n"
            "• Việc khai báo sai tuổi vi phạm điều khoản sử dụng\n"
            "• Tài khoản đã bị khóa vĩnh viễn\n\n"
            "📚 **Lời khuyên:**\n"
            "• Sử dụng app phù hợp với độ tuổi của bạn\n"
            "• Tập trung vào học tập và phát triển bản thân\n"
            "• Kết bạn trong môi trường an toàn\n\n"
            "🔒 **Quyết định này là cuối cùng và không thể thay đổi.**",
            parse_mode='Markdown'
        )
    except:
        pass  # User có thể đã block bot
    
    # Xóa user khỏi hệ thống
    if user_id in users:
        user = users[user_id]
        # Ngắt kết nối nếu đang chat
        if user.partner_id:
            partner_id = user.partner_id
            try:
                await bot.send_message(
                    partner_id, 
                    "⚠️ **Cuộc trò chuyện đã kết thúc**\n\n"
                    "Người kia đã vi phạm điều khoản sử dụng và bị cấm tài khoản.\n"
                    "Vui lòng tìm kiếm người khác để trò chuyện."
                )
            except:
                pass
            
            users[partner_id].partner_id = None
            if partner_id in connections:
                del connections[partner_id]
        
        # Xóa khỏi waiting queue
        for queue in waiting_users.values():
            if user_id in queue:
                queue.remove(user_id)
        
        # Xóa user
        del users[user_id]
        if user_id in connections:
            del connections[user_id]

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self.gender = None
        self.seeking = None
        self.partner_id = None
        self.is_registered = False
        self.age_verified = False  # Thêm trường xác minh tuổi
        self.disclaimer_accepted = False  # Thêm trường xác nhận disclaimer

def get_age_verification_keyboard():
    """Keyboard cho xác minh tuổi"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tôi đã đủ 18 tuổi", callback_data="age_verified")],
        [InlineKeyboardButton(text="❌ Tôi chưa đủ 18 tuổi", callback_data="age_under")]
    ])
    return keyboard

def get_gender_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨 Nam", callback_data="gender_male")],
        [InlineKeyboardButton(text="👩 Nữ", callback_data="gender_female")],
        [InlineKeyboardButton(text="🤷 Không muốn tiết lộ", callback_data="gender_other")]
    ])
    return keyboard

def get_seeking_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👨 Tìm Nam", callback_data="seek_male")],
        [InlineKeyboardButton(text="👩 Tìm Nữ", callback_data="seek_female")],
        [InlineKeyboardButton(text="🌈 Tìm Bất kỳ", callback_data="seek_any")]
    ])
    return keyboard

def get_main_menu_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔍 Tìm người trò chuyện", callback_data="find_chat")],
        [InlineKeyboardButton(text="⚙️ Cài đặt hồ sơ", callback_data="settings")],
        [InlineKeyboardButton(text="❌ Kết thúc chat", callback_data="stop_chat")]
    ])
    return keyboard

def get_intro_keyboard():
    """Keyboard cho màn hình giới thiệu"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Bắt đầu đăng ký", callback_data="start_register")],
        [InlineKeyboardButton(text="ℹ️ Xem thêm tính năng", callback_data="show_features")]
    ])
    return keyboard

def get_features_keyboard():
    """Keyboard cho màn hình tính năng"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Bắt đầu ngay", callback_data="start_register")],
        [InlineKeyboardButton(text="🔒 Chính sách bảo mật", callback_data="privacy_policy")]
    ])
    return keyboard

def get_disclaimer_keyboard():
    """Keyboard cho tuyên bố miễn trừ trách nhiệm"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tôi đã đọc và đồng ý với mọi điều khoản", callback_data="disclaimer_accepted")],
        [InlineKeyboardButton(text="❌ Tôi không đồng ý", callback_data="disclaimer_rejected")]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        users[user_id] = User(user_id)
    
    user = users[user_id]
    
    if not user.age_verified:
        # Age verification TRƯỚC mọi thứ
        age_warning = (
            "⚠️ **KIỂM TRA TUỔI**\n\n"
            "🔞 **SoulMatch chỉ dành cho người ĐỦ 18 TUỔI TRỞ LÊN**\n\n"
            "⚖️ **QUAN TRỌNG:**\n"
            "• Khai báo sai tuổi vi phạm pháp luật Việt Nam\n"
            "• Chúng tôi sẽ kiểm tra và cấm tài khoản gian lận\n"
            "• Trẻ em vui lòng không sử dụng dịch vụ này\n"
            "• Báo cáo ngay cho phụ huynh nếu phát hiện vi phạm\n\n"
            "🛡️ **CAM KẾT CỦA BẠN:**\n"
            "Bằng cách tiếp tục, bạn xác nhận:\n"
            "✅ Bạn đã đủ 18 tuổi theo pháp luật\n"
            "✅ Hiểu rủi ro khi chat với người lạ\n"
            "✅ Chịu trách nhiệm về hành vi của mình\n"
            "✅ Tuân thủ các quy định của platform\n\n"
            "❓ **Bạn có đủ 18 tuổi không?**"
        )
        
        await message.answer(
            age_warning,
            reply_markup=get_age_verification_keyboard(),
            parse_mode='Markdown'
        )
        return
    
    if not user.is_registered:
        # Tin nhắn chào mừng với giới thiệu chi tiết
        welcome_text = (
            "🎭 **CHÀO MỪNG ĐẾN VỚI SOULMATCH!**\n\n"
            "✨ **Trò chuyện ẩn danh - Kết nối tâm hồn**\n\n"
            "🔥 **Tính năng nổi bật:**\n"
            "• 🎯 **Smart Matching** - Tìm người phù hợp theo sở thích\n"
            "• 🔐 **100% Ẩn danh** - Không lưu thông tin cá nhân\n"
            "• 💬 **Chat tức thì** - Kết nối ngay lập tức\n"
            "• 🌈 **Đa dạng** - Hỗ trợ mọi giới tính & sở thích\n"
            "• 🚫 **An toàn** - Có thể dừng chat bất cứ lúc nào\n\n"
            "🎲 **Cách hoạt động:**\n"
            "1️⃣ Chọn giới tính của bạn\n"
            "2️⃣ Chọn đối tượng muốn trò chuyện\n" 
            "3️⃣ Hệ thống tự động ghép đôi\n"
            "4️⃣ Bắt đầu trò chuyện ẩn danh!\n\n"
            "🔒 **Cam kết:** Hoàn toàn miễn phí và bảo mật!"
        )
        
        await message.answer(
            welcome_text,
            reply_markup=get_intro_keyboard(),
            parse_mode='Markdown'
        )
    else:
        await message.answer(
            f"👋 **Chào mừng trở lại!**\n\n"
            f"📋 **Hồ sơ của bạn:**\n"
            f"• Giới tính: {user.gender}\n"
            f"• Tìm kiếm: {user.seeking}\n\n"
            f"Bạn muốn làm gì?",
            reply_markup=get_main_menu_keyboard(),
            parse_mode='Markdown'
        )

@dp.callback_query(lambda c: c.data == 'age_verified')
async def age_verified(callback_query: CallbackQuery):
    """Xử lý khi user xác nhận đủ 18 tuổi"""
    user_id = callback_query.from_user.id
    user = users[user_id]
    user.age_verified = True
    
    # Legal disclaimer mạnh mẽ
    legal_disclaimer = (
        "⚖️ **TUYÊN BỐ PHÁP LÝ**\n\n"
        "🔞 **Xác nhận tuổi:** Bạn đã cam kết mình đủ 18 tuổi\n\n"
        "🚫 **VI PHẠM SẼ BỊ:**\n"
        "• Cấm tài khoản vĩnh viễn\n"
        "• Báo cáo cho cơ quan chức năng\n"
        "• Truy cứu trách nhiệm pháp lý\n\n"
        "⚠️ **NGƯỜI DÙNG CHỊU TRÁCH NHIỆM:**\n"
        "• Tự bảo vệ thông tin cá nhân\n"
        "• Không gặp mặt người lạ một mình\n"
        "• Báo cáo hành vi đáng ngờ ngay lập tức\n"
        "• Không chia sẻ nội dung không phù hợp\n\n"
        "📞 **LIÊN HỆ KHẨN CẤP:**\n"
        "Báo ngay cho phụ huynh/cơ quan chức năng nếu gặp vấn đề\n\n"
        "🎭 **Bây giờ, chào mừng đến với SoulMatch!**"
    )
    
    await callback_query.message.edit_text(
        legal_disclaimer,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🎯 Tôi hiểu và đồng ý", callback_data="legal_accepted")]
        ]),
        parse_mode='Markdown'
    )

@dp.callback_query(lambda c: c.data == 'age_under')
async def age_under(callback_query: CallbackQuery):
    """Xử lý khi user chưa đủ 18 tuổi"""
    await callback_query.message.edit_text(
        "🚫 **XIN LỖI!**\n\n"
        "SoulMatch chỉ dành cho người từ **18 tuổi trở lên**.\n\n"
        "📚 **GIAO HẸNTHÀNH ANH EM:**\n"
        "• Tập trung vào học tập và phát triển bản thân\n"
        "• Tham gia hoạt động lành mạnh phù hợp tuổi\n"
        "• Kết bạn trong môi trường an toàn (trường học, gia đình)\n"
        "• Chờ đến khi đủ 18 tuổi để sử dụng các dịch vụ này\n\n"
        "🌟 **Chúc bạn:**\n"
        "• Học tập tốt và đạt được ước mơ\n"
        "• Phát triển toàn diện và lành mạnh\n"
        "• Có những trải nghiệm tuyệt vời phù hợp với tuổi\n\n"
        "🔒 **Tài khoản này đã bị khóa vì vi phạm độ tuổi.**",
        parse_mode='Markdown'
    )

@dp.callback_query(lambda c: c.data == 'legal_accepted')
async def legal_accepted(callback_query: CallbackQuery):
    """Sau khi user đồng ý các điều khoản pháp lý, hiển thị disclaimer"""
    disclaimer_text = (
        "📋 **TUYÊN BỐ MIỄN TRỪ TRÁCH NHIỆM**\n\n"
        "⚖️ **BẰNG CÁCH SỬ DỤNG SOULMATCH, BẠN ĐỒNG Ý:**\n\n"
        
        "🚫 **MIỄN TRỪ TRÁCH NHIỆM TOÀN DIỆN:**\n"
        "• SoulMatch KHÔNG chịu trách nhiệm về bất kỳ thiệt hại nào\n"
        "• Mọi rủi ro từ việc sử dụng dịch vụ thuộc về người dùng\n"
        "• Platform chỉ là trung gian kết nối, không can thiệp nội dung\n"
        "• Không bảo đảm về tính chính xác thông tin từ người dùng khác\n\n"
        
        "� **THIỆT HẠI KHÔNG CHỊU TRÁCH NHIỆM:**\n"
        "• Lừa đảo, quấy rối từ người dùng khác\n"
        "• Thiệt hại tinh thần, tài chính, danh tiếng\n"
        "• Hậu quả từ việc gặp mặt ngoài đời\n"
        "• Mất mát do chia sẻ thông tin cá nhân\n"
        "• Nội dung không phù hợp từ người khác\n\n"
        
        "�️ **TRÁCH NHIỆM CỦA NGƯỜI DÙNG:**\n"
        "• Tự bảo vệ thông tin cá nhân\n"
        "• Đánh giá rủi ro trước khi hành động\n"
        "• Tuân thủ pháp luật trong mọi hoạt động\n"
        "• Chịu trách nhiệm về mọi hậu quả\n\n"
        
        "⚠️ **CẢNH BÁO ĐẶC BIỆT:**\n"
        "• TUYỆT ĐỐI không gặp mặt người lạ một mình\n"
        "• KHÔNG chia sẻ thông tin tài chính\n"
        "• CẢNH GIÁC với yêu cầu chuyển tiền\n"
        "• BÁO CÁO ngay hành vi đáng ngờ\n\n"
        
        "📞 **KHẨN CẤP:**\n"
        "• Gọi 113 (Cảnh sát) nếu gặp nguy hiểm\n"
        "• Liên hệ gia đình/bạn bè khi cần thiết\n"
        "• Sử dụng các dịch vụ hỗ trợ chính thức\n\n"
        
        "🔒 **XÁC NHẬN CUỐI CÙNG:**\n"
        "Bằng cách nhấn 'Đồng ý', bạn xác nhận:\n"
        "✅ Đã đọc và hiểu toàn bộ điều khoản\n"
        "✅ Chấp nhận mọi rủi ro khi sử dụng\n"
        "✅ Tự chịu trách nhiệm về hành vi của mình\n"
        "✅ Miễn trừ mọi trách nhiệm cho SoulMatch\n\n"
        
        "❓ **Bạn có đồng ý với tất cả điều khoản trên?**"
    )
    
    await callback_query.message.edit_text(
        disclaimer_text,
        reply_markup=get_disclaimer_keyboard(),
        parse_mode='Markdown'
    )

@dp.callback_query(lambda c: c.data == 'disclaimer_accepted')
async def disclaimer_accepted(callback_query: CallbackQuery):
    """Sau khi user đồng ý disclaimer, cho phép truy cập"""
    user_id = callback_query.from_user.id
    user = users[user_id]
    
    # Đánh dấu user đã hoàn thành mọi bước xác thực
    user.disclaimer_accepted = True
    
    # Hiển thị welcome message cuối cùng
    welcome_text = (
        "🎉 **CHÀO MỪNG ĐẾN VỚI SOULMATCH!**\n\n"
        "✨ **Trò chuyện ẩn danh - Kết nối tâm hồn**\n\n"
        "🔥 **Tính năng nổi bật:**\n"
        "• 🎯 **Smart Matching** - Tìm người phù hợp theo sở thích\n"
        "• 🔐 **100% Ẩn danh** - Không lưu thông tin cá nhân\n"
        "• 💬 **Chat tức thì** - Kết nối ngay lập tức\n"
        "• 🌈 **Đa dạng** - Hỗ trợ mọi giới tính & sở thích\n"
        "• 🚫 **An toàn** - Có thể dừng chat bất cứ lúc nào\n\n"
        "🎲 **Cách hoạt động:**\n"
        "1️⃣ Chọn giới tính của bạn\n"
        "2️⃣ Chọn đối tượng muốn trò chuyện\n" 
        "3️⃣ Hệ thống tự động ghép đôi\n"
        "4️⃣ Bắt đầu trò chuyện ẩn danh!\n\n"
        "🔒 **Bạn đã hoàn tất mọi bước xác thực!**\n"
        "Giờ đây có thể sử dụng an toàn và có trách nhiệm."
    )
    
    await callback_query.message.edit_text(
        welcome_text,
        reply_markup=get_intro_keyboard(),
        parse_mode='Markdown'
    )

@dp.callback_query(lambda c: c.data == 'disclaimer_rejected')
async def disclaimer_rejected(callback_query: CallbackQuery):
    """Khi user không đồng ý disclaimer"""
    await callback_query.message.edit_text(
        "🚫 **KHÔNG THỂ SỬ DỤNG DỊCH VỤ**\n\n"
        "Do bạn không đồng ý với các điều khoản miễn trừ trách nhiệm,\n"
        "chúng tôi không thể cung cấp dịch vụ.\n\n"
        "📋 **Lý do:**\n"
        "• Việc đồng ý với điều khoản là bắt buộc\n"
        "• Đây là yêu cầu pháp lý để bảo vệ cả hai bên\n"
        "• Không có ngoại lệ cho quy định này\n\n"
        "💡 **Gợi ý:**\n"
        "• Đọc kỹ điều khoản và cân nhắc lại\n"
        "• Tìm hiểu về các rủi ro và cách phòng tránh\n"
        "• Sử dụng các dịch vụ khác phù hợp hơn\n\n"
        "🔒 **Truy cập bị từ chối vĩnh viễn.**",
        parse_mode='Markdown'
    )
@dp.callback_query(lambda c: c.data == 'start_register')
async def start_register(callback_query: CallbackQuery):
    """Bắt đầu quá trình đăng ký - kiểm tra disclaimer trước"""
    user_id = callback_query.from_user.id
    user = users[user_id]
    
    # Kiểm tra disclaimer đã được accept chưa
    if not hasattr(user, 'disclaimer_accepted') or not user.disclaimer_accepted:
        await callback_query.message.edit_text(
            "❌ **CHƯA HOÀN TẤT XÁC THỰC**\n\n"
            "Bạn cần đồng ý với tuyên bố miễn trừ trách nhiệm trước khi đăng ký.\n\n"
            "Vui lòng quay lại và hoàn tất các bước xác thực.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Quay lại xác thực", callback_data="restart_bot")]
            ])
        )
        return
    
    # Nếu đã accept disclaimer, cho phép đăng ký
    await callback_query.message.edit_text(
        "🎯 **ĐĂNG KÝ HỒ SƠ**\n\n"
        "Để tìm được người phù hợp nhất, hãy cho tôi biết giới tính của bạn:\n\n"
        "🔒 *Thông tin này chỉ dùng để ghép đôi và hoàn toàn ẩn danh*",
        reply_markup=get_gender_keyboard(),
        parse_mode='Markdown'
    )

@dp.callback_query(lambda c: c.data == 'show_features')
async def show_features(callback_query: CallbackQuery):
    """Hiển thị chi tiết tính năng"""
    features_text = (
        "🌟 **CHI TIẾT TÍNH NĂNG**\n\n"
        "🎯 **SMART MATCHING:**\n"
        "• Ghép đôi thông minh theo giới tính\n"
        "• Tương thích 2 chiều (cả 2 đều phù hợp)\n"
        "• Hàng chờ riêng cho từng sở thích\n\n"
        "🔐 **BẢO MẬT & AN TOÀN:**\n"
        "• Không lưu trữ tin nhắn\n"
        "• Không hiển thị thông tin cá nhân\n"
        "• Có thể block/report người dùng xấu\n"
        "• Dừng chat bất cứ lúc nào\n\n"
        "💬 **TRẢI NGHIỆM CHAT:**\n"
        "• Hỗ trợ text, ảnh, voice, sticker\n"
        "• Kết nối tức thì khi tìm thấy\n"
        "• Thông báo khi đối phương rời chat\n\n"
        "🌈 **ĐA DẠNG & TOÀN DIỆN:**\n"
        "• Nam tìm Nữ / Nữ tìm Nam\n"
        "• Nam tìm Nam / Nữ tìm Nữ\n" 
        "• Tìm bất kỳ giới tính nào\n"
        "• Thay đổi sở thích bất cứ lúc nào\n\n"
        "🎮 **DỄ SỬ DỤNG:**\n"
        "• Giao diện đơn giản, trực quan\n"
        "• Menu tương tác với nút bấm\n"
        "• Hướng dẫn chi tiết từng bước"
    )
    
    await callback_query.message.edit_text(
        features_text,
        reply_markup=get_features_keyboard(),
        parse_mode='Markdown'
    )

@dp.callback_query(lambda c: c.data == 'privacy_policy')
async def privacy_policy(callback_query: CallbackQuery):
    """Hiển thị chính sách bảo mật"""
    privacy_text = (
        "🔒 **CHÍNH SÁCH BẢO MẬT**\n\n"
        "✅ **CAM KẾT CỦA CHÚNG TÔI:**\n"
        "• **KHÔNG** thu thập thông tin cá nhân\n"
        "• **KHÔNG** lưu trữ tin nhắn chat\n"
        "• **KHÔNG** chia sẻ dữ liệu với bên thứ 3\n"
        "• **KHÔNG** tracking hay theo dõi\n\n"
        "📊 **THÔNG TIN LƯU TRỮ:**\n"
        "• Chỉ lưu: Giới tính & sở thích (tạm thời)\n"
        "• Mục đích: Ghép đôi phù hợp\n"
        "• Thời gian: Chỉ trong phiên sử dụng\n"
        "• Xóa tự động khi thoát bot\n\n"
        "🛡️ **QUYỀN CỦA BẠN:**\n"
        "• Thay đổi thông tin bất cứ lúc nào\n"
        "• Dừng chat mà không cần lý do\n"
        "• Thoát bot hoàn toàn\n"
        "• Báo cáo người dùng vi phạm\n\n"
        "⚠️ **LƯU Ý AN TOÀN:**\n"
        "• Không chia sẻ thông tin cá nhân\n"
        "• Không gửi ảnh nhạy cảm\n"
        "• Báo cáo hành vi không phù hợp\n"
        "• Sử dụng có trách nhiệm"
    )
    
    await callback_query.message.edit_text(
        privacy_text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🚀 Tôi hiểu, bắt đầu ngay!", callback_data="start_register")],
            [InlineKeyboardButton(text="🔙 Quay lại", callback_data="back_to_intro")]
        ]),
        parse_mode='Markdown'
    )

@dp.callback_query(lambda c: c.data == 'back_to_intro')
async def back_to_intro(callback_query: CallbackQuery):
    """Quay lại màn hình giới thiệu"""
    welcome_text = (
        "🎭 **CHÀO MỪNG ĐẾN VỚI SOULMATCH!**\n\n"
        "✨ **Trò chuyện ẩn danh - Kết nối tâm hồn**\n\n"
        "🔥 **Tính năng nổi bật:**\n"
        "• 🎯 **Smart Matching** - Tìm người phù hợp theo sở thích\n"
        "• 🔐 **100% Ẩn danh** - Không lưu thông tin cá nhân\n"
        "• 💬 **Chat tức thì** - Kết nối ngay lập tức\n"
        "• 🌈 **Đa dạng** - Hỗ trợ mọi giới tính & sở thích\n"
        "• 🚫 **An toàn** - Có thể dừng chat bất cứ lúc nào\n\n"
        "🎲 **Cách hoạt động:**\n"
        "1️⃣ Chọn giới tính của bạn\n"
        "2️⃣ Chọn đối tượng muốn trò chuyện\n" 
        "3️⃣ Hệ thống tự động ghép đôi\n"
        "4️⃣ Bắt đầu trò chuyện ẩn danh!\n\n"
        "🔒 **Cam kết:** Hoàn toàn miễn phí và bảo mật!"
    )
    
    await callback_query.message.edit_text(
        welcome_text,
        reply_markup=get_intro_keyboard(),
        parse_mode='Markdown'
    )

@dp.callback_query(lambda c: c.data.startswith('gender_'))
async def process_gender(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    # Kiểm tra user tồn tại, tạo mới nếu cần
    if user_id not in users:
        users[user_id] = User(user_id)
        # Redirect về /start nếu user không tồn tại
        await callback_query.message.edit_text(
            "❌ **Phiên làm việc đã hết hạn**\n\n"
            "Vui lòng bắt đầu lại từ đầu:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Bắt đầu lại", callback_data="restart_bot")]
            ])
        )
        return
    
    user = users[user_id]
    
    gender_map = {
        'gender_male': '👨 Nam',
        'gender_female': '👩 Nữ',
        'gender_other': '🤷 Khác'
    }
    
    user.gender = gender_map[callback_query.data]
    
    await callback_query.message.edit_text(
        f"✅ **Đã chọn giới tính:** {user.gender}\n\n"
        "🎯 **Bước tiếp theo:** Chọn đối tượng bạn muốn trò chuyện\n\n"
        "💡 *Tip: Chọn 'Bất kỳ' để có nhiều cơ hội kết nối hơn!*",
        reply_markup=get_seeking_keyboard(),
        parse_mode='Markdown'
    )

@dp.callback_query(lambda c: c.data.startswith('seek_'))
async def process_seeking(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    
    # Kiểm tra user tồn tại
    if user_id not in users:
        users[user_id] = User(user_id)
        await callback_query.message.edit_text(
            "❌ **Phiên làm việc đã hết hạn**\n\n"
            "Vui lòng bắt đầu lại:",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="🔄 Bắt đầu lại", callback_data="restart_bot")]
            ])
        )
        return
    
    user = users[user_id]
    
    seeking_map = {
        'seek_male': '👨 Nam',
        'seek_female': '👩 Nữ',
        'seek_any': '🌈 Bất kỳ'
    }
    
    user.seeking = seeking_map[callback_query.data]
    user.is_registered = True
    
    # Auto-accept disclaimer cho user đăng ký thông thường (không qua flow legal)
    if not hasattr(user, 'disclaimer_accepted'):
        user.disclaimer_accepted = True
    
    # Thông báo hoàn tất với hướng dẫn sử dụng
    completion_text = (
        f"🎉 **ĐĂNG KÝ HOÀN TẤT!**\n\n"
        f"📋 **Hồ sơ của bạn:**\n"
        f"• Giới tính: {user.gender}\n"
        f"• Tìm kiếm: {user.seeking}\n\n"
        f"🚀 **Sẵn sàng bắt đầu!**\n\n"
        f"🎯 **Hướng dẫn nhanh:**\n"
        f"• Nhấn '🔍 Tìm người trò chuyện' để bắt đầu\n"
        f"• Hệ thống sẽ tự động ghép đôi\n"
        f"• Chat thoải mái khi được kết nối\n"
        f"• Dùng '❌ Kết thúc chat' khi muốn dừng\n\n"
        f"💡 **Lời khuyên:** Hãy lịch sự và tôn trọng người khác nhé!"
    )
    
    await callback_query.message.edit_text(
        completion_text,
        reply_markup=get_main_menu_keyboard(),
        parse_mode='Markdown'
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Hiển thị hướng dẫn sử dụng"""
    help_text = (
        "📚 **HƯỚNG DẪN SỬ DỤNG SOULMATCH**\n\n"
        "🎯 **CÁC LỆNH CƠ BẢN:**\n"
        "• `/start` - Bắt đầu hoặc xem menu chính\n"
        "• `/find` - Tìm người trò chuyện\n"
        "• `/stop` - Kết thúc cuộc trò chuyện\n"
        "• `/help` - Xem hướng dẫn này\n\n"
        "🔄 **QUY TRÌNH SỬ DỤNG:**\n"
        "1️⃣ Đăng ký hồ sơ (giới tính + sở thích)\n"
        "2️⃣ Nhấn 'Tìm người trò chuyện'\n"
        "3️⃣ Chờ hệ thống ghép đôi\n"
        "4️⃣ Chat khi được kết nối\n"
        "5️⃣ Kết thúc khi muốn dừng\n\n"
        "⚙️ **TÍNH NĂNG NÂNG CAO:**\n"
        "• Thay đổi giới tính/sở thích trong Cài đặt\n"
        "• Gửi ảnh, voice, sticker trong chat\n"
        "• Smart matching theo compatibility\n\n"
        "🛡️ **AN TOÀN & BẢO MẬT:**\n"
        "• Hoàn toàn ẩn danh\n"
        "• Không lưu tin nhắn\n"
        "• Có thể dừng chat bất cứ lúc nào\n\n"
        "❓ **CẦN HỖ TRỢ?**\n"
        "Gõ `/start` để về menu chính hoặc `/help` để xem lại hướng dẫn"
    )
    
    await message.answer(
        help_text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🏠 Về menu chính", callback_data="back_menu")],
            [InlineKeyboardButton(text="🔍 Tìm ngay", callback_data="find_chat")]
        ])
    )

@dp.callback_query(lambda c: c.data == 'find_chat')
async def find_chat(callback_query: CallbackQuery):
    await process_find(callback_query.message)

@dp.message(Command("find"))
async def cmd_find(message: types.Message):
    await process_find(message)

async def process_find(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users or not users[user_id].is_registered:
        await message.answer(
            "❌ Bạn cần đăng ký trước!\nGõ /start để bắt đầu."
        )
        return
    
    user = users[user_id]
    
    # Kiểm tra age verification
    if not user.age_verified:
        await message.answer(
            "❌ Bạn cần xác nhận tuổi trước khi sử dụng dịch vụ.",
            reply_markup=get_age_verification_keyboard()
        )
        return
    
    # Kiểm tra disclaimer acceptance - Auto-accept cho user đăng ký thông thường
    if not hasattr(user, 'disclaimer_accepted'):
        user.disclaimer_accepted = True
    
    if not user.disclaimer_accepted:
        await message.answer(
            "❌ Bạn cần đồng ý với tuyên bố miễn trừ trách nhiệm trước khi sử dụng dịch vụ.\n"
            "Gõ /start để hoàn tất các bước xác thực."
        )
        return
    
    if user.partner_id:
        await message.answer("❌ Bạn đang trong cuộc trò chuyện!")
        return
    
    # Xác định queue phù hợp
    queue_key = get_queue_key(user.gender, user.seeking)
    
    # Tìm partner phù hợp
    partner_id = find_compatible_partner(user)
    
    if partner_id:
        # Kết nối
        user.partner_id = partner_id
        users[partner_id].partner_id = user_id
        connections[user_id] = partner_id
        connections[partner_id] = user_id
        
        # Thông báo kết nối thành công
        await message.answer("✅ Đã tìm thấy người trò chuyện! Hãy bắt đầu chat nhé! 💬")
        await bot.send_message(
            partner_id, 
            "✅ Đã tìm thấy người trò chuyện! Hãy bắt đầu chat nhé! 💬"
        )
    else:
        # Thêm vào hàng chờ
        waiting_users[queue_key].append(user_id)
        await message.answer(
            f"⏳ Đang tìm kiếm {user.seeking.lower()}...\n"
            f"Bạn sẽ được thông báo khi tìm thấy!"
        )

def get_queue_key(gender, seeking):
    """Tạo key cho queue dựa trên giới tính và sở thích"""
    gender_key = 'male' if '👨' in gender else 'female' if '👩' in gender else 'any'
    seeking_key = 'male' if '👨' in seeking else 'female' if '👩' in seeking else 'any'
    return f"{gender_key}_seeking_{seeking_key}"

def find_compatible_partner(user):
    """Tìm partner phù hợp"""
    user_gender = user.gender
    user_seeking = user.seeking
    
    # Duyệt qua tất cả các queue để tìm match
    for queue_key, waiting_list in waiting_users.items():
        if not waiting_list:
            continue
            
        for waiting_user_id in waiting_list[:]:
            waiting_user = users[waiting_user_id]
            
            # Kiểm tra compatibility
            if is_compatible(user, waiting_user):
                waiting_list.remove(waiting_user_id)
                return waiting_user_id
    
    return None

def is_compatible(user1, user2):
    """Kiểm tra 2 user có compatible không"""
    # User1 seeking User2's gender (hoặc any)
    user1_match = ('🌈' in user1.seeking or 
                   ('👨' in user1.seeking and '👨' in user2.gender) or 
                   ('👩' in user1.seeking and '👩' in user2.gender))
    
    # User2 seeking User1's gender (hoặc any)
    user2_match = ('🌈' in user2.seeking or 
                   ('👨' in user2.seeking and '👨' in user1.gender) or 
                   ('👩' in user2.seeking and '👩' in user1.gender))
    
    return user1_match and user2_match

@dp.callback_query(lambda c: c.data == 'stop_chat')
async def stop_chat_callback(callback_query: CallbackQuery):
    await process_stop(callback_query.message)

@dp.message(Command("stop"))
async def cmd_stop(message: types.Message):
    await process_stop(message)

async def process_stop(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        return
    
    user = users[user_id]
    
    # Xóa khỏi hàng chờ
    for queue in waiting_users.values():
        if user_id in queue:
            queue.remove(user_id)
    
    # Ngắt kết nối
    if user.partner_id:
        partner_id = user.partner_id
        await bot.send_message(partner_id, "💔 Người kia đã kết thúc cuộc trò chuyện.")
        
        # Reset partner
        users[partner_id].partner_id = None
        user.partner_id = None
        
        # Xóa connection
        if user_id in connections:
            del connections[user_id]
        if partner_id in connections:
            del connections[partner_id]
        
        await message.answer("✅ Đã kết thúc cuộc trò chuyện.", reply_markup=get_main_menu_keyboard())
    else:
        await message.answer("❌ Bạn không đang trong cuộc trò chuyện nào.")

@dp.callback_query(lambda c: c.data == 'settings')
async def settings_callback(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user = users[user_id]
    
    await callback_query.message.edit_text(
        f"⚙️ Cài đặt hồ sơ\n\n"
        f"📋 Thông tin hiện tại:\n"
        f"• Giới tính: {user.gender}\n"
        f"• Tìm kiếm: {user.seeking}\n\n"
        f"Chọn thông tin muốn thay đổi:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👤 Đổi giới tính", callback_data="change_gender")],
            [InlineKeyboardButton(text="🔍 Đổi sở thích", callback_data="change_seeking")],
            [InlineKeyboardButton(text="🔙 Quay lại", callback_data="back_menu")]
        ])
    )

@dp.callback_query(lambda c: c.data == 'change_gender')
async def change_gender(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "👤 Chọn giới tính mới:",
        reply_markup=get_gender_keyboard()
    )

@dp.callback_query(lambda c: c.data == 'change_seeking')
async def change_seeking(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        "🔍 Bạn muốn trò chuyện với:",
        reply_markup=get_seeking_keyboard()
    )

@dp.callback_query(lambda c: c.data == 'restart_bot')
async def restart_bot(callback_query: CallbackQuery):
    """Restart bot khi có lỗi session"""
    await callback_query.message.edit_text(
        "🔄 **Đang khởi động lại...**\n\n"
        "Vui lòng chờ trong giây lát..."
    )
    # Gọi lại cmd_start
    await cmd_start(callback_query.message)

@dp.callback_query(lambda c: c.data == 'back_menu')
async def back_menu(callback_query: CallbackQuery):
    user_id = callback_query.from_user.id
    user = users[user_id]
    
    await callback_query.message.edit_text(
        f"🏠 Menu chính\n\n"
        f"📋 Hồ sơ của bạn:\n"
        f"• Giới tính: {user.gender}\n"
        f"• Tìm kiếm: {user.seeking}",
        reply_markup=get_main_menu_keyboard()
    )

@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    
    if user_id not in users:
        await message.answer("❌ Gõ /start để bắt đầu!")
        return
    
    user = users[user_id]
    
    # Kiểm tra age verification
    if not user.age_verified:
        await message.answer("❌ Bạn cần xác nhận tuổi trước khi sử dụng dịch vụ.")
        return
    
    # Kiểm tra disclaimer acceptance - Auto-accept cho user đăng ký thông thường
    if not hasattr(user, 'disclaimer_accepted'):
        user.disclaimer_accepted = True
    
    if not user.disclaimer_accepted:
        await message.answer("❌ Bạn cần đồng ý với tuyên bố miễn trừ trách nhiệm trước khi sử dụng dịch vụ.")
        return
    
    # Kiểm tra content filtering cho trẻ em
    if message.text and await check_minor_behavior(message.text, user_id):
        return  # Đã bị chặn, không xử lý tiếp
    
    if not user.partner_id:
        await message.answer("❌ Bạn chưa được kết nối với ai. Gõ /find để tìm kiếm!")
        return
    
    # Chuyển tiếp tin nhắn
    try:
        if message.text:
            await bot.send_message(user.partner_id, message.text)
        elif message.photo:
            await bot.send_photo(user.partner_id, message.photo[-1].file_id, caption=message.caption)
        elif message.voice:
            await bot.send_voice(user.partner_id, message.voice.file_id)
        elif message.sticker:
            await bot.send_sticker(user.partner_id, message.sticker.file_id)
        # Thêm các loại tin nhắn khác nếu cần
    except Exception as e:
        await message.answer("❌ Không thể gửi tin nhắn!")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
