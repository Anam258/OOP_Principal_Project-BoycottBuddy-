import json
import difflib

# --- Utility Base Class (for Inheritance + Abstraction) ---
class BaseNormalizer:
    def normalize(self, text):
        return text.lower().replace(" ", "").replace("-", "")

# --- Encapsulation: ProductDatabase (inherits BaseNormalizer) ---
class ProductDatabase(BaseNormalizer):
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self._load_data()

    def _load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def get_data(self):
        return self.data

# --- Abstraction + Polymorphism + Inheritance: ProductChecker ---
class ProductChecker(BaseNormalizer):
    def __init__(self, data):
        self.data = data
        self.normalized_products = {self.normalize(p): p for p in data}
        self.normalized_alternatives = {
            self.normalize(info['alternative']): name
            for name, info in data.items()
            if "alternative" in info
        }
        self.combined_keys = {**self.normalized_products, **self.normalized_alternatives}

    def check(self, product_name):
        normalized_input = self.normalize(product_name)
        close_matches = difflib.get_close_matches(normalized_input, self.combined_keys.keys(), n=1, cutoff=0.6)

        if close_matches:
            matched_key = close_matches[0]

            if matched_key in self.normalized_products:
                product = self.normalized_products[matched_key]
                info = self.data[product]
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

            elif matched_key in self.normalized_alternatives:
                alt = matched_key
                main_product = self.normalized_alternatives[alt]
                return (
                    False,
                    f"✅ **'{self.data[main_product]['alternative']}' is NOT an Israeli product.**",
                    ""
                )

        return None, f"❌ **'{product_name.title()}' not found in our database.**", ""
