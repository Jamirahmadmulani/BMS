from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
from functools import wraps
from config import DB_CONFIG, SQLALCHEMY_DATABASE_URI
from extensions import db
from models import (
    User, Employee, Department, StorageLocation, Payroll, Vehicle, RawMaterial
)

app = Flask(__name__)
app.secret_key = 'bms_dearsoft_secret_2026'
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ---- Login / Logout ----
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    error = None
    username = ''
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id']   = user.id
            session['user_name'] = user.name
            session['username']  = user.username
            session['role']      = user.role
            return redirect(url_for('index'))
        else:
            error = 'Invalid username or password.'
    return render_template('login.html', error=error, username=username)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# Register blueprints
from modules.employees.routes import employees_bp
from modules.departments.routes import departments_bp
from modules.storage.routes import storage_bp
from modules.payroll.routes import payroll_bp
from modules.vehicles.routes import vehicles_bp
from modules.raw_materials.routes import raw_materials_bp

app.register_blueprint(employees_bp)
app.register_blueprint(departments_bp)
app.register_blueprint(storage_bp)
app.register_blueprint(payroll_bp)
app.register_blueprint(vehicles_bp)
app.register_blueprint(raw_materials_bp)


@app.route('/')
def index():
    if 'user_id' not in session:
        return render_template('landing.html')
    counts = {}
    for key, model in {
        'employees': Employee,
        'departments': Department,
        'storage_locations': StorageLocation,
        'payroll': Payroll,
        'vehicles': Vehicle,
        'raw_materials': RawMaterial,
    }.items():
        try:
            counts[key] = model.query.count()
        except Exception:
            counts[key] = 0
    return render_template('dashboard.html', counts=counts)


with app.app_context():
    db.create_all()
    if not User.query.first():
        db.session.add(User(name='Admin', username='admin', password='admin123', role='admin'))
        db.session.commit()

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
