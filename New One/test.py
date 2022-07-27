import pysftp
# credentials of targeted sftp server
host = '10.245.15.21'
port = 22
username = 'ecards'
password= 'Ecards2022!'
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
try:
  conn = pysftp.Connection(host=host,port=port,username=username, password=password, cnopts=cnopts)
  print("connection established successfully")
  with conn.cd('/home/ecards/oldtoms'):  # chdir to public
      conn.put('C:\ENR-TOM\config\serial')  # upload file to nodejs/

  # Closes the connection
  conn.close()
  print("done")
except:
  print('failed to establish connection to targeted server')
