import re
import os

files = ['About.html', 'Blog.html', 'Contact.html', 'Homepage.html']

nav_template = """<nav class="navbar navbar-expand-lg bg-white sticky-top shadow-sm">
    <div class="container">
        <a class="navbar-brand fw-bold text-success" href="#">FoodShop</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#mainNavbar">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="mainNavbar">
            <ul class="navbar-nav ms-auto mb-2 mb-lg-0 align-items-lg-center">
                <li class="nav-item"><a class="nav-link{home_active}" href="Homepage.html">Home</a></li>
                <li class="nav-item"><a class="nav-link{products_active}" href="products.html">Food List</a></li>
                <li class="nav-item"><a class="nav-link{blog_active}" href="Blog.html">Blog</a></li>
                <li class="nav-item"><a class="nav-link{about_active}" href="About.html">About Us</a></li>
                <li class="nav-item"><a class="nav-link{contact_active}" href="Contact.html">Contact</a></li>
                <li class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle" href="#" id="cartDropdown" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                        Cart <span id="cartCount" class="badge bg-danger">0</span>
                    </a>
                    <ul class="dropdown-menu dropdown-menu-end p-3 shadow" style="min-width: 320px; max-height: 400px; overflow-y: auto;" id="cartItems">
                        <li id="emptyCart" class="text-center text-muted py-2">Your cart is empty.</li>
                    </ul>
                </li>
            </ul>
            <div class="ms-lg-3 mt-2 mt-lg-0">
                <button class="btn btn-outline-success me-2 btn-sm" data-bs-toggle="modal" data-bs-target="#loginModal">Login</button>
                <button class="btn btn-main btn-sm" data-bs-toggle="modal" data-bs-target="#registerModal">Register</button>
            </div>
        </div>
    </div>
</nav>"""

update_cart_script = """function updateCartUI() {
        const cartItems = document.getElementById("cartItems");
        const cartCount = document.getElementById("cartCount");
        if (!cartItems || !cartCount) return;
        cartItems.innerHTML = "";

        if(cart.length === 0){
            cartItems.innerHTML = '<li id="emptyCart" class="text-center text-muted py-2">Your cart is empty.</li>';
            cartCount.textContent = 0;
            sessionStorage.setItem('cart', JSON.stringify(cart));
            return;
        }

        cart.forEach((item, index) => {
            const li = document.createElement("li");
            li.className = "mb-2 d-flex justify-content-between align-items-center border-bottom pb-2";
            li.innerHTML = `
                <div>
                    <span class="fw-bold text-dark">${item.name}</span><br>
                    <span class="text-muted small">${item.price} × ${item.qty}</span>
                </div>
                <button class="btn btn-sm btn-danger remove-item" data-index="${index}">Remove</button>
            `;
            cartItems.appendChild(li);
        });

        const checkoutLi = document.createElement("li");
        checkoutLi.className = "mt-3 text-center";
        checkoutLi.innerHTML = `<a href="cart.html" class="btn btn-success w-100">View Cart & Checkout</a>`;
        cartItems.appendChild(checkoutLi);

        cartCount.textContent = cart.reduce((sum, i) => sum + i.qty, 0);
        sessionStorage.setItem('cart', JSON.stringify(cart));

        document.querySelectorAll(".remove-item").forEach(btn => {
            btn.addEventListener("click", (e) => {
                e.stopPropagation();
                const idx = btn.dataset.index;
                cart.splice(idx, 1);
                updateCartUI();
            });
        });
    }"""

for file in files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    home_active = ' active text-success fw-semibold' if file == 'Homepage.html' else ''
    products_active = ' active text-success fw-semibold' if file == 'products.html' else ''
    blog_active = ' active text-success fw-semibold' if file == 'Blog.html' else ''
    about_active = ' active text-success fw-semibold' if file == 'About.html' else ''
    contact_active = ' active text-success fw-semibold' if file == 'Contact.html' else ''

    nav_new = nav_template.format(
        home_active=home_active,
        products_active=products_active,
        blog_active=blog_active,
        about_active=about_active,
        contact_active=contact_active
    )

    # replace nav
    content = re.sub(r'<nav class="navbar.*?</nav>', nav_new, content, flags=re.DOTALL)
    
    # replace updateCartUI
    content = re.sub(r'function updateCartUI\(\) \{.*?\n    \}', update_cart_script, content, flags=re.DOTALL)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Updated {file}')
