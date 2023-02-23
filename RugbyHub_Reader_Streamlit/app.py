import read_xml as read_xml
import streamlit as st
import pandas as pd
import plot

st.title("RugbyHub Reader")
# st.checkbox("チェックボックス")
st.sidebar.title("ファイルアップロード")
uploaded_file = st.sidebar.file_uploader(
    "advanced_superscout.xmlファイルをアップロードしてください")
if uploaded_file is not None:
    df = read_xml.read_xml(uploaded_file)
    action = st.selectbox(
        'Select Action', df.action.drop_duplicates(keep='first'))
    team_id = st.selectbox(
        'Select Team', df.team_id.drop_duplicates(keep='first'))
    df
    # データフレームのカラムを選択肢にする。複数選択
    item = st.multiselect("可視化するカラム", df.columns)
    p = plot.Plot_method(df, team_id)
    if item is not None:
        df[item]
    if action is not None:
        act = df.loc[df['action'] == action]
        if action == 'Ruck':
            p.ruck_speed()
        elif action == 'Kick':
            p.kick()
        elif action == 'Lineout Throw':
            p.lineout()
        else:
            st.write("選択したactionに紐づくx_coordとy_coordをプロットしています。順次機能追加予定です。")
            p.plot_by_action(action)
            act
