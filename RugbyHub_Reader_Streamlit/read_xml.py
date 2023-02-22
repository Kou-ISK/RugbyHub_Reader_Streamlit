import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image
import streamlit as st

root_directory = '/Users/isakakou/Documents/workSpace/RugbyHub_Reader_Streamlit'
path = os.getcwd()


def read_xml(FILEPATH):
    # マスタデータのインポート
    print(f'current path: {path}')
    master = pd.read_csv(
        os.path.abspath('app/data/RugbyHub_master_data.csv'), dtype=str)

    # PLID,TEAMIDのインポート
    psheets = ["PLID", "TID", "Venue"]
    plid = pd.read_csv(os.path.abspath(
        'app/data/plid_master.csv'), dtype=str)
    # XMLファイルを解析
    tree = ET.parse(FILEPATH)

    # XMLを取得
    root = tree.getroot()
    df = pd.DataFrame(index=[], columns=['ID', 'FXID', 'PLID', 'team_id', 'ps_timestamp', 'ps_endstamp', 'MatchTime', 'psID', 'period',
                                         'x_coord', 'y_coord', 'x_coord_end', 'y_coord_end', 'action', 'ActionType', 'Actionresult',
                                         'qualifier3', 'qualifier4', 'qualifier5', 'Metres', 'PlayNum', 'SetNum',
                                         'sequence_id', 'player_advantage', 'score_advantage', 'flag', 'advantage', 'assoc_player'])

    for action in root.iter('ActionRow'):
        s = pd.Series([action.get('ID'), action.get('FXID'), action.get('PLID'), action.get('team_id'),
                       action.get('ps_timestamp'), action.get(
                           'ps_endstamp'), action.get('MatchTime'), action.get('psID'),
                       action.get('period'), action.get('x_coord'), action.get(
                           'y_coord'), action.get('x_coord_end'), action.get('y_coord_end'),
                       action.get('action'), action.get('ActionType'), action.get(
                           'Actionresult'), action.get('qualifier3'),
                       action.get('qualifier4'), action.get('qualifier5'), action.get(
                           'Metres'), action.get('PlayNum'), action.get('SetNum'),
                       action.get('sequence_id'), action.get('player_advantage'), action.get(
                           'score_advantage'), action.get('flag'),
                       action.get('advantage'), action.get('assoc_player')], index=df.columns)
        df = df.append(s, ignore_index=True)

    df[['x_coord', 'y_coord', 'x_coord_end', 'y_coord_end']] = df[[
        'x_coord', 'y_coord', 'x_coord_end', 'y_coord_end']].astype(int)

    df.qualifier3 = df.qualifier3.map(master.set_index('ID').Definition)
    df.qualifier4 = df.qualifier4.map(master.set_index('ID').Definition)
    df.qualifier5 = df.qualifier5.map(master.set_index('ID').Definition)
    df.Actionresult = df.Actionresult.map(master.set_index('ID').Definition)
    df.ActionType = df.ActionType.map(master.set_index('ID').Definition)
    df.action = df.action.map(master.set_index('ID').Definition)
    df.team_id = df.team_id.map(plid.set_index('players_id').team_name)
    return df


def get_player_list(FILEPATH):
    # XMLファイルを解析
    tree = ET.parse(FILEPATH)
    # XMLを取得
    root = tree.getroot()
    df = pd.DataFrame(index=[], columns=['ShirtNo', 'Club',
                      'PosID', 'Player_name', 'team_name', 'MINS'])
    for pl in root.iter('Player'):
        s = pd.Series([int(pl.get('ShirtNo')), pl.get('Club'), pl.get('PosID'), pl.get(
            'PLFORN')+' ' + pl.get('PLSURN'), pl.get('TEAMNAME'), pl.get('MINS')], index=df.columns)
        df = df.append(s, ignore_index=True)
    return df


def plot_by_action(df, action, team_id):
    dfaction = df.loc[(df['action'] == action) & (df['team_id'] == team_id)]
    fig = plt.figure(figsize=(7, 10))
    ax = fig.add_subplot(1, 1, 1)
    plt.xlim(0, 68)
    plt.ylim(0, 100)
    # 背景画像の設定
    fig.patch.set_facecolor('white')
    im = Image.open(os.path.abspath('app/data/FIELD_image.jpeg'))
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    plt.imshow(im, extent=[*xlim, *ylim], aspect='auto', alpha=0.6)
    plt.scatter(dfaction['x_coord'], dfaction['y_coord'], marker='D', s=150)
    # ラベルの表示
    lgd = plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
    plt.gcf().subplots_adjust(wspace=4)
    st.pyplot(fig)
