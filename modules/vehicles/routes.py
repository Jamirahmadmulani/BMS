from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import os, uuid, re
from werkzeug.utils import secure_filename
from extensions import db
from models import Vehicle, Driver, Trip, VehicleMaintenance, VehicleInvestment

vehicles_bp = Blueprint('vehicles', __name__, url_prefix='/vehicles')

UPLOAD_DRIVER_AADHAR = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'uploads', 'driver_aadhar')
UPLOAD_DRIVER_LICENSE = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'uploads', 'driver_license')


def _ensure_driver_dirs():
    os.makedirs(UPLOAD_DRIVER_AADHAR, exist_ok=True)
    os.makedirs(UPLOAD_DRIVER_LICENSE, exist_ok=True)


def _save_file(file, folder):
    if not file or file.filename == '':
        return None
    ext = secure_filename(file.filename).rsplit('.', 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(folder, filename))
    return filename


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            from flask import request as _req
            if _req.headers.get('X-Requested-With') == 'XMLHttpRequest' or 'application/json' in _req.headers.get('Accept',''):
                return jsonify({'success': False, 'message': 'Session expired', 'redirect': '/login'}), 401
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def _fmt(val):
    if hasattr(val, 'isoformat'):
        return val.isoformat() if val else None
    return val


def _vehicle_dict(v):
    return {
        'id': v.id,
        'vehicle_number': v.vehicle_number,
        'vehicle_name': v.vehicle_name,
        'model': v.model,
        'year': v.year,
        'driver_id': v.driver_id,
        'insurance': v.insurance,
        'road_tax': v.road_tax,
        'puc': v.puc,
        'fuel_type': v.fuel_type,
        'status': v.status,
        'driver_name': v.driver.name if v.driver else None,
    }


VEHICLE_FUEL_TYPES = ('Petrol', 'Diesel', 'Gas', 'Battery')


def _validate_vehicle_form(data):
    errors = []
    if not data.get('vehicle_number', '').strip():
        errors.append('Vehicle Number is mandatory.')
    if not data.get('vehicle_name', '').strip():
        errors.append('Vehicle Name is mandatory.')
    if not data.get('model', '').strip():
        errors.append('Model is mandatory.')
    if not data.get('year'):
        errors.append('Year is mandatory.')
    if not data.get('driver_id'):
        errors.append('Driver selection is mandatory.')
    if not data.get('insurance', '').strip():
        errors.append('Vehicle Insurance is mandatory.')
    if not data.get('road_tax', '').strip():
        errors.append('Road Tax is mandatory.')
    if not data.get('puc', '').strip():
        errors.append('PUC is mandatory.')
    if data.get('fuel_type') not in VEHICLE_FUEL_TYPES:
        errors.append('Fuel Type is mandatory.')
    if data.get('status') not in ('active', 'inactive'):
        errors.append('Status is mandatory.')
    return errors


def _driver_dict(d, vehicle_count=None):
    result = {
        'id': d.id,
        'name': d.name,
        'license_number': d.license_number,
        'mobile': d.mobile,
        'aadhar_number': d.aadhar_number,
        'aadhar_photo': d.aadhar_photo,
        'license_photo': d.license_photo,
        'address': d.address,
        'status': d.status,
    }
    if vehicle_count is not None:
        result['vehicle_count'] = vehicle_count
    return result


def _trip_dict(t):
    return {
        'id': t.id,
        'vehicle_id': t.vehicle_id,
        'driver_id': t.driver_id,
        'from_location': t.from_location,
        'to_location': t.to_location,
        'date': _fmt(t.date),
        'purpose': t.purpose,
        'status': t.status,
        'days': t.days,
        'fuel_expense': float(t.fuel_expense) if t.fuel_expense is not None else None,
        'driver_expense': float(t.driver_expense) if t.driver_expense is not None else None,
        'other_expense': float(t.other_expense) if t.other_expense is not None else None,
        'return_date': _fmt(t.return_date),
        'vehicle_number': t.vehicle.vehicle_number if t.vehicle else None,
        'driver_name': t.driver.name if t.driver else None,
    }


MAINTENANCE_TYPES = ('Oil Change', 'Servicing', 'Washing', 'Tire Change', 'Other')


