import read_xml as read_xml
import streamlit as st
import pandas as pd
import os

st.title("RugbyHub Reader")
path = os.getcwd()
st.write(path)
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
        read_xml.plot_by_action(df, action, team_id)
        act
