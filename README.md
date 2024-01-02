# BTL-1-MMT


## Bước 1: Tải mã nguồn từ github về máy bằng lệnh git clone tại branch main
 #### • git clone https://github.com/NguyenQuy1306/BTL-1-MMT.git
 
##  Bước 2: Khởi động server:
  #### • python server.py 
##  Bước 3: Thay đổi địa chỉ IP :
   #### • Đầu tiên vào file client.py tìm kiếm từ "server_info" đầu tiên của file.
  #### • Ta sẽ thấy câu lệnh :
  
   def \__init__(self, serverhost=’localhost’, serverport=30000, server_info=(’192.168.56.1’,40000))
    
   #### • Thay 192.168.56.1 bằng địa chỉ IP của máy tính cá nhân.
##  Bước 4: Khởi động các client (ở đây để sẵn có 3 tài khoản với tk và mk như trong demo: tk:miko mk:miko ; tk:eula mk:eula ; tk:ganyu mk:ganyu):
   #### • python client.py
   #### • python client1.py
   #### • python client2.py

