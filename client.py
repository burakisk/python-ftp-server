import wx
from ftplib import FTP
import ftplib
import os

if "2.8" in wx.version():
    import wx.lib.pubsub.setupkwargs
    from wx.lib.pubsub import pub
else:
    from wx.lib.pubsub import pub

#host = '127.0.0.1'
port = 1026
ftp = FTP('')
ID_NEW = 1
ID_RENAME = 2
ID_REMOVEFILE = 3
ID_DOWNLOAD = 4
ID_REMOVEDIR = 5
ID_BACK = 6
ID_FORWARD = 7
ID_ONETRANSFER = 8
ID_MULTITRANSFER = 9
		
class LoginDialog(wx.Dialog):
    """Constructor"""
    def __init__(self):
        wx.Dialog.__init__(self, None, title="Login Dialog", size=(400, 160))
	#creating login gui
	serverip_sizer = wx.BoxSizer(wx.HORIZONTAL)
        serverip_lbl = wx.StaticText(self, label="Server ip:")
        serverip_sizer.Add(serverip_lbl, 0, wx.ALL | wx.CENTER, 5)
        self.serverip = wx.TextCtrl(self, size=(150, 30))  #creating input box 
        serverip_sizer.Add(self.serverip, 0, wx.LEFT | wx.RIGHT, 35)

        username_sizer = wx.BoxSizer(wx.HORIZONTAL)
        username_lbl = wx.StaticText(self, label="Username:")
	username_sizer.Add(username_lbl, 0, wx.ALL | wx.CENTER, 5)
        self.username = wx.TextCtrl(self, size=(150, 30))  # creating input box
        username_sizer.Add(self.username, 0, wx.LEFT | wx.RIGHT, 25)

        password_sizer = wx.BoxSizer(wx.HORIZONTAL)
        password_lbl = wx.StaticText(self, label="Password:")
        password_sizer.Add(password_lbl, 0, wx.ALL | wx.CENTER, 5)  # align center
        self.password = wx.TextCtrl(self, style=wx.TE_PASSWORD | wx.TE_PROCESS_ENTER,size=(150, 30))  # creating input box
        password_sizer.Add(self.password, 0, wx.LEFT | wx.RIGHT, 30)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(serverip_sizer, 0, wx.ALL, 5)
        main_sizer.Add(username_sizer, 0, wx.ALL, 5)
        main_sizer.Add(password_sizer, 0, wx.ALL, 5)
	
        btn = wx.Button(self, label="login", size=(300, 30))
        btn.Bind(wx.EVT_BUTTON, self.login)  # when is pressed the button call the Login function
        main_sizer.Add(btn, 0, wx.ALL | wx.CENTER, 5)

        self.SetSizer(main_sizer)

    def login(self, event):
       serverip = self.serverip.GetValue()
       username = self.username.GetValue()
       password = self.password.GetValue()
       print(username)
       print(password)
       print(serverip)
       try:	
        ftp.connect(serverip, port)
        res = ftp.login(username, password)
        if (res.lower().startswith('230 login successful')):
            global isConnect
            isConnect = True
            self.Destroy()
            main = Main()
            #main.show()
            #pub.sendMessage("frameListener", message="show")
            #self.Destroy()
       except ftplib.all_errors as e:
              print(e)
         
