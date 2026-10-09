"""Server FastAPI phục vụ cả REST API và Web Frontend cho Playlist Manager.
Chạy bằng lệnh: & "A:\\hoclaptrinh\\.venv\\Scripts\\python.exe" server.py
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(title="Music Playlist Manager API")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Bộ nhớ lưu playlist trong session backend
playlist_db: list[str] = ["Shape of You", "Blinding Lights", "Dynamite"]


class AddSongRequest(BaseModel):
    title: str


class ReorderRequest(BaseModel):
    stt_cu: int   # 1-based index
    stt_moi: int  # 1-based index


# 1. API: Lấy danh sách phát
@app.get("/api/playlist")
def get_playlist():
    return {
        "total": len(playlist_db),
        "playlist": playlist_db
    }


# 2. API: Thêm bài hát
@app.post("/api/playlist")
def add_song(payload: AddSongRequest):
    title = payload.title.strip()
    if not title:
        raise HTTPException(status_code=400, detail="Tên bài hát không được để trống!")
    
    playlist_db.append(title)
    return {
        "message": f"Đã thêm '{title}'",
        "playlist": playlist_db,
        "new_position": len(playlist_db)
    }


# 3. API: Đổi thứ tự bài hát
@app.put("/api/playlist/reorder")
def reorder_song(payload: ReorderRequest):
    stt_cu = payload.stt_cu
    stt_moi = payload.stt_moi
    total = len(playlist_db)

    if not (1 <= stt_cu <= total) or not (1 <= stt_moi <= total):
        raise HTTPException(status_code=400, detail=f"STT phải nằm trong khoảng từ 1 đến {total}")

    if stt_cu == stt_moi:
        return {
            "message": f"Bài hát đã ở vị trí {stt_cu}",
            "playlist": playlist_db
        }

    idx_cu = stt_cu - 1
    idx_moi = stt_moi - 1
    bai_chuyen = playlist_db.pop(idx_cu)
    playlist_db.insert(idx_moi, bai_chuyen)

    return {
        "message": f"Đã chuyển '{bai_chuyen}' từ vị trí {stt_cu} sang {stt_moi}",
        "playlist": playlist_db
    }


# 4. API: Xóa bài hát theo STT (1-based)
@app.delete("/api/playlist/{stt}")
def delete_song(stt: int):
    total = len(playlist_db)
    if not (1 <= stt <= total):
        raise HTTPException(status_code=400, detail=f"STT phải nằm trong khoảng từ 1 đến {total}")

    bai_da_xoa = playlist_db.pop(stt - 1)
    return {
        "message": f"Đã xóa thành công '{bai_da_xoa}'",
        "playlist": playlist_db
    }


# Route trang chủ: Trả về file playlist.html
@app.get("/")
def serve_index():
    return FileResponse(os.path.join(CURRENT_DIR, "playlist.html"))


# Phục vụ các file tĩnh (CSS, JS, hình ảnh)
app.mount("/", StaticFiles(directory=CURRENT_DIR), name="static")

if __name__ == "__main__":
    print("\n🚀 Server đang khởi chạy tại: http://localhost:8000")
    print("Mở trình duyệt truy cập: http://localhost:8000 để sử dụng Playlist Manager!\n")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
