import json
import os

from rest_framework.authentication import TokenAuthentication

from smartbankapp.models import Customer,CustomerAccount
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from smartbankapp.customer_validate import validate_customer,check_user,generate_account_number
from django.views.decorators.csrf import csrf_exempt
from openpyxl import Workbook


@csrf_exempt
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def kyc_create(request):
    user = check_user(request)
    if int(user.role) != 2:
        return HttpResponse(json.dumps({"Error": "user not found"}), content_type="application/json")
    if request.method == 'POST':
        try:
            body_data = json.loads(request.POST.get('data'))
            cus_validate,value = validate_customer(body_data)
            if not cus_validate:
                return HttpResponse(json.dumps({"Error":f'{value} Not in Correct format'}),content_type="application/json")

            id = body_data.get('id')
            name = body_data.get('name')
            email = body_data.get('email')
            id_type = body_data.get('id_type')
            address = body_data.get('address')
            city = body_data.get('city')
            state = body_data.get('state')
            pincode = body_data.get('pincode')

            id_document = request.FILES.get('id_document')
            ext = os.path.splitext(id_document.name)[1]
            valid_extensions = ['.pdf', '.jpg', '.jpeg', '.png']

            if ext.lower() not in valid_extensions:
                return HttpResponse(json.dumps({"Error":"File type in pdf or jpg or jpeg"}),status=400,content_type='application/json')

            if id_type not in ['',None] and id_type not in {1:"Aadhaar",2:"Pan",3:"Driving Linsence"}:
                return HttpResponse(json.dumps({"Error":"Choose the file type"}),status=400,content_type='application/json')

            if id not in [None,''] and isinstance(id,int):
                customer = Customer.objects.get(id=id)
                if customer:
                    customer.name = name
                    customer.email = email
                    customer.id_type = id_type
                    customer.id_document = id_document
                    customer.address = address
                    customer.city = city
                    customer.state = state
                    customer.pincode = pincode
                    customer.save()
                    return HttpResponse(json.dumps({"Message":"Successfully Updated"}),content_type="application/json")
                else:
                    return HttpResponse(json.dumps({"Message":"Invalid ID"}),content_type="application/json")
            else:

                customer_id = Customer.objects.create(
                    customer_name=name,
                    email=email,
                    id_type=id_type,
                    id_document=id_document,
                    address=address,
                    city=city,
                    state=state,
                    pincode=pincode,
                )
                return HttpResponse(json.dumps({"Message":"Successfully Created"}),content_type="application/json")

        except Exception as e:
            return HttpResponse(json.dumps({"Error":str(e)}),content_type="application/json")

    else:
        cus_id = request.GET.get('cus_id')
        cust_details = Customer.objects.get(id=cus_id)
        if cust_details:
            id_type = {"1":"Aadhaar","2":"Pan","3":"Driving Linsence"}
            cus_status = {"1":"PENDING","2":"APPROVED","3":"REJECTED"}
            cus_dict = dict()
            cus_dict['CustomerName'] = cust_details.customer_name
            cus_dict['Email'] = cust_details.email
            cus_dict['IdType'] = id_type.get(cust_details.id_type)
            cus_dict['Address'] = cust_details.address
            cus_dict['City'] = cust_details.city
            cus_dict['State'] = cust_details.state
            cus_dict['Pincode'] = cust_details.pincode
            cus_dict['Status'] = cus_status.get(cust_details.cus_status)
            return HttpResponse(json.dumps(cus_dict),content_type="application/json")
        else:
            return HttpResponse(json.dumps({"Error":"Customer not found"}),content_type="application/json")


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def customer_approver(request):
    user = check_user(request)
    if int(user.role) != 1:
        return HttpResponse(json.dumps({"Error":"You are not authorized"}),content_type="application/json")
    if request.method == 'GET':
        status = request.GET.get('status')
        cus_id = request.GET.get('cus_id')
        cus_dtls = Customer.objects.get(id=cus_id)
        if not cus_dtls:
            return HttpResponse(json.dumps({"Error":"Customer not found"}),content_type="application/json")
        cus_status = {"1": "PENDING", "2": "APPROVED", "3": "REJECTED"}
        cus_dtls.cus_status = status
        cus_dtls.save()
        return HttpResponse(json.dumps({"Status":cus_status.get(status)}),content_type="application/json")

