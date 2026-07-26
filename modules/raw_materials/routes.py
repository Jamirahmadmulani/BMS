from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from datetime import datetime
import re

from extensions import db
from models import RawMaterial, Supplier, Purchase, RawMaterialStock, RawMaterialTransaction

raw_materials_bp = Blueprint('raw_materials', __name__, url_prefix='/raw-materials')


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


def _iso(val):
    return val.isoformat() if val else None


def _material_dict(m):
    stock_quantity = float(m.stock.quantity) if m.stock else 0
    return {
        'id': m.id,
        'name': m.name,
        'unit': m.unit,
        'supplier_id': m.supplier_id,
        'supplier_name': m.supplier.name if m.supplier else None,
        'description': m.description,
        'stock_quantity': stock_quantity,
        'low_stock': stock_quantity < 100,
    }


def _validate_material_form(data):
    errors = []
    if not data.get('name', '').strip():
        errors.append('Material Name is mandatory.')
    if not data.get('unit', '').strip():
        errors.append('Unit is mandatory.')
    supplier_id = data.get('supplier_id')
    if not supplier_id or not Supplier.query.get(supplier_id):
        errors.append('Supplier Name is mandatory and must be selected from the Supplier list.')
    return errors


def _supplier_dict(s):
    return {
        'id': s.id,
        'name': s.name,
        'mobile': s.mobile,
        'address': s.address,
        'email': s.email,
        'purchase_count': len(s.purchases),
    }


EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def _validate_supplier_form(data):
    errors = []
    if not data.get('name', '').strip():
        errors.append('Supplier Name is mandatory.')
    if not re.fullmatch(r'\d{10}', data.get('mobile', '').strip()):
        errors.append('Contact Number is mandatory and must contain 10 digits.')
    email = data.get('email', '').strip()
    if email and not EMAIL_RE.match(email):
        errors.append('Email must be in a valid email format.')
    if not data.get('address', '').strip():
        errors.append('Address is mandatory.')
    return errors


def _purchase_dict(p):
    return {
        'id': p.id,
        'supplier_id': p.supplier_id,
        'material_id': p.material_id,
        'quantity': float(p.quantity) if p.quantity is not None else None,
        'unit_price': float(p.unit_price) if p.unit_price is not None else None,
        'total_price': float(p.total_price) if p.total_price is not None else None,
        'purchase_date': _iso(p.purchase_date),
        'received_at': _iso(p.received_at),
        'notes': p.notes,
        'supplier_name': p.supplier.name if p.supplier else None,
        'material_name': p.material.name,
        'unit': p.material.unit,
    }


TRANSACTION_TYPES = ('Online', 'Cash', 'RTGS', 'Cheque')


def _transaction_dict(t):
    return {
        'id': t.id,
        'supplier_id': t.supplier_id,
        'supplier_name': t.supplier.name if t.supplier else None,
        'transaction_type': t.transaction_type,
        'date': _iso(t.date),
        'notes': t.notes,
    }


def _validate_transaction_form(data):
    errors = []
    if not data.get('supplier_id') or not Supplier.query.get(data.get('supplier_id')):
        errors.append('Supplier Name is mandatory.')
    if data.get('transaction_type') not in TRANSACTION_TYPES:
        errors.append('Transaction Type is mandatory.')
    if not data.get('date'):
        errors.append('Date is mandatory.')
    return errors


@raw_materials_bp.route('/')
@login_required
def index():
    return render_template('raw_materials/list.html')


# Raw Materials CRUD
@raw_materials_bp.route('/data')
@login_required
def data():
    materials = RawMaterial.query.order_by(RawMaterial.id.desc()).all()
    return jsonify([_material_dict(m) for m in materials])


@raw_materials_bp.route('/add', methods=['POST'])
@login_required
def add():
    data = request.form
    errors = _validate_material_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        material = RawMaterial(
            name=data.get('name'),
            unit=data.get('unit'),
            supplier_id=data.get('supplier_id'),
            description=data.get('description'),
        )
        db.session.add(material)
        db.session.flush()

        stock = RawMaterialStock(material_id=material.id, quantity=0)
        db.session.add(stock)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Raw material added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@raw_materials_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    data = request.form
    errors = _validate_material_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        material = RawMaterial.query.get(id)
        material.name = data.get('name')
        material.unit = data.get('unit')
        material.supplier_id = data.get('supplier_id')
        material.description = data.get('description')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Raw material updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@raw_materials_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try:
        material = RawMaterial.query.get(id)
        if material:
            db.session.delete(material)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Raw material deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@raw_materials_bp.route('/get/<int:id>')
@login_required
def get_one(id):
    material = RawMaterial.query.get(id)
    if not material:
        return jsonify(None)
    return jsonify({
        'id': material.id,
        'name': material.name,
        'unit': material.unit,
        'supplier_id': material.supplier_id,
        'supplier_name': material.supplier.name if material.supplier else None,
        'description': material.description,
    })


@raw_materials_bp.route('/materials-list')
@login_required
def materials_list():
    materials = RawMaterial.query.order_by(RawMaterial.name).all()
    return jsonify([{'id': m.id, 'name': m.name, 'unit': m.unit} for m in materials])


# Suppliers CRUD
@raw_materials_bp.route('/suppliers/data')
@login_required
def suppliers_data():
    suppliers = Supplier.query.order_by(Supplier.id.desc()).all()
    return jsonify([_supplier_dict(s) for s in suppliers])


