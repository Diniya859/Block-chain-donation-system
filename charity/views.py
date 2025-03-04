from django.shortcuts import render, redirect
from charity.models import *
from django.http import HttpResponse,JsonResponse
import datetime
from django.views.decorators.csrf import csrf_exempt

def index(request):
    charities = charity_table.objects.all()
    return render(request, 'index.html', {'charities': charities})

def home(request):
    charities = charity_table.objects.all()
    return render(request, 'index.html', {'charities': charities})

def login_post(request):
    usn=request.POST['textfield']
    psn=request.POST['password']
    res=login_table.objects.filter(username=usn,password=psn)
    if res.exists():
        logid=res[0].id
        request.session['lid']=logid
        if res[0].usertype=='admin':
            return redirect('/admin_functions')
        elif res[0].usertype=='user':
            return redirect('/user_functions')
        else:
            return HttpResponse("<script>alert('invalid user');window.location='/home'</script>")
    else:
       return HttpResponse("<script>alert('check your username and password');window.location='/home</script>")

def admin_functions(request):
    users = registration_table.objects.all()
    complaints = complaint_table.objects.all()
    feedbacks = feedback_table.objects.all()
    charities=charity_table.objects.all()
    context = {
        'users_count': registration_table.objects.count(),
        'complaints_count': complaint_table.objects.count(),
        'feedback_count': feedback_table.objects.count(),
        'charities_count' : charity_table.objects.count(),
        'users':users,
        'charities':charities,
        'feedbacks':feedbacks,
        'complaints':complaints,
    }
    return render(request, 'admin/index.html', context)

def user_functions(request):
    if request.session['lid']=="":
        return HttpResponse("<script>alert('Logout Sucessfully');window.location='/home'</script>")

    charities = charity_table.objects.all()
    return render(request, 'user/index.html',{'charities': charities})
def reply(request):
    if request.session['lid'] == "":
        return HttpResponse("<script>alert('Logout Sucessfully');window.location='/home'</script>")
    qry=complaint_table.objects.filter(USER__Login=request.session['lid'])
    return render(request, 'user/reply.html',{"data":qry})

def register(request):
    fname=request.POST['textfield1']
    lname=request.POST['textfield']
    psn=request.POST['password']
    email=request.POST['textfield3']
    qry=login_table.objects.filter(username=email)
    if qry.exists():
        return HttpResponse("<script>alert('Email already exists!');window.location='/home'</script>")

    log=login_table()
    log.username=email
    log.password=psn
    log.usertype='user'
    log.save()

    reg=registration_table()
    reg.fname=fname
    reg.lname=lname
    reg.email=email
    reg.Login=log
    reg.save()
    return HttpResponse("<script>alert('Saved Successfully');window.location='/user_functions'</script>")


def reply_post(request, id):
    if request.method == "POST":
        reply_message = request.POST.get('textfield')

        # Update the complaint with the reply
        complaint = complaint_table.objects.get(id=id)
        complaint.reply = reply_message
        complaint.reply_date=datetime.datetime.now().strftime("%y-%m-%d")
        complaint.save()
        return HttpResponse("<script>alert('Replied');window.location='/admin_functions'</script>")

    else:
        return HttpResponse("Invalid request method.", status=405)

@csrf_exempt  # Allows handling DELETE without CSRF token for simplicity
def delete_charity(request, id):
    if request.method == "DELETE":
        try:
            charity = charity_table.objects.get(id=id)
            charity.delete()
            return JsonResponse({"success": True, "message": "Charity deleted successfully."})
        except charity_table.DoesNotExist:
            return JsonResponse({"success": False, "message": "Charity not found."}, status=404)
    return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

def add(request):
    title=request.POST['textfield']
    place = request.POST['textfield1']
    description = request.POST['textfield2']
    category = request.POST['textfield3']

    charity=charity_table()
    charity.title=title
    charity.place=place
    charity.description=description
    charity.category=category
    charity.save()
    return HttpResponse("<script>alert('Saved Successfully');window.location='/admin_functions'</script>")

#--------------------users---------------------------
def user_feedback(request):
    feedback=request.POST['textfield']
    ra =request.POST['star']
    date=datetime.datetime.now().strftime("%y-%m-%d")
    uid=registration_table.objects.get(Login=request.session['lid'])
    fed=feedback_table()
    fed.USER=uid
    fed.feedback=feedback
    fed.feedback_date=date
    fed.rating=ra
    fed.save()
    return HttpResponse("<script>alert('Send Successfully');window.location='/user_functions'</script>")

