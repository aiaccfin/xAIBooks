import os
# Email account credentials
imap_ssl_port = 993
username = "xaibooks@outlook.com"
password = "mFQi6JjQpKm1XA3Vo0fg"
imap_server = "outlook.office365.com"
# imap_server = "imap-mail.outlook.com"


cc_attachments_dir = "data/xaibooks/cc"
bank_attachments_dir = "data/xaibooks/bank"

# pip install --upgrade certifi
biz_id = 888

# Create a directory to save attachments
if not os.path.isdir(cc_attachments_dir):
    os.makedirs(cc_attachments_dir)