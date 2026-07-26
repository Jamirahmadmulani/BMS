USE bms_db;

-- =============================================
-- EXTRA DEPARTMENTS (5 more)
-- =============================================
INSERT INTO departments (name, description) VALUES
('Security', 'Site security and guard management'),
('Packing', 'Brick packing and wrapping department'),
('Kiln Operations', 'Kiln firing and temperature management'),
('Sales & Marketing', 'Sales team and customer dealing'),
('Store', 'Material store and inventory handling');

-- =============================================
-- EMPLOYEES (33 more → total ~40)
-- =============================================
INSERT INTO employees (name, father_name, cnic, phone, address, department_id, designation, joining_date, status) VALUES
('Ali Hassan',       'Hassan Ahmed',    '35201-1111111-1','0311-1111001','Mohallah Islamabad, Lahore',         1, 'Kiln Worker',        '2021-03-10', 'active'),
('Shahid Iqbal',     'Iqbal Hussain',   '35201-1111112-2','0311-1111002','Street 4, Model Town, Lahore',       2, 'Driver',             '2020-07-15', 'active'),
('Nadeem Butt',      'Zulfiqar Butt',   '35201-1111113-3','0311-1111003','Ravi Road, Lahore',                  3, 'Mechanic',           '2019-11-01', 'active'),
('Riaz Ahmed',       'Ahmed Nawaz',     '35201-1111114-4','0311-1111004','Kot Lakhpat, Lahore',                1, 'Production Worker',  '2022-01-20', 'active'),
('Kamran Shah',      'Shah Mehmood',    '35201-1111115-5','0311-1111005','Shahdara, Lahore',                   4, 'Accountant',         '2021-09-05', 'active'),
('Wasim Akram',      'Akram Gul',       '35201-1111116-6','0311-1111006','Township, Lahore',                   5, 'QC Supervisor',      '2020-04-12', 'active'),
('Faisal Mehmood',   'Mehmood Khan',    '35201-1111117-7','0311-1111007','Gulshan-e-Ravi, Lahore',             6, 'Security Guard',     '2023-02-01', 'active'),
('Zubair Ali',       'Ali Raza',        '35201-1111118-8','0311-1111008','Badami Bagh, Lahore',                7, 'Packing Worker',     '2022-06-10', 'active'),
('Imtiaz Hussain',   'Hussain Bakhsh',  '35201-1111119-9','0311-1111009','Ichhra, Lahore',                     8, 'Kiln Operator',      '2021-05-25', 'active'),
('Waqar Ahmed',      'Ahmed Raza',      '35201-1111120-0','0311-1111010','Harbanspura, Lahore',                9, 'Sales Executive',    '2023-01-15', 'active'),
('Javed Akhtar',     'Akhtar Hussain',  '35202-2222221-1','0312-2221001','Chowburji, Lahore',                  1, 'Production Worker',  '2020-08-01', 'active'),
('Pervaiz Khan',     'Khan Bahadur',    '35202-2222222-2','0312-2221002','Samanabad, Lahore',                  2, 'Driver',             '2021-02-14', 'active'),
('Naveed Hussain',   'Hussain Ali',     '35202-2222223-3','0312-2221003','Walton Road, Lahore',                3, 'Electrician',        '2022-07-07', 'active'),
('Sajjad Mehmood',   'Mehmood Akhtar',  '35202-2222224-4','0312-2221004','Multan Road, Lahore',                4, 'HR Officer',         '2019-12-01', 'active'),
('Aamir Siddiqui',   'Siddiqui Ahmed',  '35202-2222225-5','0312-2221005','Sundar Industrial, Lahore',          5, 'QC Inspector',       '2023-03-20', 'active'),
('Babar Azam',       'Azam Hussain',    '35202-2222226-6','0312-2221006','Gajjumata, Lahore',                  6, 'Security Guard',     '2022-11-11', 'active'),
('Danish Raza',      'Raza Ali',        '35202-2222227-7','0312-2221007','Bund Road, Lahore',                  7, 'Packing Supervisor', '2021-04-30', 'active'),
('Furqan Ahmed',     'Ahmed Khan',      '35202-2222228-8','0312-2221008','Dharampura, Lahore',                 8, 'Kiln Attendant',     '2020-10-05', 'active'),
('Ghulam Mustafa',   'Mustafa Khan',    '35202-2222229-9','0312-2221009','Bhati Gate, Lahore',                 9, 'Sales Officer',      '2023-04-01', 'active'),
('Hamid Raza',       'Raza Hussain',    '35202-2222230-0','0312-2221010','Anarkali, Lahore',                  10, 'Store Keeper',       '2021-08-15', 'active'),
('Ibrahim Shah',     'Shah Nawaz',      '35203-3333331-1','0313-3331001','Shalimar, Lahore',                   1, 'Kiln Worker',        '2022-09-01', 'active'),
('Junaid Ali',       'Ali Hassan',      '35203-3333332-2','0313-3331002','Beghumpura, Lahore',                 2, 'Driver',             '2020-03-25', 'inactive'),
('Khalid Rehman',    'Rehman Gul',      '35203-3333333-3','0313-3331003','Mozang, Lahore',                     3, 'Welder',             '2021-07-19', 'active'),
('Latif Butt',       'Butt Saab',       '35203-3333334-4','0313-3331004','Sheranwala Gate, Lahore',            4, 'Clerk',              '2022-12-01', 'active'),
('Mansoor Ahmed',    'Ahmed Butt',      '35203-3333335-5','0313-3331005','Azam Cloth Market, Lahore',          5, 'Inspector',          '2020-06-10', 'active'),
('Naeem Shahid',     'Shahid Iqbal',    '35203-3333336-6','0313-3331006','Gulberg III, Lahore',                6, 'Guard Supervisor',   '2021-01-01', 'active'),
('Omer Farooq',      'Farooq Ahmed',    '35203-3333337-7','0313-3331007','Cavalry Ground, Lahore',             7, 'Packing Worker',     '2023-05-10', 'active'),
('Parvez Elahi',     'Elahi Khan',      '35203-3333338-8','0313-3331008','Mustafaabad, Lahore',                8, 'Kiln Helper',        '2022-04-04', 'active'),
('Qasim Raza',       'Raza Butt',       '35203-3333339-9','0313-3331009','Raiwind Road, Lahore',               9, 'Sales Coordinator',  '2020-11-20', 'active'),
('Rashid Mehmood',   'Mehmood Butt',    '35203-3333340-0','0313-3331010','Chungi Amar Sidhu, Lahore',         10, 'Store Assistant',    '2021-10-15', 'active'),
('Saeed Ahmad',      'Ahmad Shah',      '35204-4444441-1','0314-4441001','Hanjarwal, Lahore',                   1, 'Production Worker',  '2023-06-01', 'active'),
('Tahir Mahmood',    'Mahmood Ali',     '35204-4444442-2','0314-4441002','Sundar, Lahore',                     2, 'Driver',             '2022-02-28', 'active'),
('Umar Hayat',       'Hayat Khan',      '35204-4444443-3','0314-4441003','Ferozpur Road, Lahore',              3, 'Generator Operator', '2021-03-31', 'active');

