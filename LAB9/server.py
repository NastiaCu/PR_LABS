import os
import tkinter as tk
from tkinter import filedialog
from ftplib import FTP
import smtplib
from email.mime.text import MIMEText

def upload_file_ftp():
    try:
        hostname = '138.68.98.108'
        username = 'yourusername'
        password = 'yourusername'
        
        local_file_path = file_path_entry.get()
        file_name = os.path.basename(local_file_path) 
        
        ftp = FTP(hostname)
        ftp.login(user=username, passwd=password)
        
        ftp.cwd('FAF-211')
        ftp.pwd()

        working_directory = 'Cunev' 
        if os.path.isdir(working_directory): 
            ftp.mkd(working_directory)

        ftp.cwd(working_directory)
        wb = ftp.pwd()

        with open(local_file_path, 'rb') as file:
            ftp.storbinary(f'STOR {file_name}', file)  
        
        ftp.quit()
        
        file_url = f"ftp://{username}:{password}@{hostname}/{wb}/{file_name}"
        send_email(file_url)  
        status_label.config(text="File uploaded successfully!")
    
    except Exception as e:
        print(f"File upload failed. Error: {str(e)}")
        status_label.config(text="File upload failed.")

def send_email(file_url):
    subject = subject_entry.get()
    body = body_entry.get("1.0", tk.END)
    sender = ' ' 
    password = ' '
    recipient_email = recipient_entry.get()

    body_with_url = f"{body}\n\nFile URL: {file_url}"

    msg = MIMEText(body_with_url)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient_email, msg.as_string())
            status_label.config(text="Email sent successfully!")
        return True
    
    except Exception as e:
        print(f"Email sending failed. Error: {str(e)}")
        status_label.config(text="Email sending failed.")
        return False

def browse_file():
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(tk.END, filedialog.askopenfilename())

root = tk.Tk()
root.title("FTP File Upload and Email")

file_path_label = tk.Label(root, text="File Path:")
file_path_label.pack()

file_path_entry = tk.Entry(root)
file_path_entry.pack()

browse_button = tk.Button(root, text="Browse", command=browse_file)
browse_button.pack()

recipient_label = tk.Label(root, text="Recipient Email:")
recipient_label.pack()
recipient_entry = tk.Entry(root)
recipient_entry.pack()

subject_label = tk.Label(root, text="Subject:")
subject_label.pack()
subject_entry = tk.Entry(root)
subject_entry.pack()

body_label = tk.Label(root, text="Body:")
body_label.pack()
body_entry = tk.Text(root, height=5)
body_entry.pack()

upload_button = tk.Button(root, text="Upload File and Send Email", command=upload_file_ftp)
upload_button.pack()

status_label = tk.Label(root, text="")
status_label.pack()

root.mainloop()
