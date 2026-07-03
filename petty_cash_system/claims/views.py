from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Claim, ApprovalHistory, User


@login_required
def dashboard_redirect(request):
    # യൂസറുടെ റോൾ അനുസരിച്ച് ഡാഷ്‌ബോർഡിലേക്ക് തിരിച്ചുവിടുന്നു
    if request.user.role == 'EMPLOYEE':
        return redirect('employee_dashboard')
    elif request.user.role == 'MANAGER':
        return redirect('manager_dashboard')
    elif request.user.role == 'FINANCE':
        return redirect('finance_dashboard')
    elif request.user.role == 'ADMIN':
        return redirect('admin_dashboard')
    return redirect('login')


# --- EMPLOYEE DASHBOARD ---
@login_required
def employee_dashboard(request):
    if request.user.role != 'EMPLOYEE': return redirect('dashboard')
    claims = Claim.objects.filter(employee=request.user).order_by('-submitted_date')

    context = {
        'claims': claims,
        'total': claims.count(),
        'pending': claims.filter(status__icontains='Pending').count(),
        'approved': claims.filter(status='Manager Approved').count(),
        'rejected': claims.filter(status__icontains='Rejected').count(),
        'paid': claims.filter(status='Paid').count(),
    }
    return render(request, 'claims/employee_dashboard.html', context)


@login_required
def submit_claim(request):
    if request.user.role != 'EMPLOYEE': return redirect('dashboard')
    if request.method == 'POST':
        title = request.POST['title']
        category = request.POST['category']
        amount = request.POST['amount']
        description = request.POST['description']
        receipt = request.FILES.get('receipt')

        Claim.objects.create(
            employee=request.user, title=title, category=category,
            amount=amount, description=description, receipt=receipt
        )
        messages.success(request, "Claim submitted successfully!")
        return redirect('employee_dashboard')
    return render(request, 'claims/submit_claim.html')


# --- MANAGER DASHBOARD ---
@login_required
def manager_dashboard(request):
    if request.user.role != 'MANAGER': return redirect('dashboard')
    pending_claims = Claim.objects.filter(status='Pending Manager Approval')
    all_claims = Claim.objects.exclude(status='Pending Manager Approval')
    return render(request, 'claims/manager_dashboard.html',
                  {'pending_claims': pending_claims, 'all_claims': all_claims})


@login_required
def manager_action(request, claim_id, action):
    if request.user.role != 'MANAGER': return redirect('dashboard')
    claim = get_object_or_404(Claim, id=claim_id)
    remarks = request.POST.get('remarks', '')

    if action == 'approve':
        claim.status = 'Pending Finance Approval'
        action_text = 'Approved'
    else:
        claim.status = 'Manager Rejected'
        action_text = 'Rejected'

    claim.save()
    ApprovalHistory.objects.create(claim=claim, approver=request.user, role='Manager', action=action_text,
                                   remarks=remarks)
    return redirect('manager_dashboard')


# --- FINANCE DASHBOARD ---
@login_required
def finance_dashboard(request):
    if request.user.role != 'FINANCE': return redirect('dashboard')
    pending_finance = Claim.objects.filter(status='Pending Finance Approval')
    waiting_payment = Claim.objects.filter(status='Finance Approved')
    paid_claims = Claim.objects.filter(status='Paid')

    return render(request, 'claims/finance_dashboard.html', {
        'pending_finance': pending_finance,
        'waiting_payment': waiting_payment,
        'paid_claims': paid_claims
    })


@login_required
def finance_action(request, claim_id, action):
    if request.user.role != 'FINANCE': return redirect('dashboard')
    claim = get_object_or_404(Claim, id=claim_id)
    remarks = request.POST.get('remarks', '')

    if action == 'approve':
        claim.status = 'Finance Approved'
        action_text = 'Approved'
    elif action == 'reject':
        claim.status = 'Finance Rejected'
        action_text = 'Rejected'
    elif action == 'pay':
        claim.status = 'Paid'
        action_text = 'Paid'

    claim.save()
    ApprovalHistory.objects.create(claim=claim, approver=request.user, role='Finance', action=action_text,
                                   remarks=remarks)
    return redirect('finance_dashboard')


# --- ADMIN DASHBOARD ---
@login_required
def admin_dashboard(request):
    if request.user.role != 'ADMIN': return redirect('dashboard')
    claims = Claim.objects.all()

    context = {
        'total_users': User.objects.count(),
        'total_claims': claims.count(),
        'total_amount': claims.aggregate(Sum('amount'))['amount__sum'] or 0,
        'pending_amount': claims.filter(status__icontains='Pending').aggregate(Sum('amount'))['amount__sum'] or 0,
        'paid_amount': claims.filter(status='Paid').aggregate(Sum('amount'))['amount__sum'] or 0,
        'all_claims': claims
    }
    return render(request, 'claims/admin_dashboard.html', context)