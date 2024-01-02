
import os
import json
import socket
import threading
import shutil
from Base import Base
import model
 
# GUI
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
import customtkinter


# aid
from hashfunction import MD5_hash

# ----CONSTANT----#
FORMAT = "utf-8"
BUFFER_SIZE = 2048
OFFSET = 10000

# --------------- #
# --------------- #
customtkinter.set_default_color_theme("dark-blue")

# popup notification
def display_noti(title, content):
    tkinter.messagebox.showinfo(title, content)

## ====================GUI IMPLEMENT======================##
class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.chatroom_textCons = None

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, RegisterPage, LoginPage, RepoPage):
            frame = F(parent=container, controller=self)
            # initializing frame of that object from
            # startpage, registerpage, loginpage, chatpage respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg='white')
        self.show_frame(StartPage)
    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # set color mode
        customtkinter.set_default_color_theme("blue")
        # create title
        self.page_title = customtkinter.CTkLabel(self, text="File transfer service", font=("Arial Bold", 36))
        self.page_title.pack(padx=10, pady=(80, 10))
        # set port label
        self.port_label = customtkinter.CTkLabel(self, text="Nhập giá trị port trong khoảng (1024 -> 65535)", font=("Arial", 20))
        self.port_label.pack(padx=10, pady=10)
        # set port entry
        self.port_entry = customtkinter.CTkEntry(self, placeholder_text="Nhập port number", border_width=1,width=250)
        self.port_entry.pack(padx=10, pady=10)
        # create a register button
        self.register_button = customtkinter.CTkButton(self, text="Đăng ký", command=lambda: 
                                self.enter_app(controller=controller, port=self.port_entry.get(), page=RegisterPage),fg_color="#192655",font=customtkinter.CTkFont(size=12, weight="bold"))
        self.register_button.pack(padx=10, pady=10)
        # create a login button
        self.login_button = customtkinter.CTkButton(self, text="Đăng nhập", command=lambda: 
                                self.enter_app(controller=controller, port=self.port_entry.get(), page=LoginPage),fg_color="#192655",font=customtkinter.CTkFont(size=12, weight="bold"))
        self.login_button.pack(padx=10, pady=10)

    def enter_app(self, controller, port, page):
        try:
            # get peer current ip address -> assign to serverhost
            hostname=socket.gethostname()   
            IPAddr=socket.gethostbyname(hostname)  

            # init server
            global network_peer
            network_peer = NetworkPeer(serverhost=IPAddr, serverport=int(port))
           
            # A child thread for receiving message
            recv_t = threading.Thread(target=network_peer.input_recv)
            recv_t.daemon = True
            recv_t.start()

            # A child thread for receiving file
            recv_file_t = threading.Thread(target=network_peer.recv_file_content)
            recv_file_t.daemon = True
            recv_file_t.start()
            controller.show_frame(page)
        except:
            self.port_entry.delete(0, customtkinter.END)
            display_noti("Port Error!",  "Cổng đã được sử dụng hoặc chứa giá trị rỗng")

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        customtkinter.set_default_color_theme("blue")
        # Sign Up Image
        # signup_pic = ImageTk.PhotoImage(asset.signup_image)
        # self.signupImg = tkinter.Label(self, image=signup_pic, bg='white')
        # self.signupImg.image = signup_pic
        # self.signupImg.place(x=50, y=50)        

        self.frame = customtkinter.CTkFrame(master=self, fg_color="white")
        self.frame.pack(fill='both', expand=True)

        self.title_label = customtkinter.CTkLabel(self.frame, text="Đăng ký tài khoản", font=("Roboto Bold", 32))
        self.title_label.pack(pady=(80, 10),padx=10)

        self.username = customtkinter.CTkLabel(self.frame, text="Tài khoản", font=("Roboto", 14))
        self.username.pack(pady=(0),padx=10)
        self.username_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Nhập tài khoản",  width=250,font=("Roboto", 12))
        self.username_entry.pack(pady=(0),padx=10)

        self.password = customtkinter.CTkLabel(self.frame, text="Mật khẩu", font=("Roboto", 14))
        self.password.pack(pady=(0),padx=10)
        self.password_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Nhập mật khẩu",  width=250,font=("Roboto", 12), show = '*')
        self.password_entry.pack(pady=(0, 10),padx=10)

        # Submit
        customtkinter.CTkButton(self.frame, text='Đăng ký', fg_color="#192655",font=customtkinter.CTkFont(size=12, weight="bold"),command=lambda: 
                                self.register_user(self.username_entry.get(), self.password_entry.get())).pack(pady=(0, 10),padx=10)
                                                                                                            
        customtkinter.CTkLabel(self.frame, text="Đã có tài khoản ?",font=("Roboto", 11)).pack(pady=(10, 0),padx=10)
        customtkinter.CTkButton(self.frame, text='Đăng nhập', fg_color="#192655",font=customtkinter.CTkFont(size=12, weight="bold"),command=lambda: controller.show_frame(LoginPage)).pack(pady=(0, 10),padx=1)

    def register_user(self, username, password):
        network_peer.name = str(username)
        # hash password by MD5 algorithm
        network_peer.password = MD5_hash(str(password))
        self.username_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)
        network_peer.send_register()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Login Image
        # login_pic = ImageTk.PhotoImage(asset.login_image)
        # loginImg = tkinter.Label(self, image=login_pic)
        # loginImg.image = login_pic
        # loginImg.place(x=50, y=50)
        self.frame = customtkinter.CTkFrame(master=self, fg_color="white")
        self.frame.pack(fill='both', expand=True)

        self.title_label = customtkinter.CTkLabel(self.frame, text="Đăng nhập", font=("Roboto Bold", 32))
        self.title_label.pack(pady=(80, 10),padx=10)

        self.username = customtkinter.CTkLabel(self.frame, text="Tài khoản", font=("Roboto", 14))
        self.username.pack(pady=(0),padx=10)
        self.username_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Nhập Tài khoản", width=250,font=("Roboto", 12))
        self.username_entry.pack(pady=(0),padx=10)

        self.password = customtkinter.CTkLabel(self.frame, text="Mật khẩu", font=("Roboto", 14))
        self.password.pack(pady=(0),padx=10)
        self.password_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Nhập Mật khẩu",  width=250,font=("Roboto", 12), show = '*')
        self.password_entry.pack(pady=(0, 10),padx=10)

        customtkinter.CTkButton(self.frame, text='Đăng nhập', fg_color="#192655",font=customtkinter.CTkFont(size=12, weight="bold"), command=lambda:
                                self.login_user(username=self.username_entry.get(), password=self.password_entry.get())).pack(pady=(0, 10),padx=10)
        customtkinter.CTkLabel(self.frame, text="Bạn không có tài khoản ?", font=("Roboto", 11)).pack(pady=(10, 0),padx=10)
        customtkinter.CTkButton(self.frame, text='Đăng ký', font=customtkinter.CTkFont(size=12, weight="bold"),fg_color="#192655", cursor="hand2", command=lambda: controller.show_frame(RegisterPage)).pack(pady=(0, 10),padx=10)
    
    def login_user(self, username, password):
        network_peer.name = str(username)
        # hash password by MD5 algorithm
        network_peer.password = MD5_hash(str(password))
        self.username_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)
        network_peer.send_login()

