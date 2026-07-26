from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from extensions import db
from models import Department, Employee

BRICK_SIZES = ('4 Inch', '6 Inch', '8 Inch', '9 Inch')

departments_bp = Blueprint('departments', __name__, url_prefix='/departments')


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


def _dept_to_dict(d):
    return {
        'id': d.id,
        'name': d.name,
        'description': d.description,
        'brick_size': d.brick_size,
        'rate_per_100': float(d.rate_per_100) if d.rate_per_100 is not None else None,
        'created_at': d.created_at.isoformat() if d.created_at else None,
    }


def _validate_department_form(data):
    errors = []
    if not data.get('name', '').strip():
        errors.append('Department Name is required.')
    if data.get('brick_size') not in BRICK_SIZES:
        errors.append('Brick Size must be selected from the dropdown list.')
    rate = data.get('rate_per_100', '').strip()
    try:
        float(rate)
    except (TypeError, ValueError):
        errors.append('Rate per 100 Bricks must be a valid numeric value.')
    return errors


@departments_bp.route('/')
@login_required
def index():
    return render_template('departments/list.html')


@departments_bp.route('/data')
@login_required
def data():
    departments = Department.query.order_by(Department.id.desc()).all()
    result = []
    for d in departments:
        row = _dept_to_dict(d)
        row['employee_count'] = Employee.query.filter_by(department_id=d.id, status='active').count()
        result.append(row)
    return jsonify(result)


@departments_bp.route('/add', methods=['POST'])
@login_required
def add():
    data = request.form
    errors = _validate_department_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        dept = Department(
            name=data.get('name'),
            description=data.get('description'),
            brick_size=data.get('brick_size'),
            rate_per_100=data.get('rate_per_100'),
        )
        db.session.add(dept)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Department added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@departments_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    data = request.form
    errors = _validate_department_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        dept = Department.query.get(id)
        if dept:
            dept.name = data.get('name')
            dept.description = data.get('description')
            dept.brick_size = data.get('brick_size')
            dept.rate_per_100 = data.get('rate_per_100')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Department updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@departments_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try:
        dept = Department.query.get(id)
        if dept:
            db.session.delete(dept)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Department deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@departments_bp.route('/get/<int:id>')
@login_required
def get_one(id):
    dept = Department.query.get(id)
    if dept:
        return jsonify(_dept_to_dict(dept))
    return jsonify(None)


@departments_bp.route('/employees-list')
@login_required
def employees_list():
    employees = Employee.query.filter_by(status='active').order_by(Employee.name).all()
    return jsonify([{'id': e.id, 'name': e.name} for e in employees])


@departments_bp.route('/<int:id>/employees')
@login_required
def department_employees(id):
    employees = Employee.query.filter_by(department_id=id).all()
    result = []
    for e in employees:
        row = e.to_dict()
        row['department_name'] = e.department.name if e.department else None
        result.append(row)
    return jsonify(result)
