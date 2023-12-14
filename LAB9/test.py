from ftplib import FTP
ftp = FTP('138.68.98.108')
ftp.login(user='yourusername', passwd='yourusername')
ftp.delete('remote_file.txt')

hostname = '138.68.98.108'
username = 'yourusername'
password = 'yourusername'

ftp = FTP(hostname)
ftp.login(user=username, passwd=password)

ftp.cwd('') 

contents = []
ftp.dir(contents.append)

for line in contents:
    print(line)

ftp.quit()