-- =============================================
-- ATTENDANCE (60 records, last 30 days)
-- =============================================
INSERT INTO employee_attendance (employee_id, date, status, check_in, check_out) VALUES
(1,'2026-05-17','present','08:00','17:00'),(2,'2026-05-17','present','08:10','17:05'),(3,'2026-05-17','absent',NULL,NULL),
(4,'2026-05-17','present','07:55','17:00'),(5,'2026-05-17','half_day','08:00','12:30'),(6,'2026-05-17','present','08:00','17:00'),
(1,'2026-05-18','present','08:02','17:10'),(2,'2026-05-18','absent',NULL,NULL),(3,'2026-05-18','present','08:15','17:00'),
(4,'2026-05-18','present','08:00','17:00'),(7,'2026-05-18','present','08:00','17:00'),(8,'2026-05-18','half_day','08:00','13:00'),
(1,'2026-05-19','present','07:58','17:00'),(2,'2026-05-19','present','08:05','17:00'),(5,'2026-05-19','present','08:00','17:00'),
(9,'2026-05-19','absent',NULL,NULL),(10,'2026-05-19','present','08:00','17:00'),(11,'2026-05-19','present','08:00','17:00'),
(1,'2026-06-01','present','08:00','17:00'),(2,'2026-06-01','present','08:00','17:00'),(3,'2026-06-01','present','08:00','17:00'),
(4,'2026-06-01','absent',NULL,NULL),(5,'2026-06-01','present','08:00','17:00'),(6,'2026-06-01','present','07:50','17:00'),
(7,'2026-06-02','present','08:00','17:00'),(8,'2026-06-02','present','08:00','17:00'),(9,'2026-06-02','half_day','08:00','13:00'),
(10,'2026-06-02','present','08:00','17:00'),(11,'2026-06-02','absent',NULL,NULL),(12,'2026-06-02','present','08:00','17:00'),
(1,'2026-06-03','present','08:05','17:00'),(2,'2026-06-03','present','08:00','17:00'),(3,'2026-06-03','leave',NULL,NULL),
(13,'2026-06-03','present','08:00','17:00'),(14,'2026-06-03','present','08:00','17:00'),(15,'2026-06-03','present','08:00','17:00'),
(1,'2026-06-09','present','08:00','17:00'),(2,'2026-06-09','present','08:10','17:05'),(4,'2026-06-09','present','08:00','17:00'),
(6,'2026-06-09','absent',NULL,NULL),(7,'2026-06-09','present','08:00','17:00'),(8,'2026-06-09','present','08:00','17:00'),
(1,'2026-06-10','present','08:00','17:00'),(3,'2026-06-10','present','08:00','17:00'),(5,'2026-06-10','half_day','08:00','12:00'),
(9,'2026-06-10','present','08:00','17:00'),(10,'2026-06-10','present','08:00','17:00'),(11,'2026-06-10','present','08:00','17:00'),
(1,'2026-06-11','present','08:00','17:00'),(2,'2026-06-11','present','08:00','17:00'),(12,'2026-06-11','absent',NULL,NULL),
(13,'2026-06-11','present','08:00','17:00'),(14,'2026-06-11','present','08:00','17:00'),(15,'2026-06-11','present','08:00','17:00'),
(1,'2026-06-12','present','07:55','17:00'),(2,'2026-06-12','half_day','08:00','13:00'),(3,'2026-06-12','present','08:00','17:00'),
(4,'2026-06-12','present','08:00','17:00'),(16,'2026-06-12','present','08:00','17:00'),(17,'2026-06-12','present','08:00','17:00');

