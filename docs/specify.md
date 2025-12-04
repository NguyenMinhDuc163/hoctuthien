# 📄 TÀI LIỆU ĐẶC TẢ DỰ ÁN: HỆ THỐNG "HỌC TỪ THIỆN"
> **Slogan:** *Trao tri thức - Gửi yêu thương*

## 1. TỔNG QUAN DỰ ÁN (EXECUTIVE SUMMARY)
**Học Từ Thiện** là nền tảng kết nối giáo dục trực tuyến, nơi các chuyên gia (Mentor) chia sẻ kiến thức và người học (Mentee) tiếp nhận giá trị. Điểm khác biệt cốt lõi là **100% chi phí học tập** sẽ được chuyển trực tiếp vào các tài khoản của **Thiện Nguyện App (MBBank)**.

Hệ thống hoạt động dựa trên sự minh bạch, sử dụng công nghệ để tự động hóa quy trình xác thực chuyển khoản, biến mỗi giờ học trở thành một hành động đóng góp thực tế cho xã hội.

---

## 2. PHÂN HỆ NGƯỜI DÙNG & CHỨC NĂNG

### 🎓 Mentee (Người học)
*   **Đăng ký & Kích hoạt:**
    *   Tạo tài khoản mới trên hệ thống.
    *   **Cơ chế chống Spam:** Để kích hoạt tài khoản, Mentee cần chuyển khoản xác thực **10.000 VNĐ** vào tài khoản Thiện Nguyện. Đây là bước "KYC xã hội" nhằm loại bỏ tài khoản ảo.
*   **Đặt lịch (Booking):** Tìm kiếm Mentor, xem lịch trống và đặt buổi học.
*   **Thanh toán học phí:** Sau buổi học, Mentee chuyển khoản số tiền (do Mentor quy định) trực tiếp tới tài khoản Thiện Nguyện.
    *   *Ràng buộc:* Phải hoàn tất thanh toán buổi học trước mới được quyền đặt lịch buổi tiếp theo.
*   **Theo dõi:** Xem lịch sử học tập cá nhân, lịch sử đóng góp thiện nguyện.
*   **Bảng xếp hạng:** Xem danh sách Top Mentor/Mentee đóng góp nhiều nhất trong tháng.

### 🧑‍🏫 Mentor (Người hướng dẫn)
*   **Vai trò kép:** Mentor cũng là một Mentee, có đầy đủ quyền lợi của Mentee.
*   **Profile chuyên gia:** Cập nhật thông tin cá nhân, lĩnh vực giảng dạy, kinh nghiệm.
*   **Quản lý lớp học:**
    *   Thiết lập lịch rảnh (Slots).
    *   Quy định mức "học phí" (số tiền quyên góp) cho buổi học.
    *   **Tùy chọn quỹ nhận tiền:** Mentor có quyền **chọn Tài khoản Thiện Nguyện (4 số)** cụ thể mà mình muốn ủng hộ để hiển thị cho Mentee khi thanh toán (Ví dụ: Chọn tài khoản `2000` cho quỹ Trò nghèo vùng cao, hoặc `1111` cho quỹ khác).

---

## 3. LUỒNG NGHIỆP VỤ & TÍCH HỢP THANH TOÁN (CORE WORKFLOW)

Hệ thống giải quyết bài toán tích hợp với Thiện Nguyện App (không có Webhook, bảo mật che số) bằng quy trình thông minh sau:

### 3.1. Cơ chế sinh mã giao dịch (Transaction Syntax)
Do hệ thống ngân hàng tự động mã hóa (ẩn) các dãy số liên tiếp >3 ký tự ở cuối nội dung giao dịch (VD: `123456` -> `123xxx`), hệ thống HocTuThien sử dụng thuật toán sinh mã **HOÀN TOÀN BẰNG CHỮ CÁI (ALPHABET)**.

*   **Cú pháp kích hoạt tài khoản:**
    > `HOCTUTHIEN KICHHOAT [MA_USER_CHU]`
    > *(Ví dụ: HOCTUTHIEN KICHHOAT NGUYENVANA)*

*   **Cú pháp thanh toán buổi học:**
    > `HOCTUTHIEN UNGHO [MA_BOOKING_CHU]`
    > *(Ví dụ: HOCTUTHIEN UNGHO ABCXYZ)*

### 3.2. Quy trình thanh toán & Đối soát (Payment & Reconciliation)

1.  **Tạo mã VietQR Động:**
    *   Khi Mentee cần thanh toán (kích hoạt hoặc trả phí), hệ thống hiển thị mã QR.
    *   QR này chứa sẵn: **Số tài khoản Thiện Nguyện** (do Mentor chọn), **Số tiền**, và **Nội dung cú pháp** chuẩn xác.
    *   *Lợi ích:* Ngăn chặn người dùng nhập sai nội dung hoặc số tiền, đảm bảo tỷ lệ đối soát thành công 100%.

2.  **Cơ chế Polling (Kiểm tra giao dịch):**
    *   Vì không có Webhook, Server HocTuThien sẽ định kỳ gọi API lịch sử giao dịch của các tài khoản Thiện Nguyện (2000, 1111...).
    *   Hệ thống quét nội dung giao dịch, tìm kiếm các từ khóa `KICHHOAT [MA_USER]` hoặc `UNGHO [MA_BOOKING]`.

3.  **Xử lý Logic:**
    *   Nếu khớp mã: Hệ thống tự động Kích hoạt tài khoản hoặc Xác nhận hoàn thành buổi học.
    *   Nếu nội dung không khớp chiến dịch cụ thể trên App Thiện Nguyện: Dòng tiền vẫn đi vào chiến dịch mới nhất của quỹ, đảm bảo tiền luôn đến được nơi cần đến.

---

## 4. ĐIỂM NHẤN CÔNG NGHỆ & UX (HIGHLIGHTS)

### 🛡️ Bảo mật & Chống gian lận
*   **Anti-Spam User:** Phí kích hoạt 10k giúp lọc bỏ người dùng ảo, đảm bảo cộng đồng chất lượng.
*   **Secure Syntax:** Giải quyết triệt để vấn đề "che số" của ngân hàng bằng mã định danh chữ cái.

### 📲 Trải nghiệm người dùng (User Experience)
*   **Automation:** Người dùng không cần chụp ảnh màn hình hay gửi bằng chứng chuyển khoản thủ công. Mọi thứ được xác thực tự động.
*   **QR Code thông minh:** Giảm thiểu thao tác nhập liệu, chỉ cần Quét và Xác nhận (Scan & Pay).
*   **Gamification (Game hóa):** Bảng xếp hạng thành tích tạo động lực thi đua làm việc thiện thông qua việc học và dạy.

### 🤝 Tính linh hoạt cho Mentor
*   Mentor được trao quyền quyết định dòng tiền từ công sức giảng dạy của mình sẽ chảy về quỹ nào, tạo động lực cá nhân hóa cao cho người dạy.

---

**Tóm lại:**
Dự án **Học Từ Thiện** là một hệ sinh thái khép kín: **Mentee học tập - Mentor chia sẻ - Cộng đồng hưởng lợi**. Hệ thống kỹ thuật đóng vai trò là "cầu nối tin cậy", xử lý phức tạp ở hậu trường để mang lại trải nghiệm đơn giản, minh bạch nhất cho người dùng.
