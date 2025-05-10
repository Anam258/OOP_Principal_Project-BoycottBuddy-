import streamlit as st
from checker import ProductDatabase, ProductChecker
import os


class BycottBuddyApp:
    def __init__(self):
        self.db = ProductDatabase("products.json")
        self.checker = ProductChecker(self.db.get_data())

    def load_css(self):
        """Load CSS from an external file and apply it"""
        css_path = os.path.join(os.path.dirname(__file__), "styles.css")
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    def display_header(self):
        st.markdown("<h1>Bycott Buddy 🕵️‍♂️</h1>", unsafe_allow_html=True)
        st.markdown("<h4>Say NO to Israeli Products — Explore Local Alternatives</h4>", unsafe_allow_html=True)
        st.markdown("---")

    def main_interface(self):
        product_input = st.text_input("🔍 Enter a product  name to check if it's Israeli and explore local substitutes.", "")

        if product_input:
            is_israeli, msg, alt = self.checker.check(product_input)
            if is_israeli is None:
                st.warning(msg)
            elif is_israeli:
                st.error(msg)
                st.success(alt)
            else:
                st.success(msg)

        if st.button("Exit"):
            st.info("Thanks for using Bycott Buddy! 🙏")
            st.stop()

    def display_footer(self):
        st.markdown(
            """
            <hr/>
            <footer>
                Made with ❤️ by <strong>Anam Anwer</strong><br>
                <em>Support the Palestinian cause — say no to Israeli products.</em>
            </footer>
            """,
            unsafe_allow_html=True
        )

    def run(self):
        # Call set_page_config() as the first Streamlit command
        st.set_page_config(page_title="Bycott Buddy", page_icon="🛍️")

        self.load_css()  # Load the CSS file
        self.display_header()
        self.main_interface()
        self.display_footer()

# Run the app
if __name__ == "__main__":
    app = BycottBuddyApp()
    app.run()
