import sys
import os
from streamlit_folium import st_folium
import folium


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from streamlit.runtime.scriptrunner import RerunException

from scripts.crud_books import get_books_by_category
from scripts.crud_books import get_all_books
from scripts.crud_categories import get_all_categories
from scripts.crud_customers import get_all_customers
from scripts.crud_orders import get_orders_by_user, get_order_details
from scripts.integration_books import get_book_with_category
from scripts.integration_profile_location import get_full_user_profile
from scripts.integration_profile_location import create_user_with_profile
from scripts.integration_orders import create_order_with_details
from scripts.integration_browsing import log_and_get_book
from scripts.crud_books import get_book_by_id
from scripts.integration_reviews import get_books_to_review, submit_review
from scripts.integration_books import get_book_with_category
from scripts.integration_reviews import get_review_stats
from scripts.integration_profile_location import get_all_customer_locations
from scripts.integration_profile_location import get_rating_customer_locations
from scripts.integration_profile_location import get_users_near_location
from scripts.crud_customer_profiles import get_all_states


# --- Secure Login for Local and Deployment ---

# Try loading .env if running locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception as e:
    pass  # If dotenv not installed, ignore

# Load username and password
USERNAME = st.secrets.get("USERNAME", os.getenv("USERNAME"))
PASSWORD = st.secrets.get("PASSWORD", os.getenv("PASSWORD"))

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Show login form if not logged in
if not st.session_state.logged_in:
    st.title("Secure Login Required")

    username_input = st.text_input("Username")
    password_input = st.text_input("Password", type="password")
    login_button = st.button("Login")

    if login_button:
        if username_input == USERNAME and password_input == PASSWORD:
            st.success("Login successful. Welcome!")
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Invalid credentials. Please try again.")

    st.stop()  # Stop the app until logged in

else:
    st.sidebar.success(f"Logged in as: {USERNAME}")


# Step 1: Role
role = st.sidebar.selectbox("Login As:", ["Guest", "Customer", "Admin"])
st.session_state["user_type"] = role

# Step 2: Customer user selection (only if Customer)
if role == "Customer":
    customers = get_all_customers()
    user_options = {f"{c[1]}": c[0] for c in customers}
    user_labels = list(user_options.keys())

    default_label = st.session_state.get("selected_user_label")
    if default_label not in user_labels:
        default_label = user_labels[0]

    selected_user_label = st.sidebar.selectbox("Select Profile", user_labels, index=user_labels.index(default_label))
    st.session_state["selected_user_label"] = selected_user_label
    st.session_state["user_id"] = user_options[selected_user_label]

# Step 3: Role-based page options
if role == "Admin":
    page_options = ["Home", "Customer Management", "Dashboards", "Reports"]
elif role == "Customer":
    page_options = ["Home", "Browse Books", "Place Order", "My Orders", "Recommendations", "Submit Review", "My Reviews"]
else:  # Guest
    page_options = ["Home", "Browse Books", "Place Order"]

# Step 4: Read current page from query params (or default to Home)
default_page = st.query_params.get("Home")
if default_page not in page_options:
    default_page = "Home"

# Step 5: Show navigation with remembered state
page = st.sidebar.radio("Go to", page_options, index=page_options.index(default_page))


if page == "Home":
    

    # --- GUEST ---
    if role == "Guest":
        st.subheader("📚 Welcome to the Hybrid Bookstore!")
        st.info("You're browsing as a guest. You can explore our books and place an order.")
        st.markdown("Want to place an order? Just add books from the *Browse Books* page and head to *Place Order*.")

       
            

    # --- CUSTOMER ---
    elif role == "Customer":
        
        user_id = st.session_state.get("user_id")
        profile = get_full_user_profile(user_id)

        if profile:
            st.subheader(f"Welcome to the Hybrid Bookstore, **{profile['name']}**!!")
            

            # Profile snapshot
            st.write("📌 Your Profile")
            st.write(f"**Name:** {profile['name']}")
            st.write(f"**Email:** {profile['email']}")
            st.write(f"**Preferred Categories:** {', '.join(profile['preferred_categories']) or 'None'}")
            st.write(f"**Avarage Rating Given:** {profile['avg_rating_given']}")
            addr = profile["address"]
            st.write("**Address:**", f"{addr.get('street')}, {addr.get('city')}, {addr.get('state')} {addr.get('zip')}, {addr.get('country')}")

            

    # --- ADMIN ---
    elif role == "Admin":
        st.success("You're logged in as an administrator.")
        
        col1, col2 = st.columns(2)
        col1.subheader("CUSTOMER STATS:")
        col1.metric("👥 Total Customers", len(get_all_customers()))
        col1.metric("🗺️ States Covered", len(get_all_states()))
        col2.subheader("BOOK STATS:")
        col2.metric("🗂️ Total Book Categorues", len(get_all_categories()))
        col2.metric("📚 Total Books", len(get_all_books()))

        st.markdown("Note: Use the sidebar to manage users, view dashboards, or access reports.")
        