-- =============================================
-- LEAVE REQUESTS (20 records)
-- =============================================
INSERT INTO employee_leaves (employee_id, leave_type, from_date, to_date, reason, status) VALUES
(1,'Sick Leave','2026-05-05','2026-05-06','Fever and flu','approved'),
(2,'Casual Leave','2026-05-10','2026-05-10','Personal work','approved'),
(3,'Annual Leave','2026-05-12','2026-05-16','Family trip','approved'),
(4,'Emergency Leave','2026-05-20','2026-05-21','Father hospitalized','approved'),
(5,'Sick Leave','2026-05-25','2026-05-26','Back pain','approved'),
(6,'Casual Leave','2026-06-01','2026-06-01','Wedding ceremony','pending'),
(7,'Annual Leave','2026-06-02','2026-06-06','Eid holidays','approved'),
(8,'Sick Leave','2026-06-04','2026-06-04','Stomach issue','approved'),
(9,'Casual Leave','2026-06-07','2026-06-07','CNIC renewal','pending'),
(10,'Emergency Leave','2026-06-08','2026-06-09','Mother unwell','approved'),
(11,'Sick Leave','2026-06-10','2026-06-10','High fever','pending'),
(12,'Casual Leave','2026-04-15','2026-04-15','Bank work','approved'),
(13,'Annual Leave','2026-04-20','2026-04-25','Village visit','rejected'),
(14,'Sick Leave','2026-04-28','2026-04-29','Malaria','approved'),
(15,'Casual Leave','2026-05-02','2026-05-02','House shifting','approved'),
(16,'Emergency Leave','2026-05-15','2026-05-16','Brother accident','approved'),
(17,'Sick Leave','2026-05-22','2026-05-23','Flu','pending'),
(18,'Casual Leave','2026-06-03','2026-06-03','Court appearance','approved'),
(19,'Annual Leave','2026-06-14','2026-06-20','Home town visit','pending'),
(20,'Sick Leave','2026-06-15','2026-06-15','Headache and fever','rejected');

