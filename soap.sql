DROP TABLE IF EXISTS office;
DROP TABLE IF EXISTS agency;
DROP TABLE IF EXISTS rental;
DROP TABLE IF EXISTS agreement;

CREATE TABLE IF NOT EXISTS office
(
  city VARCHAR(32) NOT NULL,
  name VARCHAR(32) NOT NULL,
  PRIMARY KEY (name)
);

CREATE TABLE IF NOT EXISTS agency
(
  agency_ID INT NOT NULL,
  name VARCHAR(32) NOT NULL,
  address VARCHAR(64) NOT NULL,
  city VARCHAR(32) NOT NULL,
  phone VARCHAR(10) NOT NULL,
  PRIMARY KEY (agency_ID)
);

CREATE TABLE IF NOT EXISTS rental
(
  rental_ID INT NOT NULL,
  amount INT NOT NULL,
  endDate DATE NOT NULL,
  squareFt INT NOT NULL,
  name VARCHAR(32) NOT NULL,
  PRIMARY KEY (rental_ID),
  FOREIGN KEY (name) REFERENCES office(name)
);

CREATE TABLE IF NOT EXISTS agreement
(
  agency_ID INT NOT NULL,
  rental_ID INT NOT NULL,
  PRIMARY KEY (agency_ID, rental_ID),
  FOREIGN KEY (agency_ID) REFERENCES agency(agency_ID),
  FOREIGN KEY (rental_ID) REFERENCES rental(rental_ID)
);