# --- BROWSE BOOKS ---
elif page == "Browse Books":
    st.subheader("Browse Books by Category")

    # Check selected_books exists
    if "selected_books" not in st.session_state:
        st.session_state.selected_books = set()

    # Step 1: Category dropdown
    categories = get_all_categories()
    category_options = {cat[1]: cat[0] for cat in categories}
    selected_name = st.selectbox("Select a category", list(category_options.keys()))

    if selected_name:
        selected_id = category_options[selected_name]
        books = get_books_by_category(selected_id)

        if books:
            st.markdown("### Select books to add to your order:")

            # Load review stats once
            review_stats = get_review_stats()

            for book in books:
                book_id = book[0]
                viewed_key = f"viewed_{book_id}"
                book_data = get_book_by_id(book_id)

                if book_data:
                    with st.expander(f"{book_data[1]}", expanded=False):
                        # 🔹 Pull stats if available
                        stats = review_stats.get(book_id, {"count": 0, "avg_rating": "N/A"})
                        show_details = st.checkbox("Show full details", key=f"details_{book_id}")

                        if show_details and role == "Customer" and not st.session_state.get(viewed_key):
                            user_id = st.session_state.get("user_id")
                            if user_id:
                                log_and_get_book(user_id, book_id)
                                st.session_state[viewed_key] = True
                        
                        if show_details:
                            st.write(f"**Book ID:** {book_data[0]}")
                            st.write(f"**Category ID:** {book_data[2]}")
                            st.write(f"**Rating:** {stats['avg_rating']} ⭐ ({stats['count']} reviews)")
                            st.write(f"**Price:** ${book_data[4]:.2f}")
                            st.write(f"**Status:** {book_data[5]}")
                            st.write(f"**In Stock:** {book_data[6]}")


                        selected = st.checkbox("Add to order", key=f"select_{book_id}")
                        if selected:
                            st.session_state.selected_books.add(book_id)
                        else:
                            st.session_state.selected_books.discard(book_id)
                else:
                    st.warning(f"Book {book_id} not found.")
        else:
            st.info("No books found in this category.")

# --- MY ORDERS ---
elif page == "My Orders" and role == "Customer":
    user_id = st.session_state.get("user_id")
    st.subheader("Your Past Orders")

    if not user_id:
        st.info("Please select a user in the Home page to view past orders.")
    else:
        orders = get_orders_by_user(user_id)
        if not orders:
            st.warning("No orders found for this user.")
        else:
            for order in orders:
                order_id, _, order_date, total_amount, total_items = order
                with st.expander(f"Order {order_id} — {order_date}"):
                    st.write(f"**Total Items:** {total_items}")
                    st.write(f"**Total Amount:** ${total_amount:.2f}")
                    details = get_order_details(order_id)
                    for _, book_id, qty, unit_price in details:
                        book = get_book_with_category(book_id)
                        title = book["title"] if book else book_id
                        category = book["category_name"] if book else "Unknown"
                        st.markdown(f"- **{title}** ({category}) — {qty} × ${unit_price:.2f}")
