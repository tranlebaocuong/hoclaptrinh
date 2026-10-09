"""Chương trình quản lý Playlist bài hát (Console Application)
Được tối ưu hóa cấu trúc hàm, xử lý ngoại lệ và trải nghiệm người dùng (UX).
"""

import sys

def la_stt_hop_le(nhap_vao: str, do_dai: int) -> bool:
    """Kiểm tra giá trị nhập vào có phải số nguyên dương và nằm trong [1, do_dai] hay không."""
    return nhap_vao.isdigit() and (1 <= int(nhap_vao) <= do_dai)


def nhap_stt(thong_bao: str, do_dai: int, cho_phep_huy: bool = True) -> int | None:
    """Hỗ trợ nhập số thứ tự an toàn, có thông báo rõ ràng và tùy chọn hủy thao tác.
    
    Trả về số thứ tự (1-based index) hoặc None nếu người dùng chọn hủy (nhập '0' hoặc 'c').
    """
    goi_y = " (nhập 0 hoặc 'c' để hủy): " if cho_phep_huy else ": "
    while True:
        nhap_vao = input(thong_bao + goi_y).strip()
        if cho_phep_huy and nhap_vao.lower() in ("0", "c", "cancel"):
            print("↩️ Đã hủy thao tác.")
            return None
        
        if la_stt_hop_le(nhap_vao, do_dai):
            return int(nhap_vao)
        
        print(f"❌ Vui lòng nhập số nguyên từ 1 đến {do_dai}!")


def hien_thi_playlist(playlist: list[str]) -> None:
    """In danh sách bài hát đẹp mắt, căn chỉnh đều và xử lý khi danh sách trống."""
    tieu_de = "🎵 PLAYLIST CỦA BẠN"
    duong_ke = "=" * 40
    print(f"\n{duong_ke}")
    print(f"{tieu_de:^38}")
    print(duong_ke)

    if not playlist:
        print("  (Danh sách hiện đang trống)")
    else:
        for stt, ten_bai in enumerate(playlist, 1):
            print(f"  {stt:>2}. {ten_bai}")
    print(duong_ke)


def them_bai_hat(playlist: list[str]) -> None:
    """Thêm một bài hát mới vào cuối danh sách, kiểm tra rỗng và trùng lặp."""
    ten_bai = input("\nTên bài hát muốn thêm (hoặc để trống để hủy): ").strip()
    if not ten_bai:
        print("↩️ Đã hủy thêm bài hát.")
        return

    # Kiểm tra xem bài hát đã có trong danh sách chưa (không phân biệt hoa/thường)
    ten_chuan_hoa = ten_bai.lower()
    da_ton_tai = any(b.lower() == ten_chuan_hoa for b in playlist)
    if da_ton_tai:
        xac_nhan = input(f"⚠️ Bài hát '{ten_bai}' đã có trong danh sách. Bạn vẫn muốn thêm? (y/n): ").strip().lower()
        if xac_nhan not in ("y", "yes"):
            print("↩️ Đã hủy thêm bài hát trùng.")
            return

    playlist.append(ten_bai)
    print(f"✅ Đã thêm: '{ten_bai}' (Vị trí {len(playlist)})")


def thay_doi_thu_tu(playlist: list[str]) -> None:
    """Thay đổi vị trí của một bài hát trong playlist."""
    if len(playlist) < 2:
        print("\n⚠️ Playlist cần ít nhất 2 bài hát để đổi vị trí.")
        return

    print("\n--- ĐỔI VỊ TRÍ BÀI HÁT ---")
    stt_cu = nhap_stt("Nhập STT bài muốn di chuyển", len(playlist))
    if stt_cu is None:
        return

    stt_moi = nhap_stt(f"Chuyển '{playlist[stt_cu - 1]}' đến vị trí số mấy", len(playlist))
    if stt_moi is None:
        return

    if stt_cu == stt_moi:
        print(f"ℹ️ Bài hát '{playlist[stt_cu - 1]}' đã ở vị trí {stt_cu} rồi, không thay đổi.")
        return

    idx_cu = stt_cu - 1
    idx_moi = stt_moi - 1
    bai_chuyen = playlist.pop(idx_cu)
    playlist.insert(idx_moi, bai_chuyen)
    print(f"✅ Đã chuyển '{bai_chuyen}' từ vị trí {stt_cu} sang vị trí {stt_moi} thành công!")


def xoa_bai_hat(playlist: list[str]) -> None:
    """Xóa một bài hát theo STT với xác nhận an toàn."""
    if not playlist:
        print("\n⚠️ Playlist hiện đang trống, không có bài hát nào để xóa!")
        return

    print("\n--- XÓA BÀI HÁT ---")
    stt_xoa = nhap_stt("Xóa bài số mấy", len(playlist))
    if stt_xoa is None:
        return

    idx_xoa = stt_xoa - 1
    bai_can_xoa = playlist[idx_xoa]
    
    xac_nhan = input(f"⚠️ Bạn có chắc muốn xóa '{bai_can_xoa}' (vị trí {stt_xoa}) không? (y/n): ").strip().lower()
    if xac_nhan in ("y", "yes"):
        bai_da_xoa = playlist.pop(idx_xoa)
        print(f"🗑️ Đã xóa thành công: '{bai_da_xoa}'")
    else:
        print("↩️ Đã hủy thao tác xóa.")


def main() -> None:
    playlist = ["Shape of You", "Blinding Lights", "Dynamite"]

    while True:
        try:
            hien_thi_playlist(playlist)
            print("\nBạn muốn làm gì?")
            print("  (1) Thêm bài hát")
            print("  (2) Thay đổi thứ tự bài hát")
            print("  (3) Xóa bài hát")
            print("  (q) Thoát")

            lua_chon = input("> ").strip().lower()

            if lua_chon in ("q", "quit", "exit"):
                print("\nTạm biệt! Hẹn gặp lại 👋\n")
                break
            elif lua_chon == "1":
                them_bai_hat(playlist)
            elif lua_chon == "2":
                thay_doi_thu_tu(playlist)
            elif lua_chon == "3":
                xoa_bai_hat(playlist)
            else:
                print("⚠️ Lựa chọn không hợp lệ, vui lòng chọn 1, 2, 3 hoặc q!")

        except (KeyboardInterrupt, EOFError):
            print("\n\nĐã nhận tín hiệu ngắt. Tạm biệt! 👋\n")
            break


if __name__ == "__main__":
    main()
