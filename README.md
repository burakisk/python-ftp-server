## Python Ftp Server 

<p> Here a simple FTP server in python and it provides basic tasks like uploading , downloading, removing, renaming files and adding new directory to the server.<p>

<p>This app will be running both the server and client on the same local machine.</p>
<p>In this project ftplib, pyftpdlib and wx libraries have been imported</p>
<p><b>! Remind python3 does not support wx library</b></p>

### Usage

Enter the following code at the command line to start the server
```
$ python server.py
```
now you can start the client 
```
$ python client.py
```
<p>you will see the login screen after the start command </p>

![LoginDialog](ss/loginDialog_ss.png?raw=true)

<p>enter server ip as 127.0.0.1, username as root and password as 1234 and then press login button</p>

<p> now you can start to use the local ftp app</p>

![mainPage](ss/mainPage_ss.png?raw=true)

### Properties

- <p>you can upload many files at the same time</p>
- <p>You can navigate on remote using the back and forward buttons</p>

![uploadFile](ss/uploadMultiFile_ss.png?raw=true)

- <p>You can change the name of the remove files or directories by pressing the rename button </p>
![renameFileName](ss/rename_ss.png?raw=true)

### other features 
- <p>You can download the name a files by pressing the download button </p>
- <p>You can remove the files by pressing the remove file button </p>
- <p>You can remove the <b>empty</b> directory by pressing the remove directory button </p>
