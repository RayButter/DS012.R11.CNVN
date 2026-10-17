import requests
from bs4 import BeautifulSoup
import pandas as pd

def thu_thap_du_lieu(url):

    response = requests.get(url, timeout=30)
    response.raise_for_status()
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")
    cac_quoc_gia = soup.select("div.country")

    if not cac_quoc_gia:
        raise ValueError("Không tìm thấy dữ liệu trên website này.")

    du_lieu = []

    for quoc_gia in cac_quoc_gia:
        ten = quoc_gia.select_one(".country-name").get_text(strip=True)
        thu_do = quoc_gia.select_one(".country-capital").get_text(strip=True)
        dan_so = quoc_gia.select_one(".country-population").get_text(strip=True)
        dien_tich = quoc_gia.select_one(".country-area").get_text(strip=True)

        du_lieu.append({
            "ten_quoc_gia": ten,
            "thu_do": thu_do,
            "dan_so": int(dan_so),
            "dien_tich_km2": float(dien_tich)
        })

    return pd.DataFrame(du_lieu)

def tien_xu_li(bang_du_lieu):

    bang_sach = bang_du_lieu.copy()

    bang_sach["thu_do"] = bang_sach["thu_do"].replace({
        "None": pd.NA,
        "": pd.NA
    })

    bang_sach = bang_sach.drop_duplicates().reset_index(drop=True)

    return bang_sach

def thong_ke_du_lieu(bang_du_lieu):

    return bang_du_lieu[["dan_so", "dien_tich_km2"]].describe()

def luu_du_lieu(bang_du_lieu, ten_file):

    if len(bang_du_lieu) < 100:
        raise ValueError("Chưa đủ tối thiểu 100 điểm dữ liệu theo thầy yêu cầu.")

    bang_du_lieu.to_csv(
        ten_file,
        index=False,
        encoding="utf-8-sig"
    )


if __name__ == "__main__":
    url = "https://www.scrapethissite.com/pages/simple/"

    bang_ban_dau = thu_thap_du_lieu(url)
    bang_du_lieu = tien_xu_li(bang_ban_dau)

    luu_du_lieu(bang_du_lieu, "quoc_gia.csv")

    print("Số bản ghi:", len(bang_du_lieu))
    print(thong_ke_du_lieu(bang_du_lieu))
