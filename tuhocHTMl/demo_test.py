"""Script tự động chạy demo và kiểm thử các tính năng của playlist_manager.py
trên môi trường ảo Python.
"""

import subprocess
import sys

def run_demo():
    python_executable = sys.executable
    print(f"[*] Đang thực thi bằng Python: {python_executable}\n")

    # Kịch bản demo:
    # 1: Thêm bài hát "See You Again"
    # 2: Đổi vị trí bài hát số 4 ("See You Again") lên vị trí 1
    # 2: Thử đổi vị trí nhưng nhập sai STT (ví dụ 99), sau đó nhập số hợp lệ hoặc nhập 'c' để hủy
    # 3: Xóa bài hát số 2 ("Shape of You"), xác nhận 'y'
    # q: Thoát chương trình
    demo_inputs = [
        # Thao tác 1: Thêm bài mới
        "1",
        "See You Again",
        # Thao tác 2: Đổi vị trí bài 4 về vị trí 1
        "2",
        "4",
        "1",
        # Thao tác 3: Thử nhập sai khi đổi vị trí rồi hủy
        "2",
        "99",  # Sai số
        "c",   # Hủy
        # Thao tác 4: Xóa bài hát số 2
        "3",
        "2",
        "y",   # Xác nhận xóa
        # Thoát
        "q"
    ]

    input_payload = "\n".join(demo_inputs) + "\n"

    process = subprocess.Popen(
        [python_executable, "playlist_manager.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8"
    )

    stdout, stderr = process.communicate(input=input_payload)

    print("===== KẾT QUẢ CHẠY DEMO TỰ ĐỘNG =====")
    print(stdout)
    if stderr:
        print("===== LỖI (STDERR) =====")
        print(stderr)

    if process.returncode == 0:
        print("🎉 Chạy demo thành công không có lỗi!")
    else:
        print(f"⚠️ Quá trình kết thúc với mã lỗi: {process.returncode}")

if __name__ == "__main__":
    run_demo()
