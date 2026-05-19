# hoclaptrinh - Python Learning Project

Dự án học tập Python với các ví dụ thực hành về cơ bản đến nâng cao, bao gồm cấu trúc dữ liệu, xử lý file, module, và ứng dụng thực tế.

## 📁 Cấu trúc dự án

```
hoclaptrinh/
├── main/                    # Code Python chính
│   ├── bill/               # Quản lý hóa đơn, tiền điện
│   ├── convert/            # Chuyển đổi dữ liệu (tiền tệ, đơn vị)
│   ├── dict/               # Làm việc với từ điển (dictionary)
│   ├── dict_list/          # Kết hợp từ điển và danh sách
│   ├── game/               # Các game/trò chơi Python
│   ├── import_module/      # Tập import và dùng module
│   ├── introduce/          # Giới thiệu bản thân, password
│   ├── list/               # Làm việc với danh sách (list)
│   ├── math/               # Bài toán toán học (hình học, v.v)
│   ├── menu/               # Tập làm menu lựa chọn
│   ├── musics/             # Quản lý danh sách phát nhạc (JSON)
│   ├── return/             # Tập dùng return trong hàm
│   └── test_code/          # Các file test và thử nghiệm
├── data/                    # Dữ liệu mẫu
│   ├── colors/             # Danh sách màu
│   ├── docs/               # Tài liệu (động vật, v.v)
│   ├── music/              # File JSON nhạc/playlist
│   ├── numbers/            # Số chẵn/lẻ
│   └── orders/             # Menu và đơn hàng
├── .venv/                   # Virtual environment
└── README.md
```

## 🚀 Bắt đầu

### 1. Clone repo
```bash
git clone https://github.com/tranlebaocuong/hoclaptrinh.git
cd hoclaptrinh
```

### 2. Tạo và kích hoạt virtual environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Chạy các ví dụ
```bash
python main/musics/music.py
python main/game/tuti.py
python main/math/tam_giac.py
```

## 📚 Các phần học chính

| Folder | Mục đích |
|--------|---------|
| `bill/` | Tính tiền điện, quản lý hóa đơn |
| `convert/` | Chuyển đổi tiền tệ, đơn vị |
| `dict/` | Các thao tác cơ bản với dictionary |
| `list/` | Làm việc với danh sách, playlist |
| `game/` | Trò chơi đơn giản (tuti, v.v) |
| `math/` | Bài toán hình học (tam giác, hình tròn) |
| `import_module/` | Tập import module và sử dụng |
| `menu/` | Xây dựng menu tương tác |
| `musics/` | Quản lý dữ liệu JSON |

## 🛠️ Yêu cầu

- Python 3.10+
- Không cần thư viện bên ngoài (dùng thư viện chuẩn)

## 💡 Cách sử dụng

1. Chọn một folder trong `main/`
2. Mở file `.py` và đọc code
3. Chạy file: `python <tên-file>`
4. Sửa code và thử nghiệm

## 📝 Ghi chú

- Tất cả code viết bằng Python thuần
- Hỗ trợ tiếng Việt (UTF-8)
- Mỗi file có comment giải thích

## 🔄 Git & Pull Request

Dự án dùng Git để quản lý phiên bản:
```bash
git checkout -b feature/tên-tính-năng
git add .
git commit -m "Mô tả thay đổi"
git push origin feature/tên-tính-năng
```

Sau đó tạo Pull Request trên GitHub.

## 📧 Tác giả

**Trần Lê Bảo Cường**
- GitHub: [@tranlebaocuong](https://github.com/tranlebaocuong)

## 📄 License

Dự án này mở cho mục đích học tập.

---

**Happy Coding! 🎉**
