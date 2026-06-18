import re

files = [
    r"c:\Users\mrtin\OneDrive\Documents\GitHub\FoodShop\Homepage.html",
    r"c:\Users\mrtin\OneDrive\Documents\GitHub\FoodShop\products.html",
    r"c:\Users\mrtin\OneDrive\Documents\GitHub\FoodShop\Blog.html",
    r"c:\Users\mrtin\OneDrive\Documents\GitHub\FoodShop\About.html",
    r"c:\Users\mrtin\OneDrive\Documents\GitHub\FoodShop\Contact.html"
]

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add id="cartNavItem" to the Cart link
    # Look for: <li class="nav-item"> ... <a class="nav-link" href="cart.html"> or <a class="nav-link active..." href="cart.html">
    # Note: Homepage has <li class="nav-item">\n <a class="nav-link" href="cart.html">
    content = re.sub(
        r'<li class="nav-item">\s*<a class="nav-link([^"]*)" href="cart\.html">',
        r'<li class="nav-item" id="cartNavItem">\n                        <a class="nav-link\1" href="cart.html">',
        content
    )

    # 2. Update updateAuthUI
    # First, add cartNavItem to the top
    content = content.replace(
        'const authSection = document.getElementById("authSection");\n',
        'const authSection = document.getElementById("authSection");\n            const cartNavItem = document.getElementById("cartNavItem");\n'
    )
    
    # Second, hide it if admin/owner
    content = content.replace(
        "dashboardLink = `<a href=\"${user.role === 'OWNER' ? 'Owner.html' : 'Admin.html'}\" class=\"btn btn-outline-success btn-sm me-3\">Dashboard</a>`;\n                }",
        "dashboardLink = `<a href=\"${user.role === 'OWNER' ? 'Owner.html' : 'Admin.html'}\" class=\"btn btn-outline-success btn-sm me-3\">Dashboard</a>`;\n                    if (cartNavItem) cartNavItem.style.display = 'none';\n                } else {\n                    if (cartNavItem) cartNavItem.style.display = 'block';\n                }"
    )

    # Third, show it if logged out
    content = re.sub(
        r'\} else \{\n(\s*)authSection\.innerHTML',
        r'} else {\n\1if (cartNavItem) cartNavItem.style.display = \'block\';\n\1authSection.innerHTML',
        content
    )

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print("Updated 5 html files")