def user_complaint(request):
    complaint = request.POST['textfield']
    date = datetime.datetime.now().strftime("%y-%m-%d")
    ur = registration_table.objects.get(Login=request.session['lid'])
    complaint_type = request.POST['textfield1']
    com = complaint_table()
    com.USER = ur
    com.complaint_type=complaint_type
    com.complaint = complaint
    com.complaint_date = date
    com.reply = 'pending'
    com.reply_date = 'pending'
    com.save()
    return HttpResponse("<script>alert('Send Successfully');window.location='/user_functions'</script>")

#-------------------------BLOCKCHAIN ------------------------------------------------------------------------------------
from django.shortcuts import render, get_object_or_404
from web3 import Web3
import json
from django.conf import settings

# Load Smart Contract ABI
with open("/DonationContract.json", "r") as file:
    contract_data = json.load(file)
    contract_abi = contract_data["abi"]

# Connect to Ganache
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
contract_address = "enter"
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

def donate(request):
    if request.method == 'POST':
        try:
            sender = request.POST.get('sender')
            private_key = request.POST.get('private_key')  # Must be handled securely!
            amount = request.POST.get('amount')

            if not sender or not private_key or not amount:
                return JsonResponse({"status": "failed", "message": "Missing required fields"}, status=400)

            amount = int(amount)  # Ensure valid integer amount
            if amount <= 0:
                return JsonResponse({"status": "failed", "message": "Invalid amount"}, status=400)

            # ✅ Fix nonce issue
            nonce = web3.eth.get_transaction_count(sender, "pending")
            gas_price = web3.eth.gas_price

            # ✅ Call Smart Contract's `donate` function instead of sending ETH directly
            txn = contract.functions.donate().build_transaction({
                'from': sender,
                'value': web3.to_wei(amount, 'ether'),
                'gas': 500000,
                'gasPrice': gas_price,
                'nonce': nonce
            })

            # ✅ Securely sign the transaction
            signed_txn = web3.eth.account.sign_transaction(txn, private_key)
            txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

            save_transaction(sender, amount, txn_hash.hex(), "Success")

            return JsonResponse({'status': 'success', 'transaction_hash': txn_hash.hex()})

        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=400)

    return render(request, 'donate.html')



def donate_page(request, charity_id):
    charity = get_object_or_404(charity_table, id=charity_id)
    return render(request, "donate.html", {"charity": charity})

@csrf_exempt  # Disable CSRF for now (use proper CSRF handling in production)
def save_transaction(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received Data:", data)  # ✅ Debugging log

            sender_address = data.get("sender_address")
            amount = data.get("amount")
            transaction_hash = data.get("transaction_hash")
            status = data.get("status", "Success")  # Default to Success

            if not sender_address or not amount or not transaction_hash:
                return JsonResponse({"error": "Missing required fields"}, status=400)

            if Transaction.objects.filter(transaction_hash=transaction_hash).exists():
                return JsonResponse({"message": "Transaction already recorded"}, status=400)

            # Save transaction
            Transaction.objects.create(
                sender_address=sender_address,
                amount=amount,
                transaction_hash=transaction_hash,
                status=status
            )

            return JsonResponse({"message": "Transaction saved successfully!"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)


def make_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode("utf-8"))
            from_address = data.get("from_address")
            amount = data.get("amount")

            if not from_address or not amount or float(amount) <= 0:
                return JsonResponse({'status': 'failed', 'error': 'Invalid input data'}, status=400)

            amount = float(amount)

            nonce = web3.eth.get_transaction_count(from_address, "pending")
            gas_price = web3.eth.gas_price

            txn = {
                'to': settings.CONTRACT_ADDRESS,
                'value': web3.to_wei(amount, 'ether'),
                'gas': 500000,
                'gasPrice': gas_price,
                'nonce': nonce
            }

            txn_hash = web3.eth.send_transaction(txn)
            txn_hash_hex = txn_hash.hex()

            # ✅ Save transaction in the database
            Transaction.objects.create(
                sender_address=from_address,
                amount=amount,
                transaction_hash=txn_hash_hex,
                status="Success"
            )

            return JsonResponse({'status': 'success', 'transaction_hash': txn_hash_hex})

        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)}, status=400)


