import streamlit as st
import dotenv
import pandas
import json
import psycopg2
from psycopg2 import sql

from config.coa import coa_data
from app.llm.openai_api import get_vendor, get_coa, get_vendor_information
CFG = dotenv.dotenv_values(".env")


class PGHandler:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(CFG['POSTGRESQL_STATEMENT_URI'])  # Connect to the database
            self.cursor = self.connection.cursor()  # Initialize a cursor
            self.create_table_if_not_exists()
        except Exception as e:
            st.error(f"Failed to connect to the database: {e}")
            raise

    def create_table_if_not_exists(self):
        try:
            create_table_business = """
                CREATE TABLE IF NOT EXISTS business (
                    business_id SERIAL PRIMARY KEY,
                    business_name VARCHAR(255) UNIQUE NOT NULL,
                    business_phone VARCHAR(255) UNIQUE NOT NULL,
                    business_country VARCHAR(255) UNIQUE NOT NULL,
                    business_address VARCHAR(255) UNIQUE NOT NULL,
                    business_industry VARCHAR(255) UNIQUE NOT NULL,
                    business_info JSONB NOT NULL,
                    business_base_currency VARCHAR(255) UNIQUE NOT NULL,
                    fiscal_year VARCHAR(255) UNIQUE NOT NULL,
                    tax_setting VARCHAR(255) UNIQUE NOT NULL,
                    default_payment_term VARCHAR(255) UNIQUE NOT NULL,
                    integration_setting VARCHAR(255) UNIQUE NOT NULL                    
                );
            """

            create_table_vendor = """
                CREATE TABLE IF NOT EXISTS vendors (
                    vendor_id SERIAL PRIMARY KEY,
                    vendor_name VARCHAR(255) UNIQUE NOT NULL,
                    business_info JSONB NOT NULL
                );
            """

            create_table_bank = """
                CREATE TABLE IF NOT EXISTS banks (
                    bank_id SERIAL PRIMARY KEY,
                    bank_account VARCHAR(255) UNIQUE NOT NULL,
                    bank_type  VARCHAR(255),
                    business_info JSONB NOT NULL
                );
            """

            create_table_cc_transactions = """
                CREATE TABLE IF NOT EXISTS cc_transactions (
                    id SERIAL PRIMARY KEY,
                    clientID VARCHAR(50),
                    date DATE ,
                    description VARCHAR(255),
                    amount NUMERIC(10, 2) ,
                    debit_account VARCHAR(50) ,
                    credit_account VARCHAR(50) ,
                    vendor_name VARCHAR(255),
                    COA VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
            """

            create_table_payments = """
                CREATE TABLE IF NOT EXISTS payments (
                    payment_id SERIAL PRIMARY KEY,
                    transaction_id INT REFERENCES cc_transactions(id) ON DELETE CASCADE,
                    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    amount DECIMAL(10, 2) NOT NULL,
                    payment_method VARCHAR(50),  -- e.g., credit card, cash, etc.
                    status VARCHAR(20) DEFAULT 'completed',  -- e.g., completed, pending, refunded, etc.
                    payment_note  VARCHAR(255),  -- e.g., credit card, cash, etc.                    -- Add any other relevant fields
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """


            create_table_bank_transactions = """
                CREATE TABLE IF NOT EXISTS bank_transactions (
                    id SERIAL PRIMARY KEY,
                    clientID VARCHAR(50),
                    date DATE ,
                    description VARCHAR(255),
                    amount NUMERIC(10, 2) ,
                    debit_account VARCHAR(50) ,
                    credit_account VARCHAR(50) ,
                    vendor_name VARCHAR(255),
                    COA VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """


            create_table_bank_transactions = """
                CREATE TABLE IF NOT EXISTS COA (
                    COA_id SERIAL PRIMARY KEY,
                    business_id INTEGER,
                    vendor_id INTEGER,
                    COA1 TEXT,
                    COA11 TEXT,
                    COA111 TEXT
                );
            """

            self.cursor.execute(create_table_cc_transactions)  # Execute the query
            self.cursor.execute(create_table_payments)  # Execute the query
            self.cursor.execute(create_table_bank_transactions)  # Execute the query
            self.cursor.execute(create_table_vendor)  # Execute the query
            self.cursor.execute(create_table_bank)  # Execute the query
            self.cursor.execute(create_table_business)  # Execute the query
            self.connection.commit()  # Commit the transaction
            st.success("DB Connection verified successfully.")
        except Exception as e:
            self.connection.rollback()  # Rollback the transaction on error
            st.error(f"Error creating table: {e}")

    def close(self):
        """Call this method to close the cursor and connection when done."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def truncate_table(self, table_name):
        try:
            self.cursor.execute(sql.SQL("TRUNCATE TABLE {}").format(sql.Identifier(table_name)))
            self.connection.commit()
            st.success(f"Table {table_name} has been truncated.")
        except Exception as e:
            st.error(f"Failed to truncate the table: {e}")
            self.connection.rollback()

    def delete_table(self, table_name):
        try:
            self.cursor.execute(sql.SQL("DELETE FROM {}").format(sql.Identifier(table_name)))
            self.connection.commit()
            st.success(f"All records in table {table_name} have been deleted.")
        except Exception as e:
            st.error(f"Failed to delete records from the table: {e}")
            self.connection.rollback()

    def get_coa_and_amount(self):
        try:
            select_query = """
                SELECT COA, amount FROM statement_cc;
            """
            self.cursor.execute(select_query)
            data = self.cursor.fetchall()  # Fetch all the rows
            return data
        except Exception as e:
            self.connection.rollback()
            st.error(f"Error fetching data: {e}")

    def get_coa_data(self):
        try:
            # Query to select the COA and amount
            query = "SELECT COA, SUM(amount) as total_amount FROM statement_cc GROUP BY COA"
            self.cursor.execute(query)

            # Fetch data
            data = self.cursor.fetchall()

            # Create a pandas DataFrame from the fetched data
            df = pandas.DataFrame(data, columns=['COA', 'total_amount'])
            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")

    def get_gl(self):
        try:
            # Query to select specific columns: date, description, COA, amount
            query = "SELECT date, COA, amount FROM statement_cc"
            self.cursor.execute(query)

            # Fetch data
            data = self.cursor.fetchall()

            # Create a pandas DataFrame from the fetched data
            df = pandas.DataFrame(data, columns=['date', 'COA', 'amount'])
            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")

    def get_journal(self, table_name):
        try:
            # Query to select specific columns: date, description, COA, amount
            query = f"SELECT clientid, date, description, amount, COA, vendor_name, debit_account, credit_account FROM {table_name}"
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            # Create a pandas DataFrame from the fetched data
            df = pandas.DataFrame(data)
            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")

    def get_vendors(self):
        try:
            # Execute the query to get vendor data
            self.cursor.execute("SELECT vendor_name, business_info FROM vendors")
            vendors = self.cursor.fetchall()

            # Return the vendor data
            return vendors

        except Exception as e:
            st.error(f"Error fetching vendors: {e}")
            return []


    def get_vendor_list(self, business_id=None):
        try:
            query = "SELECT business_id, vendor_id, vendor_name, vendor_code, tax_type , vendor_type, vendor_category, credit_limit, threshold FROM vendors"
            if business_id is not None:
                query += " WHERE business_id = %s"

            self.cursor.execute(query, (business_id,))
            # Execute the query to get vendor data
            vendors = self.cursor.fetchall()
            df = pandas.DataFrame(vendors)

            return df

        except Exception as e:
            st.error(f"Error fetching vendors: {e}")
            return []


    def get_client_list(self, business_id=None):
        try:
            query = "SELECT business_id, client_id, client_name, client_type, client_category, credit_limit, payment_method, credit_term FROM clients"
            if business_id is not None:
                query += " WHERE business_id = %s"

            self.cursor.execute(query, (business_id,))
            # Execute the query to get vendor data
            vendors = self.cursor.fetchall()
            df = pandas.DataFrame(vendors)

            return df

        except Exception as e:
            st.error(f"Error fetching vendors: {e}")
            return []


    def get_raw_cc(self):
        try:
            # Query to select specific columns: date, description, COA, amount
            query = "SELECT * FROM statement_cc"
            self.cursor.execute(query)

            # Fetch data
            data = self.cursor.fetchall()

            return data
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")


    def execute_sql(self, solution):
        try:
            _,final_query,_ = solution.split("```")
            final_query = final_query.strip('sql')
            self.cursor.execute(final_query)
            result = self.cursor.fetchall()
            return str(result)
        except Exception as e:
            st.error(f"Failed to save database details: {e}")
            raise
        finally:
            self.cursor.close()
            self.connection.close()

    def get_basic_table_details(self):

        query = """
        SELECT
            c.table_name,
            c.column_name,
            c.data_type
        FROM
            information_schema.columns c
        WHERE
            c.table_name IN (
                SELECT tablename
                FROM pg_tables
                WHERE schemaname = 'public'
        );
        """
        self.cursor.execute(query)
        tables_and_columns = self.cursor.fetchall()
        return tables_and_columns

    def get_db_schema(self):
        """ run once in global_initialization
            :param query:
            :param unique_id:
            :param db_uri:
            :return:
        """
        try:
            tables_and_columns = self.get_basic_table_details()  # Fetch table details
            df = pandas.DataFrame(tables_and_columns, columns=['table_name', 'column_name', 'data_type'])
            df.to_csv('./data/db/TABLES_COLUMNS.CSV', index=False)  # Save details to CSV file
            table_info = ''
            for table in df['table_name']:
                table_info += f'Information about table {table}:\n'
                table_info += df[df['table_name'] == table].to_string(index=False) + '\n\n\n'
            return table_info
        except Exception as e:
            st.error(f"Failed to save database details: {e}")
            raise
        finally:
            self.cursor.close()
            self.connection.close()

    def save_cc_postgres(self, transactions):
        try:
            for transaction in transactions:
                insert_query = sql.SQL("""
                    INSERT INTO statement_cc (clientID, date, description, amount, vendor_name, COA)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """)
                self.cursor.execute(insert_query, (
                    transaction['clientID'],
                    transaction['date'],
                    transaction['description'],
                    transaction['amount'],
                    transaction['vendor_name'],
                    transaction['COA']
                ))
            self.connection.commit()
            st.success("Transactions saved to PostgreSQL!")
        except Exception as e:
            self.connection.rollback()
            st.error(f"Failed to save transactions: {e}")
        finally:
            self.connection.close()  # Close connection when done


    def save_vendor_if_not_exists(self, vendor_name):
        try:
            # Check if vendor already exists in the vendor table
            select_query = """
                SELECT vendor_name FROM vendors WHERE vendor_name = %s;
            """
            self.cursor.execute(select_query, (vendor_name,))
            vendor = self.cursor.fetchone()

            # If vendor does not exist, insert it
            if not vendor:
                # Fetch business info from an external source
                business_info = json.dumps(get_vendor_information(vendor_name))
                # Insert the new vendor into the vendors table
                insert_query = """
                    INSERT INTO vendors (vendor_name, business_info)
                    VALUES (%s, %s);
                """
                self.cursor.execute(insert_query, (vendor_name, business_info))
                self.connection.commit()
            else:
                st.info(f"Vendor '{vendor_name}' already exists.")
        except Exception as e:
            self.connection.rollback()
            st.error(f"Error saving vendor information: {e}")


    def save_cc_journal_postgres(self, transactions):
        try:
            for transaction in transactions:
                insert_query = sql.SQL("""
                    INSERT INTO cc_transactions (clientID, date, description, amount, vendor_name, COA, debit_account, credit_account)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """)
                self.cursor.execute(insert_query, (
                    transaction['clientID'],
                    transaction['date'],
                    transaction['description'],
                    transaction['amount'],
                    transaction['vendor_name'],
                    transaction['COA'],
                    transaction['debit_account'],
                    transaction['credit_account']
                ))
            self.connection.commit()
            st.success("Transactions saved to PostgreSQL!")
        except Exception as e:
            self.connection.rollback()
            st.error(f"Failed to save transactions: {e}")
        finally:
            self.connection.close()  # Close connection when done

    def save_bank_journal_postgres(self, transactions):
        try:
            for transaction in transactions:
                insert_query = sql.SQL("""
                    INSERT INTO bank_transactions (clientID, date, description, amount, vendor_name, COA, debit_account, credit_account)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """)
                self.cursor.execute(insert_query, (
                    transaction['clientID'],
                    transaction['date'],
                    transaction['description'],
                    transaction['amount'],
                    transaction['vendor_name'],
                    transaction['COA'],
                    transaction['debit_account'],
                    transaction['credit_account']
                ))
            self.connection.commit()
            st.success("Transactions saved to PostgreSQL!")
        except Exception as e:
            self.connection.rollback()
            st.error(f"Failed to save transactions: {e}")
        finally:
            self.connection.close()  # Close connection when done


    def get_bills(self, vendor_name):
        try:
            query = "SELECT id, business_id, date, description, amount, due_date, paid_date FROM cc_transactions where vendor_name = %s ;"
            self.cursor.execute(query, (vendor_name,))

            data = self.cursor.fetchall()
            # Create a pandas DataFrame from the fetched data
            df = pandas.DataFrame(data)
            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")



    def get_vendor_info(self, business_id=None, vendor_name=None):
        try:
            query = "SELECT business_id, vendor_id, vendor_name, business_info, vendor_code FROM vendors WHERE business_id = %s and vendor_name = %s"
            self.cursor.execute(query, (business_id,vendor_name))
            # Execute the query to get vendor data
            vendors = self.cursor.fetchall()
            df = pandas.DataFrame(vendors)

            return df

        except Exception as e:
            st.error(f"Error fetching vendors: {e}")
            return []


    def get_payments(self, business_id=None, vendor_id=None, transaction_id = None):
        try:
            query = "SELECT transaction_id, payment_date,amount, payment_method, status, payment_note FROM payments WHERE business_id = %s and vendor_id = %s and transaction_id = %s"
            self.cursor.execute(query, (business_id,vendor_id, transaction_id))
            # Execute the query to get vendor data
            vendors = self.cursor.fetchall()
            df = pandas.DataFrame(vendors)

            return df

        except Exception as e:
            st.error(f"Error fetching vendors: {e}")
            return []


    def get_business_basic(self, business_id):
        try:
            query = "SELECT business_id, business_name, business_phone, business_country, business_address, business_industry, business_info FROM business where business_id = %s ;"
            # query = "SELECT * FROM business where business_id = %s ;"

            self.cursor.execute(query, (business_id,))

            data = self.cursor.fetchall()
            # Create a pandas DataFrame from the fetched data
            df = pandas.DataFrame(data)
            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")


    def get_business_fin(self, business_id):
        try:
            query = "SELECT business_id, business_name,  business_base_currency, fiscal_year, tax_setting, default_payment_term, integration_setting FROM business where business_id = %s ;"
            # query = "SELECT * FROM business where business_id = %s ;"

            self.cursor.execute(query, (business_id,))

            data = self.cursor.fetchall()
            # Create a pandas DataFrame from the fetched data
            df = pandas.DataFrame(data)
            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")


    def save_coa(self):
        business_id = 801
        vendor_id = 26
        coa_entry = ('Assets', 'Current Assets', '1000 - Cash on Hand')

        for coa in coa_data:
            self.cursor.execute('''
                    INSERT INTO COA (business_id, vendor_id, COA1, COA11, COA111)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (business_id, vendor_id, coa[0], coa[1], coa[2]))

        # Commit the transaction
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

        # try:
        #     for coa in coa_data:
        #         st.text(coa)
        #         self.cursor.execute('''
        #             INSERT INTO coa (business_id, vendor_id, COA1, COA11, COA111)
        #             VALUES ($1, $2, $3, $4, $5)
        #         ''', (business_id, vendor_id, coa[0], coa[1], coa[2]))
        #
        #     self.connection.commit()
        #     st.success("Transactions saved to PostgreSQL!")
        # except Exception as e:
        #     self.connection.rollback()
        #     st.error(f"Failed to save transactions: {e}")
        # finally:
        #     self.connection.close()  # Close connection when done

    def get_coa_list(self):
        try:
            query = "SELECT * FROM coa;"
            self.cursor.execute(query)

            data = self.cursor.fetchall()
            # Create a pandas DataFrame from the fetched data
            df = pandas.DataFrame(data)
            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")

