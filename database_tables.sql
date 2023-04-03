use book_store;

CREATE TABLE books (
    isbn CHAR(10) NOT NULL,
    author VARCHAR(100) NOT NULL,
    title VARCHAR(128) NOT NULL,
    price FLOAT,
    subject VARCHAR(30),
    PRIMARY KEY (isbn)
);

CREATE TABLE members (
    fname VARCHAR(20) NOT NULL,
    lname VARCHAR(20) NOT NULL,
    address VARCHAR(50) NOT NULL,
    city VARCHAR(30) NOT NULL,
    state VARCHAR(20) NOT NULL,
    zip INT NOT NULL,
    phone VARCHAR(12),
    email VARCHAR(40) UNIQUE,
    userid INT NOT NULL AUTO_INCREMENT,
    password VARCHAR(20),
    creditcardtype VARCHAR(10),
    creditcardnumber CHAR(16),
    PRIMARY KEY (userid)
);

CREATE TABLE orders (
    userid INT NOT NULL,
    ono INT NOT NULL AUTO_INCREMENT,
    recieved DATE,
    shipped DATE,
    shipAdress VARCHAR(50),
    shipCity VARCHAR(30),
    shipState VARCHAR(20),
    shipZip INT,
    FOREIGN KEY (userid) REFERENCES members (userid),
    PRIMARY KEY (ono)
);
  
CREATE TABLE odetails (
    ono INT NOT NULL,
    isbn CHAR(10) NOT NULL,
    qty INT,
    price FLOAT,
    PRIMARY KEY (ono, isbn),
    FOREIGN KEY (ono) REFERENCES orders (ono),
    FOREIGN KEY (isbn) REFERENCES books (isbn)
);

CREATE TABLE cart (
    userid INT NOT NULL,
    isbn CHAR(10) NOT NULL,
    qty INT,
    primary key (userid, isbn),
    FOREIGN KEY (userid) REFERENCES members (userid),
    FOREIGN KEY (isbn) REFERENCES books (isbn)
);