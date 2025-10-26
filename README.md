# smartbank
For Hcl hackthon

FrameWork - Django RestFrameWork
Database - Mysql

Security Features
    JWT-based authentication
    Role-based access
    Input validation

* Use Case

1. User Registration & KYC

    # Customer sign up
    # Submit the personal details
    # Upload KYC documents
    # System validate the Customer is already exists
    # hashing the password
    API LIST
        (POST)- /user_create - role based creation[admin,customer]
            * Admin - {"username":"Admin3","password":"admin@123","role":"Admin"}
            * response - {"success": "successfully Created","User": "Admin3","token": "03b475daf3f5299ff4512462b2daa5047e350791"}

            * Customer - {"username":"customer","password":"cus@123","role":"Customer"}
            * response - {"success": "successfully Created","User": "customer","token": "feb5589a4cb324bde1ee3ed59c1d213040c61072"}

        (POST)- /kyc_create - for customer getting their documents and personal details[name,aadhaar,pan,address,etc]
            Form data
            * data : {"name":"Ramesh","id_type":1,"address":"chennai","city":"chennai","state":"chennai","pincode":600002}
            * id_document : Your File
            * response - {"Message": "Successfully Created"}

            For Update - need to add ID
            * data : {"id":1,"name":"Ramesh","id_type":1,"address":"chennai","city":"chennai","state":"chennai","pincode":600002}
            * id_document : Your File
            * response - {"Message": "Successfully Created"}            

        (GET)- /customer_approver?cus_id=1&status=2 - for admin can approve or reject
            status 1 for Pending, 2 for Approve and 3 for Reject
            * response - {"Status": "APPROVED"} - it will give what status is changed

        (GET)- /kyc_create?cus_id=1 - details of customer
            * reponse - {"CustomerName": "koushik","Email": null,"IdType": "Aadhaar","Address": "chennai","City": "chennai","State": "chennai","Pincode": "600002",    "Status": "APPROVED"}

2. Account Creation
    
    # Customer will create a new Account or They can login existing account
    # If the user is Generate new Account number(Alpha Numeric)
    # Initiate Minimum Balance to the Account holder
    API LIST
        (POST)- /account_creation -  customer can create the account[name,account_type,initial_deposit]
            * body : {"cus_id":2,"account_type":2}
            * response - {"Status": "Account Created"}
            For Update
            * body : {"cus_id":2,"account_type":1,"id":1}
            * response - {"Message": "Successfully Updated"}

        (GET)- /account_creating?cus_acc_id=2 - get the account details of customer
            * response - {"account_number": "CUSKSIE202526","account_type": "Current","Customer_name": "Ramesh","balance": "0.00"}

3. Money Transfer

    # Check sender Account holder's balance before Transfering
    # Check Account holders's Limit if the limit is exceed should Initiate
    # Need to give them check balance
    # Check the Receiver's side details If exists will do transaction to account number
    API LIST
        (POST)- /transfer_money - trnasfer the money other account[customer_id,tran_date,amount,customer_account_number,other_account_number]
        (GET)- /get_transaction - get the transaction details

7. Report 

    # Fetching the customer details to Admin
    # Admin can View the Customer's profile and Check the documents(Approve or Reject)
    # customer can view the transaction history
    API LIST
        (GET) - /get_customer_list - It give all customer details for admin
        (GET)- /export_accounts_excel - it will give excel report for the admin
            * It will return the Excel of Account detail of customer
