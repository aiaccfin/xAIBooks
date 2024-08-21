import streamlit as st
import os, email, imaplib
from email.header import Header, decode_header, make_header

import config.config as cfg

def email_extraction():

    # Connect to the email server
    m = imaplib.IMAP4_SSL(cfg.imap_server, cfg.imap_ssl_port)
    m.login(cfg.username, cfg.password)

    # Select the mailbox you want to check (e.g., 'inbox')
    m.select("INBOX")

    status, folders = m.list()
    retrieved_folder = "Retrieved"
    if f' "{retrieved_folder}"' not in folders:
        m.create(retrieved_folder)

    # Search for all emails in the inbox
    # status, messages = m.search(None, "ALL")
    status, messages = m.uid('search', None, "ALL")

    # Convert messages to a list of email IDs
    email_ids = messages[0].split()

    for email_id in email_ids:
        # Fetch the email by ID
        status, msg_data = m.uid('fetch', email_id, "(RFC822)")

        for response_part in msg_data:
            if isinstance(response_part, tuple):
                # Parse the email
                msg = email.message_from_bytes(response_part[1])

                # From email
                from_ = msg.get("From")
                st.write("From:", from_)

                # Decode email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                st.write("Subject:", subject)

                # Initialize a variable to hold the plain text body
                body = None

                # Check if the email has multiple parts
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = part.get("Content-Disposition")

                        # If it's a plain text part, extract the body
                        if content_type == "text/plain" and content_disposition is None:
                            try:
                                body = part.get_payload(decode=True).decode("utf-8")
                            except UnicodeDecodeError:
                                body = part.get_payload(decode=True).decode("ISO-8859-1")  # Fallback encoding
                            st.write("Email body (text/plain):", body)
                        
                        # Save attachments
                        if content_disposition and "attachment" in content_disposition:
                            filename = part.get_filename()
                            if filename:
                                filename = decode_header(filename)[0][0]
                                if isinstance(filename, bytes):
                                    filename = filename.decode()
                                filepath = os.path.join(cfg.attachments_dir, filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                st.write(f"Saved attachment: {filepath}")
                else:
                    # If the email is not multipart, it might be plain text
                    content_type = msg.get_content_type()
                    if content_type == "text/plain":
                        try:
                            body = msg.get_payload(decode=True).decode("utf-8")
                        except UnicodeDecodeError:
                            body = msg.get_payload(decode=True).decode("ISO-8859-1")  # Fallback encoding
                        st.write("Email body (text/plain):", body)

                # If no plain text body was found, print a message
                if not body:
                    st.write("No plain text body found for this email.")

        # Move the email to the "Retrieved" folder
        # m.uid('COPY', email_id, retrieved_folder)
        # m.uid('STORE', email_id, '+FLAGS', '(\Deleted)')
        # m.expunge()  # Permanently remove emails marked for deletion

        # Close the server connection
        m.close()
        m.logout()
