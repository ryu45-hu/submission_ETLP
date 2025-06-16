import pandas as pd

def save_to_csv(df: pd.DataFrame, output_path: str = "products.csv") -> None:
    df.to_csv(output_path, index=False)
    print(f"\nData Content berhasil disimpan ke {output_path}\n")