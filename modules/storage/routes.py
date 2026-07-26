from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from extensions import db
from models import StorageLocation, StorageStock, StorageTransaction, BrickProduction, StorageDeduction, Employee

storage_bp = Blueprint('storage', __name__, url_prefix='/storage')


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


def _serialize(obj):
    if obj is None:
        return obj
    for key, val in obj.items():
        if hasattr(val, 'isoformat'):
            obj[key] = val.isoformat() if val else None
    return obj


def _location_to_dict(loc, item_count=None):
    d = {
        'id': loc.id,
        'name': loc.name,
        'location_type': loc.location_type,
        'capacity': loc.capacity,
        'description': loc.description,
    }
    if item_count is not None:
        d['item_count'] = item_count
    return d


def _stock_to_dict(s):
    return {
        'id': s.id,
        'location_id': s.location_id,
        'item_name': s.item_name,
        'item_type': s.item_type,
        'quantity': s.quantity,
        'unit': s.unit,
        'created_at': s.created_at,
    }


def _transaction_to_dict(t):
    return {
        'id': t.id,
        'location_id': t.location_id,
        'item_name': t.item_name,
        'transaction_type': t.transaction_type,
        'quantity': t.quantity,
        'date': t.date,
        'notes': t.notes,
    }


def _production_to_dict(r):
    return {
        'id': r.id,
        'employee_id': r.employee_id,
        'location_id': r.location_id,
        'production_date': r.production_date,
        'bricks_produced': r.bricks_produced,
        'department_type': r.department_type,
        'brick_size': r.brick_size,
        'created_at': r.created_at,
    }


PRODUCTION_BRICK_SIZES = ('4 Inch', '6 Inch', '8 Inch', '9 Inch')


def _validate_production_form(data):
    errors = []
    if not data.get('production_date'):
        errors.append('Production Date is required.')
    if not data.get('employee_id'):
        errors.append('Employee Name must be selected.')
    if not data.get('location_id'):
        errors.append('Set Name must be selected.')
    if data.get('brick_size') not in PRODUCTION_BRICK_SIZES:
        errors.append('Brick Size must be selected.')
    try:
        if float(data.get('bricks_produced', 0) or 0) <= 0:
            errors.append('Bricks Produced must be greater than zero.')
    except ValueError:
        errors.append('Bricks Produced must be greater than zero.')
    return errors


def _deduction_to_dict(r):
    return {
        'id': r.id,
        'location_id': r.location_id,
        'employee_id': r.employee_id,
        'previous_quantity': r.previous_quantity,
        'deducted_quantity': r.deducted_quantity,
        'current_quantity': r.current_quantity,
        'payment_amount': r.payment_amount,
        'payment_date': r.payment_date,
        'payment_status': r.payment_status,
        'reminder_date': r.reminder_date,
        'reason': r.reason,
        'created_at': r.created_at,
    }


def _validate_deduction_form(data):
    errors = []
    if not data.get('location_id'):
        errors.append('Bricks Set Name is mandatory.')
    if not data.get('employee_id'):
        errors.append('Employee Name is mandatory.')

    try:
        previous_qty = float(data.get('previous_quantity', 0) or 0)
    except ValueError:
        previous_qty = 0

    try:
        deducted_qty = float(data.get('deducted_quantity', ''))
        if deducted_qty <= 0:
            errors.append('Deducted Quantity is mandatory.')
        elif deducted_qty > previous_qty:
            errors.append('Deducted Quantity cannot exceed the Previous Bricks Quantity.')
    except (ValueError, TypeError):
        errors.append('Deducted Quantity is mandatory.')

    try:
        if float(data.get('payment_amount', '')) <= 0:
            errors.append('Payment Amount is mandatory.')
    except (ValueError, TypeError):
        errors.append('Payment Amount is mandatory.')

    if not data.get('payment_date'):
        errors.append('Payment Date is mandatory.')

    status = data.get('payment_status')
    if status not in ('Online', 'Cash', 'Pending'):
        errors.append('Payment Status is mandatory.')

    reminder_date = data.get('reminder_date')
    if status == 'Pending':
        if not reminder_date:
            errors.append('Reminder Date is mandatory when Payment Status is Pending.')
        elif data.get('payment_date') and reminder_date < data.get('payment_date'):
            errors.append('Reminder Date cannot be earlier than the Payment Date.')

    if not data.get('reason', '').strip():
        errors.append('Reason is mandatory.')

    return errors


@storage_bp.route('/')
@login_required
def index():
    return render_template('storage/list.html')


