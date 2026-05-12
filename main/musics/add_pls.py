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


def doc_du_lieu(file_path):
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


def hien_thi_kho_nhac(all_songs):
    print()
    print("=== DANH SÁCH BÀI HÁT ===")
    for i, song in enumerate(all_songs, 1):
        print(f"{i}. {song['title']}")


def luu_du_lieu(file_path, data):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except OSError as e:
        print(f"Không ghi được file ({file_path}): {e}")
        raise


def tao_playlist_moi():
    _stdio_utf8_win32()
    root_dir = Path(__file__).resolve().parents[2]
    songs_path = root_dir / "data" / "music" / "songs.json"
    playlists_path = root_dir / "data" / "music" / "playlists.json"

    try:
        all_songs = doc_du_lieu(songs_path)
        all_playlists = doc_du_lieu(playlists_path)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return

    try:
        name_playlist = input("nhập tên playlist mới: ").strip()
    except (EOFError, UnicodeDecodeError):
        print("\nKhông đọc được dữ liệu nhập.")
        return

    if not name_playlist:
        print("Tên playlist không được để trống.")
        return
    print()

    hien_thi_kho_nhac(all_songs)

    da_chon = []

    while True:
        try:
            choice = input("thêm bài (nhập STT hoặc q để xong): ").strip()
        except (EOFError, UnicodeDecodeError):
            print("\nKết thúc nhập.")
            break

        if choice.lower() == "q":
            break

        try:
            idx = int(choice.strip()) - 1
            if 0 <= idx < len(all_songs):
                song_id = all_songs[idx]["id"]
                if song_id not in da_chon:
                    da_chon.append(song_id)
                else:
                    print("bài hát có trong danh sách rồi")
            else:
                print("STT không hợp lệ")
        except ValueError:
            print("Vui lòng nhập số hoặc 'q'")

        print()
        print(f"=== {name_playlist} ===")
        for i, s_id in enumerate(da_chon, 1):
            title = next(
                (song["title"] for song in all_songs if song["id"] == s_id),
                "không rõ",
            )
            print(f"{i}. {title}")

    next_id = max((pl.get("id", 0) for pl in all_playlists), default=0) + 1
    all_playlists.append({"id": next_id, "name": name_playlist, "song_ids": da_chon})
    try:
        luu_du_lieu(playlists_path, all_playlists)
    except OSError:
        return

    print()
    print(f"đã lưu playlist: {name_playlist}")


if __name__ == "__main__":
    try:
        tao_playlist_moi()
    except KeyboardInterrupt:
        print("\nĐã hủy.")