def _maintenance_dict(r):
    return {
        'id': r.id,
        'vehicle_id': r.vehicle_id,
        'maintenance_type': r.maintenance_type,
        'date': _fmt(r.date),
        'cost': float(r.cost) if r.cost is not None else None,
        'description': r.description,
        'vehicle_number': r.vehicle.vehicle_number if r.vehicle else None,
    }


def _validate_maintenance_form(data):
    errors = []
    if not data.get('vehicle_id'):
        errors.append('Vehicle Number is mandatory.')
    if data.get('maintenance_type') not in MAINTENANCE_TYPES:
        errors.append('Maintenance Type is mandatory.')
    if not data.get('date'):
        errors.append('Date is mandatory.')
    cost = data.get('cost', '').strip()
    try:
        if cost == '' or float(cost) < 0:
            errors.append('Cost (Rs.) is mandatory and must be a valid numeric value.')
    except (ValueError, AttributeError):
        errors.append('Cost (Rs.) is mandatory and must be a valid numeric value.')
    return errors


def _investment_dict(r):
    return {
        'id': r.id,
        'vehicle_id': r.vehicle_id,
        'investment_type': r.investment_type,
        'amount': float(r.amount) if r.amount is not None else None,
        'investment_date': _fmt(r.investment_date),
        'description': r.description,
        'created_at': _fmt(r.created_at),
        'vehicle_number': r.vehicle.vehicle_number if r.vehicle else None,
    }


@vehicles_bp.route('/')
@login_required
def index():
    return render_template('vehicles/list.html')


# Vehicles CRUD
@vehicles_bp.route('/data')
@login_required
def data():
    vehicles = Vehicle.query.order_by(Vehicle.id.desc()).all()
    return jsonify([_vehicle_dict(v) for v in vehicles])


