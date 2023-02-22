import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
import os
from PIL import Image
import streamlit as st
import seaborn as sns

root_directory = '/Users/isakakou/Documents/workSpace/RugbyHub_Reader_Streamlit'


def read_xml(FILEPATH):
    # マスタデータのインポート
    master = pd.read_csv(
        os.path.abspath('./data/RugbyHub_master_data.csv'), dtype=str)

    # PLID,TEAMIDのインポート
    psheets = ["PLID", "TID", "Venue"]
    plid = pd.read_csv(os.path.abspath(
        './data/plid_master.csv'), dtype=str)
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
    im = Image.open(os.path.abspath('./data/Field_image.jpeg'))
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    plt.imshow(im, extent=[*xlim, *ylim], aspect='auto', alpha=0.6)
    plt.scatter(dfaction['x_coord'], dfaction['y_coord'], marker='D', s=150)
    # ラベルの表示
    lgd = plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
    plt.gcf().subplots_adjust(wspace=4)
    st.pyplot(fig)


def lineout(df, TEAMNAME):
    # チーム名指定でラインアウトデータ取得
    df = df.loc[(df['team_id'] == TEAMNAME)]

    dfaction = df.loc[df['action'] == 'Lineout Throw']
    b = pd.crosstab([dfaction['qualifier3'], dfaction['Actionresult']],
                    dfaction['ActionType'], margins=True)
    b = b.reindex(columns=['Throw Front', 'Throw Middle',
                  'Throw Back', 'Throw 15m+'])

    plt.gcf().subplots_adjust(wspace=4)
    fig = sns.heatmap(b, cmap='Blues', annot=True, annot_kws={'size': 20})
    st.pyplot(fig)


def ruck_speed(df, TEAMNAME):
    dfaction = df.loc[df['team_id'] == TEAMNAME]
    dfaction = dfaction.loc[dfaction['action'] == 'Ruck']
    rspeed = ['0-1 Seconds', '1-2 Seconds', '2-3 Seconds', '3-4 Seconds',
              '4-5 Seconds', '5-6 Seconds', '6+ Seconds', 'N/A Ruck Speed']
    cl = ['y', 'm', 'c', 'r', 'g', 'b', (0, 0.3, 0.5), (0, 0, 0)]
    fig = plt.figure(figsize=(7, 10))
    ax = fig.add_subplot(1, 1, 1)
    plt.xlim(0, 68)
    plt.ylim(0, 100)

    a = pd.crosstab(dfaction['action'], dfaction['qualifier4'])
    a = a.reindex(columns=rspeed).fillna(0).astype(int)
    # 背景画像の設定
    fig.patch.set_facecolor('white')
    im = Image.open(os.path.abspath('./data/Field_image.jpeg'))
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    plt.imshow(im, extent=[*xlim, *ylim], aspect='auto', alpha=0.6)

    for i in range(len(rspeed)):
        r = dfaction.loc[dfaction['qualifier4'] == rspeed[i]]
        plt.scatter(r['y_coord'], r["x_coord"], label=rspeed[i],
                    marker='D', color=cl[i], s=150)

    # ラベルの表示
    lgd = plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
    OPPONENT = get_opponent(df, TEAMNAME)
    plt.title(TEAMNAME + " Ruck (" + TEAMNAME + " vs " + OPPONENT + ")")
    plt.gcf().subplots_adjust(wspace=4)
    st.pyplot(fig)


def get_opponent(df, TEAMNAME):
    opp = df.loc[df['team_id'] != TEAMNAME].reset_index(drop=True).team_id[0]
    return opp


def kick(df, TEAMNAME):
    # Kickが入力された場合の処理-----
    dfaction = df.loc[(df['team_id'] == TEAMNAME)]
    dfaction = dfaction.loc[dfaction['action'] == 'Kick']
    kicktypes = ['Bomb', 'Chip', 'Cross Pitch', 'Territorial',
                 'Low', 'Box', 'Touch Kick', 'Kick Error']
    kicks = dfaction.loc[(dfaction['qualifier3'] == 'Kick in Play') | (
        dfaction['qualifier3'] == 'Kick in Play (Own 22)')]

    cl = ['y', 'm', 'c', 'r', 'g', 'b', (0, 0.3, 0.5), (0, 0, 0)]
    fig = plt.figure(figsize=(7, 10))
    ax = fig.add_subplot(1, 1, 1)
    plt.xlim(0, 70)
    plt.ylim(0, 100)

    print(kicks[['PLID', 'MatchTime', 'ActionType', 'Actionresult']])
    for i in range(len(kicktypes)):
        plts = kicks.loc[kicks['ActionType'] == kicktypes[i]]
        plt.quiver(plts['y_coord'], plts["x_coord"], (plts['y_coord_end']-plts['y_coord']), (plts["x_coord_end"]-plts['x_coord']), angles="xy",
                   scale_units='xy', label=kicktypes[i], color=cl[i], scale=1, width=0.008, headwidth=5, headlength=8, headaxislength=7, pivot='tail')
    # Kickの処理ここまで------

    # 背景画像の設定
    fig.patch.set_facecolor('white')
    im = Image.open(os.path.abspath('./data/Field_image.jpeg'))
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    plt.imshow(im, extent=[*xlim, *ylim], aspect='auto', alpha=0.6)

    # ラベルの表示
    lgd = plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
    plt.title(TEAMNAME)
    plt.gcf().subplots_adjust(wspace=4)
    plt.show()

    # 表を出力
    player_kicks = pd.crosstab(
        [kicks['PLID'], kicks['ActionType']], kicks['Actionresult'])
    st.pyplot(fig)