# --- Place Order ---
elif page == "Place Order":
    st.subheader("Place an Order")

    selected = list(st.session_state.get("selected_books", []))
    if not selected:
        st.warning("You haven't selected any books yet.")
        st.stop()

    order_details = {}

    # --- Guest Workflow ---
    if role == "Guest":
        with st.form("guest_order_form"):
            st.markdown("**Enter your details**")
            name = st.text_input("Name")
            email = st.text_input("Email")
            street = st.text_input("Street")
            city = st.text_input("City")
            state = st.text_input("State")
            zip_code = st.text_input("ZIP")
            country = st.text_input("Country")

            st.markdown("---")
            st.markdown("**Selected Books & Quantities**")
            for book_id in selected:
                book = get_book_with_category(book_id)
                if book:
                    qty = st.number_input(f"{book['title']} — Quantity", min_value=1, value=1, key=f"qty_{book_id}")
                    order_details[book_id] = qty

            submitted = st.form_submit_button("Place Order")

        if submitted:
            if not name or not email:
                st.error("Please fill in both name and email.")
            else:
                user_data = {"name": name, "email": email}
                profile_template = {
                    "preferred_categories": [],
                    "avg_rating_given": 0.0,
                    "address": {
                        "street": street,
                        "city": city,
                        "state": state,
                        "zip": zip_code,
                        "country": country
                    }
                }
                profile_result = create_user_with_profile(user_data, profile_template)
                user_id = profile_result["user_id"]

                books_to_order = [{"book_id": b_id, "quantity": qty} for b_id, qty in order_details.items()]
                order_result = create_order_with_details(user_id, books_to_order)
                st.success(f"Order {order_result['order_id']} placed successfully!")
                st.session_state.selected_books.clear()

    # --- Customer Workflow ---
    elif role == "Customer":
        user_id = st.session_state.get("user_id")
        if not user_id:
            st.error("No customer selected. Please go to Home and select a profile.")
            st.stop()

        st.markdown("**Selected Books & Quantities**")
        for book_id in selected:
            book = get_book_with_category(book_id)
            if book:
                qty = st.number_input(f"{book['title']} — Quantity", min_value=1, value=1, key=f"qty_{book_id}")
                order_details[book_id] = qty

        if st.button("Place Order"):
            books_to_order = [{"book_id": b_id, "quantity": qty} for b_id, qty in order_details.items()]
            order_result = create_order_with_details(user_id, books_to_order)
            st.success(f"Order {order_result['order_id']} placed successfully!")
            st.session_state.selected_books.clear()

# --- RECOMMENDATIONS ---
elif page == "Recommendations" and role == "Customer":
    st.subheader("📚 Recommended for You")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please select a user first.")
    else:
        from scripts.integration_recommendations import generate_recommendations
        from scripts.crud_recommendations import get_recommendations_by_user
        from scripts.integration_books import get_book_with_category

        # --- Cache Recommendations ---
        if "cached_recommendations" not in st.session_state:
            st.session_state.cached_recommendations = {}

        if user_id not in st.session_state.cached_recommendations:
            generate_recommendations(user_id)
            st.session_state.cached_recommendations[user_id] = get_recommendations_by_user(user_id)

        rec_data = st.session_state.cached_recommendations[user_id]

        if rec_data and rec_data.get("recommended_books"):
            # Ensure selected_books exists
            if "selected_books" not in st.session_state:
                st.session_state.selected_books = set()

            # Group books by category
            books_by_category = {}
            for book_id in rec_data["recommended_books"]:
                book = get_book_with_category(book_id)
                if book:
                    category = book["category_name"]
                    books_by_category.setdefault(category, []).append(book)

            # Display per category
            for category, books in books_by_category.items():
                st.markdown(f"### 📘 Category: {category}")
                for book in books:
                    with st.expander(f"{book['title']}"):
                        st.write(f"**Rating:** {book['star_rating']} ⭐")
                        st.write(f"**Price:** ${book['price']:.2f}")
                        st.write(f"**Status:** {book['status']}")
                        st.write(f"**In Stock:** {book['quantity']}")

                        selected = st.checkbox("Add to order", key=f"select_rec_{book['book_id']}")
                        if selected:
                            st.session_state.selected_books.add(book["book_id"])
                        else:
                            st.session_state.selected_books.discard(book["book_id"])
        else:
            st.info("No recommendations yet. Try placing an order or submitting reviews.")