-- =============================================
-- PAYROLL (50 records)
-- =============================================
INSERT INTO payroll (employee_id, month, year, basic_salary, advance_amount, deductions, net_salary, payment_date, payment_type, status, notes) VALUES
-- March 2026
(1,3,2026,25000,0,500,24500,'2026-03-31','monthly','paid','March salary'),
(2,3,2026,22000,0,200,21800,'2026-03-31','monthly','paid','March salary'),
(3,3,2026,28000,1000,0,27000,'2026-03-31','monthly','paid','March salary'),
(4,3,2026,20000,0,400,19600,'2026-03-31','monthly','paid','March salary'),
(5,3,2026,18000,0,0,18000,'2026-03-31','monthly','paid','March salary'),
(6,3,2026,30000,0,600,29400,'2026-03-31','monthly','paid','March salary'),
(7,3,2026,15000,0,0,15000,'2026-03-31','monthly','paid','March salary'),
-- April 2026
(1,4,2026,25000,3000,500,21500,'2026-04-30','monthly','paid','April salary'),
(2,4,2026,22000,0,200,21800,'2026-04-30','monthly','paid','April salary'),
(3,4,2026,28000,0,300,27700,'2026-04-30','monthly','paid','April salary'),
(4,4,2026,20000,2000,0,18000,'2026-04-30','monthly','paid','April salary'),
(5,4,2026,18000,0,200,17800,'2026-04-30','monthly','paid','April salary'),
(6,4,2026,30000,0,0,30000,'2026-04-30','monthly','paid','April salary'),
(8,4,2026,16000,0,0,16000,'2026-04-30','monthly','paid','April salary'),
(9,4,2026,19000,0,300,18700,'2026-04-30','monthly','paid','April salary'),
-- Advance payments April
(1,4,2026,0,5000,0,-5000,'2026-04-10','advance','paid','Advance against salary'),
(3,4,2026,0,3000,0,-3000,'2026-04-15','advance','paid','Medical emergency advance'),
-- May 2026
(1,5,2026,25000,2000,500,22500,'2026-05-31','monthly','paid',NULL),
(2,5,2026,22000,0,0,22000,'2026-05-31','monthly','paid',NULL),
(3,5,2026,28000,1000,300,26700,'2026-05-31','monthly','paid',NULL),
(4,5,2026,20000,0,200,19800,'2026-05-31','monthly','paid',NULL),
(5,5,2026,18000,0,0,18000,'2026-05-31','monthly','paid',NULL),
(6,5,2026,30000,0,500,29500,'2026-05-31','monthly','paid',NULL),
(7,5,2026,15000,0,0,15000,'2026-05-31','monthly','paid',NULL),
(8,5,2026,16000,1000,0,15000,'2026-05-31','monthly','paid',NULL),
(9,5,2026,19000,0,0,19000,'2026-05-31','monthly','paid',NULL),
(10,5,2026,17000,0,300,16700,'2026-05-31','monthly','paid',NULL),
(11,5,2026,21000,0,0,21000,'2026-05-31','monthly','paid',NULL),
(12,5,2026,24000,2000,400,21600,'2026-05-31','monthly','paid',NULL),
-- Weekly payments May
(1,5,2026,0,6000,0,-6000,'2026-05-07','weekly','paid','Week 1'),
(2,5,2026,0,5000,0,-5000,'2026-05-07','weekly','paid','Week 1'),
(4,5,2026,0,4500,0,-4500,'2026-05-14','weekly','paid','Week 2'),
(5,5,2026,0,4000,0,-4000,'2026-05-14','weekly','paid','Week 2'),
-- June 2026
(1,6,2026,25000,5000,0,20000,'2026-06-07','advance','paid','June advance'),
(2,6,2026,22000,0,0,22000,NULL,'monthly','pending',NULL),
(3,6,2026,28000,0,300,27700,NULL,'monthly','pending',NULL),
(4,6,2026,20000,1000,200,18800,NULL,'monthly','pending',NULL),
(5,6,2026,18000,0,0,18000,NULL,'monthly','pending',NULL),
(6,6,2026,30000,0,500,29500,NULL,'monthly','pending',NULL),
(7,6,2026,15000,0,0,15000,NULL,'monthly','pending',NULL),
(8,6,2026,16000,0,0,16000,NULL,'monthly','pending',NULL),
(9,6,2026,19000,2000,0,17000,NULL,'monthly','pending',NULL),
(10,6,2026,17000,0,200,16800,NULL,'monthly','pending',NULL),
(11,6,2026,21000,0,0,21000,NULL,'monthly','pending',NULL),
(12,6,2026,24000,0,400,23600,NULL,'monthly','pending',NULL),
(13,6,2026,26000,0,0,26000,NULL,'monthly','pending',NULL),
(14,6,2026,18500,0,300,18200,NULL,'monthly','pending',NULL),
(15,6,2026,22000,0,0,22000,NULL,'monthly','pending',NULL),
(16,6,2026,20000,1500,0,18500,NULL,'monthly','pending',NULL);

