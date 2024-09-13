import os
# Email account credentials
imap_ssl_port = 993
username = "xaibooks@outlook.com"
password = "IBM3600s"
imap_server = "outlook.office365.com"
attachments_dir = "data/xaibooks/cc"

# pip install --upgrade certifi


# Create a directory to save attachments
if not os.path.isdir(attachments_dir):
    os.makedirs(attachments_dir)