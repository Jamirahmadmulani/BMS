from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import os, uuid, re
from werkzeug.utils import secure_filename
from extensions import db
from models import Employee, Department

employees_bp = Blueprint('employees', __name__, url_prefix='/employees')

UPLOAD_PHOTOS = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'uploads', 'photos')
UPLOAD_NOTARY = os.path.join(os.path.dirname(__file__), '..', '..', 'static', 'uploads', 'notary')

def _ensure_dirs():
    os.makedirs(UPLOAD_PHOTOS, exist_ok=True)
    os.makedirs(UPLOAD_NOTARY, exist_ok=True)

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

def _save_file(file, folder):
    """Save uploaded file with uuid name. Returns filename or None."""
    if not file or file.filename == '':
        return None
    ext = secure_filename(file.filename).rsplit('.', 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file.save(os.path.join(folder, filename))
    return filename


def _validate_employee_form(data, files, require_files):
    errors = []
    if not data.get('name', '').strip():
        errors.append('Employee Name is required.')
    if not re.fullmatch(r'\d{10}', data.get('mobile', '').strip()):
        errors.append('Contact Number must contain exactly 10 digits.')
    if not re.fullmatch(r'\d{12}', data.get('aadhar_number', '').strip()):
        errors.append('Aadhaar Number must contain exactly 12 digits.')
    if not data.get('department_id'):
        errors.append('Department must be selected.')
    if not data.get('joining_date'):
        errors.append('Joining Date is required.')
    if not data.get('address', '').strip():
        errors.append('Address is required.')
    if data.get('status') not in ('active', 'inactive'):
        errors.append('Status must be selected.')

    aadhar_file = files.get('photograph')
    if aadhar_file and aadhar_file.filename:
        if not re.search(r'\.(jpg|jpeg|png)$', aadhar_file.filename, re.IGNORECASE):
            errors.append('Aadhaar Card Upload accepts only JPG, JPEG, and PNG files.')
    elif require_files:
        errors.append('Aadhaar Card Upload is required.')

    notary_file = files.get('notary_pdf')
    if notary_file and notary_file.filename:
        if not re.search(r'\.pdf$', notary_file.filename, re.IGNORECASE):
            errors.append('Notary PDF Upload accepts only PDF files.')
    elif require_files:
        errors.append('Notary PDF Upload is required.')

    return errors


@employees_bp.route('/')
@login_required
def index():
    return render_template('employees/list.html')


@employees_bp.route('/data')
@login_required
def data():
    employees = Employee.query.order_by(Employee.id.desc()).all()
    result = []
    for e in employees:
        d = e.to_dict()
        d['department_name'] = e.department.name if e.department else None
        result.append(d)
    return jsonify(result)


@employees_bp.route('/add', methods=['POST'])
@login_required
def add():
    _ensure_dirs()
    data = request.form
    errors = _validate_employee_form(data, request.files, require_files=True)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        photograph = _save_file(request.files.get('photograph'), UPLOAD_PHOTOS)
        notary_pdf = _save_file(request.files.get('notary_pdf'), UPLOAD_NOTARY)
        emp = Employee(
            name=data.get('name'), mobile=data.get('mobile'),
            aadhar_number=data.get('aadhar_number'), address=data.get('address'),
            department_id=data.get('department_id') or None,
            joining_date=data.get('joining_date') or None,
            status=data.get('status', 'active'),
            photograph=photograph, notary_pdf=notary_pdf
        )
        db.session.add(emp)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Employee added successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@employees_bp.route('/edit/<int:id>', methods=['POST'])
@login_required
def edit(id):
    _ensure_dirs()
    data = request.form
    errors = _validate_employee_form(data, request.files, require_files=False)
    if errors:
        return jsonify({'success': False, 'message': ' '.join(errors)})
    try:
        emp = Employee.query.get(id)
        if not emp:
            return jsonify({'success': False, 'message': 'Employee not found'})

        photograph = _save_file(request.files.get('photograph'), UPLOAD_PHOTOS)
        notary_pdf = _save_file(request.files.get('notary_pdf'), UPLOAD_NOTARY)

        emp.name = data.get('name')
        emp.mobile = data.get('mobile')
        emp.aadhar_number = data.get('aadhar_number')
        emp.address = data.get('address')
        emp.department_id = data.get('department_id') or None
        emp.joining_date = data.get('joining_date') or None
        emp.status = data.get('status', 'active')
        if photograph:
            emp.photograph = photograph
        if notary_pdf:
            emp.notary_pdf = notary_pdf

        db.session.commit()
        return jsonify({'success': True, 'message': 'Employee updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@employees_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete(id):
    try:
        emp = Employee.query.get(id)
        if emp:
            db.session.delete(emp)
            db.session.commit()
        return jsonify({'success': True, 'message': 'Employee deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})


@employees_bp.route('/get/<int:id>')
@login_required
def get_one(id):
    emp = Employee.query.get(id)
    return jsonify(emp.to_dict() if emp else None)


@employees_bp.route('/departments-list')
@login_required
def departments_list():
    departments = Department.query.order_by(Department.name).all()
    return jsonify([{'id': d.id, 'name': d.name} for d in departments])


@employees_bp.route('/list')
@login_required
def employee_list():
    employees = Employee.query.filter_by(status='active').order_by(Employee.name).all()
    return jsonify([{
        'id': e.id, 'name': e.name, 'designation': e.designation,
        'department_name': e.department.name if e.department else None,
    } for e in employees])
