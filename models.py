from datetime import datetime
from extensions import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='admin')
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    brick_size = db.Column(db.Enum('4 Inch', '6 Inch', '8 Inch', '9 Inch', name='brick_size_enum'))
    rate_per_100 = db.Column(db.Numeric(10, 2), default=0)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    employees = db.relationship('Employee', back_populates='department', foreign_keys='Employee.department_id')


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20))
    aadhar_number = db.Column(db.String(20))
    photograph = db.Column(db.String(255))
    notary_pdf = db.Column(db.String(255))
    address = db.Column(db.Text)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id', ondelete='SET NULL'))
    designation = db.Column(db.String(100))
    joining_date = db.Column(db.Date)
    status = db.Column(db.Enum('active', 'inactive', name='employee_status_enum'), default='active')

    department = db.relationship('Department', back_populates='employees', foreign_keys=[department_id])
    attendance = db.relationship('EmployeeAttendance', backref='employee', cascade='all, delete-orphan')
    leaves = db.relationship('EmployeeLeave', backref='employee', cascade='all, delete-orphan')
    payroll_records = db.relationship('Payroll', backref='employee', cascade='all, delete-orphan')
    production_records = db.relationship('BrickProduction', backref='employee', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id, 'name': self.name, 'mobile': self.mobile,
            'aadhar_number': self.aadhar_number, 'photograph': self.photograph,
            'notary_pdf': self.notary_pdf, 'address': self.address,
            'department_id': self.department_id, 'designation': self.designation,
            'joining_date': self.joining_date.isoformat() if self.joining_date else None,
            'status': self.status,
        }


class EmployeeAttendance(db.Model):
    __tablename__ = 'employee_attendance'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    date = db.Column(db.Date)
    status = db.Column(db.Enum('present', 'absent', 'half_day', 'leave', name='attendance_status_enum'), default='present')
    check_in = db.Column(db.Time)
    check_out = db.Column(db.Time)


class EmployeeLeave(db.Model):
    __tablename__ = 'employee_leaves'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    leave_type = db.Column(db.String(50))
    from_date = db.Column(db.Date)
    to_date = db.Column(db.Date)
    reason = db.Column(db.Text)
    status = db.Column(db.Enum('pending', 'approved', 'rejected', name='leave_status_enum'), default='pending')


class StorageLocation(db.Model):
    __tablename__ = 'storage_locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location_type = db.Column(db.Enum('A1', 'A2', 'Other', name='location_type_enum'), default='Other')
    capacity = db.Column(db.Integer)
    description = db.Column(db.Text)

    stock_items = db.relationship('StorageStock', backref='location', cascade='all, delete-orphan')
    transactions = db.relationship('StorageTransaction', backref='location', cascade='all, delete-orphan')
    production_records = db.relationship('BrickProduction', backref='location', cascade='all, delete-orphan')
    deductions = db.relationship('StorageDeduction', backref='location', cascade='all, delete-orphan')


class StorageStock(db.Model):
    __tablename__ = 'storage_stock'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('storage_locations.id', ondelete='CASCADE'))
    item_name = db.Column(db.String(100))
    item_type = db.Column(db.String(50))
    quantity = db.Column(db.Numeric(10, 2), default=0)
    unit = db.Column(db.String(20))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


class StorageTransaction(db.Model):
    __tablename__ = 'storage_transactions'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('storage_locations.id', ondelete='CASCADE'))
    item_name = db.Column(db.String(100))
    transaction_type = db.Column(db.Enum('in', 'out', name='storage_txn_type_enum'), default='in')
    quantity = db.Column(db.Numeric(10, 2))
    date = db.Column(db.Date)
    notes = db.Column(db.Text)


class BrickProduction(db.Model):
    __tablename__ = 'brick_production'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('storage_locations.id'), nullable=False)
    production_date = db.Column(db.Date, nullable=False)
    bricks_produced = db.Column(db.Integer, default=0)
    department_type = db.Column(db.String(100), nullable=False)
    brick_size = db.Column(db.Enum('4 Inch', '6 Inch', '8 Inch', '9 Inch', name='production_brick_size_enum'))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


