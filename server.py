from threading import Thread
from Base import Base
from model import *
import customtkinter
import tkinter.messagebox
from tkinter import ttk
customtkinter.set_default_color_theme("dark-blue")

# popup notification
def display_noti(title, content):
    tkinter.messagebox.showinfo(title, content)

# popup window class for files 
## to do: add clients' files to this list
class ClientFilesList(customtkinter.CTkToplevel):
    def __init__(self, master, username, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.username = username
        self.title("View")
        self.geometry("550x290")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        self.scrollable_files_frame = customtkinter.CTkScrollableFrame(self, label_text="Danh sách files",label_text_color="#3F72AF",label_font=("Danh sách files",25))
        self.scrollable_files_frame.grid(row=0, column=0, rowspan=4, padx=(10, 0), pady=(10, 0), sticky="nsew")
        
        self.scrollable_clients_files = get_user_file(self.username)
        self.scrollable_clients_files_labels = []
        for i, file_name in enumerate(self.scrollable_clients_files):
            client_label = customtkinter.CTkLabel(master=self.scrollable_files_frame, text=file_name)
            client_label.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_clients_files_labels.append(client_label)

class PlaceholderEntry(ttk.Entry):
    def __init__(self, master=None, placeholder="", *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.placeholder = placeholder
        self.insert("0", self.placeholder)

        self.bind("<FocusIn>", self.on_entry_click)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_entry_click(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self.config(foreground='black')  # Change text color when typing

    def on_focus_out(self, event):
        if not self.get():
            self.insert("0", self.placeholder)
            self.config(foreground='gray')  # Change text color when placeholder is shown
class App(customtkinter.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # __init__ function for class CTk
        # customtkinter.CTk.__init__(self, *args, **kwargs)

        # configure windows
        self.title("Upload files service")
        self.geometry(f"{1100}x{580}")
        self.configure(bg="red")
        # configure grid layout (3x?)
        

        # create sidebar frame with widgets
        self.sidebar_frame = ttk.Label(self, width=140, text="Upload files service",font=('Arial', 25),foreground="#3F72AF")  
        self.sidebar_frame.grid(column=0, row=0, sticky=tkinter.W, padx=5, pady=5)
        # self.sidebar_frame.grid(row=0, column=0, rowspan=1,  padx=(10,0),pady=(10,0),sticky="nsew"),
        # self.sidebar_frame.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure(1, weight=1)
        # create scrollable frame for clients list
        ## to do: add clients to this frame
      
        self.scrollable_clients_frame = customtkinter.CTkScrollableFrame(self, label_text="Clients",fg_color="#DBE2EF",label_text_color="#3F72AF",label_font=("Clients",25))
        self.scrollable_clients_frame.grid(row = 1, column = 0, columnspan = 2, rowspan=4, padx=(10, 10), pady=(10, 10), sticky="nsew")
        self.scrollable_clients_frame.grid_columnconfigure((0), weight=1)
        self.scrollable_clients_names = get_all_users()
        self.scrollable_clients_labels = []
            
        ## to do: modify range to number of current clients
        for i, username in enumerate(self.scrollable_clients_names):
            client_label = customtkinter.CTkLabel(master=self.scrollable_clients_frame, text=username)
            client_label.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_clients_labels.append(client_label)

            view_button = customtkinter.CTkButton(master=self.scrollable_clients_frame, text="View Files", command=lambda username=username: self.view_client_files(username),fg_color="#192655")
            view_button.grid(row=i, column=1, padx=10, pady=(0, 20))
            self.files_list = None

            ping_button = customtkinter.CTkButton(master=self.scrollable_clients_frame, text="Ping", command = lambda username = username: self.ping_client(username),fg_color="#192655")
            ping_button.grid(row=i, column=2, padx=10, pady=(0, 20))

        # create CLI

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Command...")
        self.entry.grid_columnconfigure(0, weight=0)
        self.entry.grid(row=2, column=2, padx=(10, 10), pady=(20, 0))
        # login_button = ttk.Entry(self, placeholder_text="Command...")
        # login_button.grid(column=0, row=5, sticky=tkinter.W, padx=5, pady=5)
        self.main_button_1 = customtkinter.CTkButton(master=self, text="Enter", command = lambda:self.commandLine(command = self.entry.get()), fg_color="#192655", border_width=2)
        self.main_button_1.grid(row=3, column=2, padx=(10, 10), pady=(10, 0), sticky="nsew")
        self.main_button_2 = customtkinter.CTkButton(master=self, text="Thoát", command=self.sidebar_button_event, fg_color="#192655", border_width=2,font=customtkinter.CTkFont(size=15, weight="bold"))
        self.main_button_2.grid(row=4, column=2, padx=(10, 10), pady=(10, 20), sticky="nsew")
        

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    ## to do: stop server
    def sidebar_button_event(self):
        app.destroy()

    def commandLine(self, command):
        parts = command.split()

        if len(parts) < 2:
            message = "Lệnh không hợp lệ vui lòng nhập lại!"
            tkinter.messagebox.showinfo(message)
        
        if parts[0] == "discover":
            if len(parts) == 2:
                username = parts[1]
                self.view_client_files(username)
            else:
                message = "Lệnh không hợp lệ vui lòng nhập lại!"
                tkinter.messagebox.showinfo("Thông Báo", message)

        elif parts[0] == "ping":
            if len(parts) == 2:
                username = parts[1]
                self.ping_client(username)
            else:
                message = "Lệnh không hợp lệ vui lòng nhập lại!"
                tkinter.messagebox.showinfo(message)

        else:
            message = "Lệnh không hợp lệ vui lòng nhập lại!"
            tkinter.messagebox.showinfo(message)

    def view_client_files(self,username):
        print(username)
        self.files_list=get_user_file(username)
        print("button pressed")
        if self.files_list is None or not isinstance(self.files_list, ClientFilesList):
            self.files_list = ClientFilesList(self, username)  # create window if its None or not a ClientFilesList
        else:
            self.files_list.focus()# if window exists focus it
        self.files_list.grab_set()

    ## to do:
    def ping_client(self, username):
        onlineList = get_onl_users()
        if username in onlineList:
            status_message = f"{username} đang online."
        else:
            status_message = f"{username} không trực tuyến."
        tkinter.messagebox.showinfo("Trạng thái người dùng:", status_message)


class CentralServer(Base):
    def __init__(self, serverhost='localhost', serverport=40000):
        super(CentralServer, self).__init__(serverhost, serverport)

        # get registered user list
        
        self.peerList = get_all_users()
            

        # manage online user list
        self.onlineList = {} 

        # manage online user list have file which have been searched
        self.shareList = {}

        # Delete data in table online
        delete_all_onl_users()
        
        # define handlers for received message of central server
        handlers = {
            'PEER_REGISTER': self.peer_register,
            'PEER_LOGIN': self.peer_login,
            'PEER_SEARCH': self.peer_search,
            'PEER_LOGOUT': self.peer_logout,
            'FILE_REPO': self.peer_upload,
            'DELETE_FILE': self.delete_file,
        }
        for msgtype, function in handlers.items():
            self.add_handler(msgtype, function)
        
    ## ==========implement protocol for user registration - central server==========##
    def peer_register(self, msgdata):
        # received register info (msgdata): peername, host, port, password (hashed)
        peer_name = msgdata['peername']
        peer_host = msgdata['host']
        peer_port = msgdata['port']
        peer_password = msgdata['password']
        
        # register error if peer name has been existed in central server
        # otherwise add peer to managed user list of central server
        if peer_name in self.peerList:
            self.client_send((peer_host, peer_port),
                             msgtype='REGISTER_ERROR', msgdata={})
            print(peer_name, " has been existed in central server!")
        else:
            # add peer to managed user list
            self.peerList.append(peer_name)
            # save to database
            add_new_user(peer_name, peer_password)
            self.client_send((peer_host, peer_port),
                             msgtype='REGISTER_SUCCESS', msgdata={})
            print(peer_name, " has been added to central server's managed user list!")
    ## ===========================================================##

    ## ==========implement protocol for authentication (log in) - central server==========##
    def peer_login(self, msgdata):
        # received login info (msgdata): peername, host, port, password (hashed)
        peer_name = msgdata['peername'] 
        peer_host = msgdata['host']
        peer_port = msgdata['port']
        peer_password = msgdata['password']
        # login error if peer has not registered yet or password not match
        # otherwise add peer to online user list
        if peer_name in self.peerList:
            # retrieve password
            peer_password_retrieved = get_user_password(peer_name)
            if str(peer_password) == peer_password_retrieved:
                
                # add peer to online user list
                self.onlineList[peer_name] = tuple((peer_host, peer_port))
                add_onl_user(peer_name)
                self.client_send((peer_host, peer_port),
                                 msgtype='LOGIN_SUCCESS', msgdata={})

                # update ipaddress and port using by this peer
                update_user_address_port(peer_name, peer_host, peer_port)
                
                # noti
                print(peer_name, " has been added to central server's online user list!")

            else:
                self.client_send((peer_host, peer_port),
                                 msgtype='LOGIN_ERROR', msgdata={})
                print("Password uncorrect!")
        else:
            self.client_send((peer_host, peer_port),
                             msgtype='LOGIN_ERROR', msgdata={})
            print(peer_name, " has not been existed in central server!")
    ## ===========================================================##

    ## =========implement protocol for finding user list who have file searched==============##
    def peer_search(self, msgdata):
        peer_name = msgdata['peername']
        peer_host = msgdata['host']
        peer_port = msgdata['port']
        file_name = msgdata['filename']
        user_list = search_file_name(file_name)

        for peername in user_list:
            if peername in self.onlineList:
                self.shareList[peername] = self.onlineList[peername]

        data = {
            'online_user_list_have_file': self.shareList
        }

        self.client_send((peer_host, peer_port),
                         msgtype='LIST_USER_SHARE_FILE', msgdata=data)
        print(peer_name, " has been sent latest online user list have file!")
        self.shareList.clear()

    ## ================implement protocol for log out & exit=============##
    def peer_logout(self, msgdata):
        peer_name = msgdata['peername']
        onlineList = get_onl_users()
        # delete peer out of online user list 
        if peer_name in onlineList:
            onlineList.remove(peer_name)
            remove_onl_user(peer_name)
            # noti
            print(peer_name, " has been removed from central server's online user list!")
            display_noti(peer_name," logout")
    ## ===========================================================##

    ## ================implement protocol for peer upload file=============##
    def peer_upload(self, msgdata):
        peer_name = msgdata['peername']
        file_name = msgdata['filename']
        file_path = msgdata['filepath']
        add_new_file(peer_name, file_name, file_path)
    ## ===========================================================##


    ##=================implement protocol for peer delete file=============##
    def delete_file(self, msgdata):
        peer_name = msgdata['peername']
        file_name = msgdata['filename']
        delete_file(peer_name, file_name)


app = App()
app.title('P2P File Sharing')
app.geometry("1024x600")
app.resizable(False, False)
def handle_on_closing_event():
    if tkinter.messagebox.askokcancel("Thoát", "Bạn muốn thoát khỏi ứng dụng?"):
        app.destroy()
app.protocol("WM_DELETE_WINDOW", handle_on_closing_event)
# app.mainloop()

# if __name__ == '__main__':
#     server = CentralServer()
#     server.input_recv()
def run_server():
    
    server = CentralServer()
    server.input_recv()
        

if __name__ == '__main__':
    app = App()

    server_thread = Thread(target=run_server)
    server_thread.start()

    app.mainloop()
