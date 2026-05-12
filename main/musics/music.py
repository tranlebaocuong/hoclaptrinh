import json
import sys
from pathlib import Path


def _stdio_utf8_win32():
    if sys.platform != "win32":
        return
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8")
            except (OSError, ValueError, AttributeError):
                pass


def doc_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        raise
    except json.JSONDecodeError as e:
        print(f"File JSON không hợp lệ ({file_path}): {e}")
        raise
    except OSError as e:
        print(f"Không đọc được file: {e}")
        raise


def luu_file(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"Không ghi được file ({path}): {e}")
        raise


def lay_ten_bai(s_id, songs):
    for s in songs:
        if s["id"] == s_id:
            return s["title"]
    return "không rõ"


def menu_them_bai(playlist, songs):
    print("==== DANH SÁCH BÀI HÁT ==== ")
    for i, s in enumerate(songs, 1):
        print(f"{i}. {s['title']}")

    try:
        stt = input("thêm bài số mấy? (hoặc q để thoát): ")
    except (EOFError, UnicodeDecodeError):
        print("Không đọc được dữ liệu nhập.")
        return

    if stt.lower() == "q":
        return

    if stt.isdigit():
        idx = int(stt) - 1
        if 0 <= idx < len(songs):
            id_moi = songs[idx]["id"]
            playlist.setdefault("song_ids", [])
            if id_moi not in playlist["song_ids"]:
                playlist["song_ids"].append(id_moi)
            else:
                print("đã có trong playlist")
        else:
            print("STT không hợp lệ")
    else:
        print("không có")


def menu_xoa_bai(playlist):
    playlist.setdefault("song_ids", [])
    try:
        stt = input("xóa bài số mấy? (stt): ")
    except (EOFError, UnicodeDecodeError):
        print("Không đọc được dữ liệu nhập.")
        return

    if not stt.isdigit():
        print("Vui lòng nhập STT hợp lệ.")
        return

    try:
        playlist["song_ids"].pop(int(stt) - 1)
    except IndexError:
        print("STT không hợp lệ")


def menu_doi_thu_tu(playlist):
    playlist.setdefault("song_ids", [])
    try:
        cu_raw = input("bai muốn chuyển (stt): ")
        moi_raw = input("vị trí mới (stt): ")
        cu = int(cu_raw) - 1
        moi = int(moi_raw) - 1
        id_bai = playlist["song_ids"].pop(cu)
        playlist["song_ids"].insert(moi, id_bai)
    except ValueError:
        print("Vui lòng nhập số hợp lệ.")
    except IndexError:
        print("STT không hợp lệ.")


def thuc_thi_playlist(playlist, songs, all_playlists, playlists_path):
    while True:
        print(f"=== {playlist['name']} ===")
        ids = playlist.get("song_ids") or []
        if not ids:
            print("trống")
        else:
            for i, s_id in enumerate(ids, 1):
                print(f"{i}. {lay_ten_bai(s_id, songs)}")

        print("(1). Thêm | (2). xóa | (3). đổi | (p) đổi playlist | (q) thoát")
        try:
            lenh = input("---> : ").lower()
        except (EOFError, UnicodeDecodeError):
            return "exit"

        if lenh == "q":
            return "exit"
        if lenh == "p":
            return "back"

        if lenh == "1":
            menu_them_bai(playlist, songs)
        elif lenh == "2":
            menu_xoa_bai(playlist)
        elif lenh == "3":
            menu_doi_thu_tu(playlist)

        try:
            luu_file(playlists_path, all_playlists)
        except OSError:
            pass


def _next_playlist_id(playlists):
    return max((pl.get("id", 0) for pl in playlists), default=0) + 1


def quan_ly_playlist():
    _stdio_utf8_win32()
    root_dir = Path(__file__).resolve().parents[2]
    songs_path = root_dir / "data" / "music" / "songs.json"
    playlists_path = root_dir / "data" / "music" / "playlists.json"

    try:
        songs = doc_json(songs_path)
        playlists = doc_json(playlists_path)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return

    while True:
        print("=== DANH SÁCH BÀI PLAYLIST ===")
        for i, pl in enumerate(playlists, 1):
            print(f"{i}. {pl['name']}")
        print("(n). tạo mới | (q). thoát")

        try:
            chon = input("chọn: ").lower()
        except (EOFError, UnicodeDecodeError):
            break

        if chon == "q":
            break

        if chon == "n":
            try:
                ten = input("tên playlits mới: ")
            except (EOFError, UnicodeDecodeError):
                break
            if ten.strip():
                new_id = _next_playlist_id(playlists)
                playlists.append({"id": new_id, "name": ten.strip(), "song_ids": []})
                try:
                    luu_file(playlists_path, playlists)
                except OSError:
                    playlists.pop()
                    continue
                print(f" đã tạo playlist '{ten.strip()}'")
            continue

        if chon.isdigit():
            idx_pl = int(chon) - 1
            if 0 <= idx_pl < len(playlists):
                pl_dang_chon = playlists[idx_pl]
                ket_qua = thuc_thi_playlist(
                    pl_dang_chon, songs, playlists, playlists_path
                )
                if ket_qua == "exit":
                    break
            else:
                print("playlist không tồn tại")
        else:
            print("vui lòng chọn STT hoặc lệnh(n/q)")
    print("đã lưu")


if __name__ == "__main__":
    try:
        quan_ly_playlist()
    except KeyboardInterrupt:
        print("\nĐã hủy.")
