import requests
import datetime
from django.utils import timezone
from .models import Transaction, Booking

# --- LOGIC GOOGLE MEET (MOCK) ---
def create_google_meet_link(booking):
    """
    Hàm tạo link Google Meet.
    LƯU Ý: Để chạy thật cần Credential từ Google Cloud Console.
    Ở đây mình giả lập trả về link mẫu để bạn test luồng trước.
    """
    # TODO: Tích hợp Google Calendar API thật ở đây
    return f"https://meet.google.com/test-meet-{booking.id}"

# --- LOGIC CHECK GIAO DỊCH ---
def verify_transaction_service(transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        if transaction.status == 'VERIFIED':
            return True, "Đã xác thực trước đó."

        # Cấu hình API
        acc_no = transaction.target_account.account_number
        # Lấy sao kê từ ngày tạo lệnh
        from_date = transaction.created_at.strftime('%Y-%m-%d')
        to_date = datetime.datetime.now().strftime('%Y-%m-%d')
        
        url = f"https://apiv2.thiennguyen.app/api/v2/bank-account-transaction/{acc_no}/transactionsV2"
        params = {
            'fromDate': from_date,
            'toDate': to_date,
            'pageNumber': 1,
            'pageSize': 50
        }
        
        # Gọi API
        resp = requests.get(url, params=params, headers={'Content-Type': 'application/json'})
        if resp.status_code != 200:
            return False, "Lỗi kết nối App Thiện Nguyện"

        data = resp.json()
        transactions = data.get('data', {}).get('transactions', [])

        # Duyệt danh sách giao dịch để tìm khớp lệnh
        # Logic: Nội dung chứa CODE (VD: ABCXYZ) và Tiền >= Tiền lệnh
        found = False
        for item in transactions:
            narrative = item.get('narrative', '')
            amount = item.get('transactionAmount', 0)
            
            if transaction.code in narrative and amount >= transaction.amount:
                found = True
                break
        
        if found:
            # 1. Cập nhật Transaction
            transaction.status = 'VERIFIED'
            transaction.save()
            
            # 2. Xử lý nghiệp vụ
            if transaction.transaction_type == 'ACTIVATION':
                transaction.user.is_activated = True
                transaction.user.save()
            
            elif transaction.transaction_type == 'SESSION_FEE':
                # Tìm booking và update
                try:
                    booking = Booking.objects.get(transaction=transaction)
                    booking.status = 'CONFIRMED'
                    booking.meet_link = create_google_meet_link(booking)
                    booking.save()
                    
                    # Khóa lịch mentor
                    booking.schedule.is_booked = True
                    booking.schedule.save()
                except Booking.DoesNotExist:
                    pass

            return True, "Xác thực thành công!"
        
        return False, "Chưa tìm thấy khoản tiền khớp lệnh."

    except Exception as e:
        return False, str(e)