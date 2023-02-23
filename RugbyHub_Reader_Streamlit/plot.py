from PIL import Image
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import os


class Plot_method(df, team_id):

    def get_opponent(self, team_id):
        opp = self.df.loc[self.df['team_id'] !=
                          team_id].reset_index(drop=True).team_id[0]
        return opp

    def plot_by_action(self, action, team_id):
        self.dfaction = self.df.loc[(self.df['action'] == action) & (
            self.df['team_id'] == team_id)]
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
        plt.scatter(self.dfaction['x_coord'],
                    self.dfaction['y_coord'], marker='D', s=150)
        # ラベルの表示
        lgd = plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
        plt.gcf().subplots_adjust(wspace=4)
        st.pyplot(fig)

    def lineout(self):
        # チーム名指定でラインアウトデータ取得
        fig = plt.figure()
        self.df = self.df.loc[(self.df['team_id'] == self.team_id)]

        self.dfaction = self.df.loc[self.df['action'] == 'Lineout Throw']
        b = pd.crosstab([self.dfaction['qualifier3'], self.dfaction['Actionresult']],
                        self.dfaction['ActionType'], margins=True)
        b = b.reindex(columns=['Throw Front', 'Throw Middle',
                               'Throw Back', 'Throw 15m+'])

        plt.gcf().subplots_adjust(wspace=4)
        sns.heatmap(b, cmap='Blues', annot=True, annot_kws={'size': 20})
        st.pyplot(fig)

    def ruck_speed(self):
        self.dfaction = self.df.loc[self.df['team_id'] == self.team_id]
        self.dfaction = self.dfaction.loc[self.dfaction['action'] == 'Ruck']
        rspeed = ['0-1 Seconds', '1-2 Seconds', '2-3 Seconds', '3-4 Seconds',
                  '4-5 Seconds', '5-6 Seconds', '6+ Seconds', 'N/A Ruck Speed']
        cl = ['y', 'm', 'c', 'r', 'g', 'b', (0, 0.3, 0.5), (0, 0, 0)]
        fig = plt.figure(figsize=(7, 10))
        ax = fig.add_subplot(1, 1, 1)
        plt.xlim(0, 68)
        plt.ylim(0, 100)

        a = pd.crosstab(self.dfaction['action'], self.dfaction['qualifier4'])
        a = a.reindex(columns=rspeed).fillna(0).astype(int)
        # 背景画像の設定
        fig.patch.set_facecolor('white')
        im = Image.open(os.path.abspath('./data/Field_image.jpeg'))
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        plt.imshow(im, extent=[*xlim, *ylim], aspect='auto', alpha=0.6)

        for i in range(len(rspeed)):
            r = self.dfaction.loc[self.dfaction['qualifier4'] == rspeed[i]]
            plt.scatter(r['y_coord'], r["x_coord"], label=rspeed[i],
                        marker='D', color=cl[i], s=150)

        # ラベルの表示
        lgd = plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=12)
        OPPONENT = get_opponent(self.team_id)
        plt.title(self.team_id + " Ruck (" +
                  self.team_id + " vs " + OPPONENT + ")")
        plt.gcf().subplots_adjust(wspace=4)
        st.pyplot(fig)

    def kick(self):
        # Kickが入力された場合の処理-----
        self.dfaction = self.df.loc[(self.df['team_id'] == self.team_id)]
        self.dfaction = self.dfaction.loc[self.dfaction['action'] == 'Kick']
        kicktypes = ['Bomb', 'Chip', 'Cross Pitch', 'Territorial',
                     'Low', 'Box', 'Touch Kick', 'Kick Error']
        kicks = self.dfaction.loc[(self.dfaction['qualifier3'] == 'Kick in Play') | (
            self.dfaction['qualifier3'] == 'Kick in Play (Own 22)')]

        cl = ['y', 'm', 'c', 'r', 'g', 'b', (0, 0.3, 0.5), (0, 0, 0)]
        fig = plt.figure(figsize=(7, 10))
        ax = fig.add_subplot(1, 1, 1)
        plt.xlim(0, 70)
        plt.ylim(0, 100)

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
        plt.title(self.team_id)
        plt.gcf().subplots_adjust(wspace=4)
        plt.show()

        # 表を出力
        player_kicks = pd.crosstab(
            [kicks['PLID'], kicks['ActionType']], kicks['Actionresult'])
        st.pyplot(fig)
