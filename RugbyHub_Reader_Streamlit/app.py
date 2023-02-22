import read_xml as read_xml
import streamlit as st
import pandas as pd
import os

st.title("RugbyHub Reader")
st.write("https://camp.trainocate.co.jp/magazine/streamlit-web/ このページを参考にしています。")
# st.checkbox("チェックボックス")
# st.text_input("入力欄")
uploaded_file = st.file_uploader("super_scout_advanceファイルをアップロード")
if uploaded_file is not None:
    df = read_xml.read_xml(uploaded_file)
    action = st.selectbox(
        'Select Action', df.action.drop_duplicates(keep='first'))
    team_id = st.selectbox(
        'Select Team', df.team_id.drop_duplicates(keep='first'))
    df
    if action is not None:
        act = df.loc[df['action'] == action]
        if action == 'Ruck':
            read_xml.ruck_speed(df, team_id)
        elif action == 'Kick':
            read_xml.kick(df, team_id)
        elif action == 'Lineout Throw':
            read_xml.lineout(df, team_id)
        else:
            st.write("選択したactionに紐づくx_coordとy_coordをプロットしています。順次機能追加予定です。")
            read_xml.plot_by_action(df, action, team_id)
            act
