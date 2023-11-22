from PIL import Image

icon_2 = Image.open("image/login.jfif")
logout_icon = icon_2.resize((30, 30), Image.LANCZOS)

img_3 = Image.open("image/login.jfif")
signup_image = img_3.resize((520, 480), Image.LANCZOS)

img_4 = Image.open("image/login.jfif")
login_image = img_4.resize((520, 480), Image.LANCZOS)