@raw_materials_bp.route('/suppliers/add', methods=['POST'])
@login_required
def suppliers_add():
    data = request.form
    errors = _validate_supplier_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        supplier = Supplier(
            name=data.get('name'),
            mobile=data.get('mobile'),
            address=data.get('address'),
            email=data.get('email') or None,
        )
        db.session.add(supplier)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Supplier added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@raw_materials_bp.route('/suppliers/edit/<int:id>', methods=['POST'])
@login_required
def suppliers_edit(id):
    data = request.form
    errors = _validate_supplier_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        supplier = Supplier.query.get(id)
        supplier.name = data.get('name')
        supplier.mobile = data.get('mobile')
        supplier.address = data.get('address')
        supplier.email = data.get('email') or None
        db.session.commit()
        return jsonify({'success': True, 'message': 'Supplier updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@raw_materials_bp.route('/suppliers/delete/<int:id>', methods=['POST'])
@login_required
def suppliers_delete(id):
    try:
        supplier = Supplier.query.get(id)
        if supplier:
            db.session.delete(supplier)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Supplier deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@raw_materials_bp.route('/suppliers/get/<int:id>')
@login_required
def suppliers_get(id):
    supplier = Supplier.query.get(id)
    if not supplier:
        return jsonify(None)
    return jsonify({
        'id': supplier.id,
        'name': supplier.name,
        'mobile': supplier.mobile,
        'address': supplier.address,
        'email': supplier.email,
    })


@raw_materials_bp.route('/suppliers-list')
@login_required
def suppliers_list():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return jsonify([{'id': s.id, 'name': s.name} for s in suppliers])


# Purchases CRUD
@raw_materials_bp.route('/purchases/data')
@login_required
def purchases_data():
    purchases = Purchase.query.order_by(Purchase.purchase_date.desc(), Purchase.id.desc()).all()
    return jsonify([_purchase_dict(p) for p in purchases])


@raw_materials_bp.route('/purchases/add', methods=['POST'])
@login_required
def purchases_add():
    try:
        data = request.form
        qty = float(data.get('quantity', 0))
        unit_price = float(data.get('unit_price', 0))
        total = qty * unit_price
        material_id = data.get('material_id')
        received_at = datetime.now()

        purchase = Purchase(
            supplier_id=data.get('supplier_id') or None,
            material_id=material_id,
            quantity=qty,
            unit_price=unit_price,
            total_price=total,
            purchase_date=data.get('purchase_date'),
            received_at=received_at,
            notes=data.get('notes'),
        )
        db.session.add(purchase)

        # Update stock (UPSERT semantics)
        stock = RawMaterialStock.query.filter_by(material_id=material_id).first()
        if stock:
            stock.quantity = float(stock.quantity) + qty
        else:
            stock = RawMaterialStock(material_id=material_id, quantity=qty)
            db.session.add(stock)

        db.session.commit()
        return jsonify({'success': True, 'message': 'Purchase recorded successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@raw_materials_bp.route('/purchases/edit/<int:id>', methods=['POST'])
@login_required
def purchases_edit(id):
    try:
        data = request.form
        qty = float(data.get('quantity', 0))
        unit_price = float(data.get('unit_price', 0))
        total = qty * unit_price

        purchase = Purchase.query.get(id)
        purchase.supplier_id = data.get('supplier_id') or None
        purchase.material_id = data.get('material_id')
        purchase.quantity = qty
        purchase.unit_price = unit_price
        purchase.total_price = total
        purchase.purchase_date = data.get('purchase_date')
        purchase.notes = data.get('notes')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Purchase updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@raw_materials_bp.route('/purchases/delete/<int:id>', methods=['POST'])
@login_required
def purchases_delete(id):
    try:
        purchase = Purchase.query.get(id)
        if purchase:
            db.session.delete(purchase)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Purchase record deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@raw_materials_bp.route('/purchases/get/<int:id>')
@login_required
def purchases_get(id):
    purchase = Purchase.query.get(id)
    if not purchase:
        return jsonify(None)
    return jsonify({
        'id': purchase.id,
        'supplier_id': purchase.supplier_id,
        'material_id': purchase.material_id,
        'quantity': float(purchase.quantity) if purchase.quantity is not None else None,
        'unit_price': float(purchase.unit_price) if purchase.unit_price is not None else None,
        'total_price': float(purchase.total_price) if purchase.total_price is not None else None,
        'purchase_date': _iso(purchase.purchase_date),
        'received_at': _iso(purchase.received_at),
        'notes': purchase.notes,
    })


# Stock Transactions
@raw_materials_bp.route('/transactions/data')
@login_required
def transactions_data():
    transactions = RawMaterialTransaction.query.order_by(
        RawMaterialTransaction.date.desc(), RawMaterialTransaction.id.desc()
    ).all()
    return jsonify([_transaction_dict(t) for t in transactions])


@raw_materials_bp.route('/transactions/add', methods=['POST'])
@login_required
def transactions_add():
    data = request.form
    errors = _validate_transaction_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        transaction = RawMaterialTransaction(
            supplier_id=data.get('supplier_id'),
            transaction_type=data.get('transaction_type'),
            date=data.get('date'),
            notes=data.get('notes'),
        )
        db.session.add(transaction)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Transaction recorded successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
