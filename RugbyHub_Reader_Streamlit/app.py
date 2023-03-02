import read_xml as read_xml
import streamlit as st
import pandas as pd
from plot import Plot_method

st.title("RugbyHub Reader")
# st.checkbox("チェックボックス")
st.sidebar.title("Upload")
uploaded_file = st.sidebar.file_uploader(
    "Please upload advanced_superscout.xml file")
if uploaded_file is not None:
    df = read_xml.read_xml(uploaded_file)
    st_df =  st.dataframe(df)
    st.experimental_data_editor(df)
    action = st.selectbox(
        'Select Action', df.action.drop_duplicates(keep='first'))
    team_id = st.selectbox(
        'Select Team', df.team_id.drop_duplicates(keep='first'))
    filterd_df = df.loc[df['team_id'] == team_id]
    # データフレームのカラムを選択肢にする。複数選択
    item = st.multiselect("Select Columns", df.columns)
    p = Plot_method(df, team_id)
    if st.button('Show table and plot'):
        if ((item is not None) & (action is not None)):
            filterd_df.loc[filterd_df['action'] == action][item]
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
