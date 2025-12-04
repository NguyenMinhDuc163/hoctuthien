from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import random
import string

# --- HÀM BỔ TRỢ ---
def generate_code():
    """Tạo mã giao dịch chỉ gồm chữ cái in hoa (A-Z) để tránh bị App Thiện Nguyện ẩn số"""
    return ''.join(random.choices(string.ascii_uppercase, k=6))

# --- MODEL DỮ LIỆU ---

class CharityAccount(models.Model):
    """Lưu tài khoản thiện nguyện (VD: 2000)"""
    account_number = models.CharField(max_length=20, unique=True)
    account_name = models.CharField(max_length=255)
    bank_id = models.CharField(max_length=50, default="MB") # Bin code MBBank
    
    def __str__(self):
        return f"{self.account_number} - {self.account_name}"

class Subject(models.Model):
    """Lĩnh vực giảng dạy"""
    name = models.CharField(max_length=100)
    def __str__(self): return self.name

class User(AbstractUser):
    """User mở rộng"""
    is_activated = models.BooleanField(default=False, help_text="Đã đóng 10k kích hoạt chưa")
    phone = models.CharField(max_length=15, blank=True)
    
    # Kiểm tra nhanh xem user có phải mentor không
    @property
    def is_mentor(self):
        return hasattr(self, 'mentor_profile')

class MentorProfile(models.Model):
    """Thông tin Mentor"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField()
    subjects = models.ManyToManyField(Subject)
    default_price = models.DecimalField(max_digits=10, decimal_places=0, default=50000)
    
    def __str__(self): return f"Mentor {self.user.username}"

class MentorSchedule(models.Model):
    """Lịch rảnh của Mentor"""
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='schedules')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.mentor.user.username} | {self.start_time.strftime('%H:%M %d/%m')}"

class Transaction(models.Model):
    """Lưu giao dịch chờ đối soát"""
    TYPE_CHOICES = (('ACTIVATION', 'Kích hoạt'), ('SESSION_FEE', 'Học phí'))
    STATUS_CHOICES = (('PENDING', 'Chờ xử lý'), ('VERIFIED', 'Thành công'), ('FAILED', 'Thất bại'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=0)
    code = models.CharField(max_length=10, default=generate_code, unique=True) # Mã ABCXYZ
    transaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    target_account = models.ForeignKey(CharityAccount, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_syntax(self):
        """Tạo cú pháp: HOCTUTHIEN KICHHOAT ABCXYZ"""
        prefix = "KICHHOAT" if self.transaction_type == 'ACTIVATION' else "HOCPHI"
        return f"HOCTUTHIEN {prefix} {self.code}"

class Booking(models.Model):
    """Lịch đặt học"""
    STATUS_CHOICES = (
        ('PENDING', 'Chờ thanh toán'),
        ('CONFIRMED', 'Đã xác nhận'),
    )
    mentee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_learnings')
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE, related_name='my_teachings')
    schedule = models.OneToOneField(MentorSchedule, on_delete=models.PROTECT)

    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    
    meet_link = models.URLField(blank=True, null=True) # Link Google Meet
    transaction = models.OneToOneField(Transaction, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')