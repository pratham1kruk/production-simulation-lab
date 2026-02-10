import sqlite3
from config import DATABASE

# Connect to database
conn = sqlite3.connect(DATABASE)
cur = conn.cursor()

# --- Bikes Table ---
cur.execute('''
CREATE TABLE IF NOT EXISTS bikes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    model TEXT,
    engine_cc INTEGER,
    tank_capacity INTEGER,
    year INTEGER,
    quantity INTEGER,
    image TEXT,
    ex_showroom_price REAL
)
''')

# --- Bills Table (Updated with all components) ---
cur.execute('''
CREATE TABLE IF NOT EXISTS bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT,
    contact TEXT,
    email TEXT,
    address TEXT,
    finance_option TEXT,
    down_payment REAL,
    bike_name TEXT,
    quantity INTEGER,
    price_per_unit REAL,
    total REAL,
    ex_showroom REAL,
    road_tax REAL,
    registration REAL,
    insurance REAL,
    dealer_charges REAL,
    date TEXT
)
''')

# --- Sample Bikes ---
bikes = [
    ('Shine', 'CB125', 125, 11, 2024, 10, 'shine.png', 85000),
    ('Unicorn', 'CB160', 160, 13, 2023, 8, 'unicorn.png', 110000),
    ('SP125', 'SP125X', 125, 10, 2022, 12, 'sp125.png', 90000)
]

for bike in bikes:
    cur.execute('''
    INSERT OR IGNORE INTO bikes 
    (name, model, engine_cc, tank_capacity, year, quantity, image, ex_showroom_price) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', bike)

conn.commit()
conn.close()
print("✅ Database initialized successfully with updated schema and sample data.")
