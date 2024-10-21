import streamlit as st
from streamlit_extras.stateful_button import button

import os, re, glob, pandas

from apps.db.db_postgres import PGHandler
from apps.utils import streamlit_components
from apps.llm.openai_api import get_vendor, get_coa, get_vendor_information, get_journal_entry_cc2
from apps.data_entry import email_processing, pdf_processing

streamlit_components.streamlit_ui('🦣 Dashboard for Accountant')
pg_handler = PGHandler()
# -----------------------------------------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["Transactions", "Book Journal", 'Journal Entries',''])

with tab1:
    df = pg_handler.get_journal('cc_transactions')
    df.columns = ['client id', 'Date', 'Desc', 'Amount','COA', 'Vendor','debit', 'credit']

    st.dataframe(df)

with tab2:
    if button("Load Credit Card Statement?", key='key1'):
        with st.spinner('Extracting Credit Card Statement...'):

            folder_path = "./data/xaibooks/cc"

            pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
            pdf_files.sort(key=os.path.getmtime, reverse=True)

            if pdf_files:
                pdf_path = pdf_files[0]  # The latest file
            else:
                print("No PDF files found.")

            extracted_data = pdf_processing.extract_pdf_lines(pdf_path)
            st.text(extracted_data)
        st.success('Credit Card Statement Extracted!')

    # if button("Save Credit Card Statement?", key='key111'):
    #     with st.spinner('Save Credit Card Statement...'):
    #
    #         transactions = []
    #         for entry in extracted_data:
    #             text = entry['text']
    #
    #             # match = re.match(r'(\d{2}/\d{2}/\d{2})\*? (.+) (-?\$\d{1,3}(?:,\d{3})*\.\d{2})$', text) #Amex
    #             # match = re.match(r'(\d{2}/\d{2})\s+\d{2}/\d{2}\s+(.+?)\s+(-?\$\d{1,3}(?:,\d{3})*\.\d{2})$', text)
    #             match = re.match(r'(\d{2}/\d{2})\s+\d{2}/\d{2}\s+(.+?)\s+(-?\$?[\d,]+(?:\.\d{2})?)$', text) #BOA
    #
    #             if match:
    #                 date, description, amount = match.groups()
    #                 amount = amount.replace('$', '')
    #                 amount = float(amount.replace(',', ''))
    #
    #                 transactions.append({
    #                     'clientID': 'CC888',
    #                     'date': date,
    #                     'description': description,
    #                     'amount': amount,
    #                 })
    #
    #         df_cc = pandas.DataFrame(transactions)
    #
    #         # df = df.drop(columns=['description'])
    #         st.dataframe(df_cc)
    #
    #     st.success('Credit Card Statement Extracted!')


    if button("Process for Vendor and COA?", key='key2'):
        with st.spinner('AI analyzing vendor and COA...'):
            transactions = []
            for entry in extracted_data:
                text = entry['text']
                # match = re.match(r'(\d{2}/\d{2}/\d{2})\*? (.+) (-?\$\d{1,3}(?:,\d{3})*\.\d{2})$', text) # Amex
                match = re.match(r'(\d{2}/\d{2})\s+\d{2}/\d{2}\s+(.+?)\s+(-?\$?[\d,]+(?:\.\d{2})?)$', text)

                if match:
                    date, description, amount = match.groups()
                    amount = amount.replace('$', '')
                    amount = float(amount.replace(',', ''))
                    vendor_name = get_vendor(description)
                    COA = get_coa(vendor_name)

                    pg_handler.save_vendor_if_not_exists(vendor_name)

                    transactions.append({
                        'clientID': 'CC888',
                        'date': date,
                        'description': description,
                        'amount': amount,
                        'vendor_name': vendor_name,
                        'COA': COA
                    })

            df = pandas.DataFrame(transactions)
            df['vendor_name'] = df['vendor_name'].str.replace(r'^\s*Vendor Name:\s*', '',
                                                              regex=True)  # Remove "Vendor Name:" prefix
            df['vendor_name'] = df['vendor_name'].str.replace(r'\*\*', '',
                                                              regex=True)  # Remove Markdown-style bold formatting
            df['vendor_name'] = df['vendor_name'].str.replace(r'\"', '', regex=True)  # Remove extra quotation marks
            df['COA'] = df['COA'].str.replace(r'\"', '', regex=True)  # Remove extra quotation marks

            # df = df.drop(columns=['description'])
            st.dataframe(df)

            # pg_handler.save_cc_postgres(transactions)


    if button("Book Journals for above transactions", key='key2213'):
        def safe_search(pattern, text):
            match = re.search(pattern, text, re.IGNORECASE)
            return match.group(1) if match else None

        transactions = []
        all_journal_entries = []
        for index, row in df.iterrows():
            transaction = f"Row {index + 1}: ID: {row['clientID']}, Date: {row['date']}, Description: {row['description']} , COA: {row['COA']} , vendor_name: {row['vendor_name']}, Amount: {row['amount']}"
            st.text(transaction)
            entry = get_journal_entry_cc2(transaction)[0]
            st.text(entry)

            date = safe_search(r"Date: ([\d/]+)", entry)
            description = safe_search(r"Description: ([^,]+),", entry)
            COA = safe_search(r"COA: ([^,]+),", entry)
            vendor_name = safe_search(r"vendor_name: ([^,]+),", entry)

            amount_str = safe_search(r"amount: (-?\$?[\d.]+)", entry)  # Updated to include negative amounts
            amount = float(amount_str.replace('$',
                                              '')) if amount_str else None  # Convert to float if a match is found, removing dollar sign

            debit_account = safe_search(r"Debit: ([\w\s]+) \$\d+\.\d+", entry)
            credit_account = safe_search(r"Credit: ([\w\s]+) \$\d+\.\d+", entry)

            all_journal_entries.append({
                'clientID': 'CC888',
                'date': date,
                'description': description,
                'amount': amount,
                'vendor_name': vendor_name,
                'COA': COA,
                'debit_account': debit_account,
                'credit_account': credit_account
            })

        df = pandas.DataFrame(all_journal_entries)
        st.dataframe(df)

        pg_handler.save_cc_journal_postgres(all_journal_entries)


with tab3:
    def split_debit_credit(df):
        rows = []
        for _, row in df.iterrows():
            debit_row = {'clientid': row['clientid'], 'date':row['date'],'description': row['description'],  'debit_account': row['debit_account'], 'debit': abs(row['amount']), 'credit': 0}
            credit_row = {'clientid': row['clientid'], 'date':row['date'],'description': row['description'], 'credit_account': row['credit_account'], 'debit': 0, 'credit': abs(row['amount'])}
            rows.extend([debit_row, credit_row])
        return pandas.DataFrame(rows)

    df = pg_handler.get_journal('cc_transactions')
    new_df = split_debit_credit(df)

    # Display the result in Streamlit
    st.dataframe(new_df)
    if button("Save to DB?", key='key22133'):
        pg_handler.save_cc_journal_postgres_2(new_df)