-- =============================================
-- DRIVERS (5 more)
-- =============================================
INSERT INTO drivers (name, license_number, phone, address, status) VALUES
('Arshad Mehmood',  'LHR-2021-44567','0314-5556001','Shahdara, Lahore','active'),
('Tariq Bashir',    'GRW-2019-55678','0314-5556002','Badami Bagh, Lahore','active'),
('Zafar Iqbal',     'LHR-2022-66789','0314-5556003','Ichra, Lahore','active'),
('Bashir Ahmed',    'FSD-2020-77890','0314-5556004','Ravi Road, Lahore','inactive'),
('Noman Ali',       'LHR-2023-88901','0314-5556005','Gulshan Ravi, Lahore','active');

-- =============================================
-- VEHICLES (5 more → total 10)
-- =============================================
INSERT INTO vehicles (vehicle_number, vehicle_type, make, model, year, driver_id, status) VALUES
('LEF-2233','Truck',    'Hino',    '500 Series',2019,4,'active'),
('LEG-4455','Truck',    'Isuzu',   'FVR',       2021,5,'active'),
('LEH-6677','Dumper',   'Sinotruk','HOWO',      2020,6,'active'),
('LEI-8899','Pickup',   'Toyota',  'Revo',      2022,7,'active'),
('LEJ-0011','Forklift', 'Toyota',  '8FBN25',    2019,NULL,'maintenance');

