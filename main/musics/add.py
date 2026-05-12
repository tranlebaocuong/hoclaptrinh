
import json
from pathlib import Path


def doc_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Không tìm thấy file: {path}")
        raise
    except json.JSONDecodeError as e:
        print(f"File JSON không hợp lệ ({path}): {e}")
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


def tim_ten_bai(song_id, all_songs):
    for song in all_songs:
        if song["id"] == song_id:
            return song["title"]
    return "không có"


def hien_thi_playlist(playlist, all_songs):
    print()
    print(f"=== {playlist['name']} ===")
    song_ids = playlist.get("song_ids", [])
    for i, s_id in enumerate(song_ids, 1):
        ten = tim_ten_bai(s_id, all_songs)
        print(f"{i}. {ten}")


def cap_nhat_playlist():
    root_dir = Path(__file__).resolve().parents[2]
    songs_path = root_dir / "data" / "music" / "songs.json"
    playlists_path = root_dir / "data" / "music" / "playlists.json"

    try:
        all_songs = doc_file(songs_path)
        all_playlists = doc_file(playlists_path)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return

    print()
    print("=== DANH SÁCH PLAYLIST ===")

    for i, pl in enumerate(all_playlists, 1):
        print(f"{i}. {pl['name']}")

    try:
        stt_pl = input("chọn playlist muốn sửa (nhập STT): ")
    except (EOFError, UnicodeDecodeError):
        print("Không đọc được dữ liệu nhập.")
        return

    if not stt_pl.isdigit():
        print("STT không hợp lệ.")
        return

    stt_pl = int(stt_pl)
    if stt_pl < 1 or stt_pl > len(all_playlists):
        print("STT không tồn tại.")
        return

    da_chon_pl = all_playlists[stt_pl - 1]
    da_chon_pl.setdefault("song_ids", [])

    while True:
        hien_thi_playlist(da_chon_pl, all_songs)

        print()
        print("=== DANH SÁCH BÀI HÁT TỔNG ===")

        for i, song in enumerate(all_songs, 1):
            print(f"{i}. {song['title']}")

        try:
            chon_bai = input("thêm bài nào (nhập STT hoặc q để xong): ")
        except (EOFError, UnicodeDecodeError):
            print("Kết thúc nhập.")
            break

        if chon_bai.lower() == "q":
            break

        if not chon_bai.isdigit():
            print("Vui lòng nhập số hợp lệ hoặc q để thoát.")
            continue

        stt_bai = int(chon_bai)
        if stt_bai < 1 or stt_bai > len(all_songs):
            print("STT bài hát không tồn tại.")
            continue

        id_moi = all_songs[stt_bai - 1]["id"]

        if id_moi not in da_chon_pl["song_ids"]:
            da_chon_pl["song_ids"].append(id_moi)
            print()
            print("đã thêm!")

        else:
            print("bài hát này đã có trong playlist")

    try:
        luu_file(playlists_path, all_playlists)
    except OSError:
        return
    print("Đã lưu thay đổi playlist.")


if __name__ == "__main__":
    try:
        cap_nhat_playlist()
    except KeyboardInterrupt:
        print("\nĐã hủy.")
