import streamlit as st
import json
import difflib

# --- Normalize text ---
def normalize(text):
    return text.lower().replace(" ", "").replace("-", "")

# --- Load Product Data ---
def load_data(json_path):
    try:
        with open(json_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        st.error("❌ Product database not found.")
        return {}

# --- Product Check Logic with fuzzy match ---
def check_product(product_name, data):
    normalized_input = normalize(product_name)

    normalized_db = {normalize(key): key for key in data.keys()}
    close_matches = difflib.get_close_matches(normalized_input, normalized_db.keys(), n=1, cutoff=0.6)

    if close_matches:
        matched_key = normalized_db[close_matches[0]]
        info = data[matched_key]

        if info.get("israeli"):
            return (
                True,
                f"⚠️ **'{matched_key.title()}' is an Israeli product!**",
                f"✅ Try this alternative: **{info.get('alternative', 'N/A')}**"
            )
        else:
            return (
                False,
                f"✅ **'{matched_key.title()}' is NOT an Israeli product.**",
                ""
            )
    else:
        return None, f"❌ **'{product_name.title()}' not found in our database.**", ""

# --- Streamlit UI ---
st.set_page_config(page_title="Israeli Product Checker", page_icon="🕵️‍♂️")

st.title("🛍️ Israeli Product Checker")
st.write("Enter a product name below to check if it's Israeli and find its alternative.")

# Load product data
products_data = load_data("products.json")

# User input
product_input = st.text_input("🔍 Product Name", "")

if product_input:
    is_israeli, msg, alt = check_product(product_input, products_data)
    if is_israeli is None:
        st.warning(msg)
    elif is_israeli:
        st.error(msg)
        st.success(alt)
    else:
        st.success(msg)

# Exit Button
if st.button("🚪 Exit"):
    st.info("Thanks for using Israeli Product Checker!")
    st.stop()

# --- Footer ---
st.markdown(
    """
    <hr style="margin-top: 30px;"/>
    <div style="text-align: center; font-size: 14px; color: gray;">
        Made with ❤️ by <strong>Anam Anwer</strong><br>
        <em>Support Palestinian cause by boycotting Israeli products.</em>
    </div>
    """,
    unsafe_allow_html=True
)
