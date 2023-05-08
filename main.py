import streamlit as st
import pandas as pd


def main():
    '''
    スシローHPのアレルギー情報(pdf)から読み取ったテーブルを基にして、アレルギー情報を検索するアプリ
    アレルギー情報ファイル名：allergy_table.csv
    サイドバーの
    '''

    csv_path = 'allergy_table.csv'
    type_column_name = '区分'
    names_column_name = 'メニュー名称'

    st.markdown('# 🍣スシローアレルギー情報')
    st.write('更新日:2023/4/28')

    # データフレームの読み込み
    df = pd.read_csv(csv_path, index_col=0)
    columns_list = list(df.columns)
    class_list = df[type_column_name].unique()

    # ユーザ入力
    choiced_allergy_list = st.multiselect(
        'アレルギー項目を選択',
        columns_list[2:],
        ['乳成分']
    )
    if not choiced_allergy_list:
        st.error('アレルギー項目を選択してください')
    choiced_type_list = st.multiselect(
        '区分を選択',
        class_list,
    )
    key = st.text_input('検索したいメニュー名称を入力してください')
    dropna_check = st.checkbox('アレルゲン無を非表示にする')

    # 表示用データフレームの作成
    # 選択されたアレルギー項目だけを抽出
    if choiced_allergy_list:
        drop_columns_list = [x for x in columns_list if x not in choiced_allergy_list and x != type_column_name and x != names_column_name]
    else:
        drop_columns_list = []
    df_view = df.drop(columns=drop_columns_list).copy()

    # アレルギーが含まれない行を削除する
    if dropna_check:
        df_view = df_view.dropna()

    # df_viewのNaNを無に置き換える
    df_view = df_view.fillna('無')

    # 選択した分類だけを抽出する(未選択の場合は実行しない)
    if choiced_type_list:
        df_view = df_view[df_view[type_column_name].isin(choiced_type_list)]

    # 検索keyに部分一致する商品だけを抽出する
    df_view = df_view[df_view[names_column_name].str.contains(key)]

    # デバック用情報をサイドバーに表示させる
    # st.sidebar.write(f'columns_list        : {columns_list}')
    # st.sidebar.write(f'choiced_allergy_list: {choiced_allergy_list}')
    # st.sidebar.write(f'key: {key}')
    # st.sidebar.write(f'choiced class: {choiced_type_list}')
    # st.sidebar.write(f'drop list: {drop_columns_list}')
    # st.sidebar.write('アレルギー項目リスト👇')
    # st.sidebar.write(columns_list)
    
    st.markdown('# アレルギー情報テーブル')
    st.dataframe(df_view)

    st.markdown("""
    # ⚠ 注意 caution\n
    このページは、スシロー公式サイトの情報を参照して作者が個人的に作成したものです。\n
    公的な情報ではありませんので、必ず個人の責任に基づいて利用してください。\n
    This page was personally prepared by the author in reference to information on the official Sushiro website.\n
    It is not public information and should always be used based on personal responsibility.
    """)

    return


if __name__ == '__main__':
    main()
