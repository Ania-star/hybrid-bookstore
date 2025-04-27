# 📚 Hybrid Bookstore Database System

A hybrid bookstore system that combines the strengths of relational (SQL) and non-relational (MongoDB) databases.  
Users can browse, order, and review books — while admins monitor customer locations and activities through dashboards.  
Built using **Streamlit** for a lightweight, interactive web interface.

---

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Folder Structure](#folder-structure)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)
- [Authors](#authors)
- [License](#license)

---

## Features
- Guest browsing and book ordering without account
- Customer accounts with profile management, browsing, ordering, and reviewing
- Dynamic recommendations based on user behavior
- Admin dashboards with geolocation-based customer insights
- MongoDB geospatial queries to find nearby customers
- SQL database for core bookstore management (Books, Customers, Orders)
- NoSQL database for dynamic user data (Reviews, Browsing History, Recommendations, Profiles)

---

## Tech Stack
- **Frontend:** Streamlit
- **Relational Database:** SQLite
- **NoSQL Database:** MongoDB Atlas
- **Backend Scripting:** Python (Pandas, PyMongo, SQLite3, etc.)
- **Geolocation:** Google Maps API, MongoDB 2dsphere index
- **Visualization:** Folium (maps)

---

## Folder Structure
```bash
hybrid-bookstore/
|
|├── app/                         # Streamlit frontend application
|   └── main.py                  # Main user interface and page logic
|
|├── db/                          # Databases and supporting setup
|   |
|   ├── mongo/
|   |   └── indexes.py            # MongoDB index creation script
|   |
|   └── sql/
|       ├── hybrid_bookstore.db   # SQLite database file (generated)
|       └── schema.sql            # SQL schema for tables
|
|├── scripts/                     # Backend logic
|   ├── CRUD operations           # (e.g., books, orders, customers)
|   ├── Integration scripts       # Link SQL and MongoDB data
|   └── Data loaders              # Scripts to load CSV/JSON into databases
|
|├── data/                         # Initial datasets
|   ├── books.csv
|   ├── categories.csv
|   ├── customers.csv
|   ├── orders.csv
|   ├── order_details.csv
|   ├── browsing_history.json
|   ├── customer_profiles.json
|   ├── recommendations.json
|   └── reviews.json
|
|├── .env                          # Environment variables (MongoDB URI, API keys) - NOT versioned
|├── .gitignore                    # Files/folders to ignore in version control
|├── requirements.txt              # Python dependency list
└── README.md                     # Project documentation (this file)
```

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/hybrid-bookstore.git
cd hybrid-bookstore
```

### 2. Set up the environment
```bash
pip install -r requirements.txt
```

Create a `.env` file:
```env
MONGO_URI=your_mongodb_uri
GOOGLE_API_KEY=your_google_maps_api_key
```

### 3. Set up the databases

Load SQL data:
```bash
python scripts/load_sql_tables.py
```

Load MongoDB data:
```bash
python scripts/load_to_mongodb_atlas.py
```

(Optionally) Set up MongoDB indexes:
```bash
python db/mongo/indexes.py
```

### 4. Run the application
```bash
streamlit run app/main.py
```

Access the app at `http://localhost:8501/`

---

## Usage

- **Guests:** Browse books and place orders without logging in.
- **Customers:** View their profile, orders, submit reviews, and get recommendations.
- **Admins:** Monitor customer activities, view customer maps, and access basic reporting dashboards.

---

## Acknowledgments
- Datasets adapted from [Kaggle](https://www.kaggle.com/)
- Technologies: Streamlit, MongoDB Atlas, Google Maps API, SQLite

---

## Authors
- **Anna Bajszczak**

---

## License

This project was developed as part of the **NoSQL Database** course at **Purdue University**.  
It is intended for **educational use and demonstration purposes only**.  
**All rights reserved.**

---
