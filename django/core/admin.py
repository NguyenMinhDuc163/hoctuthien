from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CharityAccount, Subject, MentorProfile, MentorSchedule, Transaction, Booking

# 1. Cấu hình User Admin
# Vì chúng ta dùng Custom User, cần khai báo lại Admin để hiển thị các trường mới
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_activated', 'is_staff')
    list_filter = ('is_activated', 'is_staff', 'is_superuser', 'groups')
    
    # Thêm phần hiển thị 'Thông tin dự án' vào trang chi tiết User
    fieldsets = UserAdmin.fieldsets + (
        ('Thông tin dự án', {'fields': ('is_activated', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)

# 2. Cấu hình Tài khoản Thiện Nguyện
@admin.register(CharityAccount)
class CharityAccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'account_name', 'bank_id')

# 3. Cấu hình Lĩnh vực (Subject)
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

# 4. Cấu hình Mentor Profile (Đã sửa lỗi)
@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'default_price', 'get_subjects')
    search_fields = ('user__username', 'user__email')
    list_filter = ('subjects',)

    def get_subjects(self, obj):
        # Sửa lỗi cũ: thêm vòng lặp chuẩn xác
        return ", ".join([s.name for s in obj.subjects.all()])
    get_subjects.short_description = 'Lĩnh vực chuyên môn'

# 5. Cấu hình Lịch rảnh (Schedule)
@admin.register(MentorSchedule)
class MentorScheduleAdmin(admin.ModelAdmin):
    list_display = ('mentor', 'start_time', 'end_time', 'is_booked')
    list_filter = ('is_booked', 'start_time')
    ordering = ('start_time',)

# 6. Cấu hình Giao dịch (Transaction)
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'amount', 'transaction_type', 'status', 'created_at')
    list_filter = ('status', 'transaction_type', 'created_at')
    search_fields = ('code', 'user__username', 'user__email')
    readonly_fields = ('code', 'created_at') # Mã code và ngày tạo chỉ xem, không sửa

# 7. Cấu hình Booking (Lịch đặt)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'mentee', 'mentor', 'subject', 'status', 'payment_status_display', 'meet_link')
    list_filter = ('status',)
    search_fields = ('mentee__username', 'mentor__user__username')
    
    def payment_status_display(self, obj):
        if obj.transaction:
            return obj.transaction.get_status_display()
        return "Chưa tạo GD"
    payment_status_display.short_description = 'Trạng thái thanh toán'