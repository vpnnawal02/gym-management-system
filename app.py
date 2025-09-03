from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Paths to data files
DATA_FOLDER = 'gym_data'
CLIENTS_FILE = os.path.join(DATA_FOLDER, 'clients.json')
SETTINGS_FILE = os.path.join(DATA_FOLDER, 'settings.json')

# Ensure data folder exists
os.makedirs(DATA_FOLDER, exist_ok=True)

# Initialize data files if not exist
if not os.path.exists(CLIENTS_FILE):
    with open(CLIENTS_FILE, 'w') as f:
        json.dump([], f)

if not os.path.exists(SETTINGS_FILE):
    default_settings = {
        "admin_id": "admin",
        "admin_password": "admin123"
    }
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(default_settings, f)

# Helper functions
def load_clients():
    with open(CLIENTS_FILE, 'r') as f:
        return json.load(f)

def save_clients(clients):
    with open(CLIENTS_FILE, 'w') as f:
        json.dump(clients, f, indent=4)

def check_login(username, password):
    with open(SETTINGS_FILE) as f:
        settings = json.load(f)
    return username == settings['admin_id'] and password == settings['admin_password']

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_login(username, password):
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    clients = load_clients()
    today = datetime.now().date()

    for c in clients:
        expiry_str = c.get('expiry_date')
        if expiry_str:
            expiry = datetime.strptime(expiry_str, "%Y-%m-%d").date()
            days_left = (expiry - today).days
            c['days_left'] = days_left if days_left >= 0 else 0
        else:
            c['days_left'] = '-'
    return render_template('dashboard.html', clients=clients)

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        membership_days = int(request.form['membership_days'])
        join_date = datetime.now().strftime('%Y-%m-%d')
        expiry_date = (datetime.now() + timedelta(days=membership_days)).strftime('%Y-%m-%d')
        new_client = {
            'id': len(load_clients()) + 1,
            'name': name,
            'email': email,
            'phone': '+91'+ phone,
            'join_date': join_date,
            'expiry_date': expiry_date,
            'membership_days': membership_days
        }
        clients = load_clients()
        clients.append(new_client)
        save_clients(clients)
        flash('Client added successfully!')
        return redirect(url_for('dashboard'))
    return render_template('add_client.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

@app.route('/renew_membership', methods=['POST'])
def renew_membership():
    data = request.get_json()
    member_id = str(data.get('member_id')).strip()
    new_expiry = data.get('new_expiry').strip()

    clients = load_clients()
    updated = False

@app.route('/remove_client', methods=['POST'])
def remove_client():
    data = request.get_json()
    client_id = str(data.get('client_id')).strip()
    clients = load_clients()
    new_clients = [c for c in clients if str(c.get('id')) != client_id]

    if len(new_clients) == len(clients):
        return jsonify({"success": False, "message": "Client not found"}), 404

    save_clients(new_clients)
    return jsonify({"success": True})


    # Find and update the client by id
    for c in clients:
        if str(c.get("id")) == member_id:
            c['expiry_date'] = new_expiry
            updated = True
            break

    if updated:
        save_clients(clients)
        return jsonify({"success": True, "message": "Membership renewed"})
    else:
        return jsonify({"success": False, "message": "Client not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