# Storage Locations
@storage_bp.route('/data')
@login_required
def data():
    locations = StorageLocation.query.order_by(StorageLocation.id.desc()).all()
    result = []
    for loc in locations:
        item_count = len(loc.stock_items)
        d = _location_to_dict(loc, item_count=item_count)
        _serialize(d)
        result.append(d)
    return jsonify(result)


@storage_bp.route('/add', methods=['POST'])
@login_required
def add():
    try:
        data = request.form
        loc = StorageLocation(
            name=data.get('name'),
            location_type=data.get('location_type') or None,
            capacity=data.get('capacity') or None,
            description=data.get('description'),
        )
        db.session.add(loc)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Storage location added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    try:
        data = request.form
        loc = StorageLocation.query.get(id)
        if loc:
            loc.name = data.get('name')
            loc.location_type = data.get('location_type') or None
            loc.capacity = data.get('capacity') or None
            loc.description = data.get('description')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Storage location updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try:
        loc = StorageLocation.query.get(id)
        if loc:
            db.session.delete(loc)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Storage location deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/get/<int:id>')
@login_required
def get_one(id):
    loc = StorageLocation.query.get(id)
    d = _location_to_dict(loc) if loc else None
    if d:
        _serialize(d)
    return jsonify(d)


# Stock
@storage_bp.route('/stock/data')
@login_required
def stock_data():
    stock = StorageStock.query.order_by(StorageStock.quantity.asc()).all()
    result = []
    for s in stock:
        d = _stock_to_dict(s)
        d['location_name'] = s.location.name if s.location else None
        d['low_stock'] = float(s.quantity) < 100
        _serialize(d)
        result.append(d)
    return jsonify(result)


@storage_bp.route('/stock/add', methods=['POST'])
@login_required
def stock_add():
    try:
        data = request.form
        s = StorageStock(
            location_id=data.get('location_id'),
            item_name=data.get('item_name'),
            item_type=data.get('item_type'),
            quantity=data.get('quantity', 0),
            unit=data.get('unit'),
        )
        db.session.add(s)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Stock item added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/stock/edit/<int:id>', methods=['POST'])
@login_required
def stock_edit(id):
    try:
        data = request.form
        s = StorageStock.query.get(id)
        if s:
            s.location_id = data.get('location_id')
            s.item_name = data.get('item_name')
            s.item_type = data.get('item_type')
            s.quantity = data.get('quantity', 0)
            s.unit = data.get('unit')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Stock item updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/stock/delete/<int:id>', methods=['POST'])
@login_required
def stock_delete(id):
    try:
        s = StorageStock.query.get(id)
        if s:
            db.session.delete(s)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Stock item deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/stock/get/<int:id>')
@login_required
def stock_get(id):
    s = StorageStock.query.get(id)
    d = _stock_to_dict(s) if s else None
    if d:
        _serialize(d)
    return jsonify(d)


# Transactions
@storage_bp.route('/transactions/data')
@login_required
def transactions_data():
    transactions = StorageTransaction.query.order_by(
        StorageTransaction.date.desc(), StorageTransaction.id.desc()
    ).all()
    result = []
    for t in transactions:
        d = _transaction_to_dict(t)
        d['location_name'] = t.location.name if t.location else None
        _serialize(d)
        result.append(d)
    return jsonify(result)


