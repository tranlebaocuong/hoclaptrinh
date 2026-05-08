import requests

def get_currency_list():
    """
    Lấy danh sách tất cả các loại tiền tệ.
    Dùng API từ: https://github.com/fawazahmed0/exchange-api
    """
    url = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
    response = requests.get(url)
    return response.json()

def get_exchange_rate(base_currency, date='latest'):
    """
    Lấy tỷ giá hối đoái cho một ngày và loại tiền tệ cơ sở cụ thể.
    Dùng API từ: https://github.com/fawazahmed0/exchange-api

    Args:
        base_currency (str): Mã tiền tệ cơ sở (ví dụ: 'usd', 'eur').
        date (str): Ngày để lấy tỷ giá, theo định dạng năm-tháng-ngày (ví dụ: '2023-01-01').

    Returns:
        dict: Một dictionary chứa tỷ giá hối đoái hoặc None nếu có lỗi.
    """
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@{date}/v1/currencies/{base_currency}.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi lấy tỷ giá hối đoái cho {base_currency} vào ngày {date}: {e}")
        return None


# Viết code của bạn tại đây
def hien_thi_pho_bien(all_currencies):
    #hàm chuyên trách việc in danh sách tiền tệ
    print('='*5, 'DANH SÁCH TIỀN TỆ', '='*5)
    tien_te = ['usd', 'eur', 'jpy', 'sgd', 'thb', 'cny']
    for ngoai_te in tien_te:
        if ngoai_te in all_currencies:
            print(f"{ngoai_te} - {all_currencies[ngoai_te]}")
    print()

def nhap_ma_ngoai_te(all_currencies):
    while True:
        ma = input('nhập mã ngoại tệ (hoặc xong để thoát): ').strip().lower()
        if ma == 'xong':
            return 'xong'
        if ma in all_currencies:
            return ma
        print(f"mã {ma} không tồn tại.")

def nhap_so_tien(ten_ma):
    while True:
        nhap = input(f"nhập số tiền {ten_ma.upper()}: ").strip()
        if not nhap: continue

        so_tien = float(nhap)
        if so_tien >= 0:
            return so_tien
        print('số tiền phải lớn hơn hoặc bằng 0.')

def lay_ty_gia_vnd(ma_ngoai_te):
    data = get_exchange_rate(ma_ngoai_te)
    if not data:
        return None
    return data.get(ma_ngoai_te, {}).get('vnd')

def ket_qua_doi_tien(ma, so_tien, ty_gia):
    if not ty_gia:
        print(f"không tìm thấy tỷ giá {ma.upper()}")
        return

    tong_vnd = so_tien * ty_gia
    print(f"tỷ giá: 1 {ma.upper()} = {ty_gia:,} VND")
    print(f"{so_tien:,} {ma.upper()} = {tong_vnd:,}VND")

def main():
    all_currencies = get_currency_list()
    hien_thi_pho_bien(all_currencies)

    while True:
        ma_nhap = nhap_ma_ngoai_te(all_currencies)
        if ma_nhap == 'xong': break

        ty_gia = lay_ty_gia_vnd(ma_nhap)

        if ty_gia:
            so_tien = nhap_so_tien(ma_nhap)

            ket_qua_doi_tien(ma_nhap, so_tien, ty_gia)
        else:
            print('không có dữ liệu')


if __name__ == "__main__":
    main()