class RepoPage(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent)
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure(( 1), weight=1)

        #### create frame for repo
        self.repo_frame = customtkinter.CTkFrame(self, fg_color="#DBE2EF",corner_radius=10)
        self.repo_frame.grid(row=0, column=3, sticky="nsew",pady=(10,10),padx=(10, 10))
        self.repo_frame.grid_rowconfigure(0, weight=1)
        self.repo_frame.grid_columnconfigure(0, weight=1)
        # create scrollable frame for repo list
        ## to do: add file names to this frame
        self.scrollable_repo_frame = customtkinter.CTkScrollableFrame(self, label_text="Repository",label_text_color="#3F72AF",fg_color="#DBE2EF")
        self.scrollable_repo_frame.grid(row=0, column=0,columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_repo_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_file_names = []
        self.fileListBox = tk.Listbox(self.scrollable_repo_frame, width=145, height=20)
        self.fileListBox.grid(row=0, column=0, padx=10,columnspan=3, pady=(10, 10))

        # create temp frame
        self.temp_frame = customtkinter.CTkFrame(master=self.repo_frame, fg_color="transparent")
        self.temp_frame.grid(row=0, column=1, sticky="nsew")
        # self.temp_frame.grid_rowconfigure(0, weight=1)
        # self.temp_frame.grid_columnconfigure(0, weight=1)
        # self.temp_frame.grid_columnconfigure(1, weight=1)
        # create delete button
        self.delete_button = customtkinter.CTkButton(master=self.temp_frame, border_width=2, text="Xóa file", fg_color="#192655",command=lambda: self.deleteSelectedFile())
        self.delete_button.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create choose file button 
        self.add_button = customtkinter.CTkButton(master=self.temp_frame, border_width=2, text="Tải file lên repository",fg_color="#192655", command=lambda: self.chooseFile())
        self.add_button.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create update to server button
        self.update_button = customtkinter.CTkButton(master=self.temp_frame, border_width=2, text="Cập nhật Server", fg_color="#192655",command=lambda: self.updateListFile())
        self.update_button.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create reload repo button
        self.update_button = customtkinter.CTkButton(master=self.temp_frame, border_width=2, text="Reload repository", fg_color="#192655",command=lambda: self.reloadRepo())
        self.update_button.grid(row=3, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

        self.greeting_label_var = tk.StringVar()
        self.greeting_label = customtkinter.CTkLabel(master=self.temp_frame, textvariable=self.greeting_label_var, font=("Roboto", 14))
        self.greeting_label.grid(row=4, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")


        ####

        self.peer_frame = customtkinter.CTkFrame(self, fg_color="#DBE2EF",corner_radius=10)
        self.peer_frame.grid(row=2, column=3,sticky="nsew",padx=(10,10),pady=(10,10))
        self.peer_frame.grid_rowconfigure(1, weight=1)
        self.peer_frame.grid_columnconfigure(1, weight=1)   
        # # ###
        self.scrollable_peer_frame = customtkinter.CTkScrollableFrame(self, label_text="Peer List",label_text_color="#3F72AF",fg_color="#DBE2EF")
        self.scrollable_peer_frame.grid(row=2, column=0,columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_peer_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_peer_names = []
        self.peerListBox = tk.Listbox(self.scrollable_peer_frame, width=175, height=20)
        self.peerListBox.grid(row=0, column=1, padx=10, pady=(10, 10))
        # # ####
        #  29/11
        # self.search_frame = customtkinter.CTkFrame(self.peer_frame, fg_color="#DBE2EF")
        # self.search_frame.grid(row=2, column=6, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # self.search_frame.grid_rowconfigure(0, weight=1)
        # self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_entry = customtkinter.CTkEntry(master=self.peer_frame, placeholder_text="Search...")
        self.search_entry.grid(row=4, column=2,padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.search_button = customtkinter.CTkButton(master=self.peer_frame, text="Search", border_width=2, command=lambda: self.get_users_share_file_from_entry(),fg_color="#192655")
        self.search_button.grid(row=5, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create send connect request button
        self.request_button = customtkinter.CTkButton(master=self.peer_frame, border_width=2,
                                                     command=lambda:self.fileRequest(), text="Gửi yêu cầu kết nối",fg_color="#192655")
        self.request_button.grid(row=6, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        
        #create CLI
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Command...")
        self.entry.grid(row=4, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(self, text="Enter", command = lambda:self.commandLine(command = self.entry.get()), fg_color="#192655", border_width=2)
        self.main_button_1.grid(row=4, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.main_button_2 = customtkinter.CTkButton(self, text="Thoát", command=lambda: self.quit_user(), fg_color="#192655", border_width=2,font=customtkinter.CTkFont(size=15, weight="bold"))
        self.main_button_2.grid(row=4, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")


    def update_user_greeting(self, username):
        """Cập nhật nhãn chào mừng với tên người dùng."""
        greeting = f"Xin chào, {username}!"
        print(greeting)
        self.greeting_label_var.set(greeting)

    def logout_user(self):
        network_peer.send_logout_request()
        app.show_frame(StartPage)

    def quit_user(self):
        network_peer.send_logout_request()
        app.destroy()
    
    def commandLine(self, command):
        parts = command.split()

        if parts[0] == "publish":
            if len(parts) == 3:
                file_path = parts[1]
                file_name = parts[2]
                #Implement something to update file to server here#
                #To do#
                network_peer.updateToServer(file_name, file_path)
                self.fileListBox.insert(0,file_name + "(" + file_path +")")
                self.sendtoServerPath(file_path)
                
            else:
                message = "Lệnh không hợp lệ vui lòng nhập lại!"
                tkinter.messagebox.showinfo(message)
        elif parts[0] == "fetch":
            if len(parts) == 2:
                file_name = parts[1]
                #Implement something to search file and doawnload it#
                #To do#
                network_peer.send_listpeer(file_name)
                peer_info = self.peerListBox.get(0)
                network_peer.send_request(peer_info, file_name)
            else:
                message = "Lệnh không hợp lệ vui lòng nhập lại!"
                tkinter.messagebox.showinfo(message)
        else:
            message = "Lệnh không hợp lệ vui lòng nhập lại!"
            tkinter.messagebox.showinfo(message)

    def sendFile(self, peername):
        file_path = tkinter.filedialog.askopenfilename(initialdir="/",
                                                       title="Select a File",
                                                       filetypes=(("All files", "*.*"),))
        file_name = os.path.basename(file_path)
        msg_box = tkinter.messagebox.askquestion('File Explorer', 'Are you sure to send {} to {}?'.format(file_name, peername),
                                                 icon="question")
        if msg_box == 'yes':
            sf_t = threading.Thread(
                target=network_peer.transfer_file, args=(peername, file_path))
            sf_t.daemon = True
            sf_t.start()
            tkinter.messagebox.showinfo(
                "File Transfer", '{} has been sent to {}!'.format(file_name, peername))
            
    def sendtoLocalPath(self, file_path):
        # create a folder named "repo" in this folder
        if not os.path.exists("localRepo1"):
            os.makedirs("localRepo1")
        destination = os.path.join(os.getcwd(), "localRepo1")
        shutil.copy(file_path, destination)

    def sendtoServerPath(self, file_path):
        # create a folder named "repo" in this folder
        if not os.path.exists("serverRepo"):
            os.makedirs("serverRepo")
        destination = os.path.join(os.getcwd(), "serverRepo")
        shutil.move(file_path, destination)    

    def chooseFile(self):
        file_path = tkinter.filedialog.askopenfilename(initialdir="/",
                                                       title="Select a File",
                                                       filetypes=(("All files", "*.*"),))
        # file_name = os.path.basename(file_path)
        file_name = file_path
        msg_box = tkinter.messagebox.askquestion('File Explorer', 'Upload {} to local repository?'.format(file_name),
                                                 icon="question")
        if msg_box == 'yes':
            # popup = simpledialog.askstring("Input","Nhập tên file trên Localrepo",parent = self)
            self.fileListBox.insert(0,file_name)
            tkinter.messagebox.showinfo(
                "Local Repository", '{} has been added to localrepo1!'.format(file_name))
            self.sendtoLocalPath(file_name)
            
    def chooseFilefromPath(self, file_path):
            self.fileListBox.insert(0,file_path)
            tkinter.messagebox.showinfo(
                "Local Repository", '{} has been added to localrepo1!'.format(file_path))
            
    def fileRequest(self):
        peer_info = self.peerListBox.get(tk.ANCHOR)
        file_name = self.search_entry.get()
        network_peer.send_request(peer_info, file_name)

    def updateListFile(self):
        self.fileNameServer = simpledialog.askstring("Input","Nhập tên file lưu trên Server", parent = self)
        file_path = self.fileListBox.get(tk.ANCHOR)
        self.sendtoServerPath(file_path)
        network_peer.updateToServer(self.fileNameServer, file_path)
        self.fileListBox.delete(tk.ANCHOR)
        self.fileListBox.insert(0,self.fileNameServer + "(" + file_path +")")

    def updateListFilefromFetch(self, file_name, file_name_server):
        file_path = os.path.join(os.getcwd(), file_name)
        self.sendtoServerPath(file_path)
        network_peer.updateToServer(file_name_server, file_path)
        self.fileListBox.delete(tk.ANCHOR)
        self.fileListBox.insert(0,file_name_server + "(" + file_name +")")

    def deleteSelectedFile(self):
        file_name = self.fileListBox.get(tk.ANCHOR)
        self.fileListBox.delete(tk.ANCHOR)
        network_peer.deleteFileServer(file_name)

    def get_users_share_file_from_entry(self):
        file_name = self.search_entry.get()
        self.peerListBox.delete(0, tk.END)
        network_peer.send_listpeer(file_name)

    def insertToPeerList(self, info):
        self.peer_list.insert(tk.END, info)

    def reloadRepo(self):
        for file in self.fileListBox.get(0, tk.END):
            self.fileListBox.delete(0, tk.END)
        path = os.path.join(os.getcwd(), "localRepo1")
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            self.fileListBox.insert(tk.END, file_path)
        network_peer.reloadRepoList()

    ## to do: stop server
    def sidebar_button_event(self):
        print("huhu")

    def listbox_callback(self):
        print("done")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

# ------ end of GUI ------- #

class NetworkPeer(Base):
    def __init__(self, serverhost='localhost', serverport=30000, server_info=('192.168.56.1', 40000)):
        super(NetworkPeer, self).__init__(serverhost, serverport)

        # init host and port of central server
        self.server_info = server_info

        # peer name
        self.name = ""
        # peer password
        self.password = ""

        # all peers it can connect (network peers)
        self.connectable_peer = {}

        # peers it has connected (friend)
        self.friendlist = {}

        self.message_format = '{peername}: {message}'
        # file buffer
        self.file_buf = []

        # define handlers for received message of network peer
        handlers = {
            'REGISTER_SUCCESS': self.register_success,
            'REGISTER_ERROR': self.register_error,
            'LOGIN_SUCCESS': self.login_success,
            'LOGIN_ERROR': self.login_error,
            'LIST_USER_SHARE_FILE': self.get_users_share_file,
            'FILE_REQUEST': self.file_request,
            'FILE_ACCEPT': self.file_accept,
            'FILE_REFUSE': self.file_refuse,
        }
        for msgtype, function in handlers.items():
            self.add_handler(msgtype, function)

    ## ==========implement protocol for user registration - network peer==========##
    def send_register(self):
        """ Send a request to server to register peer's information. """
        peer_info = {
            'peername': self.name,
            'password': self.password,
            'host': self.serverhost,
            'port': self.serverport
        }
        self.client_send(self.server_info,
                         msgtype='PEER_REGISTER', msgdata=peer_info)

    def register_success(self, msgdata):
        """ Processing received message from server: Successful registration on the server. """
        display_noti('Thông báo', 'Đăng ký tài khoản thành công')
        print('Register Successful.')

    def register_error(self, msgdata):
        """ Processing received message from server: Registration failed on the server. """
        display_noti('Thông báo',
                     'Đăng ký thất bại. Tên đăng nhập đã tồn tại hoặc không hợp lệ!')
        print('Register Error. Username existed. Login!')
    ## ===========================================================##

    ## ==========implement protocol for authentication (log in) - network peer==========##
    def send_login(self):
        """ Send a request to server to login. """
        peer_info = {
            'peername': self.name,
            'password': self.password,
            'host': self.serverhost,
            'port': self.serverport
        }
        self.client_send(self.server_info,
                         msgtype='PEER_LOGIN', msgdata=peer_info)

    def login_success(self, msgdata):
        """ Processing received message from server: Successful login on the server. """
        print('Đăng nhập thành công.')
        display_noti('Thông báo', 'Đăng nhập thành công.')
        app.geometry("1100x600")
        app.resizable(False, False)
        app.show_frame(RepoPage)
        app.frames[RepoPage].update_user_greeting(self.name)

    def login_error(self, msgdata):
        """ Processing received message from server: Login failed on the server. """
        display_noti('Thông báo', 'Đăng nhập thất bại. Tài khoản không tồn tại')
        print('Đăng nhập thất bại. Tài khoản không tồn tại hoặc mật khẩu sai')
    ## ===========================================================##

    ## ==========implement protocol for getting online user list who have file that client find==========##
    def file_not_found_notification(self, filename):
        """Notify the user that the file was not found."""
        display_noti('Thông báo', f'File "{filename}" không tồn tại.')
        print(f'File "{filename}" not found.')

    # Modify your existing send_listpeer function to call file_not_found_notification
    def send_listpeer(self, filename):
        """Send a request to the server to get all online peers who have the file that the client is searching for."""
        self.filename = filename  # Set the filename attribute in the class
        peer_info = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': filename
        }
        self.client_send(self.server_info, msgtype='PEER_SEARCH', msgdata=peer_info)


    # Modify your get_users_share_file function to check if the list is empty and call file_not_found_notification
    def get_users_share_file(self, msgdata):
        shareList = msgdata.get('online_user_list_have_file', {})
        
        if not shareList:
            self.file_not_found_notification(self.filename)
            return

        for peername, data in shareList.items():
            peer_host, peer_port = data
            info = f"{peer_host},{peer_port}"
            app.frames[RepoPage].peerListBox.insert(0, info)


    def reloadRepoList(self):
        fileList = []
        fileList = model.get_user_file(self.name)
        for file in fileList:
            app.frames[RepoPage].fileListBox.insert(0,file)

    # def not_get_users_share_file(self, msgdata):
    #     """ Processing received message from server:
    #         Output username of all peers that have file which client is finding."""
    #     self.connectable_peer.clear()
    #     for key, value in msgdata['online_user_list_have_file'].items():
    #         self.connectable_peer[key] = tuple(value)
    #     if self.name in self.connectable_peer:
    #         self.connectable_peer.pop(self.name)

    ## ===========================================================##

    ## ==========implement protocol for file request==========##
    def send_request(self, peerinfo, filename):
        """ Send a file request to an online user. """
        peerhost, peerport = peerinfo.split(',')
        peer = (peerhost, int(peerport))
        data = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': filename
        }
        self.client_send(
        peer, msgtype='FILE_REQUEST', msgdata=data)

    ##=====NEED MODIFY: Hàm này dùng để hiển thị có yêu cầu chia sẻ file để người dùng chọn đồng ý hoặc không====#
    def file_request(self, msgdata):
        """ Processing received file request message from peer. """
        peername = msgdata['peername']
        host, port = msgdata['host'], msgdata['port']
        filename = msgdata['filename']
        msg_box = tkinter.messagebox.askquestion('File Request', 'User: {} - host {}: port: {} yêu cầu gửi file "{}"?'.format(peername, host, port, filename),
                                            icon="question")
        if msg_box == 'no':
            self.client_send((host, port), msgtype='FILE_REFUSE', msgdata={})
        if msg_box == 'yes':
            # if request is agreed, connect to peer (add to friendlist)
            data = {
                'peername': self.name,
                'host': self.serverhost,
                'port': self.serverport
            }
            self.client_send((host, port), msgtype='FILE_ACCEPT', msgdata=data)
            # display_noti("Yêu cầu file được chấp nhận.",
            #              "Gửi file!")
            self.friendlist[peername] = (host, port)
            destination = os.path.join(os.getcwd(), "serverRepo")
            file_path = tkinter.filedialog.askopenfilename(initialdir=destination,
                                                       title="Select a File",
                                                       filetypes=(("All files", "*.*"),))
            file_name = os.path.basename(file_path)
            msg_box = tkinter.messagebox.askquestion('File Explorer', 'Bạn có chắc muốn gửi file {} đến user: {}?'.format(file_name, peername),
                                                 icon="question")
            if msg_box == 'yes':
                sf_t = threading.Thread(
                    target=network_peer.transfer_file, args=(peername, file_path, filename))
                sf_t.daemon = True
                sf_t.start()
                tkinter.messagebox.showinfo(
                    "File Transfer", '{} đã được gửi đến user: {}!'.format(file_name, peername))
            else:
                self.client_send((host, port), msgtype='FILE_REFUSE', msgdata={})

    #=======Hàm này dùng để chuyển file cho máy khách sau khi đã chọn đồng ý=======#
    def file_accept(self, msgdata):
        """ Processing received accept file request message from peer.
            Add the peer to collection of friends. """
        peername = msgdata['peername']
        host = msgdata['host']
        port = msgdata['port']
        display_noti("Thông báo",
                     "Yêu cầu file được chấp nhận!")
        self.friendlist[peername] = (host, port)

    def file_refuse(self, msgdata):
        """ Processing received refuse chat request message from peer. """
        display_noti("Thông báo", 'Yêu cầu file bị từ chối!')
    ## ===========================================================##
    
    def recv_public_message(self, msgdata):
        """ Processing received public chat message from central server."""
        # insert messages to text box
        message = msgdata['name'] + ": " + msgdata['message']
        app.chatroom_textCons.config(state=tkinter.NORMAL)
        app.chatroom_textCons.insert(tkinter.END, message+"\n\n")
        app.chatroom_textCons.config(state=tkinter.DISABLED)
        app.chatroom_textCons.see(tkinter.END)
    ## ===========================================================##

    # def recv_message(self, msgdata):
    #     """ Processing received chat message from peer."""
    #     friend_name = msgdata['friend_name']
    #     if friend_name in self.friendlist:
    #         # insert messages to text box
    #         message = friend_name + ": " + msgdata['message']
    #         app.frames[ChatPage].frame_list[friend_name].message_area.config(
    #             state=tk.NORMAL)
    #         app.frames[ChatPage].frame_list[friend_name].message_area.insert(
    #             tk.END, message+"\n\n")
    #         app.frames[ChatPage].frame_list[friend_name].message_area.config(
    #             state=tk.DISABLED)
    #         app.frames[ChatPage].frame_list[friend_name].message_area.see(
    #             tk.END)
    ## ===========================================================##

    ## ==========implement protocol for file tranfering==========##
    def transfer_file(self, peer, file_path, file_name_server):
        """ Transfer a file. """
        try:
            peer_info = self.friendlist[peer]
        except KeyError:
            display_noti("Thông báo", 'Người này không tồn tại!')
        else:
            file_name = os.path.basename(file_path)
            def fileThread(filename):
                file_sent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                file_sent.connect((peer_info[0], peer_info[1] + OFFSET))

                # send filename and friendname
                fileInfo = {
                    'filename': filename,
                    'friendname': peer,
                    'filenameserver': file_name_server,
                }

                fileInfo = json.dumps(fileInfo).encode(FORMAT)
                file_sent.send(fileInfo)

                msg = file_sent.recv(BUFFER_SIZE).decode(FORMAT)
                print(msg)

                # Change the path to localRepo1
                localRepo_path = os.path.join(os.getcwd(), "localRepo1")
                file_path = os.path.join(localRepo_path, filename)

                # Receive and save the file
                with open(file_path, "wb") as f:
                    while True:
                        bytes_read = file_sent.recv(BUFFER_SIZE)
                        if not bytes_read:
                            # Nothing is received, file transmission is done
                            break
                        f.write(bytes_read)

                # Close the file socket
                file_sent.close()
                display_noti("Thông báo", 'File đã được gửi!')
                return
            t_sf = threading.Thread(target=fileThread,args=(file_name,))
            t_sf.daemon = True
            t_sf.start()

    def recv_file_content(self):
        """ Processing received file content from peer."""
        self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to our local address
        self.file_socket.bind((self.serverhost, int(self.serverport) + OFFSET))
        self.file_socket.listen(5)

        while True:
            conn, addr = self.file_socket.accept()
            buf = conn.recv(BUFFER_SIZE)
            message = buf.decode(FORMAT)

            # deserialize (json type -> python type)
            recv_file_info = json.loads(message)

            conn.send("Filename received.".encode(FORMAT))
            print(recv_file_info)

            file_name = recv_file_info['filename']
            friend_name = recv_file_info['friendname']

            localRepo_path = os.path.join(os.getcwd(), "localRepo1")
            file_path = os.path.join(localRepo_path, file_name)

            # Open the file with the correct path for writing binary data
            with open(file_path, "wb") as f:
                while True:
                    bytes_read = conn.recv(BUFFER_SIZE)
                    if not bytes_read:
                        # Nothing is received, file transmitting is done
                        break
                    # Write to the file the bytes we just received
                    f.write(bytes_read)

            # Update the file list in your application (you may need to implement this method)
            app.frames[RepoPage].updateListFilefromFetch(file_name, recv_file_info['filenameserver'])

            # Shutdown and close the connection
            conn.shutdown(socket.SHUT_WR)
            conn.close()

            # Display a notification
            display_noti("Thông báo", f'Bạn đã nhận được một file với tên "{file_name}" từ "{friend_name}"')

    ## ===========================================================##
    
    ## ==========implement protocol for log out & exit ===================##

    def send_logout_request(self):
        """ Central Server deletes user out of online user list """
        peer_info = {
            'peername': self.name,
        }
        self.client_send(self.server_info,
                         msgtype='PEER_LOGOUT', msgdata=peer_info)

    ## ===========================================================##
    def deleteFileServer(self,file_name):
        """ Delete file from server. """
        peer_info = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': file_name
        }
        self.client_send(self.server_info,
                         msgtype='DELETE_FILE', msgdata=peer_info)
        
    def updateToServer(self, file_name, file_path):
        """ Upload repo to server. """
        peer_info = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': file_name,
            'filepath': file_path
        }
        self.client_send(self.server_info,
                         msgtype='FILE_REPO', msgdata=peer_info)
    
# ------ app run ---------- #
if __name__ == "__main__":
    app = tkinterApp()
    app.title('File transfer service')
    app.geometry("1024x600")
    app.resizable(False, False)

    def handle_on_closing_event():
        if tkinter.messagebox.askokcancel("Thoát", "Bạn muốn thoát khỏi ứng dụng?"):
            app.destroy()

    app.protocol("WM_DELETE_WINDOW", handle_on_closing_event)
=======
##################################################
##################################################
##################################################
import os
import json
import socket
import threading
import time
import random
import sys
import platform
import shutil
from Base import Base
import persistence
 
# GUI
import tkinter as tk
import tkinter.messagebox
import tkinter.filedialog
from tkinter import simpledialog
import tkinter.ttk as ttk
from PIL import ImageTk 
from PIL import Image
import customtkinter
from flask import Flask

# aid
from hashfunction import MD5_hash
import asset

# ----CONSTANT----#
FORMAT = "utf-8"
BUFFER_SIZE = 2048
OFFSET = 10000

# --------------- #
# --------------- #
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

# popup notification
def display_noti(title, content):
    tkinter.messagebox.showinfo(title, content)

## ====================GUI IMPLEMENT======================##
class tkinterApp(tk.Tk):
    # __init__ function for class tkinterApp
    def __init__(self, *args, **kwargs):
        # __init__ function for class Tk
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.chatroom_textCons = None

        # initializing frames to an empty array
        self.frames = {}

        # iterating through a tuple consisting
        # of the different page layouts
        for F in (StartPage, RegisterPage, LoginPage, RepoPage):
            frame = F(parent=container, controller=self)
            # initializing frame of that object from
            # startpage, registerpage, loginpage, chatpage respectively with
            # for loop
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            frame.configure(bg='white')
        self.show_frame(StartPage)
    # to display the current frame passed as parameter
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # set color mode
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        # create title
        self.page_title = customtkinter.CTkLabel(self, text="P2P File Sharing", font=("Arial Bold", 36))
        self.page_title.pack(padx=10, pady=(80, 10))
        # set port label
        self.port_label = customtkinter.CTkLabel(self, text="Nhập giá trị port trong khoảng (1024 -> 65535)", font=("Arial", 20))
        self.port_label.pack(padx=10, pady=10)
        # set port entry
        self.port_entry = customtkinter.CTkEntry(self, placeholder_text="Nhập port number", border_width=1,width=250)
        self.port_entry.pack(padx=10, pady=10)
        # create a register button
        self.register_button = customtkinter.CTkButton(self, text="Đăng ký", command=lambda: 
                                self.enter_app(controller=controller, port=self.port_entry.get(), page=RegisterPage),fg_color="#192655",font=customtkinter.CTkFont(size=12, weight="bold"))
        self.register_button.pack(padx=10, pady=10)
        # create a login button
        self.login_button = customtkinter.CTkButton(self, text="Đăng nhập", command=lambda: 
                                self.enter_app(controller=controller, port=self.port_entry.get(), page=LoginPage),fg_color="#192655",font=customtkinter.CTkFont(size=12, weight="bold"))
        self.login_button.pack(padx=10, pady=10)

    def enter_app(self, controller, port, page):
        try:
            # get peer current ip address -> assign to serverhost
            hostname=socket.gethostname()   
            IPAddr=socket.gethostbyname(hostname)  

            # init server
            global network_peer
            network_peer = NetworkPeer(serverhost=IPAddr, serverport=int(port))
           
            # A child thread for receiving message
            recv_t = threading.Thread(target=network_peer.input_recv)
            recv_t.daemon = True
            recv_t.start()

            # A child thread for receiving file
            recv_file_t = threading.Thread(target=network_peer.recv_file_content)
            recv_file_t.daemon = True
            recv_file_t.start()
            controller.show_frame(page)
        except:
            self.port_entry.delete(0, customtkinter.END)
            display_noti("Port Error!",  "Cổng đã được sử dụng hoặc chứa giá trị rỗng")

class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("blue")
        # Sign Up Image
        # signup_pic = ImageTk.PhotoImage(asset.signup_image)
        # self.signupImg = tkinter.Label(self, image=signup_pic, bg='white')
        # self.signupImg.image = signup_pic
        # self.signupImg.place(x=50, y=50)        

        self.frame = customtkinter.CTkFrame(master=self, fg_color="white")
        self.frame.pack(fill='both', expand=True)

        self.title_label = customtkinter.CTkLabel(self.frame, text="Đăng ký tài khoản", font=("Roboto Bold", 32))
        self.title_label.pack(pady=(80, 10),padx=10)

        self.username = customtkinter.CTkLabel(self.frame, text="Tài khoản", font=("Roboto", 14))
        self.username.pack(pady=(0),padx=10)
        self.username_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Nhập tài khoản",  width=250,font=("Roboto", 12))
        self.username_entry.pack(pady=(0),padx=10)

        self.password = customtkinter.CTkLabel(self.frame, text="Mật khẩu", font=("Roboto", 14))
        self.password.pack(pady=(0),padx=10)
        self.password_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Nhập mật khẩu",  width=250,font=("Roboto", 12), show = '*')
        self.password_entry.pack(pady=(0, 10),padx=10)

        # Submit
        customtkinter.CTkButton(self.frame, text='Đăng ký', fg_color="#192655",font=customtkinter.CTkFont(size=12, weight="bold"),command=lambda: 
                                self.register_user(self.username_entry.get(), self.password_entry.get())).pack(pady=(0, 10),padx=10)
                                                                                                            
        customtkinter.CTkLabel(self.frame, text="Đã có tài khoản ?",font=("Roboto", 11)).pack(pady=(10, 0),padx=10)
        customtkinter.CTkButton(self.frame, text='Đăng nhập', fg_color="#192655",font=customtkinter.CTkFont(size=12, weight="bold"),command=lambda: controller.show_frame(LoginPage)).pack(pady=(0, 10),padx=1)

    def register_user(self, username, password):
        network_peer.name = str(username)
        # hash password by MD5 algorithm
        network_peer.password = MD5_hash(str(password))
        self.username_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)
        network_peer.send_register()

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        # Login Image
        # login_pic = ImageTk.PhotoImage(asset.login_image)
        # loginImg = tkinter.Label(self, image=login_pic)
        # loginImg.image = login_pic
        # loginImg.place(x=50, y=50)
        self.frame = customtkinter.CTkFrame(master=self, fg_color="white")
        self.frame.pack(fill='both', expand=True)

        self.title_label = customtkinter.CTkLabel(self.frame, text="Đăng nhập", font=("Roboto Bold", 32))
        self.title_label.pack(pady=(80, 10),padx=10)

        self.username = customtkinter.CTkLabel(self.frame, text="Tài khoản", font=("Roboto", 14))
        self.username.pack(pady=(0),padx=10)
        self.username_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Nhập Tài khoản", width=250,font=("Roboto", 12))
        self.username_entry.pack(pady=(0),padx=10)

        self.password = customtkinter.CTkLabel(self.frame, text="Mật khẩu", font=("Roboto", 14))
        self.password.pack(pady=(0),padx=10)
        self.password_entry = customtkinter.CTkEntry(self.frame, placeholder_text="Nhập Mật khẩu",  width=250,font=("Roboto", 12), show = '*')
        self.password_entry.pack(pady=(0, 10),padx=10)

        customtkinter.CTkButton(self.frame, text='Đăng nhập', fg_color="#192655",font=customtkinter.CTkFont(size=12, weight="bold"), command=lambda:
                                self.login_user(username=self.username_entry.get(), password=self.password_entry.get())).pack(pady=(0, 10),padx=10)
        customtkinter.CTkLabel(self.frame, text="Bạn không có tài khoản ?", font=("Roboto", 11)).pack(pady=(10, 0),padx=10)
        customtkinter.CTkButton(self.frame, text='Đăng ký', font=customtkinter.CTkFont(size=12, weight="bold"),fg_color="#192655", cursor="hand2", command=lambda: controller.show_frame(RegisterPage)).pack(pady=(0, 10),padx=10)
    
    def login_user(self, username, password):
        network_peer.name = str(username)
        # hash password by MD5 algorithm
        network_peer.password = MD5_hash(str(password))
        self.username_entry.delete(0, customtkinter.END)
        self.password_entry.delete(0, customtkinter.END)
        network_peer.send_login()

class RepoPage(tk.Frame):
    def __init__(self, parent, **kwargs):
        tk.Frame.__init__(self, parent)
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure(( 1), weight=1)

        #### create frame for repo
        self.repo_frame = customtkinter.CTkFrame(self, fg_color="#DBE2EF",corner_radius=10)
        self.repo_frame.grid(row=0, column=3, sticky="nsew",pady=(10,10),padx=(10, 10))
        self.repo_frame.grid_rowconfigure(0, weight=1)
        self.repo_frame.grid_columnconfigure(0, weight=1)
        # create scrollable frame for repo list
        ## to do: add file names to this frame
        self.scrollable_repo_frame = customtkinter.CTkScrollableFrame(self, label_text="Repository",label_text_color="#3F72AF",fg_color="#DBE2EF")
        self.scrollable_repo_frame.grid(row=0, column=0,columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_repo_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_file_names = []
        self.fileListBox = tk.Listbox(self.scrollable_repo_frame, width=145, height=20)
        self.fileListBox.grid(row=0, column=0, padx=10,columnspan=3, pady=(10, 10))

        # create temp frame
        self.temp_frame = customtkinter.CTkFrame(master=self.repo_frame, fg_color="transparent")
        self.temp_frame.grid(row=0, column=1, sticky="nsew")
        # self.temp_frame.grid_rowconfigure(0, weight=1)
        # self.temp_frame.grid_columnconfigure(0, weight=1)
        # self.temp_frame.grid_columnconfigure(1, weight=1)
        # create delete button
        self.delete_button = customtkinter.CTkButton(master=self.temp_frame, border_width=2, text="Xóa file", fg_color="#192655",command=lambda: self.deleteSelectedFile())
        self.delete_button.grid(row=0, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create choose file button 
        self.add_button = customtkinter.CTkButton(master=self.temp_frame, border_width=2, text="Tải file lên repository",fg_color="#192655", command=lambda: self.chooseFile())
        self.add_button.grid(row=1, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create update to server button
        self.update_button = customtkinter.CTkButton(master=self.temp_frame, border_width=2, text="Cập nhật Server", fg_color="#192655",command=lambda: self.updateListFile())
        self.update_button.grid(row=2, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create reload repo button
        self.update_button = customtkinter.CTkButton(master=self.temp_frame, border_width=2, text="Reload repository", fg_color="#192655",command=lambda: self.reloadRepo())
        self.update_button.grid(row=3, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")


        ####

        self.peer_frame = customtkinter.CTkFrame(self, fg_color="#DBE2EF",corner_radius=10)
        self.peer_frame.grid(row=2, column=3,sticky="nsew",padx=(10,10),pady=(10,10))
        self.peer_frame.grid_rowconfigure(1, weight=1)
        self.peer_frame.grid_columnconfigure(1, weight=1)   
        # # ###
        self.scrollable_peer_frame = customtkinter.CTkScrollableFrame(self, label_text="Peer List",label_text_color="#3F72AF",fg_color="#DBE2EF")
        self.scrollable_peer_frame.grid(row=2, column=0,columnspan=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_peer_frame.grid_rowconfigure(0, weight=1)
        self.scrollable_peer_names = []
        self.peerListBox = tk.Listbox(self.scrollable_peer_frame, width=175, height=20)
        self.peerListBox.grid(row=0, column=1, padx=10, pady=(10, 10))
        # # ####
        #  29/11
        # self.search_frame = customtkinter.CTkFrame(self.peer_frame, fg_color="#DBE2EF")
        # self.search_frame.grid(row=2, column=6, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # self.search_frame.grid_rowconfigure(0, weight=1)
        # self.search_frame.grid_columnconfigure(0, weight=1)
        self.search_entry = customtkinter.CTkEntry(master=self.peer_frame, placeholder_text="Search...")
        self.search_entry.grid(row=4, column=2,padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.search_button = customtkinter.CTkButton(master=self.peer_frame, text="Search", border_width=2, command=lambda: self.get_users_share_file_from_entry(),fg_color="#192655")
        self.search_button.grid(row=5, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")
        # create send connect request button
        self.request_button = customtkinter.CTkButton(master=self.peer_frame, border_width=2,
                                                     command=lambda:self.fileRequest(), text="Gửi yêu cầu kết nối",fg_color="#192655")
        self.request_button.grid(row=6, column=2, padx=(10, 10), pady=(10, 10), sticky="nsew")

        #create CLI
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Command...")
        self.entry.grid(row=4, column=0, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.main_button_1 = customtkinter.CTkButton(self, text="Enter",command=lambda:self.commandLine(command = self.entry.get()), border_width=2, fg_color="#192655")
        self.main_button_1.grid(row=4, column=1, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.main_button_2 = customtkinter.CTkButton(self, text="Thoát", command=lambda: self.quit_user(), fg_color="#192655", border_width=2,font=customtkinter.CTkFont(size=15, weight="bold"))
        self.main_button_2.grid(row=4, column=3, padx=(10, 10), pady=(10, 10), sticky="nsew")

    def logout_user(self):
        network_peer.send_logout_request()
        app.show_frame(StartPage)

    def quit_user(self):
        network_peer.send_logout_request()
        app.destroy()
    
    def commandLine(self, command):
        parts = command.split()

        if parts[0] == "publish":
            if len(parts) == 3:
                file_path = parts[1]
                file_name = parts[2]
                #Implement something to update file to server here#
                #To do#
                network_peer.updateToServer(file_name, file_path)
                self.fileListBox.insert(0,file_name + "(" + file_path +")")
                self.sendtoServerPath(file_path)
                
            else:
                message = "Lệnh không hợp lệ vui lòng nhập lại!"
                tkinter.messagebox.showinfo(message)
        elif parts[0] == "fetch":
            if len(parts) == 2:
                file_name = parts[1]
                #Implement something to search file and doawnload it#
                #To do#
                network_peer.send_listpeer(file_name)
                peer_info = self.peerListBox.get(0)
                network_peer.send_request(peer_info, file_name)
            else:
                message = "Lệnh không hợp lệ vui lòng nhập lại!"
                tkinter.messagebox.showinfo(message)
        else:
            message = "Lệnh không hợp lệ vui lòng nhập lại!"
            tkinter.messagebox.showinfo(message)

    def sendFile(self, peername):
        file_path = tkinter.filedialog.askopenfilename(initialdir="/",
                                                       title="Select a File",
                                                       filetypes=(("All files", "*.*"),))
        file_name = os.path.basename(file_path)
        msg_box = tkinter.messagebox.askquestion('File Explorer', 'Are you sure to send {} to {}?'.format(file_name, peername),
                                                 icon="question")
        if msg_box == 'yes':
            sf_t = threading.Thread(
                target=network_peer.transfer_file, args=(peername, file_path))
            sf_t.daemon = True
            sf_t.start()
            tkinter.messagebox.showinfo(
                "File Transfer", '{} has been sent to {}!'.format(file_name, peername))
            
    def sendtoLocalPath(self, file_path):
        # create a folder named "repo" in this folder
        if not os.path.exists("localRepo1"):
            os.makedirs("localRepo1")
        destination = os.path.join(os.getcwd(), "localRepo1")
        shutil.copy(file_path, destination)

    def sendtoServerPath(self, file_path):
        # create a folder named "repo" in this folder
        if not os.path.exists("serverRepo"):
            os.makedirs("serverRepo")
        destination = os.path.join(os.getcwd(), "serverRepo")
        shutil.move(file_path, destination)    

    def chooseFile(self):
        file_path = tkinter.filedialog.askopenfilename(initialdir="/",
                                                       title="Select a File",
                                                       filetypes=(("All files", "*.*"),))
        # file_name = os.path.basename(file_path)
        file_name = file_path
        msg_box = tkinter.messagebox.askquestion('File Explorer', 'Upload {} to local repository?'.format(file_name),
                                                 icon="question")
        if msg_box == 'yes':
            # popup = simpledialog.askstring("Input","Nhập tên file trên Localrepo",parent = self)
            self.fileListBox.insert(0,file_name)
            tkinter.messagebox.showinfo(
                "Local Repository", '{} has been added to localrepo1!'.format(file_name))
            self.sendtoLocalPath(file_name)
            
    def chooseFilefromPath(self, file_path):
            self.fileListBox.insert(0,file_path)
            tkinter.messagebox.showinfo(
                "Local Repository", '{} has been added to localrepo1!'.format(file_path))
            
    def fileRequest(self):
        peer_info = self.peerListBox.get(tk.ANCHOR)
        file_name = self.search_entry.get()
        network_peer.send_request(peer_info, file_name)

    def updateListFile(self):
        self.fileNameServer = simpledialog.askstring("Input","Nhập tên file lưu trên Server", parent = self)
        file_path = self.fileListBox.get(tk.ANCHOR)
        self.sendtoServerPath(file_path)
        network_peer.updateToServer(self.fileNameServer, file_path)
        self.fileListBox.delete(tk.ANCHOR)
        self.fileListBox.insert(0,self.fileNameServer + "(" + file_path +")")

    def updateListFilefromFetch(self, file_name, file_name_server):
        file_path = os.path.join(os.getcwd(), file_name)
        self.sendtoServerPath(file_path)
        network_peer.updateToServer(file_name_server, file_path)
        self.fileListBox.delete(tk.ANCHOR)
        self.fileListBox.insert(0,file_name_server + "(" + file_name +")")

    def deleteSelectedFile(self):
        file_name = self.fileListBox.get(tk.ANCHOR)
        self.fileListBox.delete(tk.ANCHOR)
        network_peer.deleteFileServer(file_name)

    def get_users_share_file_from_entry(self):
        file_name = self.search_entry.get()
        self.peerListBox.delete(0, tk.END)
        network_peer.send_listpeer(file_name)

    def insertToPeerList(self, info):
        self.peer_list.insert(tk.END, info)

    def reloadRepo(self):
        for file in self.fileListBox.get(0, tk.END):
            self.fileListBox.delete(0, tk.END)
        path = os.path.join(os.getcwd(), "localRepo1")
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            self.fileListBox.insert(tk.END, file_path)
        network_peer.reloadRepoList()

    ## to do: stop server
    def sidebar_button_event(self):
        print("huhu")

    def listbox_callback(self):
        print("done")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

# ------ end of GUI ------- #

class NetworkPeer(Base):
    def __init__(self, serverhost='localhost', serverport=30000, server_info=('192.168.56.1', 40000)):
        super(NetworkPeer, self).__init__(serverhost, serverport)

        # init host and port of central server
        self.server_info = server_info

        # peer name
        self.name = ""
        # peer password
        self.password = ""

        # all peers it can connect (network peers)
        self.connectable_peer = {}

        # peers it has connected (friend)
        self.friendlist = {}

        self.message_format = '{peername}: {message}'
        # file buffer
        self.file_buf = []

        # define handlers for received message of network peer
        handlers = {
            'REGISTER_SUCCESS': self.register_success,
            'REGISTER_ERROR': self.register_error,
            'LOGIN_SUCCESS': self.login_success,
            'LOGIN_ERROR': self.login_error,
            'LIST_USER_SHARE_FILE': self.get_users_share_file,
            'FILE_REQUEST': self.file_request,
            'FILE_ACCEPT': self.file_accept,
            'FILE_REFUSE': self.file_refuse,
        }
        for msgtype, function in handlers.items():
            self.add_handler(msgtype, function)

    ## ==========implement protocol for user registration - network peer==========##
    def send_register(self):
        """ Send a request to server to register peer's information. """
        peer_info = {
            'peername': self.name,
            'password': self.password,
            'host': self.serverhost,
            'port': self.serverport
        }
        self.client_send(self.server_info,
                         msgtype='PEER_REGISTER', msgdata=peer_info)

    def register_success(self, msgdata):
        """ Processing received message from server: Successful registration on the server. """
        display_noti('Thông báo', 'Đăng ký tài khoản thành công')
        print('Register Successful.')

    def register_error(self, msgdata):
        """ Processing received message from server: Registration failed on the server. """
        display_noti('Thông báo',
                     'Đăng ký thất bại. Tên đăng nhập đã tồn tại hoặc không hợp lệ!')
        print('Register Error. Username existed. Login!')
    ## ===========================================================##

    ## ==========implement protocol for authentication (log in) - network peer==========##
    def send_login(self):
        """ Send a request to server to login. """
        peer_info = {
            'peername': self.name,
            'password': self.password,
            'host': self.serverhost,
            'port': self.serverport
        }
        self.client_send(self.server_info,
                         msgtype='PEER_LOGIN', msgdata=peer_info)

    def login_success(self, msgdata):
        """ Processing received message from server: Successful login on the server. """
        print('Đăng nhập thành công.')
        display_noti('Thông báo', 'Đăng nhập thành công.')
        app.geometry("1100x600")
        app.resizable(False, False)
        app.show_frame(RepoPage)

    def login_error(self, msgdata):
        """ Processing received message from server: Login failed on the server. """
        display_noti('Thông báo', 'Đăng nhập thất bại. Tài khoản không tồn tại')
        print('Đăng nhập thất bại. Tài khoản không tồn tại hoặc mật khẩu sai')
    ## ===========================================================##

    ## ==========implement protocol for getting online user list who have file that client find==========##
    def file_not_found_notification(self, filename):
        """Notify the user that the file was not found."""
        display_noti('Thông báo', f'File "{filename}" không tồn tại.')
        print(f'File "{filename}" not found.')

    # Modify your existing send_listpeer function to call file_not_found_notification
    def send_listpeer(self, filename):
        """Send a request to the server to get all online peers who have the file that the client is searching for."""
        self.filename = filename  # Set the filename attribute in the class
        peer_info = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': filename
        }
        self.client_send(self.server_info, msgtype='PEER_SEARCH', msgdata=peer_info)


    # Modify your get_users_share_file function to check if the list is empty and call file_not_found_notification
    def get_users_share_file(self, msgdata):
        shareList = msgdata.get('online_user_list_have_file', {})
        
        if not shareList:
            self.file_not_found_notification(self.filename)
            return

        for peername, data in shareList.items():
            peer_host, peer_port = data
            info = f"{peer_host},{peer_port}"
            app.frames[RepoPage].peerListBox.insert(0, info)


    def reloadRepoList(self):
        fileList = []
        fileList = persistence.get_user_file(self.name)
        for file in fileList:
            app.frames[RepoPage].fileListBox.insert(0,file)

    # def not_get_users_share_file(self, msgdata):
    #     """ Processing received message from server:
    #         Output username of all peers that have file which client is finding."""
    #     self.connectable_peer.clear()
    #     for key, value in msgdata['online_user_list_have_file'].items():
    #         self.connectable_peer[key] = tuple(value)
    #     if self.name in self.connectable_peer:
    #         self.connectable_peer.pop(self.name)

    ## ===========================================================##

    ## ==========implement protocol for file request==========##
    def send_request(self, peerinfo, filename):
        """ Send a file request to an online user. """
        peerhost, peerport = peerinfo.split(',')
        peer = (peerhost, int(peerport))
        data = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': filename
        }
        self.client_send(
        peer, msgtype='FILE_REQUEST', msgdata=data)

    ##=====NEED MODIFY: Hàm này dùng để hiển thị có yêu cầu chia sẻ file để người dùng chọn đồng ý hoặc không====#
    def file_request(self, msgdata):
        """ Processing received file request message from peer. """
        peername = msgdata['peername']
        host, port = msgdata['host'], msgdata['port']
        filename = msgdata['filename']
        msg_box = tkinter.messagebox.askquestion('File Request', 'User: {} - host {}: port: {} yêu cầu gửi file "{}"?'.format(peername, host, port, filename),
                                            icon="question")
        if msg_box == 'no':
            self.client_send((host, port), msgtype='FILE_REFUSE', msgdata={})
        if msg_box == 'yes':
            # if request is agreed, connect to peer (add to friendlist)
            data = {
                'peername': self.name,
                'host': self.serverhost,
                'port': self.serverport
            }
            self.client_send((host, port), msgtype='FILE_ACCEPT', msgdata=data)
            # display_noti("Yêu cầu file được chấp nhận.",
            #              "Gửi file!")
            self.friendlist[peername] = (host, port)
            destination = os.path.join(os.getcwd(), "serverRepo")
            file_path = tkinter.filedialog.askopenfilename(initialdir=destination,
                                                       title="Select a File",
                                                       filetypes=(("All files", "*.*"),))
            file_name = os.path.basename(file_path)
            msg_box = tkinter.messagebox.askquestion('File Explorer', 'Bạn có chắc muốn gửi file {} đến user: {}?'.format(file_name, peername),
                                                 icon="question")
            if msg_box == 'yes':
                sf_t = threading.Thread(
                    target=network_peer.transfer_file, args=(peername, file_path, filename))
                sf_t.daemon = True
                sf_t.start()
                tkinter.messagebox.showinfo(
                    "File Transfer", '{} đã được gửi đến user: {}!'.format(file_name, peername))
            else:
                self.client_send((host, port), msgtype='FILE_REFUSE', msgdata={})

    #=======Hàm này dùng để chuyển file cho máy khách sau khi đã chọn đồng ý=======#
    def file_accept(self, msgdata):
        """ Processing received accept file request message from peer.
            Add the peer to collection of friends. """
        peername = msgdata['peername']
        host = msgdata['host']
        port = msgdata['port']
        display_noti("Thông báo",
                     "Yêu cầu file được chấp nhận!")
        self.friendlist[peername] = (host, port)

    def file_refuse(self, msgdata):
        """ Processing received refuse chat request message from peer. """
        display_noti("Thông báo", 'Yêu cầu file bị từ chối!')
    ## ===========================================================##
    
    def recv_public_message(self, msgdata):
        """ Processing received public chat message from central server."""
        # insert messages to text box
        message = msgdata['name'] + ": " + msgdata['message']
        app.chatroom_textCons.config(state=tkinter.NORMAL)
        app.chatroom_textCons.insert(tkinter.END, message+"\n\n")
        app.chatroom_textCons.config(state=tkinter.DISABLED)
        app.chatroom_textCons.see(tkinter.END)
    ## ===========================================================##

    # def recv_message(self, msgdata):
    #     """ Processing received chat message from peer."""
    #     friend_name = msgdata['friend_name']
    #     if friend_name in self.friendlist:
    #         # insert messages to text box
    #         message = friend_name + ": " + msgdata['message']
    #         app.frames[ChatPage].frame_list[friend_name].message_area.config(
    #             state=tk.NORMAL)
    #         app.frames[ChatPage].frame_list[friend_name].message_area.insert(
    #             tk.END, message+"\n\n")
    #         app.frames[ChatPage].frame_list[friend_name].message_area.config(
    #             state=tk.DISABLED)
    #         app.frames[ChatPage].frame_list[friend_name].message_area.see(
    #             tk.END)
    ## ===========================================================##

    ## ==========implement protocol for file tranfering==========##
    def transfer_file(self, peer, file_path, file_name_server):
        """ Transfer a file. """
        try:
            peer_info = self.friendlist[peer]
        except KeyError:
            display_noti("Thông báo", 'Người này không tồn tại!')
        else:
            file_name = os.path.basename(file_path)
            def fileThread(filename):
                file_sent = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                file_sent.connect((peer_info[0], peer_info[1] + OFFSET))

                # send filename and friendname
                fileInfo = {
                    'filename': filename,
                    'friendname': peer,
                    'filenameserver': file_name_server,
                }

                fileInfo = json.dumps(fileInfo).encode(FORMAT)
                file_sent.send(fileInfo)

                msg = file_sent.recv(BUFFER_SIZE).decode(FORMAT)
                print(msg)

                # Change the path to localRepo1
                localRepo_path = os.path.join(os.getcwd(), "localRepo1")
                file_path = os.path.join(localRepo_path, filename)

                # Receive and save the file
                with open(file_path, "wb") as f:
                    while True:
                        bytes_read = file_sent.recv(BUFFER_SIZE)
                        if not bytes_read:
                            # Nothing is received, file transmission is done
                            break
                        f.write(bytes_read)

                # Close the file socket
                file_sent.close()
                display_noti("Thông báo", 'File đã được gửi!')
                return
            t_sf = threading.Thread(target=fileThread,args=(file_name,))
            t_sf.daemon = True
            t_sf.start()

    def recv_file_content(self):
        """ Processing received file content from peer."""
        self.file_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to our local address
        self.file_socket.bind((self.serverhost, int(self.serverport) + OFFSET))
        self.file_socket.listen(5)

        while True:
            conn, addr = self.file_socket.accept()
            buf = conn.recv(BUFFER_SIZE)
            message = buf.decode(FORMAT)

            # deserialize (json type -> python type)
            recv_file_info = json.loads(message)

            conn.send("Filename received.".encode(FORMAT))
            print(recv_file_info)

            file_name = recv_file_info['filename']
            friend_name = recv_file_info['friendname']

            localRepo_path = os.path.join(os.getcwd(), "localRepo1")
            file_path = os.path.join(localRepo_path, file_name)

            # Open the file with the correct path for writing binary data
            with open(file_path, "wb") as f:
                while True:
                    bytes_read = conn.recv(BUFFER_SIZE)
                    if not bytes_read:
                        # Nothing is received, file transmitting is done
                        break
                    # Write to the file the bytes we just received
                    f.write(bytes_read)

            # Update the file list in your application (you may need to implement this method)
            app.frames[RepoPage].updateListFilefromFetch(file_name, recv_file_info['filenameserver'])

            # Shutdown and close the connection
            conn.shutdown(socket.SHUT_WR)
            conn.close()

            # Display a notification
            display_noti("Thông báo", f'Bạn đã nhận được một file với tên "{file_name}" từ "{friend_name}"')

    ## ===========================================================##
    
    ## ==========implement protocol for log out & exit ===================##

    def send_logout_request(self):
        """ Central Server deletes user out of online user list """
        peer_info = {
            'peername': self.name,
        }
        self.client_send(self.server_info,
                         msgtype='PEER_LOGOUT', msgdata=peer_info)

    ## ===========================================================##
    def deleteFileServer(self,file_name):
        """ Delete file from server. """
        peer_info = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': file_name
        }
        self.client_send(self.server_info,
                         msgtype='DELETE_FILE', msgdata=peer_info)
        
    def updateToServer(self, file_name, file_path):
        """ Upload repo to server. """
        peer_info = {
            'peername': self.name,
            'host': self.serverhost,
            'port': self.serverport,
            'filename': file_name,
            'filepath': file_path
        }
        self.client_send(self.server_info,
                         msgtype='FILE_REPO', msgdata=peer_info)
    
# ------ app run ---------- #
if __name__ == "__main__":
    app = tkinterApp()
    app.title('P2P File Sharing')
    app.geometry("1024x600")
    app.resizable(False, False)

    def handle_on_closing_event():
        if tkinter.messagebox.askokcancel("Thoát", "Bạn muốn thoát khỏi ứng dụng?"):
            app.destroy()

    app.protocol("WM_DELETE_WINDOW", handle_on_closing_event)
    app.mainloop()