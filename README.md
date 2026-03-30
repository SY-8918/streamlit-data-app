# Snowflake Secure Connection Project

Secure Python project demonstrating how to connect to Snowflake using RSA key authentication and insert data into a database.

## Project Objective

This project reproduces a real-world secure connection workflow between a Python client and Snowflake.

Main goals:

* authenticate with RSA private/public keys
* connect to Snowflake without a password
* create a database and table
* insert and visualize data

## Technologies

* Python
* Snowflake
* RSA Authentication
* snowflake-connector-python
* cryptography

## Architecture

Python Client → RSA Private Key → Snowflake → Warehouse → Database → Table

The private key remains on the client side, while the public key is stored in Snowflake.

## Security

This project uses RSA 2048-bit authentication with a PKCS#8 private key.

Example Snowflake configuration:

```sql
ALTER USER ZEBRA
SET RSA_PUBLIC_KEY='...';
```

The authentication is performed without using a password.

## Database Objects

* Database: `YOUNESS_STREAMING_LAB`
* Table: `SIMPLE_DATA`

The project inserts sample sensor-style data into the table.

## Results

* Secure connection established
* 13 rows inserted successfully
* Data visible inside Snowflake interface

## Key Learning

This project demonstrates a real enterprise use case involving:

* secure authentication
* Snowflake administration
* database permissions
* Python-to-cloud integration