-- =============================================
-- TRIPS (25 records)
-- =============================================
INSERT INTO trips (vehicle_id, driver_id, from_location, to_location, date, purpose, status) VALUES
(1,1,'Kiln Site','DHA Lahore',        '2026-05-20','Brick delivery 5000 pcs','completed'),
(2,2,'Kiln Site','Gujranwala Factory','2026-05-21','Brick delivery 8000 pcs','completed'),
(3,3,'Kiln Site','Sheikhupura',       '2026-05-22','Raw material pickup','completed'),
(1,1,'Kiln Site','Johar Town',        '2026-05-24','Brick delivery 4000 pcs','completed'),
(2,2,'Kiln Site','Faisalabad',        '2026-05-26','Bulk delivery','completed'),
(6,4,'Kiln Site','Raiwind',           '2026-05-28','Clay pickup','completed'),
(7,5,'Kiln Site','Lahore Cantt',      '2026-05-30','Brick delivery 3000 pcs','completed'),
(3,3,'Kiln Site','Kasur',             '2026-06-01','Sand pickup','completed'),
(1,1,'Kiln Site','Bahria Town',       '2026-06-02','Brick delivery 6000 pcs','completed'),
(2,2,'Kiln Site','Valencia Town',     '2026-06-03','Brick delivery 4500 pcs','completed'),
(8,6,'Kiln Site','Sheikhupura',       '2026-06-04','Coal pickup','completed'),
(6,4,'Kiln Site','PAF Colony',        '2026-06-05','Brick delivery 2000 pcs','completed'),
(7,5,'Kiln Site','Model Town',        '2026-06-06','Brick delivery 5000 pcs','completed'),
(1,1,'Kiln Site','Gulberg',           '2026-06-07','Delivery to contractor','completed'),
(3,3,'Kiln Site','Havelian',          '2026-06-08','Clay purchase trip','completed'),
(2,2,'Kiln Site','Sialkot',           '2026-06-09','Bulk brick delivery','completed'),
(8,6,'Kiln Site','Rawalpindi',        '2026-06-10','Material pickup','completed'),
(1,1,'Kiln Site','Wapda Town',        '2026-06-11','Brick delivery 7000 pcs','completed'),
(6,4,'Kiln Site','Township',          '2026-06-12','Brick delivery 3500 pcs','completed'),
(7,5,'Kiln Site','Allama Iqbal Town', '2026-06-13','Delivery','completed'),
(9,7,'Kiln Site','Sundar',            '2026-06-13','Spare parts pickup','completed'),
(1,1,'Kiln Site','DHA Phase 6',       '2026-06-14','Brick delivery','completed'),
(2,2,'Kiln Site','Gujranwala',        '2026-06-15','Delivery in progress','in_progress'),
(3,3,'Kiln Site','Sheikhupura',       '2026-06-16','Raw material pickup','planned'),
(8,6,'Kiln Site','Multan Road',       '2026-06-17','Coal pickup planned','planned');

-- =============================================
-- VEHICLE MAINTENANCE (10 records)
-- =============================================
INSERT INTO vehicle_maintenance (vehicle_id, maintenance_type, date, cost, description, status) VALUES
(1,'Oil Change',         '2026-04-15',  3500,'Engine oil and filter','completed'),
(2,'Tire Replacement',   '2026-04-20', 18000,'Front two tires replaced','completed'),
(3,'Battery',            '2026-04-25',  8500,'Battery replaced','completed'),
(4,'Engine Repair',      '2026-05-01', 45000,'Engine overhaul','pending'),
(1,'Brake Service',      '2026-05-10',  5500,'Brake pads replaced','completed'),
(6,'Oil Change',         '2026-05-15',  3200,'Routine oil change','completed'),
(7,'AC Repair',          '2026-05-20',  7000,'AC gas refilled','completed'),
(2,'Wheel Alignment',    '2026-05-28',  2500,'Alignment and balancing','completed'),
(8,'Engine Service',     '2026-06-05', 12000,'Full engine service','completed'),
(9,'Tire Replacement',   '2026-06-10', 22000,'All four tires replaced','completed');

