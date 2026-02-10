from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import sqlite3
from config import DATABASE
import pdfkit
from datetime import datetime
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

UPLOAD_FOLDER = 'static/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- Database Helper ---
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# --- Home Page ---
@app.route('/')
def home():
    return render_template('home.html')

# --- Stock Management ---
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    conn = get_db_connection()
    if request.method == 'POST':
        bike_id = int(request.form['bike_id'])
        action = request.form['action']
        cur = conn.cursor()
        cur.execute("SELECT quantity FROM bikes WHERE id=?", (bike_id,))
        qty = cur.fetchone()[0]
        if action == 'add':
            qty += 1
        elif action == 'subtract' and qty > 0:
            qty -= 1
        cur.execute("UPDATE bikes SET quantity=? WHERE id=?", (qty, bike_id))
        conn.commit()
    bikes = conn.execute("SELECT * FROM bikes").fetchall()
    conn.close()
    return render_template('stock.html', bikes=bikes)

# --- Add New Bike ---
@app.route('/add_bike', methods=['POST'])
def add_bike():
    name = request.form['name']
    model = request.form['model']
    engine_cc = int(request.form['engine_cc'])
    tank_capacity = int(request.form['tank_capacity'])
    year = int(request.form['year'])
    quantity = int(request.form['quantity'])
    ex_showroom_price = float(request.form.get('ex_showroom_price', engine_cc * 100))

    image_file = request.files['image']
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(image_path)

    conn = get_db_connection()
    conn.execute(
        '''INSERT INTO bikes (name, model, engine_cc, tank_capacity, year, quantity, image, ex_showroom_price)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (name, model, engine_cc, tank_capacity, year, quantity, filename, ex_showroom_price)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('stock'))

# --- Delete Bike ---
@app.route('/delete_bike/<int:bike_id>', methods=['POST'])
def delete_bike(bike_id):
    conn = get_db_connection()
    bike = conn.execute("SELECT image FROM bikes WHERE id=?", (bike_id,)).fetchone()
    if bike and bike['image']:
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], bike['image'])
        if os.path.exists(image_path):
            os.remove(image_path)
    conn.execute("DELETE FROM bikes WHERE id=?", (bike_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('stock'))

# --- Billing Page ---
@app.route('/billing', methods=['GET', 'POST'])
def billing():
    conn = get_db_connection()
    bikes = conn.execute("SELECT * FROM bikes WHERE quantity > 0").fetchall()

    if request.method == 'POST':
        data = request.form
        customer_name = data['customer_name']
        contact = data['contact']
        email = data['email']
        address = data['address']
        finance_option = data.get('finance_option', 'None')
        down_payment = float(data.get('down_payment', 0))
        bike_id = int(data['bike_id'])
        quantity = int(data['quantity'])

        cur = conn.cursor()
        bike = cur.execute("SELECT * FROM bikes WHERE id=?", (bike_id,)).fetchone()

        if bike['quantity'] < quantity:
            flash("❌ Not enough stock available.", "error")
            return redirect(url_for('billing'))

        # --- On-Road Price Calculation ---
        ex_showroom = bike['ex_showroom_price']
        road_tax = ex_showroom * 0.12
        registration = 1500
        insurance = ex_showroom * 0.03
        dealer_charges = 2000

        total_per_unit = ex_showroom + road_tax + registration + insurance + dealer_charges
        grand_total = total_per_unit * quantity
        final_payable = grand_total - down_payment

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # --- Insert Bill ---
        cur.execute('''INSERT INTO bills 
            (customer_name, contact, email, address, finance_option, down_payment, 
             bike_name, quantity, price_per_unit, total,
             ex_showroom, road_tax, registration, insurance, dealer_charges, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (customer_name, contact, email, address, finance_option, down_payment,
             bike['name'], quantity, total_per_unit, final_payable,
             ex_showroom, road_tax, registration, insurance, dealer_charges, date)
        )

        # --- Update Stock ---
        cur.execute("UPDATE bikes SET quantity=? WHERE id=?", (bike['quantity'] - quantity, bike_id))

        conn.commit()
        bill_id = cur.lastrowid
        conn.close()

        return redirect(url_for('generate_pdf', bill_id=bill_id))

    conn.close()
    return render_template('billing.html', bikes=bikes)

# --- Billing History Page ---
@app.route('/billing_history')
def billing_history():
    conn = get_db_connection()
    bills = conn.execute("SELECT * FROM bills ORDER BY date DESC").fetchall()
    conn.close()
    return render_template('billing_history.html', bills=bills)

# --- Generate Bill PDF ---
@app.route('/generate_pdf/<int:bill_id>')
def generate_pdf(bill_id):
    conn = get_db_connection()
    bill = conn.execute("SELECT * FROM bills WHERE id=?", (bill_id,)).fetchone()
    conn.close()

    rendered = render_template('bill_pdf.html', bill=bill)
    pdf_file = f"bill_{bill_id}.pdf"

    config = pdfkit.configuration(wkhtmltopdf=r"D:\wkhtmltopdf\bin\wkhtmltopdf.exe")
    options = {'enable-local-file-access': None}
    pdfkit.from_string(rendered, pdf_file, configuration=config, options=options)

    return send_file(pdf_file, as_attachment=True)

# --- Search Bike ---
@app.route('/search_bike', methods=['GET'])
def search_bike():
    query = request.args.get('query', '').strip().lower()
    conn = get_db_connection()
    if query:
        bikes = conn.execute("""
            SELECT * FROM bikes 
            WHERE LOWER(name) LIKE ? OR LOWER(model) LIKE ?
        """, (f'%{query}%', f'%{query}%')).fetchall()
    else:
        bikes = conn.execute("SELECT * FROM bikes").fetchall()
    conn.close()
    return render_template('stock.html', bikes=bikes)

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True, port=8000)

#ckp 001