import streamlit as st
import pandas as pd
import pdfplumber
import io
import streamlit.components.v1 as components  # FIX: Added missing import
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- 1. CONFIGURATION & UI ---
st.set_page_config(page_title="IFRS Cash Flow AI | GDP Consultants", layout="wide")

# Hide Streamlit elements to protect code and maintain branding
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .main {background-color: #F8FAFC;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. MODULAR FUNCTIONS ---

def prepare_cash_flow(uploaded_file):
    """
    Logic to extract and classify data into IFRS categories.
    In production, this would use pandas to calculate deltas between opening/closing balances.
    """
    # Professional IFRS Structure (Indirect Method)
    data = {
        "IFRS Classification": [
            "Cash flows from operating activities",
            "  Profit before tax",
            "  Adjustments for: Depreciation",
            "  Increase/Decrease in Inventories",
            "  Increase/Decrease in Trade Receivables",
            "Net cash from operating activities",
            "",
            "Cash flows from investing activities",
            "  Purchase of Property, Plant & Equipment",
            "  Proceeds from sale of equipment",
            "Net cash used in investing activities",
            "",
            "Cash flows from financing activities",
            "  Proceeds from loans",
            "  Dividends paid",
            "Net cash from financing activities",
            "",
            "NET INCREASE IN CASH"
        ],
        "Amount (USD)": [
            None, 500000.00, 45000.00, -12000.00, -8000.00, 525000.00,
            None, None, -120000.00, 15000.00, -105000.00,
            None, None, 50000.00, -15000.00, 35000.00,
            None, 455000.00
        ]
    }
    return pd.DataFrame(data)

def generate_pdf(df, biz_name, period, currency):
    """Generates an IFRS-standard PDF report."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Header
    elements.append(Paragraph(f"<b>{biz_name}</b>", styles['Title']))
    elements.append(Paragraph(f"Statement of Cash Flows (IFRS - LKAS 7)", styles['Heading2']))
    elements.append(Paragraph(f"Period: {period} | Currency: {currency}", styles['Normal']))
    elements.append(Spacer(1, 20))

    # Data Table
    table_data = [df.columns.to_list()] + df.values.tolist()
    formatted_data = [[str(item) if item is not None else "" for item in row] for row in table_data]
    
    t = Table(formatted_data, colWidths=[350, 120])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.darkgreen),
    ]))
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# --- 3. MAIN APP FLOW ---

with st.sidebar:
    try: st.image("logo-removebg-preview.png")
    except: st.info("GDP Consultants")
    st.write("### IFRS Automation Tool")
    st.markdown("---")
    st.write("📧 info@taxcalculator.lk")

st.title("IFRS Cash Flow Statement Automation")
st.info("Upload Financial Statements to generate IFRS (LKAS 7) compliant reports.")

uploaded_file = st.file_uploader("Upload Opening Balance Sheet & P&L (Excel/PDF)", type=['xlsx', 'pdf'])

if uploaded_file:
    # 1. Generate Logic
    cf_df = prepare_cash_flow(uploaded_file)
    
    # 2. Preview Block (Restricted)
    st.subheader("🏁 Statement Preview")
    # Show only the top rows and hide final totals to encourage payment
    st.dataframe(cf_df.iloc[:6].style.format({"Amount (USD)": "{:,.2f}"})) 
    st.warning("🔒 Full report is locked. Pay USD 5 to download PDF and Excel versions.")

    # 3. PayPal Integration
    paypal_btn_html = f"""
    <div id="paypal-button-container" style="text-align: center;"></div>
    <script src="https://www.paypal.com/sdk/js?client-id=AaXH1xGEvvmsTOUgFg_vWuMkZrAtD0HLzas87T-Hhzn0esGcceV0J9lGEg-ptQlQU0k89J3jyI8MLzQD&currency=USD"></script>
    <script>
        paypal.Buttons({{
            createOrder: function(data, actions) {{
                return actions.order.create({{
                    purchase_units: [{{ amount: {{ value: '5.00' }} }}]
                }});
            }},
            onApprove: function(data, actions) {{
                return actions.order.capture().then(function(details) {{
                    window.parent.postMessage({{type: 'payment_success'}}, '*');
                }});
            }}
        }}).render('#paypal-button-container');
    </script>
    """
    components.html(paypal_btn_html, height=450)

    # 4. Post-Payment (Using a checkbox to simulate verification for this demo)
    if st.checkbox("Unlock Download (Payment Verified)"):
        st.success("✅ Access Granted.")
        
        # PDF Download
        pdf_report = generate_pdf(cf_df, "ABC ENTERPRISES", "FY 2025", "USD")
        st.download_button("📥 Download IFRS PDF Report", pdf_report, "IFRS_CashFlow.pdf")
        
        # Excel Download
        excel_buffer = io.BytesIO()
        cf_df.to_excel(excel_buffer, index=False)
        st.download_button("📥 Download Excel Data", excel_buffer.getvalue(), "IFRS_CashFlow.xlsx")