# --- REVIEW ---
elif page == "Submit Review" and role == "Customer":
    
    user_id = st.session_state.get("user_id")
    st.subheader("Leave a Review")

    if not user_id:
        st.warning("Please select a user first.")
        st.stop()

    # Step 1: Get reviewable books
    reviewable_books = get_books_to_review(user_id)

    if not reviewable_books:
        st.info("You have no books left to review. Try ordering more books!")
        st.stop()

    # Step 2: Select a book
    book_titles = {}
    for b_id in reviewable_books:
        book = get_book_with_category(b_id)
        if book:
            book_titles[f"{book['title']} ({b_id})"] = b_id

    selected_book_label = st.selectbox("Select a book to review", list(book_titles.keys()))
    selected_book_id = book_titles[selected_book_label]

    # Step 3: Review form
    with st.form("submit_review_form"):
        rating = st.slider("Rating (1 to 5)", 1, 5, 4)
        review_text = st.text_area("Write your review")
        submitted = st.form_submit_button("Submit Review")

    # Step 4: Submit
    if submitted:
        result = submit_review(user_id, selected_book_id, rating, review_text)
        if result["status"] == "submitted":
            st.success("Your review has been submitted!")
        else:
            st.error("Something went wrong. Please try again.")

# --- MY REVIEWS PAGE ---
elif page == "My Reviews" and role == "Customer":
    st.subheader("📝 Your Reviews")

    user_id = st.session_state.get("user_id")
    if not user_id:
        st.warning("Please select a user first.")
        st.stop()

    from scripts.integration_reviews import get_reviews_by_user
    from scripts.integration_books import get_book_with_category

    reviews = get_reviews_by_user(user_id)

    if not reviews:
        st.info("You haven't written any reviews yet!")
    else:
        for review in reviews:
            book = get_book_with_category(review["book_id"])
            book_title = book["title"] if book else f"Book ID {review['book_id']}"

            with st.expander(f"📖 {book_title}"):
                st.write(f"**Rating:** {review['rating']} ⭐")
                st.write(f"**Review Text:** {review['review_text']}")
                st.write(f"**Date:** {review['timestamp'][:10]}")  # show only YYYY-MM-DD

# --- Dashboards ---
elif page == "Dashboards" and role == "Admin":
    st.subheader("Customer Maps")
    hq_coords = {
        "Headquarters": [-86.148003, 39.791000],  # [longitude, latitude]
    }

    # Step 1: Select Map Type
    map_option = st.selectbox("Choose map view:", [
        "All Customers",
        "Top-Rated Customers (>= 4.0)",
        "Low-Rated Customers (< 4.0)",
        "Nearby Customers"
    ])

    # Step 2: Additional filters for Nearby Customers
    if map_option == "Nearby Customers":
        selected_location = "Headquarters"
        coords = hq_coords[selected_location]

        st.markdown(f"**Reference Location:** {selected_location} ({coords[1]:.6f}, {coords[0]:.6f})")

        max_km = st.slider("Select search radius (in km):", min_value=10, max_value=1000, value=100)

    # Step 3: Load data based on selection
    if map_option == "All Customers":
        data = get_all_customer_locations()
    elif map_option == "Top-Rated Customers (>= 4.0)":
        data = get_rating_customer_locations(min_rating=4.0)
    elif map_option == "Low-Rated Customers (< 4.0)":
        data = get_rating_customer_locations(max_rating=4.0)
    elif map_option == "Nearby Customers":
        center = coords
        data = get_users_near_location(center, max_km)
    else:
        data = []

    # 🛑 Step 4 must stay inside the "elif page == Dashboards" block!
    if not data:
        st.warning("No location data found for the selected view.")
    else:
        map_center = [data[0]["lat"], data[0]["lon"]] if data else [39.8283, -98.5795]
        m = folium.Map(location=map_center, zoom_start=3)

        # Add HQ pin
        if map_option == "Nearby Customers":
            folium.Marker(
                location=[coords[1], coords[0]],
                popup="📍 Headquarters",
                icon=folium.Icon(color="red", icon="home")
            ).add_to(m)

        # Add customer pins
        for entry in data:
            popup = f"{entry['name']} ({entry['email']})"
            folium.Marker([entry["lat"], entry["lon"]], popup=popup).add_to(m)

        # Show map
        st_folium(m, width=700, height=500)
