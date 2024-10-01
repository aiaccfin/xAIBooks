import os
# Email account credentials
imap_ssl_port = 993
username = "xaibooks@outlook.com"
password = "IBM3600s"
imap_server = "outlook.office365.com"
cc_attachments_dir = "data/xaibooks/cc"
bank_attachments_dir = "data/xaibooks/bank"

# pip install --upgrade certifi


# Create a directory to save attachments
if not os.path.isdir(cc_attachments_dir):
    os.makedirs(cc_attachments_dir)