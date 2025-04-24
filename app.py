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
            return json.load(file)
    except FileNotFoundError:
        st.error("❌ Product database not found.")
        return {}

# --- Product Check Logic ---
def check_product(product_name, data):
    normalized_input = normalize(product_name)

    # Create mappings for product names and alternative names
    normalized_products = {normalize(p): p for p in data}
    normalized_alternatives = {
        normalize(info['alternative']): name
        for name, info in data.items()
        if "alternative" in info
    }

    # Combine both dictionaries
    combined_keys = {**normalized_products, **normalized_alternatives}

    close_matches = difflib.get_close_matches(normalized_input, combined_keys.keys(), n=1, cutoff=0.6)

    if close_matches:
        matched_key = close_matches[0]
        if matched_key in normalized_products:
            product = normalized_products[matched_key]
            info = data[product]
            if info.get("israeli"):
                return (
                    True,
                    f"⚠️ **'{product.title()}' is an Israeli product!**",
                    f"✅ Try this alternative: **{info.get('alternative', 'N/A')}**"
                )
            else:
                return (
                    False,
                    f"✅ **'{product.title()}' is NOT an Israeli product.**",
                    ""
                )
        elif matched_key in normalized_alternatives:
            alt = matched_key
            main_product = normalized_alternatives[alt]
            return (
                False,
                f"✅ **'{data[main_product]['alternative']}' is NOT an Israeli product.**",
                ""
            )

    return None, f"❌ **'{product_name.title()}' not found in our database.**", ""

# --- Streamlit UI ---
st.set_page_config(page_title="Israeli Product Checker", page_icon="🕵️‍♂️")

st.title("🛍️ Israeli Product Checker")
st.write("Enter a product or alternative name to check if it's Israeli and explore local substitutes.")

# Load product data
products_data = load_data("products.json")

# Input field
product_input = st.text_input("🔍 Product or Alternative Name", "")

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
        <em>Support the Palestinian cause — say no to Israeli products.</em>
    </div>
    """,
    unsafe_allow_html=True
)
