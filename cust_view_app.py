import gradio as gr
from supabase import create_client, Client
import pandas as pd
import requests

# --- 1. CONFIGURATION & ASSETS ---
SUPABASE_URL = "https://gadqrxklkwxtkikrpunj.supabase.co"
SUPABASE_KEY = "sb_publishable_6bXDsSqLmi7ATDnXtm3jQg_DE_aC9AU"
LOGO_URL = "https://github.com/vidushisingh311/mishtee/blob/main/mishTee_logo.png?raw=true"
CSS_URL = "https://raw.githubusercontent.com/vidushisingh311/mishtee/refs/heads/main/style.css"

# Initialize Supabase Client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Fetch Custom CSS from GitHub
try:
    response = requests.get(CSS_URL)
    mishtee_css = response.text if response.status_code == 200 else ""
except Exception:
    mishtee_css = "" # Fallback to default if URL is unreachable

# --- 2. BACKEND FUNCTIONS ---

def get_trending_products():
    """Retrieves top 4 best-selling products based on quantity."""
    try:
        # Fetching from order_items with a join on products
        res = supabase.table("order_items").select(
            "quantity, products(sweet_name, variant_type, base_unit_cost)"
        ).execute()
        
        if not res.data:
            return pd.DataFrame(columns=["Sweet Name", "Variant", "Total Sold", "Price"])

        raw_df = pd.json_normalize(res.data)
        summary = raw_df.groupby(['products.sweet_name', 'products.variant_type']).agg({
            'quantity': 'sum',
            'products.base_unit_cost': 'first'
        }).reset_index()
        
        trending = summary.sort_values(by='quantity', ascending=False).head(4)
        trending.columns = ["Sweet Name", "Variant", "Total Sold", "Price"]
        return trending
    except Exception:
        return pd.DataFrame(columns=["Sweet Name", "Variant", "Total Sold", "Price"])

def login_and_fetch_data(phone_number):
    """Handles user login, greeting, and history retrieval."""
    if not phone_number.strip():
        return "Please enter a valid phone number.", pd.DataFrame(), get_trending_products()

    # 1. Fetch Customer Name
    cust_res = supabase.table("customers").select("customer_name").eq("phone_number", phone_number).execute()
    
    if cust_res.data:
        name = cust_res.data[0]['customer_name']
        greeting = f"### Namaste, {name} ji! \nGreat to see you again."
    else:
        greeting = "### Namaste! \nWelcome to the magic of MishTee."

    # 2. Fetch Order History
    order_res = supabase.table("orders").select(
        "order_id, order_date, total_amount"
    ).eq("phone_number", phone_number).execute()
    
    history_df = pd.DataFrame(order_res.data)
    if not history_df.empty:
        history_df.columns = ["Order ID", "Date", "Total (₹)"]
    else:
        history_df = pd.DataFrame(columns=["Order ID", "Date", "Total (₹)"])

    # 3. Refresh Trending
    trending_df = get_trending_products()

    return greeting, history_df, trending_df

# --- 3. GRADIO UI LAYOUT ---

with gr.Blocks(css=mishtee_css, title="MishTee-Magic") as demo:
    
    # Header Section
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML(f"""
                <div style="display: flex; flex-direction: column; align-items: center; padding: 30px 0;">
                    <img src="{LOGO_URL}" alt="MishTee-Magic" style="max-height: 100px; margin-bottom: 10px;">
                    <p style="font-family: 'Playfair Display', serif; font-size: 1.1rem; color: #C06C5C; letter-spacing: 3px;">
                        PURITY AND HEALTH
                    </p>
                </div>
            """)

    # Personalized Greeting Area
    greeting_output = gr.Markdown(value="### Welcome to MishTee-Magic", elem_id="greeting")

    # Login Section
    with gr.Row():
        with gr.Column(scale=1): pass # Spacer
        with gr.Column(scale=2):
            phone_input = gr.Textbox(
                label="Registered Phone Number", 
                placeholder="e.g. +91 98765 43210",
                lines=1
            )
            login_btn = gr.Button("ACCESS YOUR MAGIC", variant="primary")
        with gr.Column(scale=1): pass # Spacer

    gr.HTML("<div style='margin: 30px 0;'></div>") # Whitespace padding

    # Content Tabs
    with gr.Tabs():
        with gr.TabItem("Trending Today"):
            trending_table = gr.DataFrame(
                value=get_trending_products(),
                interactive=False,
                elem_id="trending_df"
            )
            
        with gr.TabItem("My Order History"):
            history_table = gr.DataFrame(
                headers=["Order ID", "Date", "Total (₹)"],
                interactive=False,
                elem_id="history_df"
            )

    # Event Logic
    login_btn.click(
        fn=login_and_fetch_data,
        inputs=[phone_input],
        outputs=[greeting_output, history_table, trending_table]
    )

if __name__ == "__main__":
    demo.launch()
