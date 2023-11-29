# BTL-1-MMT

## Bước 1: Tải mã nguồn từ github về máy bằng lệnh git clone
 #### • git clone https://github.com/NguyenQuy1306/BTL-1-MMT.git
##  Bước 2: Khởi động server:
  #### • python central_server.py server_port
##  Bước 3: Thay đổi địa chỉ IP :
   #### • Đầu tiên vào file client.py tìm kiếm từ "server_info" đầu tiên của file.
  #### • Ta sẽ thấy câu lệnh :
  
   def \__init__(self, serverhost=’localhost’, serverport=30000, server_info=(’192.168.56.1’,40000))
    
   #### • Thay 192.168.56.1 bằng địa chỉ IP của máy tính cá nhân.
##  Bước 4: Khởi động client:
   #### • python client.py server_port