@storage_bp.route('/transactions/add', methods=['POST'])
@login_required
def transactions_add():
    try:
        data = request.form
        location_id = data.get('location_id')
        item_name = data.get('item_name')
        transaction_type = data.get('transaction_type')
        quantity = float(data.get('quantity', 0))

        t = StorageTransaction(
            location_id=location_id,
            item_name=item_name,
            transaction_type=transaction_type,
            quantity=quantity,
            date=data.get('date'),
            notes=data.get('notes'),
        )
        db.session.add(t)

        stock = StorageStock.query.filter_by(location_id=location_id, item_name=item_name).first()
        if stock:
            if transaction_type == 'in':
                new_qty = float(stock.quantity) + quantity
            else:
                new_qty = max(0, float(stock.quantity) - quantity)
            stock.quantity = new_qty

        db.session.commit()
        return jsonify({'success': True, 'message': f'Stock {transaction_type} transaction recorded successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/locations-list')
@login_required
def locations_list():
    locations = StorageLocation.query.order_by(StorageLocation.name).all()
    result = [{'id': loc.id, 'name': loc.name} for loc in locations]
    return jsonify(result)


# Brick Production
@storage_bp.route('/production/data')
@login_required
def production_data():
    records = BrickProduction.query.order_by(
        BrickProduction.production_date.desc(), BrickProduction.id.desc()
    ).all()
    result = []
    for r in records:
        d = _production_to_dict(r)
        d['employee_name'] = r.employee.name if r.employee else None
        d['location_name'] = r.location.name if r.location else None
        _serialize(d)
        result.append(d)
    return jsonify(result)


@storage_bp.route('/production/add', methods=['POST'])
@login_required
def production_add():
    data = request.form
    errors = _validate_production_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        employee = Employee.query.get(data.get('employee_id'))
        department_type = employee.department.name if employee and employee.department else 'Unassigned'
        r = BrickProduction(
            employee_id=data.get('employee_id'),
            location_id=data.get('location_id'),
            production_date=data.get('production_date'),
            bricks_produced=data.get('bricks_produced', 0),
            department_type=department_type,
            brick_size=data.get('brick_size'),
        )
        db.session.add(r)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Brick production record added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/production/delete/<int:id>', methods=['POST'])
@login_required
def production_delete(id):
    try:
        r = BrickProduction.query.get(id)
        if r:
            db.session.delete(r)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Production record deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


# Storage Deductions / Payment Management
@storage_bp.route('/deductions/data')
@login_required
def deductions_data():
    records = StorageDeduction.query.order_by(
        StorageDeduction.payment_date.desc(), StorageDeduction.id.desc()
    ).all()
    result = []
    for r in records:
        d = _deduction_to_dict(r)
        d['location_name'] = r.location.name if r.location else None
        d['employee_name'] = r.employee.name if r.employee else None
        d['contact_number'] = r.employee.mobile if r.employee else None
        _serialize(d)
        result.append(d)
    return jsonify(result)


@storage_bp.route('/deductions/set-quantity/<int:location_id>')
@login_required
def deductions_set_quantity(location_id):
    total = db.session.query(db.func.coalesce(db.func.sum(StorageStock.quantity), 0)).filter(
        StorageStock.location_id == location_id
    ).scalar()
    return jsonify({'previous_quantity': float(total)})


@storage_bp.route('/deductions/add', methods=['POST'])
@login_required
def deductions_add():
    data = request.form
    errors = _validate_deduction_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        location_id = data.get('location_id')
        previous_qty = float(data.get('previous_quantity', 0))
        deducted_qty = float(data.get('deducted_quantity', 0))
        current_qty = previous_qty - deducted_qty
        status = data.get('payment_status')

        r = StorageDeduction(
            location_id=location_id,
            employee_id=data.get('employee_id'),
            previous_quantity=previous_qty,
            deducted_quantity=deducted_qty,
            current_quantity=current_qty,
            payment_amount=data.get('payment_amount'),
            payment_date=data.get('payment_date'),
            payment_status=status,
            reminder_date=data.get('reminder_date') if status == 'Pending' else None,
            reason=data.get('reason'),
        )
        db.session.add(r)

        # Proportionally reduce stock at this location to reflect the deduction
        stocks = StorageStock.query.filter_by(location_id=location_id).all()
        if previous_qty > 0:
            for s in stocks:
                s.quantity = max(0, float(s.quantity) - (float(s.quantity) / previous_qty) * deducted_qty)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Deduction recorded successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/deductions/delete/<int:id>', methods=['POST'])
@login_required
def deductions_delete(id):
    try:
        r = StorageDeduction.query.get(id)
        if r:
            db.session.delete(r)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Deduction record deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/deductions/mark-paid/<int:id>', methods=['POST'])
@login_required
def deductions_mark_paid(id):
    try:
        data = request.form
        method = data.get('payment_status')
        if method not in ('Online', 'Cash'):
            return jsonify({'success': False, 'message': 'Payment method must be Online or Cash.'})
        r = StorageDeduction.query.get(id)
        if r:
            r.payment_status = method
            r.reminder_date = None
        db.session.commit()
        return jsonify({'success': True, 'message': 'Payment marked as completed'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@storage_bp.route('/deductions/pending-reminders')
@login_required
def deductions_pending_reminders():
    from datetime import date
    records = StorageDeduction.query.filter(
        StorageDeduction.payment_status == 'Pending',
        StorageDeduction.reminder_date <= date.today(),
    ).all()
    result = []
    for r in records:
        result.append({
            'id': r.id,
            'employee_name': r.employee.name if r.employee else None,
            'payment_amount': float(r.payment_amount) if r.payment_amount is not None else None,
            'reminder_date': r.reminder_date.isoformat() if r.reminder_date else None,
        })
    return jsonify(result)
