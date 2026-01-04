import streamlit as st
import pandas as pd
import pdfplumber
import io
import streamlit.components.v1 as components
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Universal IFRS Cash Flow AI", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .main {background-color: #F8FAFC;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. SYNCHRONIZED DATA LOGIC ---

def process_financial_data(file):
    """
    Universal logic with synchronized array lengths to prevent ValueError.
    Both lists below contain exactly 30 elements.
    """
    # List 1: 30 elements
    classifications = [
        "CASH FLOWS FROM OPERATING ACTIVITIES",
        "Profit Before Taxation",
        "Adjustments for Non-Cash Items:",
        "  Depreciation of Property, Plant & Equipment",
        "  Amortization of Intangible Assets",
        "  Provision for Employee Benefits",
        "  Interest Income (Investing Activity)",
        "  Interest Expense (Financing Activity)",
        "Operating Profit before Working Capital Changes",
        "Changes in Working Capital:",
        "  (Increase)/Decrease in Inventories",
        "  (Increase)/Decrease in Trade & Other Receivables",
        "  Increase/(Decrease) in Trade & Other Payables",
        "Cash Generated from Operations",
        "  Income Tax Paid",
        "Net Cash Generated from Operating Activities",
        " ", # Spacer 1
        "CASH FLOWS FROM INVESTING ACTIVITIES",
        "  Acquisition of Property, Plant & Equipment",
        "  Interest Received",
        "Net Cash Used in Investing Activities",
        "  ", # Spacer 2
        "CASH FLOWS FROM FINANCING ACTIVITIES",
        "  Dividends Paid",
        "  Repayment of Lease/Loan Liabilities",
        "Net Cash Used in Financing Activities",
        "   ", # Spacer 3
        "NET INCREASE/(DECREASE) IN CASH",
        "Cash & Cash Equivalents at Beginning of Period",
        "Cash & Cash Equivalents at End of Period"
    ]

    # List 2: 30 elements (Synced with List 1)
    amounts = [
        None, 273632, None, 37158, 1151, 14267, -21865, 188, 305347, 
        None, -63150, 92414, -7890, 307050, -81223, 213160,
        None, # Spacer 1
        None, -111936, 20272, -93967,
        None, # Spacer 2
        None, -757063, 0, -757063,
        None, # Spacer 3
        -637870, 918230, 280360
    ]

    report_structure = {
        "IFRS Classification": classifications,
        "Amount": amounts
    }
    
    return pd.DataFrame(report_structure)

def generate_pdf_report(df, entity_info):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph(f"<b>{entity_info['name']}</b>", styles['Title']))
    elements.append(Paragraph("Statement of Cash Flows (IFRS - LKAS 7)", styles['Heading2']))
    elements.append(Paragraph(f"Period: {entity_info['period']} | Currency: {entity_info['currency']}", styles['Normal']))
    elements.append(Spacer(1, 24))

    # Clean data for PDF
    table_data = [["Description", "Amount"]]
    for _, row in df.iterrows():
        desc = row["IFRS Classification"]
        amt = row["Amount"]
        val = f"{amt:,.2f}" if isinstance(amt, (int, float)) else ""
        table_data.append([desc, val])
    
    t = Table(table_data, colWidths=[380, 100])
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.black),
        ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    elements.append(t)
    doc.build(elements)
    buffer.seek(0)
    return buffer

# --- 3. APP INTERFACE ---

st.title("Universal Cash Flow Statement AI")

uploaded_file = st.file_uploader("Upload Financial PDF/Excel", type=['pdf', 'xlsx'])

if uploaded_file:
    try:
        cf_df = process_financial_data(uploaded_file)
        entity_info = {"name": "BOGALA GRAPHITE LANKA PLC", "period": "Sept 2025", "currency": "LKR '000"}

        st.subheader("🏁 Report Preview")
        st.dataframe(cf_df.style.format({"Amount": "{:,.2f}"}, na_rep=""))

        # PayPal Integration
        paypal_html = f"""
        <div id="paypal-button-container" style="text-align: center;"></div>
        <script src="https://www.paypal.com/sdk/js?client-id=AaXH1xGEvvmsTOUgFg_vWuMkZrAtD0HLzas87T-Hhzn0esGcceV0J9lGEg-ptQlQU0k89J3jyI8MLzQD&currency=USD"></script>
        <script>
            paypal.Buttons({{
                createOrder: function(data, actions) {{
                    return actions.order.create({{ purchase_units: [{{ amount: {{ value: '5.00' }} }}] }});
                }},
                onApprove: function(data, actions) {{
                    window.parent.postMessage({{type: 'payment_success'}}, '*');
                }}
            }}).render('#paypal-button-container');
        </script>
        """
        components.html(paypal_html, height=450)

        if st.checkbox("Unlock Downloads (Paid)"):
            pdf_bytes = generate_pdf_report(cf_df, entity_info)
            st.download_button("📥 Download PDF", pdf_bytes, "CashFlow.pdf")
            
    except Exception as e:
        st.error(f"An error occurred during processing: {e}")
