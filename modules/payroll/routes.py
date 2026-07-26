from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
from datetime import date
from sqlalchemy import extract

from extensions import db
from models import Payroll, Employee, Department, BrickProduction

payroll_bp = Blueprint('payroll', __name__, url_prefix='/payroll')


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


def _payroll_to_dict(p):
    d = {c.name: getattr(p, c.name) for c in Payroll.__table__.columns}
    return _serialize(d)


def _validate_payroll_form(data):
    errors = []
    if not data.get('employee_id'):
        errors.append('Employee Name is mandatory.')
    if not data.get('month'):
        errors.append('Month is mandatory.')
    if not data.get('year'):
        errors.append('Year is mandatory.')
    if data.get('payment_type') not in ('monthly', 'weekly'):
        errors.append('Payment Type is mandatory.')
    if data.get('status') not in ('pending', 'paid'):
        errors.append('Status is mandatory.')
    if not data.get('payment_date'):
        errors.append('Payment Date is mandatory.')
    return errors


def _sum_prior_advances(employee_id, month, year):
    total = db.session.query(db.func.coalesce(db.func.sum(Payroll.advance_amount), 0)).filter(
        Payroll.employee_id == employee_id,
        Payroll.payment_type == 'advance',
        Payroll.month == month,
        Payroll.year == year,
    ).scalar()
    return float(total or 0)


@payroll_bp.route('/')
@login_required
def index():
    return render_template('payroll/list.html')


@payroll_bp.route('/data')
@login_required
def data():
    records = Payroll.query.order_by(Payroll.year.desc(), Payroll.month.desc(), Payroll.id.desc()).all()
    result = []
    for p in records:
        d = _payroll_to_dict(p)
        d['employee_name'] = p.employee.name if p.employee else None
        d['designation'] = p.employee.designation if p.employee else None
        d['department_name'] = p.employee.department.name if p.employee and p.employee.department else None
        result.append(d)
    return jsonify(result)


