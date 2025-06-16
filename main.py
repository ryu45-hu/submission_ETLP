from utils.extract import scraping_product
from utils.transform import transform_product
from utils.load import save_to_csv
import pandas as pd

"""def save_to_csv(df, filename="cleaned_products.csv"):
    df.to_csv(filename, index=False)
    print(f"Data disimpan ke: {filename}")"""

def main():
    # Ekstrasi data dari web
    BASE_URL_1 = "https://fashion-studio.dicoding.dev/"
    PAGES_URL_TO50 = "https://fashion-studio.dicoding.dev/page{}"

    raw_df = scraping_product(BASE_URL_1, PAGES_URL_TO50, start_page=1, end_page=50)

    print("Data sebelum transformasi:\n")
    df = pd.DataFrame(raw_df)
    print(df)

    # Transformasi data
    print("Data setelah transformasi: \n")
    df_clean = transform_product(raw_df)
    print(df_clean)
    print("\n")
    print(f"Jumlah data setelah transformasi: {len(df_clean)}\n")
    print(df_clean.info())
    
    # Load data
    save_to_csv(df_clean)
    
if __name__== "__main__":
    main()