# Petty Cash Claims and Approval System

## 1. Project Overview
This project is a Python Django web application designed to manage employee petty cash claims efficiently. Employees can submit claims for day-to-day office expenses (like meals, travel, or stationery), which then automatically enter a structured, multi-level review and approval workflow before payment processing.

## 2. User Roles
The application enforces role-based access control (RBAC) with four distinct roles:
*   *Employee:* Can submit claims, upload receipts, and track their personal claim statuses.
*   *Manager:* Can view, add remarks to, and approve/reject claims pending manager review.
*   *Finance:* Can view manager-approved claims, approve/reject them, and change the status to "Paid".
*   *Admin:* Manages user accounts, assigns system roles, and accesses the full Django Admin panel.

## 3. Claim Workflow
Claims flow through a strict sequential pipeline:
1. *Submission:* Employee creates a claim $\rightarrow$ Status: Pending Manager Approval.
2. *Manager Review:* Manager approves $\rightarrow$ Status: Pending Finance Approval (or Manager Rejected).
3. *Finance Review:* Finance approves $\rightarrow$ Status: Finance Approved (or Finance Rejected).
4. *Disbursement:* Finance marks the approved claim as paid $\rightarrow$ Status: Paid.

## 4. How an Employee Submits a Claim
1. Log in using an Employee account.
2. Navigate to the "Submit Claim" form on the dashboard.
3. Fill in the Title, Category (e.g., Meals, Travel, Stationery), Amount, and Description.
4. Upload an image or document of the expense receipt.
5. Click *Submit*. The claim will appear under your recent claims tracking dashboard.

## 5. How Manager Approval Works
1. Log in using a Manager account.
2. The dashboard displays all incoming claims flagged as Pending Manager Approval.
3. Click on a claim to view its full details and uploaded receipt.
4. Input decision notes in the *Remarks* field.
5. Click *Approve* to pass it to Finance, or *Reject* to stop the claim.

## 6. How Finance Approval Works
1. Log in using a Finance account.
2. The dashboard populates with claims that show a status of Pending Finance Approval.
3. Review the claim details, manager notes, and receipt integrity.
4. Provide a financial review remark and click *Approve* (or *Reject*).

## 7. How to Mark a Claim as Paid
1. While logged in as Finance, locate the *"Claims waiting for payment"* section.
2. Click the *"Mark as Paid"* action button next to an approved claim.
3. The system logs the final action, updates the audit history, and moves the status to Paid. (No external payment gateway integration is utilized).

## 8. MySQL Database Details
The production version of this application uses a *MySQL Database* instead of SQLite. 
*   *Database Schema Name:* petty_cash_db
*   *Core Tables:* 
    *   auth_user: Handles application users and role flags.
    *   claims_claim: Stores core claim metadata (titles, categories, amounts, receipt paths, statuses).
    *   claims_approvalhistory: Logs the complete sequential audit trail of user actions and remarks.

### Local Configuration Setup
Update your settings.py:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'petty_cash_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
