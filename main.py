from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()



# 1. Định nghĩa câis trúc dữ liệu (request body)


#Dùng pydantic để kiểm tra dữ liệu gửi lên cho POST ENDPOINT
class UserProfile(BaseModel):
    name: str
    old: int
    living: str


# 2. các Get END point (chuyển đổi từ hàm nhập liệu có sẵn)


# End point 1: nhận tham số qua URL và trả về câu giới thiệu đầy đủ:
@app.get("/introduce")
def introduce(name: str, old: int, living: str):
    intro_message = f"Xin chào, tôi tên là {name}, tôi {old} tuổi và tôi sống tại {living}."
    return {
        "status": "success",
        "message": intro_message
    }

# End point 2: nhận thông tin thành phố qua url và trả về lời chào:
@app.get("/location")
def get_location(living: str):
    return {
        "status": "success",
        "message": f"Chào mừng bạn đến với {living}!, chúc bạn có một thời gian tuyệt vời tại đây."
    }


# 3. POST END POINT (nhận dữ liệu ẩn qua Request body)


# Endpoint post: nhận gói dữ liệu JSON gửi lên body của yêu cầu:
@app.post("/submit-profile")
def create_profile(user: UserProfile):
    # Dữ liệu gửi lên tự động chuyển thành object 'user', truy cập qua user.name, user.old....
    intro_message = f"Hồ sơ đã được lưu! Xin chào: {user.name}, {user.old} tuổi, đến từ thành phố {user.living}."
    return {
        "status": "success",
        "data_received": user,
        "message": intro_message
    }