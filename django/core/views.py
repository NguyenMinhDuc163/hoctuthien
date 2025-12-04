from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Transaction, CharityAccount, MentorSchedule, Booking, MentorProfile
from .services import verify_transaction_service

# --- 1. KÍCH HOẠT TÀI KHOẢN ---
@login_required
def activation_view(request):
    if request.user.is_activated:
        return render(request, 'core/success.html', {'msg': 'Tài khoản đã kích hoạt!'})

    target_acc = CharityAccount.objects.first() # Lấy TK thiện nguyện đầu tiên trong DB
    if not target_acc:
        return render(request, 'core/error.html', {'msg': 'Hệ thống chưa cấu hình TK nhận tiền'})

    # Tạo hoặc lấy giao dịch cũ chưa thanh toán
    trans, _ = Transaction.objects.get_or_create(
        user=request.user,
        transaction_type='ACTIVATION',
        status='PENDING',
        defaults={'amount': 10000, 'target_account': target_acc}
    )
    
    # Link VietQR
    qr_link = f"https://img.vietqr.io/image/{target_acc.bank_id}-{target_acc.account_number}-compact.png?amount={int(trans.amount)}&addInfo={trans.get_syntax()}"

    return render(request, 'core/payment.html', {
        'transaction': trans,
        'qr_link': qr_link,
        'syntax': trans.get_syntax()
    })

# --- 2. ĐẶT LỊCH HỌC ---
@login_required
def book_mentor_view(request, schedule_id):
    if not request.user.is_activated:
        return redirect('activation')
        
    schedule = get_object_or_404(MentorSchedule, id=schedule_id, is_booked=False)
    mentor_profile = schedule.mentor
    
    # Tạo Booking và Transaction
    target_acc = CharityAccount.objects.first()
    
    # Logic: Nếu user chưa có booking cho slot này thì tạo mới
    booking, created = Booking.objects.get_or_create(
        mentee=request.user,
        schedule=schedule,
        defaults={
            'mentor': mentor_profile,
            'status': 'PENDING'
        }
    )
    
    if created or not booking.transaction:
        trans = Transaction.objects.create(
            user=request.user,
            amount=mentor_profile.default_price,
            transaction_type='SESSION_FEE',
            target_account=target_acc
        )
        booking.transaction = trans
        booking.save()
    
    trans = booking.transaction
    
    # Link VietQR
    qr_link = f"https://img.vietqr.io/image/{target_acc.bank_id}-{target_acc.account_number}-compact.png?amount={int(trans.amount)}&addInfo={trans.get_syntax()}"

    return render(request, 'core/payment.html', {
        'transaction': trans,
        'qr_link': qr_link,
        'syntax': trans.get_syntax(),
        'is_booking': True
    })

# --- 3. API KIỂM TRA GIAO DỊCH (AJAX) ---
@login_required
def check_transaction_api(request, transaction_id):
    success, msg = verify_transaction_service(transaction_id)
    return JsonResponse({'success': success, 'message': msg})