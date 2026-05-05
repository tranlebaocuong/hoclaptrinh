import json

def doc_json(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def luu_file(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def lay_ten_bai(s_id, songs):
    for s in songs:
        if s['id'] == s_id:
            return s['title']
    return "không rõ"

# def in_danh_sach_trong_pl(playlist, songs):
#     for i, s_id in enumerate(playlist['song_ids'], 1):
#         print(f"{i}. {lay_ten_bai(s_id, songs)}")

def menu_them_bai(playlist, songs):
    print("==== DANH SÁCH BÀI HÁT ==== ")
    for i, s in enumerate(songs, 1):
        print(f"{i}. {s['title']}")

    stt = input("thêm bài số mấy? (hoặc q để thoát): ")
    if stt.isdigit():
        idx = int(stt) - 1
        id_moi = songs[idx]['id']

        if id_moi not in playlist['song_ids']:
            playlist['song_ids'].append(id_moi)
        else:
            print("đã có trong playlist")
    else: print("không có")



def menu_xoa_bai(playlist):
    stt = input("xóa bài số mấy? (stt): ")
    if stt.isdigit():
        playlist['song_ids'].pop(int(stt) - 1)


def menu_doi_thu_tu(playlist):
    cu = int(input("bai muốn chuyển (stt): ")) - 1
    moi = int(input("vị trí mới (stt): ")) - 1

    id_bai = playlist['song_ids'].pop(cu)
    playlist['song_ids'].insert(moi,id_bai)

def thuc_thi_playlist(playlist, songs, all_playlists):
    while True:
        print(f"=== {playlist['name']} ===")
        if not (f"==== {playlist['name']} ==="):
            print('trống')

        else:
            for i, s_id in enumerate(playlist['song_ids'], 1):
                print(f"{i}. {lay_ten_bai(s_id, songs)}")

        print("(1). Thêm | (2). xóa | (3). đổi | (p) đổi playlist | (q) thoát")
        lenh = input("---> : ").lower()

        if lenh == 'q': return "exit"
        if lenh == 'p': return "back"

        if lenh == '1': menu_them_bai(playlist, songs)
        elif lenh == '2': menu_xoa_bai(playlist)
        elif lenh == '3': menu_doi_thu_tu(playlist)

        luu_file("practicing/music/playlists.json", all_playlists)


def quan_ly_playlist():
    songs = doc_json("practicing/music/songs.json")
    playlists = doc_json("practicing/music/playlists.json")

    while True:
        print("=== DANH SÁCH BÀI PLAYLIST ===")
        for i, pl in enumerate(playlists, 1):
            print(f"{i}. {pl['name']}")
        print("(n). tạo mới | (q). thoát")

        chon = input("chọn: "). lower()
        if chon == 'q': break

        if chon == 'n':
            ten = input("tên playlits mới: ")
            if ten.strip():
                new_id = len(playlists) + 1
                playlists.append({"id": new_id, "name": ten, "song_ids": []})
                luu_file("practicing/music/playlists.json", playlists)
                print(f" đã tạo playlist '{ten}'")
            continue

        if chon.isdigit():
            idx_pl = int(chon) - 1
            if 0 <= idx_pl < len(playlists):
                pl_dang_chon = playlists[idx_pl]
                ket_qua = thuc_thi_playlist(pl_dang_chon, songs, playlists)
                if ket_qua == "exit": break
            else: print("playlist không tồn tại")
        else: print("vui lòng chọn STT hoặc lệnh(n/q)")
    print("đã lưu")


quan_ly_playlist()
