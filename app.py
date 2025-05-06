import streamlit as st
from checker import ProductDatabase, ProductChecker

class BycottBuddyApp:
    def __init__(self):
        self.db = ProductDatabase("products.json")
        self.checker = ProductChecker(self.db.get_data())

    def run(self):
        st.set_page_config(page_title="Bycott Buddy", page_icon="🛍️", layout="centered")

        # --- Clean Professional Styling ---
        st.markdown("""
            <style>
            body {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', sans-serif;
            }
            .main-title {
                font-size: 2.5rem;
                font-weight: 700;
                color: #222;
                text-align: center;
                margin-top: 40px;
                margin-bottom: 10px;
            }
            .subtitle {
                font-size: 1rem;
                color: #555;
                text-align: center;
                margin-bottom: 30px;
            }
            .stTextInput input {
                font-size: 1rem;
                padding: 10px;
            }
            .stButton > button {
                background-color: #007bff;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-size: 1rem;
                margin-top: 10px;
            }
            .footer {
                text-align: center;
                font-size: 0.9rem;
                color: #777;
                margin-top: 40px;
            }
            </style>
        """, unsafe_allow_html=True)

        # --- UI Layout ---
        st.markdown("<div class='main-title'>Bycott Buddy 🛍️</div>", unsafe_allow_html=True)
        st.markdown("<div class='subtitle'> 🔎 Check if a product is Israeli and explore alternatives</div>", unsafe_allow_html=True)

        product_input = st.text_input("Enter Product Name 👇")

        if product_input:
            is_israeli, msg, alt = self.checker.check(product_input)

            if is_israeli is None:
                st.warning(msg)
            elif is_israeli:
                st.error(msg)
                if alt:
                    st.success(alt)
            else:
                st.success(msg)

        if st.button("Exit"):
            st.info("Thanks for using Bycott Buddy!")
            st.stop()

        st.markdown("<div class='footer'>Made with ❤️ by <b>Anam Anwer</b><br>Support the Palestinian cause.</div>", unsafe_allow_html=True)

# --- Run the app ---
if __name__ == "__main__":
    app = BycottBuddyApp()
    app.run()