@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def customer_deactivate(request):
    user = check_user(request)
    if int(user.role) != 1:
        return HttpResponse(json.dumps({"Error":"You are not authorized"}),content_type="application/json")
    if request.method == 'GET':
        status = request.GET.get('status')
        cus_id = request.GET.get('cus_id')
        cus_dtls = Customer.objects.get(id=cus_id)
        if not cus_dtls:
            return HttpResponse(json.dumps({"Error":"Customer not found"}),content_type="application/json")
        cus_dtls.status = status
        cus_dtls.save()
        return HttpResponse(json.dumps({"Status":"Deactivated"}),content_type="application/json")


@csrf_exempt
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def account_creating(request):
    user = check_user(request)
    if int(user.role) != 2:
        return HttpResponse(json.dumps({"Error":"You are not authorized"}),content_type="application/json")

    if request.method == 'POST':
        body_data=json.loads(request.body)
        cus_id = body_data.get('cus_id')
        account_type = body_data.get('account_type')
        id = body_data.get('id')

        if account_type in ['',None] or cus_id in [None,'']:
            return HttpResponse(json.dumps({"Error":"Cannot Be Empty"}),content_type="application/json")
        cus_dtls = Customer.objects.get(id=cus_id)
        if not cus_dtls:
            return HttpResponse(json.dumps({"Error":"Customer not found"}),content_type="application/json")

        kyc_verified = False
        if int(cus_dtls.cus_status) != 2:
            cus_status = {"1": "PENDING","3": "REJECTED"}
            return HttpResponse(json.dumps({"Error":f'Customer in {cus_status.get(cus_dtls.cus_status)} Status'}),content_type="application/json")
        else:
            kyc_verified = True

        #update
        if id not in [None,'']:
            cus_acc_dtls = CustomerAccount.objects.get(id=id)
            if cus_acc_dtls:
                cus_acc_dtls.account_type = account_type
                cus_acc_dtls.save()
                return HttpResponse(json.dumps({"Message":"Successfully Updated"}),content_type="application/json")
            else:
                return HttpResponse(json.dumps({"Error":"Customer Account not found"}),content_type="application/json")
        #create
        else:
            if CustomerAccount.objects.filter(customer=cus_id).exists():
                return HttpResponse(json.dumps({"Error":"Customer Account already exist"}),content_type="application/json")

            account_number = generate_account_number()
            while CustomerAccount.objects.filter(account_number=account_number).exists():
                account_number = generate_account_number()

            CustomerAccount.objects.create(
                account_number=account_number,
                account_type=account_type,
                customer_id = cus_dtls.id,
                kyc_verified = kyc_verified,
            )
            return HttpResponse(json.dumps({"Status":"Account Created"}),content_type="application/json")

    else:
        cus_acc_id = request.GET.get('cus_acc_id')
        cus_acc_dtls = CustomerAccount.objects.get(id=cus_acc_id)
        if not cus_acc_dtls:
            return HttpResponse(json.dumps({"Error":"Customer Account not found"}),content_type="application/json")
        cus_acc_type = {"1":"Savings","2":"Current"}
        cus_acc_dict = dict()
        cus_acc_dict['account_number'] = cus_acc_dtls.account_number
        cus_acc_dict['account_type'] = cus_acc_type.get(cus_acc_dtls.account_type)
        cus_acc_dict['Customer_name'] =cus_acc_dtls.customer.customer_name
        cus_acc_dict['balance'] = str(cus_acc_dtls.balance)
        return HttpResponse(json.dumps(cus_acc_dict),content_type="application/json")

@csrf_exempt
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def export_accounts_excel(request):
    # Create workbook and sheet
    wb = Workbook()
    ws = wb.active
    ws.title = "Customer Accounts"

    # Write header
    ws.append([
        "Username", "Email","Address","City","Pincode","Account Number", "Account Type",
        "Balance", "KYC Verified"
    ])
    cus_acc_type = {"1": "Savings", "2": "Current"}
    # Write data
    for account in CustomerAccount.objects.all():
        ws.append([
            account.customer.customer_name,
            account.customer.email,
            account.customer.address,
            account.customer.city,
            account.customer.pincode,
            account.account_number,
            cus_acc_type.get(account.account_type),
            float(account.balance),
            "Yes" if account.kyc_verified else "No",
            account.created_at.strftime("%Y-%m-%d %H:%M")
        ])

    # Create HTTP response with Excel file
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="customer_accounts.xlsx"'

    # Save workbook to response
    wb.save(response)
    return response