@vehicles_bp.route('/add', methods=['POST'])
@login_required
def add():
    data = request.form
    errors = _validate_vehicle_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        vehicle = Vehicle(
            vehicle_number=data.get('vehicle_number'),
            vehicle_name=data.get('vehicle_name'),
            model=data.get('model'),
            year=data.get('year') or None,
            driver_id=data.get('driver_id') or None,
            insurance=data.get('insurance'),
            road_tax=data.get('road_tax'),
            puc=data.get('puc'),
            fuel_type=data.get('fuel_type'),
            status=data.get('status', 'active')
        )
        db.session.add(vehicle)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Vehicle added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    data = request.form
    errors = _validate_vehicle_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        vehicle = Vehicle.query.get(id)
        vehicle.vehicle_number = data.get('vehicle_number')
        vehicle.vehicle_name = data.get('vehicle_name')
        vehicle.model = data.get('model')
        vehicle.year = data.get('year') or None
        vehicle.driver_id = data.get('driver_id') or None
        vehicle.insurance = data.get('insurance')
        vehicle.road_tax = data.get('road_tax')
        vehicle.puc = data.get('puc')
        vehicle.fuel_type = data.get('fuel_type')
        vehicle.status = data.get('status', 'active')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Vehicle updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try:
        vehicle = Vehicle.query.get(id)
        if vehicle:
            db.session.delete(vehicle)
            db.session.commit()
        return jsonify({'success': True, 'message': 'Vehicle deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/get/<int:id>')
@login_required
def get_one(id):
    vehicle = Vehicle.query.get(id)
    if not vehicle:
        return jsonify(None)
    return jsonify(_vehicle_dict(vehicle))


def _validate_driver_form(data, files, require_files):
    errors = []
    if not data.get('name', '').strip():
        errors.append('Driver Name is mandatory.')
    if not data.get('license_number', '').strip():
        errors.append('License Number is mandatory.')
    if not re.fullmatch(r'\d{10}', data.get('mobile', '').strip()):
        errors.append('Contact Number must contain 10 digits.')
    if not re.fullmatch(r'\d{12}', data.get('aadhar_number', '').strip()):
        errors.append('Aadhaar Number must contain 12 digits.')
    if not data.get('address', '').strip():
        errors.append('Address is mandatory.')
    if data.get('status') not in ('active', 'inactive'):
        errors.append('Status is mandatory.')

    aadhar_photo = files.get('aadhar_photo')
    if require_files and not (aadhar_photo and aadhar_photo.filename):
        errors.append('Aadhaar Card Photo Upload is mandatory.')

    license_photo = files.get('license_photo')
    if require_files and not (license_photo and license_photo.filename):
        errors.append('Driving License Photo Upload is mandatory.')

    return errors


# Drivers CRUD
@vehicles_bp.route('/drivers/data')
@login_required
def drivers_data():
    drivers = Driver.query.order_by(Driver.id.desc()).all()
    result = []
    for d in drivers:
        vehicle_count = Vehicle.query.filter_by(driver_id=d.id).count()
        result.append(_driver_dict(d, vehicle_count))
    return jsonify(result)


@vehicles_bp.route('/drivers/add', methods=['POST'])
@login_required
def drivers_add():
    _ensure_driver_dirs()
    data = request.form
    errors = _validate_driver_form(data, request.files, require_files=True)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        aadhar_photo = _save_file(request.files.get('aadhar_photo'), UPLOAD_DRIVER_AADHAR)
        license_photo = _save_file(request.files.get('license_photo'), UPLOAD_DRIVER_LICENSE)
        driver = Driver(
            name=data.get('name'),
            license_number=data.get('license_number'),
            mobile=data.get('mobile'),
            aadhar_number=data.get('aadhar_number'),
            aadhar_photo=aadhar_photo,
            license_photo=license_photo,
            address=data.get('address'),
            status=data.get('status', 'active')
        )
        db.session.add(driver)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Driver added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/drivers/edit/<int:id>', methods=['POST'])
@login_required
def drivers_edit(id):
    _ensure_driver_dirs()
    data = request.form
    errors = _validate_driver_form(data, request.files, require_files=False)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        driver = Driver.query.get(id)
        aadhar_photo = _save_file(request.files.get('aadhar_photo'), UPLOAD_DRIVER_AADHAR)
        license_photo = _save_file(request.files.get('license_photo'), UPLOAD_DRIVER_LICENSE)
        driver.name = data.get('name')
        driver.license_number = data.get('license_number')
        driver.mobile = data.get('mobile')
        driver.aadhar_number = data.get('aadhar_number')
        if aadhar_photo:
            driver.aadhar_photo = aadhar_photo
        if license_photo:
            driver.license_photo = license_photo
        driver.address = data.get('address')
        driver.status = data.get('status', 'active')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Driver updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/drivers/delete/<int:id>', methods=['POST'])
@login_required
def drivers_delete(id):
    try:
        driver = Driver.query.get(id)
        if driver:
            db.session.delete(driver)
            db.session.commit()
        return jsonify({'success': True, 'message': 'Driver deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/drivers/get/<int:id>')
@login_required
def drivers_get(id):
    driver = Driver.query.get(id)
    if not driver:
        return jsonify(None)
    return jsonify(_driver_dict(driver))


@vehicles_bp.route('/drivers-list')
@login_required
def drivers_list():
    drivers = Driver.query.filter_by(status='active').order_by(Driver.name).all()
    return jsonify([{'id': d.id, 'name': d.name} for d in drivers])


@vehicles_bp.route('/vehicles-list')
@login_required
def vehicles_list():
    vehicles = Vehicle.query.filter_by(status='active').order_by(Vehicle.vehicle_number).all()
    return jsonify([{'id': v.id, 'vehicle_number': v.vehicle_number} for v in vehicles])


# Trips CRUD
@vehicles_bp.route('/trips/data')
@login_required
def trips_data():
    trips = Trip.query.order_by(Trip.date.desc(), Trip.id.desc()).all()
    return jsonify([_trip_dict(t) for t in trips])


@vehicles_bp.route('/trips/add', methods=['POST'])
@login_required
def trips_add():
    try:
        data = request.form
        trip = Trip(
            vehicle_id=data.get('vehicle_id'),
            driver_id=data.get('driver_id') or None,
            from_location=data.get('from_location'),
            to_location=data.get('to_location'),
            date=data.get('date'),
            purpose=data.get('purpose'),
            status=data.get('status', 'planned'),
            days=data.get('days') or None,
            fuel_expense=data.get('fuel_expense') or 0,
            driver_expense=data.get('driver_expense') or 0,
            other_expense=data.get('other_expense') or 0,
            return_date=data.get('return_date') or None
        )
        db.session.add(trip)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Trip added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/trips/edit/<int:id>', methods=['POST'])
@login_required
def trips_edit(id):
    try:
        data = request.form
        trip = Trip.query.get(id)
        trip.vehicle_id = data.get('vehicle_id')
        trip.driver_id = data.get('driver_id') or None
        trip.from_location = data.get('from_location')
        trip.to_location = data.get('to_location')
        trip.date = data.get('date')
        trip.purpose = data.get('purpose')
        trip.status = data.get('status', 'planned')
        trip.days = data.get('days') or None
        trip.fuel_expense = data.get('fuel_expense') or 0
        trip.driver_expense = data.get('driver_expense') or 0
        trip.other_expense = data.get('other_expense') or 0
        trip.return_date = data.get('return_date') or None
        db.session.commit()
        return jsonify({'success': True, 'message': 'Trip updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/trips/delete/<int:id>', methods=['POST'])
@login_required
def trips_delete(id):
    try:
        trip = Trip.query.get(id)
        if trip:
            db.session.delete(trip)
            db.session.commit()
        return jsonify({'success': True, 'message': 'Trip deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/trips/get/<int:id>')
@login_required
def trips_get(id):
    trip = Trip.query.get(id)
    if not trip:
        return jsonify(None)
    return jsonify(_trip_dict(trip))


# Maintenance CRUD
@vehicles_bp.route('/maintenance/data')
@login_required
def maintenance_data():
    records = VehicleMaintenance.query.order_by(VehicleMaintenance.date.desc(), VehicleMaintenance.id.desc()).all()
    return jsonify([_maintenance_dict(r) for r in records])


@vehicles_bp.route('/maintenance/add', methods=['POST'])
@login_required
def maintenance_add():
    data = request.form
    errors = _validate_maintenance_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        record = VehicleMaintenance(
            vehicle_id=data.get('vehicle_id'),
            maintenance_type=data.get('maintenance_type'),
            date=data.get('date'),
            cost=data.get('cost'),
            description=data.get('description'),
        )
        db.session.add(record)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Maintenance record added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/maintenance/edit/<int:id>', methods=['POST'])
@login_required
def maintenance_edit(id):
    data = request.form
    errors = _validate_maintenance_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        record = VehicleMaintenance.query.get(id)
        record.vehicle_id = data.get('vehicle_id')
        record.maintenance_type = data.get('maintenance_type')
        record.date = data.get('date')
        record.cost = data.get('cost')
        record.description = data.get('description')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Maintenance record updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/maintenance/delete/<int:id>', methods=['POST'])
@login_required
def maintenance_delete(id):
    try:
        record = VehicleMaintenance.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
        return jsonify({'success': True, 'message': 'Maintenance record deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/maintenance/get/<int:id>')
@login_required
def maintenance_get(id):
    record = VehicleMaintenance.query.get(id)
    if not record:
        return jsonify(None)
    return jsonify(_maintenance_dict(record))


# Vehicle Investments
@vehicles_bp.route('/investments/data')
@login_required
def investments_data():
    records = VehicleInvestment.query.order_by(VehicleInvestment.investment_date.desc(), VehicleInvestment.id.desc()).all()
    return jsonify([_investment_dict(r) for r in records])


@vehicles_bp.route('/investments/add', methods=['POST'])
@login_required
def investments_add():
    try:
        data = request.form
        record = VehicleInvestment(
            vehicle_id=data.get('vehicle_id'),
            investment_type=data.get('investment_type'),
            amount=data.get('amount') or 0,
            investment_date=data.get('investment_date'),
            description=data.get('description')
        )
        db.session.add(record)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Investment recorded successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/investments/delete/<int:id>', methods=['POST'])
@login_required
def investments_delete(id):
    try:
        record = VehicleInvestment.query.get(id)
        if record:
            db.session.delete(record)
            db.session.commit()
        return jsonify({'success': True, 'message': 'Investment record deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@vehicles_bp.route('/expenses-summary')
@login_required
def expenses_summary():
    vehicles = Vehicle.query.all()
    result = []
    for v in vehicles:
        total_fuel = sum(float(t.fuel_expense or 0) for t in v.trips)
        total_driver_expense = sum(float(t.driver_expense or 0) for t in v.trips)
        total_other_expense = sum(float(t.other_expense or 0) for t in v.trips)
        total_maintenance = sum(float(m.cost or 0) for m in v.maintenance_records)
        total_investment = sum(float(i.amount or 0) for i in v.investments)
        result.append({
            'id': v.id,
            'vehicle_number': v.vehicle_number,
            'total_fuel': total_fuel,
            'total_driver_expense': total_driver_expense,
            'total_other_expense': total_other_expense,
            'total_maintenance': total_maintenance,
            'total_investment': total_investment,
        })
    return jsonify(result)
