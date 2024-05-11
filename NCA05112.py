import streamlit as st
import pandas as pd
import base64
from datetime import datetime

# ページのタイトルを設定
st.markdown('<h1 style="color: red;">栄養価計算アプリ</h1>', unsafe_allow_html=True)

# セッション状態を管理するための初期化
if 'result_df' not in st.session_state:
    st.session_state['result_df'] = pd.DataFrame(columns=['食品名', '重量（g）', 'エネルギー（kcal）', 'たんぱく質（g）', '脂質（g）', '炭水化物（g）', '食塩（g）', '単価（円）'])
    st.session_state['reset_clicked'] = False  # 初期状態ではリセットボタンがクリックされていない状態とします

# ウィジェットを配置
uploaded_file = st.file_uploader('食品データベースをアップロード', type='csv')
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    selected_food = st.selectbox('食品を選択', df['食品名'].unique())

    # 重量の入力ウィジェットを配置
    weight = st.number_input('重量（g）', min_value=0.0, format='%f')

    if st.button('登録') and weight > 0:
        # 選択した食品の情報を取得
        selected_food_info = df[df['食品名'] == selected_food].iloc[0]
        
        # 栄養価の計算
        energy = selected_food_info['エネルギー'] * weight / 100
        protein = selected_food_info['たんぱく質'] * weight / 100
        fat = selected_food_info['脂質'] * weight / 100
        carbs = selected_food_info['炭水化物'] * weight / 100
        salt = selected_food_info['食塩'] * weight / 100
        price = selected_food_info['単価'] * weight / 100

        # 登録したデータをDataFrameに追加
        new_row = pd.DataFrame({
            '食品名': [selected_food],
            '重量（g）': [weight],
            'エネルギー（kcal）': [energy],
            'たんぱく質（g）': [protein],
            '脂質（g）': [fat],
            '炭水化物（g）': [carbs],
            '食塩（g）': [salt],
            '単価（円）': [price]
        })
        st.session_state['result_df'] = pd.concat([st.session_state['result_df'], new_row], ignore_index=True)

# 登録した表を表示
st.subheader('登録済みデータ')
if 'result_df' in st.session_state:
    # 行を選択するためのチェックボックスを追加
    rows_to_delete = st.session_state['result_df'].index.tolist()
    checked_rows = st.checkbox("全て選択")
    if checked_rows:
        rows_to_delete = st.session_state['result_df'].index.tolist()
    else:
        rows_to_delete = st.multiselect('削除する行を選択', st.session_state['result_df'].index.tolist())

    # チェックされた行を削除
    if st.button('選択した行を削除'):
        st.session_state['result_df'] = st.session_state['result_df'].drop(rows_to_delete)
        st.success('選択した行が削除されました。')
    
     # 登録したデータを表示
    st.dataframe(st.session_state['result_df'].round(1))  # 小数点第1位までに修正


    # 登録したデータのみをCSVファイルとしてダウンロードするリンクを生成
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    registered_filename = f'registered_food_list_{current_time}.csv'
    b64_registered = base64.b64encode(st.session_state['result_df'].to_csv(index=False).encode()).decode()
    href_registered = f'<a href="data:file/csv;base64,{b64_registered}" download="{registered_filename}">登録したデータのみをダウンロード</a>'
    st.markdown(href_registered, unsafe_allow_html=True)

    # 合計を計算
    total_energy = st.session_state['result_df']['エネルギー（kcal）'].sum()
    total_protein = st.session_state['result_df']['たんぱく質（g）'].sum()
    total_fat = st.session_state['result_df']['脂質（g）'].sum()
    total_carbs = st.session_state['result_df']['炭水化物（g）'].sum()
    total_salt = st.session_state['result_df']['食塩（g）'].sum()
    total_price = st.session_state['result_df']['単価（円）'].sum()

    # 合計を表で表示
    st.write('### 合計')
    total_row = pd.DataFrame({
        '食品名': ['合計'],
        '重量（g）': [''],
        'エネルギー（kcal）': [total_energy],
        'たんぱく質（g）': [total_protein],
        '脂質（g）': [total_fat],
        '炭水化物（g）': [total_carbs],
        '食塩（g）': [total_salt],
        '単価（円）': [total_price]
    })

    # 登録データと合計を組み合わせた表を作成
    combined_table = pd.concat([st.session_state['result_df'], total_row])
    st.dataframe(combined_table)

    # 結合した食品データをCSVファイルとしてダウンロードするリンクを生成
    combined_filename = f'combined_food_list_{current_time}.csv'
    b64_combined = base64.b64encode(combined_table.to_csv(index=False).encode()).decode()
    href_combined = f'<a href="data:file/csv;base64,{b64_combined}" download="{combined_filename}">結合した食品データをダウンロード</a>'
    st.markdown(href_combined, unsafe_allow_html=True)
 
 
