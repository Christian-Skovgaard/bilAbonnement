USE user_db;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50),
    password VARCHAR(255) NOT NULL,
    role ENUM('application','user','admin','leadership') DEFAULT 'user',
    department ENUM('Aarhus','Koling','København') DEFAULT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

INSERT INTO users (username, password, role, department) VALUES
('Bo', 'Elefant', 'admin', 'Koling'),
('AndersElten42', 'chalklin', 'user', 'København'),
('custommerManagementService','Ugenkendlig Thai-ret','application',NULL),
('subscriptionManagementService','Hungren efter druknedød','application',NULL)