class StorageDeduction(db.Model):
    __tablename__ = 'storage_deductions'
    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey('storage_locations.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    previous_quantity = db.Column(db.Numeric(10, 2), nullable=False)
    deducted_quantity = db.Column(db.Numeric(10, 2), nullable=False)
    current_quantity = db.Column(db.Numeric(10, 2), nullable=False)
    payment_amount = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    payment_date = db.Column(db.Date, nullable=False)
    payment_status = db.Column(db.Enum('Online', 'Cash', 'Pending', name='deduction_payment_status_enum'), nullable=False, default='Pending')
    reminder_date = db.Column(db.Date)
    reason = db.Column(db.String(255))
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    employee = db.relationship('Employee')


class Payroll(db.Model):
    __tablename__ = 'payroll'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'))
    department_type = db.Column(db.Enum('Maker', 'Carrier', 'Converter', 'Transporter', 'Other', name='payroll_dept_type_enum'), default='Other')
    total_bricks = db.Column(db.Integer, default=0)
    rate_per_100 = db.Column(db.Numeric(10, 2), default=0)
    calculated_salary = db.Column(db.Numeric(10, 2), default=0)
    month = db.Column(db.Integer)
    year = db.Column(db.Integer)
    basic_salary = db.Column(db.Numeric(10, 2))
    advance_amount = db.Column(db.Numeric(10, 2), default=0)
    payment_date = db.Column(db.Date)
    payment_type = db.Column(db.Enum('weekly', 'advance', 'monthly', name='payment_type_enum'), default='monthly')
    status = db.Column(db.Enum('pending', 'paid', name='payroll_status_enum'), default='pending')
    notes = db.Column(db.Text)


class Driver(db.Model):
    __tablename__ = 'drivers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    license_number = db.Column(db.String(50))
    mobile = db.Column(db.String(20))
    aadhar_number = db.Column(db.String(20))
    aadhar_photo = db.Column(db.String(255))
    license_photo = db.Column(db.String(255))
    address = db.Column(db.Text)
    status = db.Column(db.Enum('active', 'inactive', name='driver_status_enum'), default='active')

    vehicles = db.relationship('Vehicle', backref='driver')
    trips = db.relationship('Trip', backref='driver')


class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_number = db.Column(db.String(50), nullable=False)
    vehicle_name = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id', ondelete='SET NULL'))
    insurance = db.Column(db.String(100))
    road_tax = db.Column(db.String(100))
    puc = db.Column(db.String(100))
    fuel_type = db.Column(db.Enum('Petrol', 'Diesel', 'Gas', 'Battery', name='vehicle_fuel_type_enum'))
    status = db.Column(db.Enum('active', 'inactive', name='vehicle_status_enum'), nullable=False, default='active')

    trips = db.relationship('Trip', backref='vehicle', cascade='all, delete-orphan')
    maintenance_records = db.relationship('VehicleMaintenance', backref='vehicle', cascade='all, delete-orphan')
    investments = db.relationship('VehicleInvestment', backref='vehicle', cascade='all, delete-orphan')


class Trip(db.Model):
    __tablename__ = 'trips'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='CASCADE'))
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id', ondelete='SET NULL'))
    from_location = db.Column(db.String(100))
    to_location = db.Column(db.String(100))
    date = db.Column(db.Date)
    purpose = db.Column(db.Text)
    status = db.Column(db.Enum('planned', 'in_progress', 'completed', 'cancelled', name='trip_status_enum'), default='planned')
    days = db.Column(db.Integer, default=1)
    fuel_expense = db.Column(db.Numeric(10, 2), default=0)
    driver_expense = db.Column(db.Numeric(10, 2), default=0)
    other_expense = db.Column(db.Numeric(10, 2), default=0)
    return_date = db.Column(db.Date)


class VehicleMaintenance(db.Model):
    __tablename__ = 'vehicle_maintenance'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id', ondelete='CASCADE'))
    maintenance_type = db.Column(db.String(100))
    date = db.Column(db.Date)
    cost = db.Column(db.Numeric(10, 2))
    description = db.Column(db.Text)


class VehicleInvestment(db.Model):
    __tablename__ = 'vehicle_investments'
    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'), nullable=False)
    investment_type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    investment_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


class RawMaterial(db.Model):
    __tablename__ = 'raw_materials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='SET NULL'))
    description = db.Column(db.Text)

    supplier = db.relationship('Supplier', foreign_keys=[supplier_id])
    stock = db.relationship('RawMaterialStock', backref='material', uselist=False, cascade='all, delete-orphan')
    purchases = db.relationship('Purchase', backref='material', cascade='all, delete-orphan')


class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(20))
    address = db.Column(db.Text)
    email = db.Column(db.String(100))

    purchases = db.relationship('Purchase', backref='supplier')


class Purchase(db.Model):
    __tablename__ = 'purchases'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='SET NULL'))
    material_id = db.Column(db.Integer, db.ForeignKey('raw_materials.id', ondelete='CASCADE'))
    quantity = db.Column(db.Numeric(10, 2))
    unit_price = db.Column(db.Numeric(10, 2))
    total_price = db.Column(db.Numeric(10, 2))
    purchase_date = db.Column(db.Date)
    received_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    notes = db.Column(db.Text)


class RawMaterialStock(db.Model):
    __tablename__ = 'raw_material_stock'
    id = db.Column(db.Integer, primary_key=True)
    material_id = db.Column(db.Integer, db.ForeignKey('raw_materials.id', ondelete='CASCADE'), unique=True)
    quantity = db.Column(db.Numeric(10, 2), default=0)
    updated_at = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=datetime.utcnow)


class RawMaterialTransaction(db.Model):
    __tablename__ = 'raw_material_transactions'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'))
    transaction_type = db.Column(db.Enum('Online', 'Cash', 'RTGS', 'Cheque', name='material_txn_type_enum'), nullable=False, default='Cash')
    date = db.Column(db.Date)
    notes = db.Column(db.Text)

    supplier = db.relationship('Supplier')
