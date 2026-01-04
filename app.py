import streamlit as st
import pandas as pd
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFont
import streamlit.components.v1 as components
import io

# --- 1. CONFIGURATION & BRANDING ---
st.set_page_config(page_title="IFRS Cash Flow AI", layout="wide", page_icon="📈")

# Security: Hide developer menus to protect code
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    .main {background-color: #f8fafc;}
    </style>
    """, unsafe_allow_html=True)

# --- 2. IFRS CASH FLOW LOGIC ---
def generate_preview_image(data):
    """Generates a professional IFRS formatted image preview with watermark"""
    img = Image.new('RGB', (1000, 1400), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    
    # Header - Corporate Blue
    d.rectangle([0, 0, 1000, 120], fill="#1E3A8A")
    d.text((50, 40), f"{data['biz_name']} - Statement of Cash Flows (IFRS)", fill="white")
    
    y = 150
    d.text((50, y), f"Period Ended: {data['period']}", fill="black")
    
    # Section: Operating Activities
    y += 80
    d.rectangle([0, y, 1000, y+40], fill="#E5E7EB")
    d.text((50, y+10), "Cash Flows from Operating Activities (Indirect Method)", fill="black")
    y += 60
    d.text((70, y), "Net Profit Before Tax", fill="black"); d.text((850, y), f"{data['net_profit']:,.2f}", fill="black")
    y += 40
    d.text((70, y), "Adjustments for: Depreciation & Amortization", fill="gray"); d.text((850, y), f"{data['depreciation']:,.2f}", fill="black")
    
    # Section: Investing Activities
    y += 100
    d.rectangle([0, y, 1000, y+40], fill="#E5E7EB")
    d.text((50, y+10), "Cash Flows from Investing Activities", fill="black")
    y += 60
    d.text((70, y), "Purchase of Property, Plant & Equipment", fill="gray"); d.text((850, y), f"({data['ppe_purchase']:,.2f})", fill="black")
    
    # Section: Financing Activities
    y += 100
    d.rectangle([0, y, 1000, y+40], fill="#E5E7EB")
    d.text((50, y+10), "Cash Flows from Financing Activities", fill="black")
    
    # Total Cash Movement
    y += 150
    d.rectangle([0, y, 1000, y+50], fill="#1E3A8A")
    d.text((50, y+15), "Net Increase/Decrease in Cash", fill="white")
    d.text((850, y+15), f"{data['net_increase']:,.2f}", fill="white")

    # Watermark
    d.text((250, 700), "PREVIEW ONLY - PAY USD 5 TO DOWNLOAD", fill=(200, 200, 200))
    return img

# --- 3. UI WORKFLOW ---
with st.sidebar:
    try: st.image("logo-removebg-preview.png")
    except: st.info("Place logo file in root directory.")
    st.header("GDP Consultants")
    st.write("IFRS Automation Suite")
    st.divider()
    st.write("📧 info@taxcalculator.lk")

st.title("IFRS Cash Flow Statement AI")
st.write("Upload your Balance Sheet and P&L to generate a professional Cash Flow Statement.")

# Step 1: Upload
uploaded_file = st.file_uploader("Upload Opening Balance Sheet / Trial Balance (Excel/PDF)", type=['xlsx', 'csv', 'pdf'])

if uploaded_file:
    # 1. Processing Logic (Simulation of AI extraction)
    # In a real scenario, you would use pandas or a PDF extractor here
    report_data = {
        "biz_name": "CORPORATE CLIENT LTD",
        "period": "Financial Year 2025",
        "net_profit": 500000.00,
        "depreciation": 45000.00,
        "ppe_purchase": 120000.00,
        "net_increase": 425000.00
    }

    # Step 2: Preview
    st.subheader("🏁 Automated IFRS Preview")
    preview = generate_preview_image(report_data)
    st.image(preview, use_container_width=True)

    # Step 3: Payment
    st.divider()
    st.warning("💳 **Secure Payment Required:** Pay USD 5 to download the full PDF and Excel report.")
    
    paypal_html = f"""
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
    components.html(paypal_html, height=500)
