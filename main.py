from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # replace with your own secret key

# set maximum loan amount for each user
MAX_LOAN_AMOUNT = {'Alice': 1000, 'Bob': 2000, 'Charlie': 3000}

# in-memory data store for loan amounts and pending loan requests
loan_amounts = {'Alice': 0, 'Bob': 0, 'Charlie': 0}
pending_loans = []

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        print("working")
        print(username)
        if username in MAX_LOAN_AMOUNT:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return 'Invalid username'
    return render_template('login.html')

# dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    username = session['username']
    loan_amount = loan_amounts[username]
    max_loan_amount = MAX_LOAN_AMOUNT[username]
    if request.method == 'POST':
        loan_request = int(request.form['loan_amount'])
        if loan_request <= max_loan_amount:
            pending_loans.append((username, loan_request))
            return redirect('/dashboard')
        else:
            return 'Loan request exceeds maximum amount'
    return render_template('dashboard.html', username=username, loan_amount=loan_amount, max_loan_amount=max_loan_amount, pending_loans=pending_loans)

# loan request route
@app.route('/request_loan', methods=['POST'])
def request_loan():
    if 'username' not in session:
        return redirect('/login')
    username = session['username']
    max_loan_amount = MAX_LOAN_AMOUNT[username]
    loan_request = int(request.form['loan_amount'])
    if loan_request <= max_loan_amount:
        pending_loans.append((username, loan_request))
        return redirect('/dashboard')
    else:
        return 'Loan request exceeds maximum amount'

# approve loan route
@app.route('/approve_loan/<int:loan_id>', methods=['GET', 'POST'])
def approve_loan(loan_id):
    if 'username' not in session:
        return redirect('/login')
    username = session['username']
    if request.method == 'POST':
        vote = int(request.form['vote'])
        if vote == 1:
            approved = True
        else:
            approved = False
        for i, (borrower, loan_amount) in enumerate(pending_loans):
            if i == loan_id and borrower != username:
                if approved:
                    loan_amounts[borrower] += loan_amount
                pending_loans.pop(i)
                return redirect('/dashboard')
    else:
        for i, (borrower, loan_amount) in enumerate(pending_loans):
            if i == loan_id and borrower != username:
                return render_template('approve_loan.html', borrower=borrower, loan_amount=loan_amount)
    return 'Invalid loan ID'

if __name__ == '__main__':
    app.run(debug=True)




