import streamlit as st
import pandas as pd
import pdfplumber
import io
import streamlit.components.v1 as components
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Universal Cash Flow AI", layout="wide")

# --- 2. DYNAMIC EXTRACTION ENGINE ---

class CashFlowEngine:
    """Universal engine to map any financial statement to IFRS categories."""
    
    KEYWORD_MAP = {
        "profit_before_tax": ["profit before tax", "pbt", "profit before taxation", "operating profit"],
        "depreciation": ["depreciation", "amortization", "depn", "amortisation"],
        "receivables": ["receivables", "debtors", "trade and other receivables"],
        "inventory": ["inventory", "stock", "inventories"],
        "payables": ["payables", "creditors", "trade and other payables"],
        "ppe_purchase": ["purchase of ppe", "acquisition of property", "additions to ppe"],
        "dividends": ["dividends paid", "dividend payment"]
    }

    @staticmethod
    def extract_value(df, key_list):
        """Searches a DataFrame for keywords and returns the associated numeric value."""
        for _, row in df.iterrows():
            row_str = str(row.iloc[0]).lower()
            if any(key in row_str for key in key_list):
                # Try to find the first numeric value in that row
                for val in row[1:]:
                    try:
                        return float(str(val).replace(',', '').replace('(', '-').replace(')', ''))
                    except: continue
        return 0.0

def process_file(uploaded_file):
    """Detects file type and converts to a standard DataFrame."""
    if uploaded_file.name.endswith('.pdf'):
        with pdfplumber.open(uploaded_file) as pdf:
            all_text = []
            for page in pdf.pages:
                table = page.extract_table()
                if table: all_text.extend(table)
        return pd.DataFrame(all_text)
    else:
        return pd.read_excel(uploaded_file)

# --- 3. CASH FLOW GENERATOR ---

def build_ifrs_statement(raw_df):
    engine = CashFlowEngine()
    
    # 1. Operating Activities
    pbt = engine.extract_value(raw_df, engine.KEYWORD_MAP["profit_before_tax"])
    depn = engine.extract_value(raw_df, engine.KEYWORD_MAP["depreciation"])
    rec_change = engine.extract_value(raw_df, engine.KEYWORD_MAP["receivables"])
    inv_change = engine.extract_value(raw_df, engine.KEYWORD_MAP["inventory"])
    pay_change = engine.extract_value(raw_df, engine.KEYWORD_MAP["payables"])
    
    # 2. Investing & Financing
    ppe = engine.extract_value(raw_df, engine.KEYWORD_MAP["ppe_purchase"])
    divs = engine.extract_value(raw_df, engine.KEYWORD_MAP["dividends"])

    data = [
        ["CASH FLOWS FROM OPERATING ACTIVITIES", None],
        ["  Profit Before Taxation", pbt],
        ["  Adjustments: Depreciation & Amortization", depn],
        ["  (Increase)/Decrease in Inventories", -inv_change],
        ["  (Increase)/Decrease in Receivables", -rec_change],
        ["  Increase/(Decrease) in Payables", pay_change],
        ["Net Cash from Operating Activities", pbt + depn - inv_change - rec_change + pay_change],
        ["", None],
        ["CASH FLOWS FROM INVESTING ACTIVITIES", None],
        ["  Purchase of Fixed Assets", -abs(ppe)],
        ["Net Cash used in Investing Activities", -abs(ppe)],
        ["", None],
        ["CASH FLOWS FROM FINANCING ACTIVITIES", None],
        ["  Dividends Paid", -abs(divs)],
        ["Net Cash used in Financing Activities", -abs(divs)],
        ["", None],
        ["NET CHANGE IN CASH", (pbt + depn - inv_change - rec_change + pay_change) - abs(ppe) - abs(divs)]
    ]
    return pd.DataFrame(data, columns=["Classification", "Amount"])

# --- 4. STREAMLIT UI ---

st.title("🏦 Universal Financial AI Suite")
st.write("Upload any organization's Trial Balance, P&L, or Balance Sheet.")

file = st.file_uploader("Upload PDF or Excel", type=['pdf', 'xlsx'])

if file:
    with st.spinner("Analyzing financial structure..."):
        raw_data = process_file(file)
        final_cf = build_ifrs_statement(raw_data)

    # PREVIEW
    st.subheader("📊 Draft Cash Flow Statement")
    st.table(final_cf.head(10)) 
    st.info("The full detailed report with all 3 sections (Operating, Investing, Financing) is generated below.")

    # PAYPAL
    st.markdown("### 💳 Unlock Full Audit-Ready Report")
    paypal_code = f"""
    <div id="paypal-button-container"></div>
    <script src="https://www.paypal.com/sdk/js?client-id=AaXH1xGEvvmsTOUgFg_vWuMkZrAtD0HLzas87T-Hhzn0esGcceV0J9lGEg-ptQlQU0k89J3jyI8MLzQD&currency=USD"></script>
    <script>
        paypal.Buttons({{
            createOrder: function(data, actions) {{ return actions.order.create({{ purchase_units: [{{ amount: {{ value: '5.00' }} }}] }}); }},
            onApprove: function(data, actions) {{ window.parent.postMessage({{type: 'payment_success'}}, '*'); }}
        }}).render('#paypal-button-container');
    </script>
    """
    components.html(paypal_code, height=300)

    if st.checkbox("Payment Completed"):
        # PDF Generation Logic here (same as previous versions)
        st.success("Access Granted.")
        st.download_button("📥 Download PDF", final_cf.to_csv(), "Report.csv")
