# FundWise
## Empower financial literacy: Track teen spending &amp; guide parents' oversight.


 ### Fundwise is a Django-based project consisting of two apps: Accounts and Parent. It serves as an expense tracking system enabling parents to monitor and manage their child's expenditure.


### Features
1. Accounts App: Manages student data, allowing student registration and zero balance upon login.
2. Parent App: Handles parent data and the connection between parent and child accounts.
3. Parent-Child Connection: Parents register by linking their account to their child's username, facilitating one-way money transfers from parent to child.
4. Transaction History: Parents can view the transaction history and wallet balance of their child's account.
5. Wallet Management: Parents can automatically add funds to their wallet, while children rely on parents for fund allocation.


### How It Works
1. Student Registration: Students register and log in with a zero balance in their wallet.
2. Parent Registration: Parents register and link their account to their child's username.
3. Transaction Process: Money can only be transferred from the parent to the child's account, ensuring controlled expenditure.
4. Wallet Balances: Parents can monitor their child's wallet balance and transaction history.


### Usage
1. Clone the repository:
git clone https://github.com/{your-username}/fundwise.git
2. Set up the Django environment and required dependencies.
3. Run the Django server:  python manage.py runserver
4. Access the application via the specified port in your browser.


### Contribution
Feel free to contribute by submitting bug fixes or additional features via pull requests.

### License
This project is licensed under the MIT License.
