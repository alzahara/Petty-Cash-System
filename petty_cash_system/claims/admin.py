from django.contrib import admin
from .models import  Claim,ApprovalHistory
# Register your models here.
admin.site.register(Claim)
admin.site.register(ApprovalHistory)
