def tinh_bmi(can_nang, chieu_cao_cm):
    """Tính BMI và tự động đổi cm sang m"""
    chieu_cao_m = chieu_cao_cm / 100
    return round(can_nang / (chieu_cao_m ** 2), 2)

def phan_loai_bmi(bmi, khu_vuc):
    """Phân loại BMI theo chuẩn Âu/Á dựa trên logic của bạn"""
    # Định nghĩa các nhãn kết quả
    A, B, C, D, E, J, G = 'Thiếu cân', 'Bình thường', 'Thừa cân', 'Béo phì', 'Béo phì độ 1', 'Béo phì độ 2', 'Béo phì độ 3'
    
    if khu_vuc == 'âu':
        if bmi < 18.5: return A
        if bmi <= 25.5: return B
        if bmi <= 28.0: return C # Tối ưu lại khoảng cách giữa thừa cân và béo phì
        if bmi <= 30.0: return D
        if bmi <= 35.0: return E
        if bmi <= 40.0: return J
        return G
    
    else: # Khu vực 'á'
        if bmi < 18.5: return A
        if bmi <= 22.9: return B
        if bmi <= 24.9: return C
        if bmi == 25.0: return D
        if bmi <= 29.9: return E
        if bmi <= 39.9: return J
        return G

# --- CHƯƠNG TRÌNH CHÍNH ---
f = input('Âu hay Á? (âu/á): ').strip().lower()
w = float(input('Cân nặng nhiêu á bạn? (kg): '))
h = float(input('Cao nhiêu á bạn? (cm): '))

# Gọi hàm tính toán
chi_so_bmi = tinh_bmi(w, h)

# Gọi hàm phân loại (sử dụng kết quả từ hàm tính toán)
chan_doan = phan_loai_bmi(chi_so_bmi, f)

# Xuất kết quả
ten_khu_vuc = "Châu Âu" if f == 'âu' else "Châu Á"
print(f"\nBạn thuộc nhóm {ten_khu_vuc}")
print(f"Chỉ số BMI của bạn là: {chi_so_bmi}")
print(f"Kết quả: {chan_doan} rồi.")