@payroll_bp.route('/add', methods=['POST'])
@login_required
def add():
    data = request.form
    errors = _validate_payroll_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        total_bricks = int(data.get('total_bricks', 0) or 0)
        rate_per_100 = float(data.get('rate_per_100', 0) or 0)
        calculated_salary = (total_bricks / 100.0) * rate_per_100
        advance = _sum_prior_advances(data.get('employee_id'), data.get('month'), data.get('year'))

        p = Payroll(
            employee_id=data.get('employee_id'),
            month=data.get('month'),
            year=data.get('year'),
            total_bricks=total_bricks,
            rate_per_100=rate_per_100,
            calculated_salary=calculated_salary,
            basic_salary=calculated_salary,
            advance_amount=advance,
            payment_date=data.get('payment_date') or None,
            payment_type=data.get('payment_type', 'monthly'),
            status=data.get('status', 'pending'),
            notes=data.get('notes')
        )
        db.session.add(p)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Payroll record added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@payroll_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    data = request.form
    errors = _validate_payroll_form(data)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        total_bricks = int(data.get('total_bricks', 0) or 0)
        rate_per_100 = float(data.get('rate_per_100', 0) or 0)
        calculated_salary = (total_bricks / 100.0) * rate_per_100
        advance = _sum_prior_advances(data.get('employee_id'), data.get('month'), data.get('year'))

        p = Payroll.query.get(id)
        if p:
            p.employee_id = data.get('employee_id')
            p.month = data.get('month')
            p.year = data.get('year')
            p.total_bricks = total_bricks
            p.rate_per_100 = rate_per_100
            p.calculated_salary = calculated_salary
            p.basic_salary = calculated_salary
            p.advance_amount = advance
            p.payment_date = data.get('payment_date') or None
            p.payment_type = data.get('payment_type', 'monthly')
            p.status = data.get('status', 'pending')
            p.notes = data.get('notes')
            db.session.commit()
        return jsonify({'success': True, 'message': 'Payroll record updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@payroll_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try:
        p = Payroll.query.get(id)
        if p:
            db.session.delete(p)
            db.session.commit()
        return jsonify({'success': True, 'message': 'Payroll record deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@payroll_bp.route('/get/<int:id>')
@login_required
def get_one(id):
    p = Payroll.query.get(id)
    if not p:
        return jsonify(None)
    d = _payroll_to_dict(p)
    d['employee_name'] = p.employee.name if p.employee else None
    d['department_name'] = p.employee.department.name if p.employee and p.employee.department else None
    return jsonify(d)


@payroll_bp.route('/employees-list')
@login_required
def employees_list():
    employees = Employee.query.filter_by(status='active').order_by(Employee.name).all()
    result = []
    for e in employees:
        result.append({
            'id': e.id,
            'name': e.name,
            'designation': e.designation,
            'department_name': e.department.name if e.department else None,
            'rate_per_100': e.department.rate_per_100 if e.department else None,
        })
    return jsonify(result)


@payroll_bp.route('/slip/<int:id>')
@login_required
def salary_slip(id):
    p = Payroll.query.get(id)
    if not p:
        return jsonify(None)
    d = _payroll_to_dict(p)
    d['employee_name'] = p.employee.name if p.employee else None
    d['department_name'] = p.employee.department.name if p.employee and p.employee.department else None
    return jsonify(d)


@payroll_bp.route('/production-summary')
@login_required
def production_summary():
    employee_id = request.args.get('employee_id')
    month = request.args.get('month')
    year = request.args.get('year')

    total_bricks = db.session.query(
        db.func.coalesce(db.func.sum(BrickProduction.bricks_produced), 0)
    ).filter(
        BrickProduction.employee_id == employee_id,
        extract('month', BrickProduction.production_date) == month,
        extract('year', BrickProduction.production_date) == year
    ).scalar()
    total_bricks = int(total_bricks)

    emp = Employee.query.get(employee_id)
    rate_per_100 = float(emp.department.rate_per_100 or 0) if emp and emp.department and emp.department.rate_per_100 else 0
    calculated_salary = (total_bricks / 100.0) * rate_per_100
    advance = _sum_prior_advances(employee_id, month, year)

    return jsonify({
        'total_bricks': total_bricks,
        'rate_per_100': rate_per_100,
        'calculated_salary': round(calculated_salary, 2),
        'advance_amount': advance,
        'department_name': emp.department.name if emp and emp.department else None,
    })


@payroll_bp.route('/from-production', methods=['POST'])
@login_required
def from_production():
    try:
        data = request.form
        employee_id = data.get('employee_id')
        month = data.get('month')
        year = data.get('year')

        total_bricks = int(db.session.query(
            db.func.coalesce(db.func.sum(BrickProduction.bricks_produced), 0)
        ).filter(
            BrickProduction.employee_id == employee_id,
            extract('month', BrickProduction.production_date) == month,
            extract('year', BrickProduction.production_date) == year
        ).scalar())

        if total_bricks == 0:
            return jsonify({'success': False, 'message': 'No production records found for this employee in selected month/year'})

        emp = Employee.query.get(employee_id)
        rate_per_100 = float(emp.department.rate_per_100 or 0) if emp and emp.department else 0

        calculated_salary = (total_bricks / 100.0) * rate_per_100
        advance = _sum_prior_advances(employee_id, month, year)

        p = Payroll(
            employee_id=employee_id,
            month=month,
            year=year,
            total_bricks=total_bricks,
            rate_per_100=rate_per_100,
            calculated_salary=calculated_salary,
            basic_salary=calculated_salary,
            advance_amount=advance,
            payment_date=data.get('payment_date') or None,
            payment_type='monthly',
            status='pending',
            notes='Auto-generated from production records'
        )
        db.session.add(p)
        db.session.commit()
        return jsonify({'success': True, 'message': f'Payroll generated — {total_bricks:,} bricks × Rs.{rate_per_100}/100 = Rs.{calculated_salary:,.2f}'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@payroll_bp.route('/mark-paid/<int:id>', methods=['POST'])
@login_required
def mark_paid(id):
    try:
        p = Payroll.query.get(id)
        if p:
            p.status = 'paid'
            p.payment_date = date.today()
            db.session.commit()
        return jsonify({'success': True, 'message': 'Payment marked as paid'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})
