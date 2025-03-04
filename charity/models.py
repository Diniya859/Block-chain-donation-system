from django.db import models
class login_table(models.Model):
    username=models.CharField(max_length=100)
    password=models.CharField(max_length=30)
    usertype=models.CharField(max_length=50)

class registration_table(models.Model):
    Login=models.ForeignKey(login_table,on_delete=models.CASCADE)
    fname=models.CharField(max_length=100,null=True)
    lname=models.CharField(max_length=100,null=True)
    email=models.EmailField(max_length=100,unique=True,null=True)

class charity_table(models.Model):
    title=models.CharField(max_length=100)
    place=models.CharField(max_length=100)
    description=models.CharField(max_length=255)
    category=models.CharField(max_length=100)
from django.db import models


class Transaction(models.Model):
    sender_address = models.CharField(max_length=255)  # Wallet Address of Sender
    amount = models.DecimalField(max_digits=18, decimal_places=8)  # ETH Amount
    transaction_hash = models.CharField(max_length=255, unique=True)  # Blockchain Txn Hash
    status = models.CharField(
        max_length=20,
        choices=[('Success', 'Success'), ('Failed', 'Failed')],
        default='Success'
    )
    timestamp = models.DateTimeField(auto_now_add=True)  # Time of Transaction

    def __str__(self):
        return f"{self.sender_address} - {self.amount} ETH - {self.status}"


class complaint_table(models.Model):
    complaint_date=models.CharField(max_length=300)
    reply_date=models.CharField(max_length=100)
    USER=models.ForeignKey(registration_table,on_delete=models.CASCADE,default=1)
    complaint=models.CharField(max_length=300)
    reply=models.CharField(max_length=100)
    complaint_type=models.CharField(max_length=255, default='General')

class feedback_table(models.Model):
    USER = models.ForeignKey(registration_table, on_delete=models.CASCADE, default=1)
    feedback=models.CharField(max_length=300)
    feedback_date=models.CharField(max_length=100)
    rating=models.CharField(max_length=100,default=1)

