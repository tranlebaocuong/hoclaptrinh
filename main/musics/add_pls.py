import json

def doc_du_lieu(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def hien_thi_kho_nhac(all_songs):
    print()
    print("=== DANH SÁCH BÀI HÁT ===")
    for i, song in enumerate(all_songs, 1):
        print(f"{i}. {song['title']}")

def luu_du_lieu(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def tao_playlist_moi():
    all_songs = doc_du_lieu("practicing/music/songs.json")
    all_playlists = doc_du_lieu("practicing/music/playlists.json")

    name_playlist = input("nhập tên playlist mới: ")
    print()

    hien_thi_kho_nhac(all_songs)

    da_chon = []

    while True:
        choice = input("thêm bài (nhập STT hoặc q để xong): ")
        if choice.lower() == 'q':
            break

        name_song = all_songs[int(choice) - 1]['title']


        if name_song not in da_chon:
            da_chon.append(name_song)
        else:
            print("bài hát có trong danh sách rồi")

        print()
        print(f"=== {name_playlist} ===")
        for i, s in enumerate(da_chon, 1):
            print(f"{i}. {s}")


    all_playlists.append({"name": name_playlist, "songs": da_chon})
    luu_du_lieu("practicing/music/playlists.json", all_playlists)

    print()
    print(f"đã lưu playlist: {name_playlist}")


tao_playlist_moi()