-- =============================================
-- RAW MATERIALS (5 more → total 10)
-- =============================================
INSERT INTO raw_materials (name, unit, description) VALUES
('Gypsum',    'kg',     'Used in brick mixture for strength'),
('Fly Ash',   'kg',     'Byproduct used to reduce clay usage'),
('Lime',      'kg',     'Calcium oxide for brick quality'),
('Sawdust',   'kg',     'Used as fuel additive in kiln'),
('Pebbles',   'kg',     'Coarse aggregate for brick texture');

-- =============================================
-- SUPPLIERS (5 more → total 10)
-- =============================================
INSERT INTO suppliers (name, phone, address, email, status) VALUES
('Sindh Clay Traders',   '0305-1234001','Hyderabad, Sindh',         'sindhclay@gmail.com','active'),
('Punjabi Fuel Depot',   '0306-1234002','Ferozpur Road, Lahore',    'punjabifuel@gmail.com','active'),
('National Sand Co.',    '0307-1234003','Canal Road, Lahore',       NULL,'active'),
('Green Ash Suppliers',  '0308-1234004','SITE Area, Karachi',       'greenash@gmail.com','active'),
('Kashmir Lime Works',   '0309-1234005','Murree Road, Rawalpindi',  'kashmirlime@gmail.com','active');

-- =============================================
-- PURCHASES (25 records)
-- =============================================
INSERT INTO purchases (supplier_id, material_id, quantity, unit_price, total_price, purchase_date, notes) VALUES
(1,1,8000,2.80,22400,'2026-04-05','Clay purchase April batch 1'),
(2,2,4000,1.50, 6000,'2026-04-08','Sand for production'),
(3,3,3000,16.00,48000,'2026-04-10','Coal for kiln April'),
(4,4,1500,3.50, 5250,'2026-04-12','Rice husk April'),
(6,6,2000,5.00,10000,'2026-04-15','Gypsum purchase'),
(1,1,6000,2.80,16800,'2026-04-20','Clay April batch 2'),
(3,3,2500,16.00,40000,'2026-04-25','Coal mid April'),
(7,7,1000,4.00, 4000,'2026-04-28','Fly ash purchase'),
(2,2,5000,1.50, 7500,'2026-05-02','Sand May batch 1'),
(1,1,9000,2.90,26100,'2026-05-05','Clay May batch 1'),
(3,3,4000,16.50,66000,'2026-05-08','Coal May large order'),
(4,4,2000,3.50, 7000,'2026-05-10','Rice husk May'),
(5,5,500, 12.00, 6000,'2026-05-12','Water supply'),
(8,8,1500,5.50, 8250,'2026-05-15','Lime purchase'),
(6,6,1000,5.00, 5000,'2026-05-18','Gypsum restock'),
(1,1,7000,2.90,20300,'2026-05-20','Clay May batch 2'),
(2,2,3000,1.50, 4500,'2026-05-22','Sand restock'),
(3,3,3500,16.50,57750,'2026-05-25','Coal May batch 2'),
(7,7,800, 4.00, 3200,'2026-05-28','Fly ash restock'),
(9,9,600, 8.00, 4800,'2026-05-30','Sawdust purchase'),
(1,1,10000,2.90,29000,'2026-06-03','Clay June batch 1'),
(3,3,5000,17.00,85000,'2026-06-05','Coal June large order'),
(2,2,4000,1.60, 6400,'2026-06-08','Sand June batch'),
(4,4,1500,3.50, 5250,'2026-06-10','Rice husk June'),
(8,8,2000,5.50,11000,'2026-06-12','Lime June purchase');

-- Update raw material stock after purchases
UPDATE raw_material_stock SET quantity = quantity + 40000 WHERE material_id = 1;
UPDATE raw_material_stock SET quantity = quantity + 19000 WHERE material_id = 2;
UPDATE raw_material_stock SET quantity = quantity + 18000 WHERE material_id = 3;
UPDATE raw_material_stock SET quantity = quantity + 7000  WHERE material_id = 4;
UPDATE raw_material_stock SET quantity = quantity + 500   WHERE material_id = 5;
INSERT INTO raw_material_stock (material_id, quantity) VALUES (6,3000),(7,1800),(8,3500),(9,600),(10,600)
ON DUPLICATE KEY UPDATE quantity = quantity;

