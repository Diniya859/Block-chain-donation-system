from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("sender_address", "amount", "transaction_hash", "status", "timestamp")
    list_filter = ("status",)
    search_fields = ("sender_address", "transaction_hash")