import streamlit as st
import pandas as pd
import base64
from datetime import datetime

# データフレームを初期化
data = {'食品名': [], 'エネルギー(kcal)': [], 'たんぱく質(g)': [], '脂質(g)': [], '炭水化物(g)': [], '食塩(g)': [], '単価(円)': []}
df = pd.DataFrame(data)


# Streamlitアプリを設定
st.markdown('<h1 style="color: red;">食品データベース</h1>', unsafe_allow_html=True)

# 食品成分の登録フォーム
food_name = st.text_input('食品名')
energy = st.number_input('エネルギー(kcal)', min_value=0.0, step=0.1, format="%.1f")
protein = st.number_input('たんぱく質(g)', min_value=0.0, step=0.1, format="%.1f")
fat = st.number_input('脂質(g)', min_value=0.0, step=0.1, format="%.1f")
carbs = st.number_input('炭水化物(g)', min_value=0.0, step=0.1, format="%.1f")
salt = st.number_input('食塩(g)', min_value=0.0, step=0.1, format="%.1f")
price = st.number_input('単価(円)', min_value=0.0, step=0.01, format="%.1f")
register_button = st.button('食品成分を登録')

# 食品成分を登録する関数
def register_food(food_name, energy, protein, fat, carbs, salt, price):
    df.loc[len(df)] = [food_name, energy, protein, fat, carbs, salt, price]

# 登録ボタンがクリックされたら食品成分を登録
if register_button:
    if food_name != '':
        register_food(food_name, energy, protein, fat, carbs, salt, price)
        st.success('食品成分を登録しました。')

# 新しく登録された食品成分を表示する
st.subheader('新しい食品データ:')
st.write(df)

# リセットボタンを配置
reset_button = st.button('リセット')
if reset_button:
    df = pd.DataFrame(data)
    st.success('データをリセットしました。')

# CSVファイルをストリーミングしてダウンロード
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()
download_filename = f"food_data_{current_time}.csv"
href = f'<a href="data:file/csv;base64,{b64}" download="{download_filename}">食品データをダウンロード</a>'
st.markdown(href, unsafe_allow_html=True)

# 保存した食品データをアップロード
uploaded_file = st.file_uploader('保存した食品データをアップロード', type=['csv'])
if uploaded_file is not None:
    uploaded_df = pd.read_csv(uploaded_file)
    combined_df = pd.concat([df, uploaded_df], ignore_index=True)
    st.subheader('保存した食品データと新しい食品データ:')
    st.write(combined_df)
else:
    # データがない場合も初めから表示させる
    st.subheader('保存した食品データと新しい食品データ:')
    st.write(df if not df.empty else pd.DataFrame(data))

# 初期表示時に結合した食品データをダウンロードできるリンクを表示
combined_filename = f'combined_food_list_{current_time}.csv'
b64_combined = base64.b64encode(df.to_csv(index=False).encode()).decode()
href_combined = f'<a href="data:file/csv;base64,{b64_combined}" download="{combined_filename}">結合した食品データをダウンロード</a>'
st.markdown(href_combined, unsafe_allow_html=True)

