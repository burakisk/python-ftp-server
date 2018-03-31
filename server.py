from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

authorizer = DummyAuthorizer()
authorizer.add_user("root", "pass", "/home/burakisik/Documents/bilgisayar-aglari/ftpserver-python/serverFiles", perm="elradfmw") #The third paramater is root directory of ftp server

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 1026), handler)
server.serve_forever()
