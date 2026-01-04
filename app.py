import streamlit as st
import pandas as pd
import numpy as np
import pdfplumber
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image, ImageDraw, ImageFilter

# --- 1. CONFIGURATION & SECURITY ---
st.set_page_config(page_title="IFRS Cash Flow AI", layout="wide")

# Hide Streamlit UI to protect code
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
    try:
        df = pd.read_excel(file)
        # In a production AI, this would map dynamic headers to standard tags
        return df
    except Exception as e:
        st.error(f"Excel Parsing Error: {e}")
        return None

def parse_pdf(file):
    try:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        # Simulated extraction logic
        return text
    except Exception as e:
        st.error(f"PDF Parsing Error: {e}")
        return None

def prepare_cash_flow(data):
    """
    IFRS (LKAS 7) Indirect Method Classification
    1. Operating Activities (Profit, Depreciation, Working Capital)
    2. Investing Activities (PPE, Investments)
    3. Financing Activities (Loans, Dividends)
    """
    # Placeholder Logic: In real use, this calculates deltas from Opening/Closing Balance Sheets
    cf_data = {
        "Description": [
            "Cash flows from operating activities",
            "  Profit before tax", "  Adjustments for: Depreciation", "  Working Capital Changes",
            "Net cash from operating activities",
            "",
            "Cash flows from investing activities",
            "  Purchase of PPE", "  Proceeds from sale of investments",
            "Net cash used in investing activities",
            "",
            "Cash flows from financing activities",
            "  Proceeds from loans", "  Dividends paid",
            "Net cash from financing activities",
            "",
            "Net increase in cash and cash equivalents"
        ],
        "Amount (USD)": [
            None, 50000.00, 12000.00, -5000.00, 57000.00, 
            None, None, -25000.00, 10000.00, -15000.00, 
            None, None, 20000.00, -10000.00, 10000.00,
            None, 52000.00
        ]
    }
    return pd.DataFrame(cf_data)

def generate_pdf(df, biz_name, period):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Professional IFRS Header
    elements.append(Paragraph(biz_name.upper(), styles['Heading1']))
    elements.append(Paragraph(f"Statement of Cash Flows - {period}", styles['Heading2']))
    elements.append(Paragraph("Prepared under IFRS (Indirect Method)", styles['Italic']))
    elements.append(Spacer(1, 20))

    # Table Formatting
    data = [df.columns.to_list()] + df.values.tolist()
    # Replace None with empty strings for PDF
    data = [[str(item) if item is not None else "" for item in row] for row in data]
    
    t = Table(data, colWidths=[350, 100])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.black),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(t)
    doc.build(elements)
    return buffer.getvalue()

# --- 3. UI & PAYMENT WORKFLOW ---

st.title("IFRS Cash Flow Statement AI")
st.write("Professional Automation for Accountants and Auditors")

with st.sidebar:
    st.image("logo-removebg-preview.png")
    st.header("GDP Consultants")
    st.info("IFRS (LKAS 7) Compliance Tool")
    st.divider()
    st.write("📧 info@taxcalculator.lk")

# File Upload
col1, col2 = st.columns(2)
file = col1.file_uploader("Upload Financial Statements (Excel/PDF)", type=['xlsx', 'pdf'])

if file:
    with st.spinner("Analyzing Financial Data..."):
        # Process data
        if file.name.endswith('xlsx'):
            raw_data = parse_excel(file)
        else:
            raw_data = parse_pdf(file)
            
        cf_df = prepare_cash_flow(raw_data)
        
        # PREVIEW MODE
        st.subheader("🏁 Cash Flow Preview (Watermarked)")
        
        # Blur logic for preview
        preview_df = cf_df.copy()
        preview_df.iloc[1:, 1] = "🔒 [PAY TO VIEW]"
        st.table(preview_df)

        # Payment Section
        st.divider()
        st.warning("💳 Pay **USD 5.00** to download the full audited PDF and Excel report.")
        
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
        st.components.v1.html(paypal_btn, height=500)

        # Download Buttons (Enabled after payment verification)
        # Note: In a live app, use session_state to track payment success from the postMessage
        if st.checkbox("Simulate Payment Success (For Testing)"):
            pdf_bytes = generate_pdf(cf_df, "Sample Entity", "FY 2025")
            
            st.success("✅ Payment Verified!")
            d_col1, d_col2 = st.columns(2)
            d_col1.download_button("📥 Download IFRS PDF", pdf_bytes, "Cash_Flow_Statement.pdf", "application/pdf")
            
            # Excel Download
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                cf_df.to_excel(writer, index=False, sheet_name='Cash Flow')
            d_col2.download_button("📥 Download Excel File", output.getvalue(), "Cash_Flow.xlsx")
