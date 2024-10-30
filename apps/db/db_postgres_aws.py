import streamlit as st
from streamlit_extras.stateful_button import button

import dotenv, re
import pandas
import numpy
import json

import psycopg2
from psycopg2 import sql
from psycopg2.extensions import register_adapter, AsIs

register_adapter(numpy.int64, AsIs)

CFG = dotenv.dotenv_values(".env")

from .seeds import default_coa, naics_data
from apps.llm.openai_api import get_vendor, get_coa, get_vendor_information, get_journal_entry_cc2


class PGHandler:

    def __init__(self):
        try:
            self.connection = psycopg2.connect(CFG['POSTGRESQL_STATEMENT_URI'])  # Connect to the database
            self.cursor = self.connection.cursor()  # Initialize a cursor
        except Exception as e:
            st.error(f"Failed to connect to the database: {e}")
            raise

    def create_table_if_not_exists(self):
        try:
            create_table_default = """
                CREATE TABLE IF NOT EXISTS xai (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(30) UNIQUE NOT NULL
                );


                CREATE TABLE IF NOT EXISTS default_coa (
                    coa_id SERIAL PRIMARY KEY,       -- Auto-incremented primary key for COA
                    biz_type  INT NOT NULL,
                    account_type VARCHAR(255) NOT NULL, 
                    account_subtype VARCHAR(255) NOT NULL,
                    parent_account VARCHAR(255) NOT NULL,
                    sub_account VARCHAR(255) NOT NULL,
                    coa_note VARCHAR(255) NOT NULL
                );                


                CREATE TABLE IF NOT EXISTS biz_coa (
                    biz_coa_id SERIAL PRIMARY KEY,  
                    LIKE default_coa EXCLUDING CONSTRAINTS, 
                    biz_id INTEGER NOT NULL
                );


                CREATE TABLE IF NOT EXISTS default_naics (
                    id SERIAL PRIMARY KEY,       -- Auto-incremented primary key for COA
                    industry_category_id INT NOT NULL,
                    industry_category_name VARCHAR(100) NOT NULL,
                    business_type_id INT NOT NULL,
                    business_type_name VARCHAR(100) NOT NULL,
                    business_subtype_id INT NOT NULL,
                    business_subtype_name VARCHAR(100) NOT NULL
                );                

            """

            create_table_biz = """
                CREATE TABLE IF NOT EXISTS biz_coa (
                    coa_id SERIAL PRIMARY KEY,       -- Auto-incremented primary key for COA
                    account_type VARCHAR(255) NOT NULL, 
                    account_subtype VARCHAR(255) NOT NULL,
                    parent_account VARCHAR(255) NOT NULL,
                    sub_account VARCHAR(255) NOT NULL,
                    coa_note VARCHAR(255) NOT NULL
                );


                CREATE TABLE IF NOT EXISTS biz_entity (
                    biz_id SERIAL PRIMARY KEY,
                    biz_name VARCHAR(255) NOT NULL,
                    biz_phone VARCHAR(255),
                    biz_country VARCHAR(255),
                    biz_address VARCHAR(255),
                    biz_industry VARCHAR(255),
                    biz_base_currency VARCHAR(255),
                    biz_fiscal_year VARCHAR(255),
                    biz_tax_setting VARCHAR(255),
                    biz_default_payment_term VARCHAR(255),
                    biz_integration_setting VARCHAR(255),
                    biz_industry_id     INT,
                    biz_primary_bank_id INT,
                    biz_info JSONB
                );


                CREATE TABLE IF NOT EXISTS vendors (
                    vendor_id SERIAL PRIMARY KEY,
                    vendor_biz_id INT,
                    vendor_name VARCHAR(255) UNIQUE NOT NULL,                    
                    business_info JSONB
                );

                CREATE TABLE IF NOT EXISTS banks (
                    bank_id SERIAL PRIMARY KEY,
                    bank_biz_id INTEGER REFERENCES biz_entity(biz_id) ON DELETE CASCADE,
                    bank_account_number VARCHAR(255) NOT NULL,
                    bank_name VARCHAR(255) NOT NULL,
                    bank_code  VARCHAR(50),
                    bank_type  VARCHAR(50),
                    bank_info JSONB NOT NULL
                );

                CREATE TABLE IF NOT EXISTS cc_journals (
                    journal_id SERIAL PRIMARY KEY,
                    clientID VARCHAR(255),
                    date  Date,
                    description VARCHAR(255),
                    account VARCHAR(255),
                    debit NUMERIC(10, 2) ,
                    credit NUMERIC(10, 2)
                );

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

                CREATE TABLE IF NOT EXISTS invoices (
                    invoice_id SERIAL PRIMARY KEY,
                    invoice_number VARCHAR(50)   NOT NULL,
                    biz_id INTEGER,
                    biz_name VARCHAR(255),
                    customer_id INTEGER,
                    customer_name VARCHAR(100),
                    client_id INTEGER,
                    client_name VARCHAR(100),
                    client_address VARCHAR(100),
                    client_payment_mentod VARCHAR(100),
                    issue_date DATE,
                    due_date DATE,
                    status VARCHAR(20),
                    item_description VARCHAR(255),
                    item_quantity NUMERIC(10, 2),
                    item_unit_price NUMERIC(10, 2),
                    item_tax_rate NUMERIC(10, 2),
                    item_tax  NUMERIC(10, 2),
                    item_amount NUMERIC(10, 2),
                    invoice_total_amount DECIMAL(10, 2),
                    invoice_recurring BOOLEAN, 
                    invoice_note VARCHAR(255)                                                        
                    );
            """

            self.cursor.execute(create_table_default)  # Execute the query
            self.cursor.execute(create_table_biz)  # Execute the query
            self.connection.commit()  # Commit the transaction
            st.success("DB Connection verified successfully.")
        except Exception as e:
            self.connection.rollback()  # Rollback the transaction on error
            st.error(f"Error creating table: {e}")

    def load_default_coa(self):
        st.text(default_coa)
        try:
            # Insert the COA data into the default_coa table
            insert_query = """
                    INSERT INTO default_coa (biz_type, account_type, account_subtype, parent_account, sub_account, coa_note)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
            self.cursor.executemany(insert_query, default_coa)

            # Commit the changes to the database
            self.connection.commit()
            st.write("Seed data inserted successfully.")

        except Exception as e:
            print(f"Error seeding data: {e}")
            self.connection.rollback()

    def load_default_naics(self):
        try:

            # Insert the COA data into the default_coa table
            insert_query = """
                INSERT INTO default_naics (industry_category_id, industry_category_name, business_type_id, business_type_name, business_subtype_id, business_subtype_name)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.executemany(insert_query, naics_data)

            self.connection.commit()
            st.write("Seed data inserted successfully.")

        except Exception as e:
            st.error(f"Error seeding data: {e}")
            self.connection.rollback()

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
            query = "SELECT COA, SUM(amount) as total_amount FROM cc_transactions GROUP BY COA"
            self.cursor.execute(query)

            # Fetch data
            data = self.cursor.fetchall()

            # Create a pandas DataFrame from the fetched data
            df = pandas.DataFrame(data, columns=['COA', 'total_amount'])
            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")

    def get_journals(self):
        try:
            # Query to select specific columns: date, description, COA, amount
            query = "SELECT * FROM cc_journals"
            self.cursor.execute(query)

            # Fetch data
            data = self.cursor.fetchall()

            # Create a pandas DataFrame from the fetched data
            column_names = [desc[0] for desc in self.cursor.description]
            df = pandas.DataFrame(data, columns=column_names)

            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")

    def get_journal(self, table_name):
        try:
            # Query to select specific columns: date, description, COA, amount
            query = f"SELECT clientid, date,description, amount, COA, vendor_name, debit_account, credit_account FROM {table_name}"
            self.cursor.execute(query)
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]

            # Create a pandas DataFrame from the fetched data
            df = pandas.DataFrame(data, columns=column_names)

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

    def get_raw_cc(self):
        try:
            # Query to select specific columns: date, description, COA, amount
            query = "SELECT * FROM cc_transactions"
            self.cursor.execute(query)

            # Fetch data
            data = self.cursor.fetchall()

            return data
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")

    def execute_sql(self, solution):
        try:
            _, final_query, _ = solution.split("```")
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
            self.cursor.execute(query, (business_id, vendor_name))
            # Execute the query to get vendor data
            vendors = self.cursor.fetchall()
            df = pandas.DataFrame(vendors)

            return df

        except Exception as e:
            st.error(f"Error fetching vendors: {e}")
            return []

    def get_payments(self, business_id=None, vendor_id=None, transaction_id=None):
        try:
            query = "SELECT * FROM payments WHERE business_id = %s and vendor_id = %s and transaction_id = %s"
            self.cursor.execute(query, (business_id, vendor_id, transaction_id))
            # Execute the query to get vendor data
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            df = pandas.DataFrame(data, columns=column_names)
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
            df = pandas.DataFrame(data)
            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")

    def get_business_fin(self, business_id):
        try:
            # query = "SELECT business_id, business_name,  business_base_currency, fiscal_year, tax_setting, default_payment_term, integration_setting, bank1, bank2, bank3 FROM business where business_id = %s ;"
            query = "SELECT * FROM business where business_id = %s ;"

            self.cursor.execute(query, (business_id,))
            data = self.cursor.fetchall()
            df = pandas.DataFrame(data)

            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")

    def save_coa(self):
        business_id = 801
        vendor_id = 26
        coa_entry = ('Assets', 'Current Assets', '1000 - Cash on Hand')

        for coa in default_coa:
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
            column_names = [desc[0] for desc in self.cursor.description]
            df = pandas.DataFrame(data, columns=column_names)

            return df
        except Exception as e:
            raise Exception(f"Failed to retrieve data from the database: {e}")

    def get_invoice(self, biz_id=None, invoice_number=None):
        try:
            query = "SELECT * FROM invoices WHERE biz_id = %s and invoice_number = %s"
            self.cursor.execute(query, (biz_id, invoice_number))
            # Execute the query to get vendor data
            invoices = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]

            df = pandas.DataFrame(invoices, columns=column_names)
            return df

        except Exception as e:
            st.error(f"Error fetching vendors: {e}")
            return []

    def save_cc_journal_postgres_2(self, new_df):
        try:
            for index, row in new_df.iterrows():
                insert_query = sql.SQL("""
                    INSERT INTO cc_journals (clientid, date, description, debit_account, credit_account, debit, credit)
                    VALUES (%s, %s, %s, %s, %s,%s, %s)
                """)
                self.cursor.execute(insert_query, (
                    row['clientid'],
                    row['date'],
                    row['description'],
                    row['debit_account'],
                    row['credit_account'],
                    row['debit'],
                    row['credit']
                ))

            update_query = sql.SQL(
                "UPDATE cc_journals SET account = COALESCE(NULLIF(debit_account, 'NaN'), credit_account) ;")
            self.cursor.execute(update_query)
            self.connection.commit()
            st.success("Transactions saved to PostgreSQL!")
        except Exception as e:
            self.connection.rollback()
            st.error(f"Failed to save transactions: {e}")
        finally:
            self.connection.close()  # Close connection when done

    def get_naics(self, table_name='default_naics'):
        try:
            query = (f"SELECT * FROM {table_name}")

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            df = pandas.DataFrame(data, columns=column_names)
            return df

        except Exception as e:
            print(f"Error fetching data: {e}")  # Using print for error handling (you can use logging too)
            return pandas.DataFrame()  # Return an empty DataFrame in case of an error

    def get_default_coa(self, table_name='default_coa'):
        try:
            query = (f"""
                SELECT * FROM default_coa  
            """)

            self.cursor.execute(query)
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            df = pandas.DataFrame(data, columns=column_names)
            return df

        except Exception as e:
            print(f"Error fetching data: {e}")  # Using print for error handling (you can use logging too)
            return pandas.DataFrame()  # Return an empty DataFrame in case of an error

    def copy_default_coa_to_biz(self, biz_type, biz_id):

        try:
            # Check if biz_type already exists in biz_coa
            check_query = '''
                SELECT EXISTS (
                    SELECT 1 FROM biz_coa WHERE biz_type = %s
                );
            '''
            st.write(f"Type of biz_type: {type(biz_type)}")
            self.cursor.execute(check_query, (biz_type,))
            exists = self.cursor.fetchone()[0]

            if exists:
                st.info(f"biz_type {biz_type} already exists in biz_coa. No data copied.")
                return

            # Copy data from default_coa to biz_coa for the new biz_type
            copy_query = '''
                INSERT INTO biz_coa (coa_id,biz_type,account_type,account_subtype,parent_account,sub_account,coa_note, biz_id)
                SELECT coa_id,biz_type,account_type,account_subtype,parent_account,sub_account,coa_note, %s FROM default_coa
                WHERE biz_type = %s 
            '''
            self.cursor.execute(copy_query, (biz_id, biz_type,))
            self.connection.commit()
            st.success(f"Data copied to biz_coa for biz_type {biz_type}.")

        except Exception as e:
            self.connection.rollback()  # Rollback in case of error
            st.error(f"Failed to copy data: {e}")
            raise

    def email_new_transactions_process(self, table_name='bk_transaction', biz_entity_id=801,
                                       biz_status='s1_biz_entity_id'):
        try:
            query = f"""
                SELECT COUNT(*) FROM {table_name}
                WHERE biz_entity_id IS NULL;
            """

            self.cursor.execute(query)
            null_count = self.cursor.fetchone()[0]

            if null_count > 0:
                if button('There are new emails. Process them?', key='email1'):
                    query = f"""
                        UPDATE  {table_name}
                        SET biz_entity_id = %s, biz_status  = %s,  
                        WHERE biz_entity_id IS NULL;
                    """
                    self.cursor.execute(query, (biz_entity_id, biz_status))
                    self.connection.commit()
            else:
                st.warning('There is no new emails.')

            if button('Show emails?', key='email112'):
                query = f"""
                    SELECT * FROM {table_name}
                    WHERE biz_entity_id = %s and  biz_status  = %s;
                """
                self.cursor.execute(query, (biz_entity_id, biz_status,))
                data = self.cursor.fetchall()
                column_names = [desc[0] for desc in self.cursor.description]
                df = pandas.DataFrame(data, columns=column_names)
                return df


        except Exception as e:
            print(f"Error fetching data: {e}")  # Using print for error handling (you can use logging too)
            return pandas.DataFrame()  # Return an empty DataFrame in case of an error

    def get_and_update_(self, table_name='bk_transaction', biz_entity_id=801, case='new email',
                        biz_status='s1_biz_entity_id'):
        def safe_search(pattern, text):
            match = re.search(pattern, text, re.IGNORECASE)
            return match.group(1) if match else None

        try:
            if case == 'vendor_and_coa':
                query = (f"SELECT * FROM {table_name} WHERE biz_entity_id = %s and  biz_status  = %s;")
            elif case == 'book_journals':
                query = (f"SELECT * FROM {table_name} WHERE biz_entity_id = %s and  biz_status  = %s;")

            self.cursor.execute(query, (biz_entity_id, biz_status,))
            records = self.cursor.fetchall()

            for record in records:
                record_id = record[0]
                description = record[6]
                if case == 'vendor_and_coa':
                    vendor_name = get_vendor(description)
                    COA = get_coa(vendor_name)

                    self.save_vendor_if_not_exists(vendor_name)

                    update_query = f"""
                        UPDATE {table_name}
                        SET biz_vendor_name = %s, biz_coa = %s, biz_status  = 's2_coa'
                        WHERE id = %s;
                    """
                    self.cursor.execute(update_query, (vendor_name, COA, record_id))
                    self.connection.commit()  # Commit the transaction
                    st.success("Vendor COA updated successfully.")

                elif case == 'book_journals':
                    entry = get_journal_entry_cc2(record)[0]
                    debit_account = safe_search(r"Debit: ([\w\s]+) \$\d+\.\d+", entry)
                    credit_account = safe_search(r"Credit: ([\w\s]+) \$\d+\.\d+", entry)
                    update_query = f"""
                        UPDATE {table_name}
                        SET biz_debit_account = %s, biz_credit_account = %s, biz_status = 's3_book_journals'
                        WHERE id = %s;
                    """
                    self.cursor.execute(update_query, (debit_account, credit_account, record_id))
                    self.connection.commit()  # Commit the transaction

            st.success("Finish.")

        except Exception as e:
            print(f"Error fetching data: {e}")  # Using print for error handling (you can use logging too)
            return pandas.DataFrame()  # Return an empty DataFrame in case of an error

    def show_transactions(self, table_name='bk_transactions', biz_entity_id=801, biz_status='s2_coa'):
        try:
            query = (f"""
                SELECT * 
                FROM {table_name}
                WHERE biz_id = %s and biz_status  = %s;
            """)

            self.cursor.execute(query, (biz_entity_id, biz_status,))
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            df = pandas.DataFrame(data, columns=column_names)
            return df

        except Exception as e:
            print(f"Error fetching data: {e}")  # Using print for error handling (you can use logging too)
            return pandas.DataFrame()  # Return an empty DataFrame in case of an error

    def show_general(self, table_name='bk_transactions', biz_id=888, module = 'ALL'):
        try:
            if module == 'biz_entity_setup_financial':
                query = (f"""
                    SELECT a.*, b.* FROM {table_name} a
                    LEFT JOIN banks b                
                    ON a.biz_id = b.bank_biz_id
                    WHERE a.biz_id = %s;
                """)
            else:
                query = (f"""SELECT * FROM {table_name} WHERE biz_id = %s;""")

            self.cursor.execute(query, (biz_id,))
            data = self.cursor.fetchall()
            column_names = [desc[0] for desc in self.cursor.description]
            df = pandas.DataFrame(data, columns=column_names)
            return df

        except Exception as e:
            print(f"Error fetching data: {e}")  # Using print for error handling (you can use logging too)
            return pandas.DataFrame()  # Return an empty DataFrame in case of an error

