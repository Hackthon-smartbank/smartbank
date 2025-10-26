# SmartBank Backend System

For HCL Hackathon

Framework: Django Rest Framework
Database: MySQL

Security Features:

* JWT-based authentication
* Role-based access control
* Input validation

---

## Use Cases

### 1. User Registration & KYC - COMPLETED

**Customer Sign Up:**

* Submit personal details
* Upload KYC documents
* System validates if the customer already exists
* Passwords are hashed

**APIs:**

**a) Create User (Admin/Customer)**
POST `/user_create`

Admin Example:

```json
{
  "username": "Admin3",
  "password": "admin@123",
  "role": "Admin"
}
```

Response:

```json
{
  "success": "Successfully Created",
  "User": "Admin3",
  "token": "03b475daf3f5299ff4512462b2daa5047e350791"
}
```

Customer Example:

```json
{
  "username": "customer",
  "password": "cus@123",
  "role": "Customer"
}
```

Response:

```json
{
  "success": "Successfully Created",
  "User": "customer",
  "token": "feb5589a4cb324bde1ee3ed59c1d213040c61072"
}
```

**b) Create/Update KYC in Form Data**
POST `/kyc_create`

Create Example:

```json
data: {
  "name": "Ramesh",
  "id_type": 1,
  "address": "Chennai",
  "city": "Chennai",
  "state": "Chennai",
  "pincode": 600002
}
id_document: <File>
```

Response:

```json
{"Message": "Successfully Created"}
```

Update Example:

```json
data: {
  "id": 1,
  "name": "Ramesh",
  "id_type": 1,
  "address": "Chennai",
  "city": "Chennai",
  "state": "Chennai",
  "pincode": 600002
}
id_document: <File>
```

Response:

```json
{"Message": "Successfully Updated"}
```

**c) Approve/Reject Customer KYC**
GET `/customer_approver?cus_id=1&status=2`
status: 1 = Pending, 2 = Approve, 3 = Reject

Response:

```json
{"Status": "APPROVED"}
```

**d) Get Customer KYC Details**
GET `/kyc_create?cus_id=1`
Response:

```json
{
  "CustomerName": "koushik",
  "Email": null,
  "IdType": "Aadhaar",
  "Address": "Chennai",
  "City": "Chennai",
  "State": "Chennai",
  "Pincode": "600002",
  "Status": "APPROVED"
}
```

---

### 2. Account Creation - COMPLETED

Customer Account Creation / Login

* Generate new alphanumeric account number
* Initiate minimum balance

**APIs:**

**a) Create Account**
POST `/account_creation`

```json
{
  "cus_id": 2,
  "account_type": 2
}
```

Response:

```json
{"Status": "Account Created"}
```

Update Account:

```json
{
  "cus_id": 2,
  "account_type": 1,
  "id": 1
}
```

Response:

```json
{"Message": "Successfully Updated"}
```

**b) Get Account Details**
GET `/account_creating?cus_acc_id=2`
Response:

```json
{
  "account_number": "CUSKSIE202526",
  "account_type": "Current",
  "Customer_name": "Ramesh",
  "balance": "0.00"
}
```

---

### 3. Money Transfer

**Features:**

* Check sender balance
* Validate transfer limits
* Verify receiver account exists

**APIs:**

**a) Transfer Money**
POST `/transfer_money`


**b) Get Transaction History**
GET `/get_transaction`


### 4. Reports

**Admin & Customer Reports:**

* Admin can view customer profiles and KYC documents
* Customer can view transaction history

**APIs:**

**a) Get All Customers**
GET `/get_customer_list`
Response: List of customers with details

**b) Export Accounts to Excel** -COMPLETED
GET `/export_accounts_excel`
Returns `.xlsx` file containing all customer account details

---

### Tech Stack

* Framework: Django Rest Framework
* Database: MySQL
* Authentication: JWT
* Features: Role-based access, KYC validation, Money transfer, Excel reporting
