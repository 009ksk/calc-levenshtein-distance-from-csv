import pandas as pd
import sys
import os
from Levenshtein import distance


def generate_output_path(base_name, ext):
    """出力ファイルが既に存在する場合に、番号を付けて新しいファイル名を生成する"""
    counter = 1
    new_output_path = f"{base_name}_with_similarity{ext}"
    while os.path.exists(new_output_path):
        new_output_path = f"{base_name}_with_similarity({counter}){ext}"
        counter += 1
    return new_output_path


def calculate_similarity(input_csv_path, column_a, column_b):
    try:
        # CSVファイルを読み込む
        df = pd.read_csv(input_csv_path)

        # カラム名の検証
        if column_a not in df.columns or column_b not in df.columns:
            raise ValueError(f"Error: One or both of the specified columns '{column_a}' and '{column_b}' do not exist in the input CSV file.")

        # 類似率を計算して新しい列に追加
        def similarity_rate(a, b):
            lev_distance = distance(a, b)
            max_len = max(len(a), len(b))
            return 1 - lev_distance / max_len if max_len > 0 else 1

        df['similarity_rate'] = df.apply(lambda row: similarity_rate(
            str(row[column_a]), str(row[column_b])), axis=1)

        # output_csv_pathの生成
        base, ext = os.path.splitext(input_csv_path)
        output_csv_path = generate_output_path(base, ext)

        # 新しいCSVファイルに書き出し
        df.to_csv(output_csv_path, index=False)
        print(f"Successfully processed the file. Output saved to '{output_csv_path}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_csv_path}' was not found.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{input_csv_path}' is empty.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_csv_path> <column_a> <column_b>")
        sys.exit(1)  # エラーステータスで終了

    input_csv_path = sys.argv[1]
    column_a = sys.argv[2]
    column_b = sys.argv[3]

    calculate_similarity(input_csv_path, column_a, column_b)