class ContentMain(wx.Panel):
      previousPath ="" #class variable
      def __init__(self, parent):
          wx.Panel.__init__(self, parent)  
          hbox = wx.BoxSizer(wx.HORIZONTAL)
            
          clientDirectoryTree_sizer = wx.BoxSizer(wx.VERTICAL)
          self.clientTree_lbl = wx.StaticText(self,-1,style = wx.ALIGN_CENTER,label="My Local Directory Tree") 
          self.dirClient = wx.GenericDirCtrl(self, -1, 
                        dir=os.path.expanduser('~'), # os.path.expanduser('~') == /home/burakisik 
                                 style=
                                       wx.DIRCTRL_3D_INTERNAL |
                                       wx.DIRCTRL_MULTIPLE,
                                 filter="*",size = (250,400))      
          clientDirectoryTree_sizer.Add(self.clientTree_lbl, 0, wx.ALL | wx.CENTER, 5)
          clientDirectoryTree_sizer.Add(self.dirClient, 0, wx.ALL | wx.CENTER, 5)

          #creating transfer buttons
          transfer_sizer = wx.BoxSizer(wx.VERTICAL)
          self.oneTransfer = wx.Button(self, ID_ONETRANSFER, '>')     
          self.multiTransfer = wx.Button(self, ID_MULTITRANSFER, '>>')    
          self.Bind(wx.EVT_BUTTON, self.uploadSingleFile, id=ID_ONETRANSFER)
          self.Bind(wx.EVT_BUTTON, self.uploadMultiFile, id=ID_MULTITRANSFER)
          transfer_sizer.Add(self.oneTransfer, 1,wx.CENTER, 5)
          transfer_sizer.Add(self.multiTransfer, 1,wx.CENTER, 5)
	        
          remoteDirectoryList_sizer = wx.BoxSizer(wx.VERTICAL)
	  self.remoteFiles_lbl = wx.StaticText(self,-1,style = wx.ALIGN_CENTER,label="Remote Directories and Files List")
          self.dirRemote = wx.ListBox(self, -1,size = (250,400))
          remoteDirectoryList_sizer.Add(self.remoteFiles_lbl, 0, wx.ALL | wx.CENTER, 5)
          remoteDirectoryList_sizer.Add(self.dirRemote,0, wx.ALL | wx.CENTER, 5)

          #creating back and forward button
	  navigation_sizer = wx.BoxSizer(wx.HORIZONTAL)  
          self.back = wx.Button(self, ID_BACK, 'BACK') 
          self.forward = wx.Button(self, ID_FORWARD, 'FORWARD')
          self.Bind(wx.EVT_BUTTON, self.goBack, id=ID_BACK)
          self.Bind(wx.EVT_BUTTON, self.goForward, id=ID_FORWARD)
          navigation_sizer.Add(self.back,0,wx.LEFT | wx.RIGHT, 5)
          navigation_sizer.Add(self.forward,0, wx.LEFT | wx.RIGHT, 5)	

	  remoteDirectoryList_sizer.Add(navigation_sizer,0, wx.ALL | wx.CENTER, 5)
          self.fillRemoteList(self)

          #creating items gui
          btnPanel = wx.Panel(self, -1)
          vbox = wx.BoxSizer(wx.VERTICAL)
          self.itemstag_lbl = wx.StaticText(btnPanel,-1,style = wx.ALIGN_CENTER,label="Items")
          new = wx.Button(btnPanel, ID_NEW, 'mkDir', size=(110, 30))
          rename = wx.Button(btnPanel, ID_RENAME, 'Rename', size=(110, 30))
          removeFile = wx.Button(btnPanel, ID_REMOVEFILE, 'Remove File', size=(110, 30))
          download = wx.Button(btnPanel, ID_DOWNLOAD, 'Download', size=(110, 30))
          removeDir = wx.Button(btnPanel, ID_REMOVEDIR, 'Remove Dir', size=(110, 30))
          
          self.Bind(wx.EVT_BUTTON, self.NewItem, id=ID_NEW)
          self.Bind(wx.EVT_BUTTON, self.OnRename, id=ID_RENAME)
          self.Bind(wx.EVT_BUTTON, self.OnRemoveFile, id=ID_REMOVEFILE)
          self.Bind(wx.EVT_BUTTON, self.OnDownload, id=ID_DOWNLOAD)
          self.Bind(wx.EVT_BUTTON, self.OnRemoveDir, id=ID_REMOVEDIR)
          self.Bind(wx.EVT_LISTBOX_DCLICK, self.OnRename) # Call the onRename function when list item is clicked

          #vbox.Add((-1, 20))
          vbox.Add(self.itemstag_lbl ,0, wx.ALL | wx.CENTER, 5)
          vbox.Add(new)
          vbox.Add(rename, 0, wx.TOP, 5)
          vbox.Add(removeFile, 0, wx.TOP, 5)
          vbox.Add(removeDir, 0, wx.TOP, 5)
          vbox.Add(download, 0, wx.TOP, 5)

          btnPanel.SetSizer(vbox)
          hbox.Add(clientDirectoryTree_sizer,0.6,wx.EXPAND | wx.RIGHT, 20)
          hbox.Add(transfer_sizer,0.6,wx.CENTER, 20)
          hbox.Add(remoteDirectoryList_sizer,0.6,wx.EXPAND | wx.RIGHT, 20)
          hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
          
          self.SetSizer(hbox)
	  #self.Fit() 
          self.Centre()
          self.Show(True)
     
      def NewItem(self, event):
          try:    
             text = wx.GetTextFromUser('Enter Directory Name', 'Create New Directory')
             if text != '':
                ftp.mkd(text)
                self.dirRemote.Append(text)
                self.fillRemoteList(self)
          except:
                 dial = wx.MessageDialog(None, 'Unvalid Name', 'Error',wx.OK | wx.ICON_ERROR)
                 dial.ShowModal()
            
      def OnRename(self, event):
          try:
              sel = self.dirRemote.GetSelection()
              text = self.dirRemote.GetString(sel)
              renamed = wx.GetTextFromUser('Enter New Name', 'Rename File or Directory Name', text)
              if renamed != '':
                 ftp.rename(text, renamed)
                 self.dirRemote.Delete(sel)
                 self.dirRemote.Insert(renamed, sel)
                 self.fillRemoteList(self)
          except:
                dial = wx.MessageDialog(None, 'Please Choose File in Remote File List', 'Error',wx.OK | wx.ICON_ERROR)
                dial.ShowModal()
              
      def OnRemoveFile(self, event):
          try:
              sel = self.dirRemote.GetSelection()
              text = self.dirRemote.GetString(sel)
              if sel != -1:
                 ftp.delete(text)
                 self.dirRemote.Delete(sel)
                 self.fillRemoteList(self) #reflesh remote list
          except:
                 dial = wx.MessageDialog(None, 'Please Choose Just a File in Remote List','Error',wx.OK | wx.ICON_ERROR)
                 dial.ShowModal()
			
      def OnRemoveDir(self, event):
          try:
              sel = self.dirRemote.GetSelection()
              text = self.dirRemote.GetString(sel)
              if sel != -1:
                 ftp.rmd(text)
                 self.dirRemote.Delete(sel)
                 self.fillRemoteList(self) #reflesh remote list
          except:
                 dial = wx.MessageDialog(None, 'Please Choose Just a Directory in Remote List','Error',wx.OK | wx.ICON_ERROR)
                 dial.ShowModal()

      def OnDownload(self, event):
          try:
              sel = self.dirRemote.GetSelection()
              filename = self.dirRemote.GetString(sel)
              if sel != -1:
                 localfile = open(filename, 'wb')
                 ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
          except:
               dial = wx.MessageDialog(None, 'Please Choose Just a File in Remote Directory Tree','Error',wx.OK | wx.ICON_ERROR)
               dial.ShowModal()

      def uploadSingleFile(self, event): 
          try:
             path = self.dirClient.GetPath() #GetFilePath() #GetDefaultPath() #GetSelections() #GetFilePath()     
             #print self.dirClient.GetPath()             
             if os.path.isfile(path):
                fileName = os.path.basename(path)
                print fileName
                ftp.storbinary('STOR ' + fileName, open(path,'rb'))
                self.fillRemoteList(self) #reflesh dirremote list
             else:
                  dial = wx.MessageDialog(None, 'Please Choose just One File not Directory in Client Directory Tree', 'Error',wx.OK | wx.ICON_ERROR)
                  dial.ShowModal()
          except:
              dial = wx.MessageDialog(None, 'Please Choose just One File not Directory in Client Directory Tree', 'Error',wx.OK | wx.ICON_ERROR)
              dial.ShowModal()
          
      def uploadMultiFile(self,event):
          try:
              paths = self.dirClient.GetFilePaths()
              if paths: #list paths if not empty
                 for path in paths:
                     if os.path.isfile(path): 
                        fileName = os.path.basename(path)
                        ftp.storbinary('STOR ' + fileName, open(path,'rb'))
                        self.fillRemoteList(self) #reflesh dirremote list
             
              else:
                   dial = wx.MessageDialog(None, 'Please Choose one File or lots of File not Directories in Client Directory Tree', 'Error',wx.OK | wx.ICON_ERROR)
                   dial.ShowModal()

          except:
              dial = wx.MessageDialog(None, 'Please Choose Files not Directories in Client Directory Tree', 'Error',wx.OK | wx.ICON_ERROR)
              dial.ShowModal()
	                   
      def goBack(self, event):
          try:
             print self.previousPath
             if self.previousPath != '':
                ftp.cwd(self.previousPath)
                self.fillRemoteList(self)
          except ftplib.all_errors as er:
                 print (er)
          
      def goForward(self, event):
          try:
              sel = self.dirRemote.GetSelection()
              dirname = self.dirRemote.GetString(sel)
              if dirname != '':
	         self.previousPath = ftp.pwd() #register the previous path
                 ftp.cwd(dirname)
                 #print ftp.pwd()
                 self.fillRemoteList(self)
          except ftplib.all_errors as er:
                 print (er)
      @staticmethod	
      def fillRemoteList(self):
          self.dirRemote.Clear() #clear remote files and directories's list
          try:
            files = []
            ftp.retrlines('LIST',lambda line: files.append(line.split()[-1])) #thanks to split function return only file or dir "name" instead of size, type, modified date etc. #ftp.retrlines('LIST',files.append)
            for file in files: 
	        self.dirRemote.Append(file)
          except ftplib.all_errors as er:
                 print (er)
                 """if str(er) == "550 No files found":
                       print "No files in this directory"
                    else:
                 raise"""

class Main(wx.Frame):
      def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Main Page", size=(785,500),style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER)
        panel = ContentMain(self)
 	pub.subscribe(self.myListener, "frameListener")
        #Ask user to login
        #dlg = LoginDialog()
        #dlg.ShowModal()
	self.Show()
        
      def myListener(self, message, arg2=None):
          self.Show()

if __name__ == "__main__":
   app = wx.App(False)
   login= LoginDialog()
   login.ShowModal()
   app.MainLoop()