-- =============================================
-- RAW MATERIAL TRANSACTIONS (20 records)
-- =============================================
INSERT INTO raw_material_transactions (material_id, transaction_type, quantity, date, reference, notes) VALUES
(1,'in', 8000,'2026-04-05','PO-004','Clay purchase April'),
(1,'out',5000,'2026-04-10','PRD-102','Production batch 102'),
(2,'in', 4000,'2026-04-08','PO-005','Sand April'),
(3,'in', 3000,'2026-04-10','PO-006','Coal April'),
(3,'out',1500,'2026-04-15','KLN-002','Kiln consumption'),
(1,'in', 6000,'2026-04-20','PO-007','Clay April batch 2'),
(1,'out',4000,'2026-04-25','PRD-103','Production batch 103'),
(4,'in', 1500,'2026-04-12','PO-008','Rice husk April'),
(4,'out', 800,'2026-04-28','KLN-003','Kiln fuel usage'),
(1,'in', 9000,'2026-05-05','PO-009','Clay May batch 1'),
(3,'in', 4000,'2026-05-08','PO-010','Coal May'),
(3,'out',2500,'2026-05-15','KLN-004','Kiln May firing'),
(1,'out',6000,'2026-05-20','PRD-104','Production batch 104'),
(2,'in', 5000,'2026-05-02','PO-011','Sand May'),
(2,'out',3000,'2026-05-25','PRD-105','Mixed in production 105'),
(1,'in',10000,'2026-06-03','PO-012','Clay June batch 1'),
(3,'in', 5000,'2026-06-05','PO-013','Coal June'),
(3,'out',2000,'2026-06-10','KLN-005','Kiln June consumption'),
(1,'out',7000,'2026-06-12','PRD-106','Production batch 106'),
(4,'in', 1500,'2026-06-10','PO-014','Rice husk June');

-- =============================================
-- STORAGE TRANSACTIONS (20 more)
-- =============================================
INSERT INTO storage_transactions (location_id, item_name, transaction_type, quantity, date, notes) VALUES
(1,'Standard Red Bricks','in', 8000,'2026-04-10','Production batch 102'),
(1,'Standard Red Bricks','out',5000,'2026-04-15','Sale to contractor A'),
(5,'Export Quality Bricks','in',10000,'2026-04-18','Production for export'),
(5,'Export Quality Bricks','out',8000,'2026-04-25','Export shipment'),
(1,'Jumbo Bricks','in',3000,'2026-05-01','Production batch 103'),
(1,'Jumbo Bricks','out',2000,'2026-05-05','Local sale'),
(2,'Clay','in',8000,'2026-05-06','Clay stock in'),
(2,'Clay','out',5000,'2026-05-12','Sent to production'),
(3,'Diesel','in',1500,'2026-05-08','Fuel purchase'),
(3,'Diesel','out',800,'2026-05-15','Kiln and vehicle use'),
(1,'Standard Red Bricks','in',12000,'2026-05-20','Production batch 104'),
(1,'Standard Red Bricks','out',7000,'2026-05-26','Sale to DHA project'),
(4,'Bearing Set','in',30,'2026-05-18','Spare parts restock'),
(4,'Bearing Set','out',15,'2026-05-25','Used in maintenance'),
(5,'Export Quality Bricks','in',15000,'2026-06-01','June production'),
(1,'Standard Red Bricks','in',10000,'2026-06-05','Production batch 105'),
(1,'Standard Red Bricks','out',6000,'2026-06-10','Delivery to Bahria Town'),
(2,'Sand','in',5000,'2026-06-08','Sand restock'),
(3,'Diesel','in',2000,'2026-06-09','Fuel restock'),
(3,'Diesel','out',600,'2026-06-13','Vehicle and kiln');
