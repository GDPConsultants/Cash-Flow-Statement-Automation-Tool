Financial AI Automation Suite (IFRS & CPA Standards)
A professional, high-security financial automation suite developed by GDP Consultants. This suite features two primary tools: the Bank Reconciliation AI and the IFRS Cash Flow Statement Generator.

Designed for WordPress embedding, these tools provide a monetized, audit-ready experience with dynamic pricing and secure image-based previews.

🌟 Key Features
1. Bank Reconciliation AI (CPA Standard)

4-Step Methodology: Follows the official CPA Ireland step-by-step approach.
+1


Carryforward Logic: Automatically tracks unpresented cheques and unrealised deposits from the previous month.
+2


Adjusted Cash Book: Identifies bank charges, direct debits, and interest missing from internal records before final reconciliation.
+1


Error Detection: Highlights discrepancies between bank statements and cash books with reference details and dates.
+1

2. IFRS Cash Flow Statement Generator
Indirect Method: Automatically prepares Cash Flow Statements from Balance Sheets and P&L data according to IFRS standards.

Automated Adjustments: Calculates deltas for non-cash items like Depreciation and Amortization.

Classification: Properly categorizes Operating, Investing, and Financing activities.

3. Commercial & Security Features
Monetization: Integrated PayPal API for instant payments (USD 5 minimum).

Dynamic Pricing: For BRS, fees are calculated based on transaction volume ($5 for <100 entries, +$1 per additional 100).

Secure Preview: Generates high-resolution, watermarked image previews based on professional templates to prevent data copying before payment.

Branding: Automatically pulls the Business Name and Bank details from uploaded files to brand the reports.

Code Protection: Custom UI configuration hides developer menus and source code access for end-users.

🚀 Installation & Setup
Prerequisites
Python 3.9+

A private GitHub Repository

Streamlit Community Cloud account

PayPal Developer Account (Client ID & Secret)

1. Repository Structure
Ensure your GitHub folder contains the following:

Plaintext

├── app.py                      # Main Python application
├── logo-removebg-preview.png   # Your corporate logo
├── requirements.txt            # Dependency list
└── .streamlit/
    └── config.toml             # Security & Theme settings
2. Dependencies (requirements.txt)
Plaintext

streamlit
pandas
openpyxl
fpdf2
Pillow
requests
3. Security Configuration (.streamlit/config.toml)
To hide the "View Source" menu and developer tools from users, include the following:

Ini, TOML

[client]
toolbarMode = "minimal"

[browser]
gatherUsageStats = false
🛠 Deployment to WordPress
To add this tool to your WordPress homepage, use a Custom HTML Block with an IFrame:

HTML

<iframe
    src="https://your-app-name.streamlit.app/?embed=true"
    frameborder="0"
    width="100%"
    height="1200px"
    allow="payment"
></iframe>
📊 Accounting Methodology
Our tool follows the rigorous CPA Ireland Step-by-Step Guide:


Step 1: Reconcile Opening Balances.


Step 2: Eliminate matching amounts and details.


Step 3: Reconcile the Bank Account (Internal Book adjustments).


Step 4: Reconcile the Bank Statement (Unpresented items & Lodgements in transit).
+1

📞 Support & Contact
GDP Consultants

Email: info@taxcalculator.lk

Website: www.taxcalculator.lk
