USE employee_management_db;

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    position VARCHAR(100) NOT NULL,
    hire_date DATE NOT NULL,
    department_id INT,    
     FOREIGN KEY (department_id) REFERENCES departments(id)

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    location VARCHAR(100) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO departments (name, location) VALUES
('Brøndby', 'Storkøbenhavn'),
('Aarhus', 'Jylland'),
('Odense', 'Fyn');

INSERT INTO employees (first_name, last_name, position, hire_date, department_id) VALUES
('Lars', 'Hansen', 'Leder', '2017-03-15', 1),
('Mette', 'Jensen', 'Receptionist', '2019-07-22', 2),
('Klaus', 'Nielsen', 'Inspektør', '2021-01-10', 3);