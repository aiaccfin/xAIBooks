import streamlit as st
import dotenv
import pandas
import json
import psycopg2
from psycopg2 import sql


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


            create_table_statement_cc = """
                CREATE TABLE IF NOT EXISTS statement_cc (
                    transaction_id SERIAL PRIMARY KEY,
                    clientID VARCHAR(50) NOT NULL,
                    date DATE NOT NULL,
                    description VARCHAR(255),
                    amount NUMERIC(12, 2) NOT NULL,
                    vendor_name VARCHAR(255) NOT NULL,
                    COA VARCHAR(255) NOT NULL
                );
            """

            create_table_vendor = """
                CREATE TABLE IF NOT EXISTS vendors (
                    vendor_id SERIAL PRIMARY KEY,
                    vendor_name VARCHAR(255) UNIQUE NOT NULL,
                    business_info JSONB NOT NULL
                );
            """


            create_table_vendor = """
                CREATE TABLE IF NOT EXISTS journal_entries_cc (
                    id SERIAL PRIMARY KEY,
                    clientID VARCHAR(50),
                    date DATE ,
                    description TEXT ,
                    amount NUMERIC(10, 2) ,
                    debit_account VARCHAR(50) ,
                    credit_account VARCHAR(50) ,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """



            self.cursor.execute(create_table_statement_cc)  # Execute the query
            self.cursor.execute(create_table_vendor)  # Execute the query
            self.connection.commit()  # Commit the transaction
            st.success("Table 'transactions_cc' verified successfully.")
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
                    INSERT INTO journal_entries_cc (clientID, date, description, amount, debit_account, credit_account)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """)
                self.cursor.execute(insert_query, (
                    transaction['clientID'],
                    transaction['date'],
                    transaction['description'],
                    transaction['amount'],
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
