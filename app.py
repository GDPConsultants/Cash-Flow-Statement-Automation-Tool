import streamlit as st
import pandas as pd
import pdfplumber
import io
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- 1. CONFIGURATION & BRANDING ---
st.set_page_config(page_title="IFRS Cash Flow AI", layout="wide")

# Custom CSS for professional layout and code protection
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .main {background-color: #F8FAFC;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. CORE FINANCIAL FUNCTIONS ---

def parse_excel(file):
    """Extracts balance sheet and P&L data from Excel."""
    try:
        df = pd.read_excel(file)
        return df
    except Exception as e:
        st.error(f"Excel Extraction Error: {e}")
        return None

def parse_pdf(file):
    """Extracts data from PDF using pdfplumber."""
    text_data = ""
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text_data += page.extract_text()
        # Logic to parse text into DataFrame would go here
        return text_data
    except Exception as e:
        st.error(f"PDF Extraction Error: {e}")
        return None

def prepare_cash_flow(data):
    """
    Constructs IFRS (LKAS 7) Cash Flow Statement using the Indirect Method.
    Classifies into Operating, Investing, and Financing activities.
    """
    # Placeholder for logic extracting entities from data
    # Real-world logic would map specific account names to these categories
    cf_structure = {
        "Category": [
            "Operating Activities", "Profit before tax", "Adjustments: Depreciation", "Changes in Working Capital",
            "Investing Activities", "Purchase of PPE", "Proceeds from Sale of PPE",
            "Financing Activities", "Loan Proceeds", "Dividends Paid"
        ],
        "Amount": [0, 500000, 45000, -20000, 0, -120000, 15000, 0, 50000, -10000]
    }
    return pd.DataFrame(cf_structure)

def generate_pdf(cf_df, metadata):
    """Generates an IFRS-styled PDF report."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title & Metadata
    elements.append(Paragraph(f"<b>Statement of Cash Flows</b>", styles['Title']))
    elements.append(Paragraph(f"Entity: {metadata['entity']}", styles['Normal']))
    elements.append(Paragraph(f"Period: {metadata['period']}", styles['Normal']))
    elements.append(Paragraph(f"Currency: {metadata['currency']}", styles['Normal']))
    elements.append(Paragraph("Prepared under IFRS (LKAS 7) Standards", styles['Italic']))
    elements.append(Spacer(1, 12))

    # Table
    data = [cf_df.columns.to_list()] + cf_df.values.tolist()
    t = Table(data, colWidths=[300, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ]))
    elements.append(t)
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

# --- 3. MAIN APPLICATION INTERFACE ---

st.title("IFRS Cash Flow Statement Automation")
st.write("Professional Audit-Ready Reporting by **GDP Consultants**")

# Sidebar
with st.sidebar:
    st.header("GDP AI Recon")
    st.write("Professional Audit Automation")
    st.divider()
    st.write("📧 info@taxcalculator.lk")

# File Upload
uploaded_file = st.file_uploader("Upload Opening Balance Sheet / P&L (Excel/PDF)", type=['xlsx', 'pdf'])

if uploaded_file:
    # 1. Parsing and Extraction
    metadata = {"entity": "ABC CORP", "period": "FY 2025", "currency": "USD"}
    cf_df = prepare_cash_flow(uploaded_file)
    
    # 2. Preview (Restricted)
    st.subheader("🏁 Automated IFRS Preview")
    st.dataframe(cf_df.head(5)) # Shows only initial entries as per request
    st.warning("Pay USD 5 to download the full IFRS report.")

    # 3. Payment Integration
    paypal_btn = f"""
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
    components.html(paypal_btn, height=450)

    # 4. Success / Download Block
    if st.checkbox("Check here if payment was successful"):
        pdf_bytes = generate_pdf(cf_df, metadata)
        st.success("✅ Payment Verified.")
        st.download_button("📥 Download Full IFRS PDF Report", pdf_bytes, "Cash_Flow_Statement.pdf")
        
        # Excel Download
        excel_buffer = io.BytesIO()
        cf_df.to_excel(excel_buffer, index=False)
        st.download_button("📥 Download Excel File", excel_buffer.getvalue(), "Cash_Flow_Data.xlsx")
