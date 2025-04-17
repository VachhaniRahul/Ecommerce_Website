<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
</head>
<body>
    <h1>eCommerce Website</h1>
    <h2>Description</h2>
    <p>
        The <strong>eCommerce Website</strong> is a Django-based web application that allows users to browse products, add them to their shopping cart, and complete their purchase through a secure checkout process. Customers can manage their accounts, view their order history, and make payments online. Sellers can upload and manage products in their online store.
    </p>
    <h2>Features</h2>
    <ul>
        <li><strong>Browse Products:</strong> Explore a variety of products available for purchase.</li>
        <li><strong>Product Search:</strong> Easily search for products by categories or keywords.</li>
        <li><strong>Add to Cart:</strong> Add items to your shopping cart and view the total price.</li>
        <li><strong>Checkout:</strong> Complete your purchase with secure payment options.</li>
        <li><strong>Order History:</strong> View your past orders and track delivery status.</li>
        <li><strong>Admin Panel:</strong> Sellers can manage products, orders, and customers.</li>
    </ul>
    <h2>Tech Stack</h2>
    <ul>
        <li><strong>Backend:</strong> Django, Django Rest Framework (DRF)</li>
        <li><strong>Frontend:</strong> HTML, CSS, JavaScript (React.js, optional for frontend)</li>
        <li><strong>Database:</strong> PostgreSQL (or SQLite for development)</li>
        <li><strong>Payment Gateway:</strong> Stripe or PayPal (optional integration)</li>
    </ul>
    <h2>Requirements</h2>
    <p>To run this project locally, make sure you have the following installed:</p>
    <ul>
        <li>Python 3.x</li>
        <li>Django 5.x</li>
        <li>PostgreSQL (if used) or SQLite</li>
    </ul>
    <h2>Installation</h2>
    <ol>
        <li>Clone the repository:
            <pre><code>git clone https://github.com/yourusername/ecommerce-website.git</code></pre>
        </li>
        <li>Navigate to the project directory:
            <pre><code>cd ecommerce-website</code></pre>
        </li>
        <li>Create a virtual environment:
            <pre><code>python -m venv venv</code></pre>
        </li>
        <li>Activate the virtual environment:
            <ul>
                <li>On Windows:
                    <pre><code>.\venv\Scripts\Activate.ps1</code></pre>
                </li>
                <li>On macOS/Linux:
                    <pre><code>source venv/bin/activate</code></pre>
                </li>
            </ul>
        </li>
        <li>Install the required dependencies:
            <pre><code>pip install -r requirements.txt</code></pre>
        </li>
        <li>Set up the database:
            <pre><code>python manage.py migrate</code></pre>
        </li>
        <li>Create a superuser (for the admin panel):
            <pre><code>python manage.py createsuperuser</code></pre>
        </li>
        <li>Start the development server:
            <pre><code>python manage.py runserver</code></pre>
        </li>
        <li>Open your browser and go to:
            <pre><code>http://127.0.0.1:8000/</code></pre>
        </li>
    </ol>
    <h2>Usage</h2>
    <h3>Browsing Products</h3>
    <ul>
        <li>Click on the "Browse Products" link to see all available products.</li>
    </ul>
    <h3>Product Search</h3>
    <ul>
        <li>Use the search bar to find specific products by name, category, or brand.</li>
    </ul>
    <h3>Adding to Cart</h3>
    <ul>
        <li>Click on "Add to Cart" to add an item to your shopping cart.</li>
        <li>View the cart by clicking on the "Cart" icon in the header.</li>
    </ul>
    <h3>Checkout</h3>
    <ul>
        <li>Proceed to checkout by clicking on "Checkout" in the cart.</li>
        <li>Enter your shipping information and payment details to complete the purchase.</li>
    </ul>
    <h3>Admin Panel</h3>
    <ul>
        <li>Admins can log in to the admin panel to manage products, orders, and users.</li>
        <li>To access the admin panel, navigate to <strong>http://127.0.0.1:8000/admin/</strong>.</li>
    </ul>

</body>
</html>
