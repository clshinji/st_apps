import tabula
import pandas as pd
from pprint import pprint


def get_table(target_pdf, config):
    ''' Streamlit上でアップしたPDFからデータテーブル用CSVを生成する
        ※元々ノートブック上で手動で実行していた操作を移植
    Args:
        target_pdf(str): StreamlitにアップしたPDFファイルパス
        config(instance): config.ymlを読み込んだ設定ファイル
    '''

    # 列名のチェック用
    print('＜列名のチェック＞')
    print('pattern1')
    print(f'column counts(p.1):{len(config.column_names_pg1)}')
    print(f'column names (p.1):{config.column_names_pg1}')

    print('pattern2')
    print(f'column counts(p.1):{len(config.column_names_pg2)}')
    print(f'column names (p.1):{config.column_names_pg2}')

    # PDFファイルから表を読み込む
    print('PDFファイルを読み込む')
    # df = tabula.read_pdf('allergy.pdf', pages='all')
    df = tabula.read_pdf(target_pdf, pages='all')

    # 読み込まれたデータの確認
    print('読み込まれたデータを確認')
    print(f'data type(p.1): {type(df[0])}')

    # ページ数を取得する
    page_counts = len(df)
    print(f'page counts:{page_counts}')

    # 全ページのカラム数が一致していることを確認する
    # p.1のみ31列として読み込まれることが多い？
    for i in range(len(df)):
        df_org = df[i].copy()
        # print(f'column names :{df_org.columns}')
        print(f'page No.:{i}, column counts:{len(df_org.columns)}')

    # df check -> p.1のデータフレームだけ表示してみる
    pprint(df[0].head(10))

    # 1ページ目だけ先に読み込む
    # 1ページ目の表を取得する
    df_org = df[0].copy()
    print(f"p.1 columns counts = {len(df_org.columns)}")

    if len(df[0].columns) == 31:
        print("column_names_pg1 apply")
        # 1ページ目だけ31ページある場合に実行
        # カラム名を設定する
        df_org.columns = config.column_names_pg1
        # 「'●', '○'」を含まない行を削除する
        df_allergy = df_org[df_org[config.column_names_pg1].isin(['●', '○']).any(axis=1)].copy()
        # 1ページ目の不要な列を削除する
        df_allergy = df_allergy.drop(columns='不要')
    else:
        print("column_names_pg2 apply")
        # カラム名を設定する
        df_org.columns = config.column_names_pg2
        # 「'●', '○'」を含まない行を削除する
        df_allergy = df_org[df_org[config.column_names_pg2].isin(['●', '○']).any(axis=1)].copy()

    # 2ページ目以降の表を取得して結合する
    for i in range(1, len(df)):
        df_org = df[i].copy()
        df_org.columns = config.column_names_pg2
        # print(f'column names :{df_org.columns}')
        print(f'page No.:{i}, column counts:{len(df_org.columns)}')
        # 「'●', '○'」を含まない行を削除する
        df_org = df_org[df_org[config.column_names_pg2].isin(['●', '○']).any(axis=1)].copy()
        # df_allergyにdf_orgを縦方向に連結する
        df_allergy = pd.concat([df_allergy, df_org], axis=0, ignore_index=True).copy()
        print(f' -> df_allergy shape: {df_allergy.shape}')

    pprint(df_allergy)

    # 作成したdf_allergyをcsv形式で保存する
    df_allergy.to_csv('allergy_table.csv')
    print('CSV Convert > allergy_table.csv')


if __name__ == '__main__':
    print('This file is for module')

