import xml.etree.ElementTree as ET
import pandas as pd
import os

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
    df.PLID = df.PLID.map(plid.set_index('players_id').player_known_name)
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
