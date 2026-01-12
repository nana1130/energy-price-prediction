import pandas as pd
import requests
import os
import io

def fetch_jepx_spot_prices(year):
    """
    指定した年度のJEPXスポット価格データを取得して整形する関数
    year: 西暦 (例: 2023)
    """
    # 【修正1】 URLを .org から .jp に変更
    url = f"https://www.jepx.jp/market/excel/spot_{year}.csv"
    
    print(f"{year}年度のデータを取得中: {url}")
    
    # 【修正2】 ブラウザのふりをするためのヘッダー情報（User-Agent）
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        # headers=headers を追加してアクセス
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        
        # JEPXのCSVは Shift-JIS (cp932) でエンコードされています
        csv_data = io.BytesIO(response.content)
        
        # 読み込み
        df = pd.read_csv(csv_data, encoding='cp932')
        
        return df
    
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return None

def save_data(df, year):
    """データをローカルに保存"""
    save_dir = "data/raw"
    os.makedirs(save_dir, exist_ok=True)
    
    file_path = os.path.join(save_dir, f"spot_prices_{year}.csv")
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"保存完了: {file_path}")

if __name__ == "__main__":
    # 2023年度と2024年度を取得
    target_years = [2023, 2024] 
    
    for y in target_years:
        df = fetch_jepx_spot_prices(y)
        if df is not None:
            print(f"データ取得成功: {len(df)}行")
            print(df.head())
            save_data(df, y)