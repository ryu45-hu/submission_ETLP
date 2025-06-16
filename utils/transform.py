import pandas as pd

dirty_content = {
    "Title": ["Unknown Product"],
    "Rating": ["Invalid Rating / 5", "Not Rated"],
    "Price": ["Price Unavailable", None],
}

def transform_product(df: pd.DataFrame) -> pd.DataFrame:
    try:
        # Pembersihan data dengan Title, Rating, atau Price
        df = df[~df["Title"].isin(dirty_content["Title"])]
        df = df[~df["Rating"].isin(dirty_content["Rating"])]
        df = df[~df["Price"].isin(dirty_content["Price"])]

        # Pembersihan kolom Price dan Ubah ke rupiah
        df["Price"] = df["Price"].str.replace("$", "", regex=False)
        df["Price"] = df["Price"].str.strip()
        df["Price"] = df["Price"].astype(float) * 16000

        # Mengambil float dari rating
        df["Rating"] = df["Rating"].str.extract(r"([\d.]+)").astype(float)

        # Ambil float dari Colors
        df["Colors"] = df["Colors"].str.extract(r"(\d+)").astype(int)

        # Bersihkan Size dan Gender
        df["Size"] = df["Size"].str.replace("Size: ", "", regex=False).str.strip()
        df["Gender"] = df["Gender"].str.replace("Gender: ", "", regex=False).str.strip()

        # Drop duplikat dan data kosong
        df = df.drop_duplicates()
        df = df.dropna()

        # Menyesuaikan type datanya
        df = df.astype({
            "Title": "object",
            "Price": "float64",
            "Rating": "float64",
            "Colors": "int64",
            "Size": "object",
            "Gender": "object"
        })

        return df

    except Exception as e:
            print(f"Terjadi kesalahan saat melakukan transformasi : {e}")
            return pd.DataFrame()