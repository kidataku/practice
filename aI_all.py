# AI_all 競馬予測用プログラムをすべてまとめてここに
# TODO Output.moto()の実行 fuku@ayなおすため
#

# ①ライブラリの読み込み
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import numpy as np
import datetime
import time
import os
import itertools
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn
import lightgbm as lgb
from sklearn.model_selection import train_test_split
import category_encoders as ce
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# ②元データclass⇒特徴量作成用の元データを作る。Rstan用データ機能もここに。
# region 元データclass
class Output:
    @staticmethod
    def moto():
        """
        特徴量作成用の元データを作成する関数
        Parameters:
        -----------

        Returns:
        -----------
        moto_df : pandas.DataFrame
            特徴量作成用に様々な元データをひとまとめにしたもの
        """
        start = time.time()
        # 元データをpostgreから取得---------------------------------------------------------------------
        # DBの初期設定
        DATABASE = 'postgresql'
        USER = 'postgres'
        PASSWORD = 'taku0703'
        HOST = 'localhost'
        PORT = '5432'
        DB_NAME = 'everydb2'
        CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする
        # postgreからpandasに出力するデータを指定するSQL
        sql1 = "SELECT * FROM public.n_uma;"  # 実行SQL 競走馬マスタ
        sql2 = "SELECT * FROM public.n_uma_race;"  # 実行SQL 馬毎レース情報
        sql3 = "SELECT * FROM public.n_race;"  # 実行SQL レース詳細
        sql4 = "SELECT * FROM public.n_harai;"  # 実行SQL 払い戻し
        sqlodds = "SELECT year,monthday,jyocd,kaiji,nichiji,racenum,happyotime,umaban,tanodds,tanninki FROM public.n_jodds_tanpuku WHERE year='2020' AND jyocd='10';"  # 実行SQL 払い戻し
        # DBのデータをpandasで取得
        n_uma_pro = pd.read_sql(sql1, conn)  # sql:実行したいsql，conn:対象のdb名
        n_uma_race = pd.read_sql(sql2, conn)  # sql:実行したいsql，conn:対象のdb名
        n_race = pd.read_sql(sql3, conn)  # sql:実行したいsql，conn:対象のdb名
        n_harai = pd.read_sql(sql4, conn)  # sql:実行したいsql，conn:対象のdb名
        n_tanodds = pd.read_sql(sqlodds, conn)  # sql:実行したいsql，conn:対象のdb名
        ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる
        # データのmergeなど---------------------------------------------------------------------------------
        # 元データ(n_uma_race,n_race,n_harai,n_uma_pro)から必要なものだけ抽出
        # n_uma_race
        # データを2010年～2020年の11年分のデータにフィルタリングする
        n_uma_race['year'] = n_uma_race['year'].astype(int)
        n_uma_race = n_uma_race[(2010 <= n_uma_race['year']) & (n_uma_race['year'] <= 2020)]
        n_uma_race['year'] = n_uma_race['year'].astype(str)
        matome_data = n_uma_race.loc[:,['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'wakuban', 'umaban', 'kettonum', 'bamei', 'sexcd', 'barei', 'tozaicd', 'futan',
                                        'chokyosiryakusyo', 'banusiname', 'kisyuryakusyo', 'bataijyu', 'zogenfugo', 'zogensa', 'ijyocd', 'time', 'kakuteijyuni',
                                        'chakusacd', 'jyuni1c', 'jyuni2c', 'jyuni3c', 'jyuni4c', 'odds', 'ninki', 'honsyokin', 'harontimel3', 'kettonum1', 'bamei1', 'timediff', 'kyakusitukubun']]
        matome_data['ID'] = n_uma_race['year'] + n_uma_race['monthday'] + n_uma_race['jyocd'] + n_uma_race['kaiji'] + n_uma_race['nichiji'] + n_uma_race['racenum']  # レースIDを追加
        # レース順で並べ替え
        matome_data['tuika'] = matome_data['ID'] + matome_data['umaban']
        matome_data = matome_data.sort_values('tuika')  # 昇順で並べ替え
        matome_data = matome_data.reset_index(drop=True)  # index振りなおす
        matome_data = matome_data.drop(columns=['tuika'])  # いらん列削除で並べ替え完了
        # n_race　追加データ(くっつけられる方)
        matomerare_race = n_race.loc[:,
                   ['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'gradecd', 'syubetucd','jyokencd1', 'jyokencd2', 'jyokencd3', 'jyokencd4',
                    'jyokencd5', 'kyori', 'trackcd', 'tenkocd', 'sibababacd', 'dirtbabacd', 'kigocd', 'laptime1', 'laptime2', 'laptime3',
                    'laptime4', 'laptime5', 'laptime6', 'laptime7', 'laptime8', 'laptime9', 'laptime10', 'laptime11',
                    'laptime12', 'laptime13', 'laptime14', 'laptime15', 'laptime16', 'laptime17', 'laptime18', 'hassotime', 'syussotosu', 'corner1', 'syukaisu1',
                    'jyuni1', 'corner2', 'syukaisu2', 'jyuni2', 'corner3', 'syukaisu3', 'jyuni3', 'corner4', 'syukaisu4', 'jyuni4', 'ryakusyo6']]
        matomerare_race['ID'] = n_race['year'] + n_race['monthday'] + n_race['jyocd'] + n_race['kaiji'] + n_race['nichiji'] + n_race['racenum']  # レースIDを追加
        # n_harai　追加データ(くっつけられる方)
        n_harai_matome = n_harai.loc[:,
                     ['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'paytansyoumaban1', 'paytansyopay1',
                      'paytansyoumaban2', 'paytansyopay2', 'paytansyoumaban3', 'paytansyopay3', 'payfukusyoumaban1','payfukusyopay1',
                      'payfukusyoumaban2', 'payfukusyopay2', 'payfukusyoumaban3', 'payfukusyopay3', 'payfukusyoumaban4',
                      'payfukusyopay4', 'payfukusyoumaban5', 'payfukusyopay5', ]]
        n_harai_matome['ID'] = n_harai['year'] + n_harai['monthday'] + n_harai['jyocd'] + n_harai['kaiji'] + n_harai['nichiji'] + n_harai['racenum']  # レースIDの作成
        # n_uma_pro　追加データ(くっつけられる方)
        n_uma_pro_matome = n_uma_pro.loc[:,['bamei', 'ketto3infobamei1']]
        # データをlistにして高速化---------------------------------------------------------------------------------
        matome_data_list = list(matome_data['ID'])  # レースIDをlistで取得
        matome_bamei_list = list(matome_data['bamei'])  # レースIDをlistで取得
        matomerare_race_list = list(matomerare_race['ID'])  # レースIDをlistで取得
        n_harai_matome_list = list(n_harai_matome['ID'])  # レースIDをlistで取得
        matomerare_bamei_list = list(n_uma_pro_matome['bamei'])  # レースIDをlistで取得
        # race
        gradecd_list = list(matomerare_race['gradecd'])
        syubetu_list = list(matomerare_race['syubetucd'])
        jyokencd1_list = list(matomerare_race['jyokencd1'])
        jyokencd2_list = list(matomerare_race['jyokencd2'])
        jyokencd3_list = list(matomerare_race['jyokencd3'])
        jyokencd4_list = list(matomerare_race['jyokencd4'])
        jyokencd5_list = list(matomerare_race['jyokencd5'])
        kyori_list = list(matomerare_race['kyori'])
        trackcd_list = list(matomerare_race['trackcd'])
        tenkocd_list = list(matomerare_race['tenkocd'])
        sibababacd_list = list(matomerare_race['sibababacd'])
        dirtbabacd_list = list(matomerare_race['dirtbabacd'])
        kigocd_list = list(matomerare_race['kigocd'])
        fathername_list = list(n_uma_pro_matome['ketto3infobamei1'])
        lap1_list = list(matomerare_race['laptime1'])
        lap2_list = list(matomerare_race['laptime2'])
        lap3_list = list(matomerare_race['laptime3'])
        lap4_list = list(matomerare_race['laptime4'])
        lap5_list = list(matomerare_race['laptime5'])
        lap6_list = list(matomerare_race['laptime6'])
        lap7_list = list(matomerare_race['laptime7'])
        lap8_list = list(matomerare_race['laptime8'])
        lap9_list = list(matomerare_race['laptime9'])
        lap10_list = list(matomerare_race['laptime10'])
        lap11_list = list(matomerare_race['laptime11'])
        lap12_list = list(matomerare_race['laptime12'])
        lap13_list = list(matomerare_race['laptime13'])
        lap14_list = list(matomerare_race['laptime14'])
        lap15_list = list(matomerare_race['laptime15'])
        lap16_list = list(matomerare_race['laptime16'])
        lap17_list = list(matomerare_race['laptime17'])
        lap18_list = list(matomerare_race['laptime18'])
        hassotime_list = list(matomerare_race['hassotime'])
        syussotosu_list = list(matomerare_race['syussotosu'])
        corner1_list = list(matomerare_race['corner1'])
        syukaisu1_list = list(matomerare_race['syukaisu1'])
        jyuni1_list = list(matomerare_race['jyuni1'])
        corner2_list = list(matomerare_race['corner2'])
        syukaisu2_list = list(matomerare_race['syukaisu2'])
        jyuni2_list = list(matomerare_race['jyuni2'])
        corner3_list = list(matomerare_race['corner3'])
        syukaisu3_list = list(matomerare_race['syukaisu3'])
        jyuni3_list = list(matomerare_race['jyuni3'])
        corner4_list = list(matomerare_race['corner4'])
        syukaisu4_list = list(matomerare_race['syukaisu4'])
        jyuni4_list = list(matomerare_race['jyuni4'])
        ryakusyo6_list = list(matomerare_race['ryakusyo6'])
        # harai
        n_harai_matome_tanuma1 = list(n_harai_matome['paytansyoumaban1'])  # レースIDをlistで取得
        n_harai_matome_tanpay1 = list(n_harai_matome['paytansyopay1'])  # レースIDをlistで取得
        n_harai_matome_tanuma2 = list(n_harai_matome['paytansyoumaban2'])  # レースIDをlistで取得
        n_harai_matome_tanpay2 = list(n_harai_matome['paytansyopay2'])  # レースIDをlistで取得
        n_harai_matome_tanuma3 = list(n_harai_matome['paytansyoumaban3'])  # レースIDをlistで取得
        n_harai_matome_tanpay3 = list(n_harai_matome['paytansyopay3'])  # レースIDをlistで取得
        n_harai_matome_uma1 = list(n_harai_matome['payfukusyoumaban1'])  # レースIDをlistで取得
        n_harai_matome_pay1 = list(n_harai_matome['payfukusyopay1'])  # レースIDをlistで取得
        n_harai_matome_uma2 = list(n_harai_matome['payfukusyoumaban2'])  # レースIDをlistで取得
        n_harai_matome_pay2 = list(n_harai_matome['payfukusyopay2'])  # レースIDをlistで取得
        n_harai_matome_uma3 = list(n_harai_matome['payfukusyoumaban3'])  # レースIDをlistで取得
        n_harai_matome_pay3 = list(n_harai_matome['payfukusyopay3'])  # レースIDをlistで取得
        n_harai_matome_uma4 = list(n_harai_matome['payfukusyoumaban4'])  # レースIDをlistで取得
        n_harai_matome_pay4 = list(n_harai_matome['payfukusyopay4'])  # レースIDをlistで取得
        n_harai_matome_uma5 = list(n_harai_matome['payfukusyoumaban5'])  # レースIDをlistで取得
        n_harai_matome_pay5 = list(n_harai_matome['payfukusyopay5'])  # レースIDをlistで取得
        # データをmerge---------------------------------------------------------------------------------
        # raceデータをlistに格納し高速化
        a_gradecd, a_syubetu, a_jyokencd1, a_jyokencd2, a_jyokencd3, a_jyokencd4, a_jyokencd5, a_kyori, a_trackcd, a_tenkocd, a_sibababacd, a_dirtbabacd, a_kigocd, a_father = \
            [], [], [], [], [], [], [], [], [], [], [], [], [], []
        # raceデータをlistに格納し高速化
        a_lap1, a_lap2, a_lap3, a_lap4, a_lap5, a_lap6, a_lap7, a_lap8, a_lap9, a_lap10, a_lap11, a_lap12, a_lap13, a_lap14, a_lap15, a_lap16, a_lap17, a_lap18 = \
            [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
        # raceデータをlistに格納し高速化
        a_hasso, a_syussou, a_corner1, a_syukaisu1, a_jyuni1, a_corner2, a_syukaisu2, a_jyuni2, a_corner3, a_syukaisu3, a_jyuni3, a_corner4, a_syukaisu4, a_jyuni4, a_ryakusyo6 = \
            [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
        # haraiデータをlistに格納し高速化
        a_tanuma1, a_tanpay1, a_tanuma2, a_tanpay2, a_tanuma3, a_tanpay3 = [], [], [], [], [], []
        a_uma1, a_pay1, a_uma2, a_pay2, a_uma3, a_pay3, a_uma4, a_pay4, a_uma5, a_pay5 = [], [], [], [], [], [], [], [], [], []
        # 行番号を探す関数を定義
        def my_index(l, x, default=np.nan):
            if x in l:  # Lにxがあれば
                return l.index(x)  # 一致するデータがあるときはindexを返す
            else:
                return default  # ないときはNaNを返す
        # for文でデータを抽出
        for i in range(len(matome_data)):
        # for i in range(50000):
            if i % 100000 == 0:
                print(i)
            idx_race = my_index(matomerare_race_list, matome_data_list[i])  # 行番号を取得 matome_data_list⇒n_uma_race,matomerare_race_list⇒n_race　IDで検索
            idx_father = my_index(matomerare_bamei_list, matome_bamei_list[i])  # 行番号を取得 matome_bamei_list⇒n_uma_race,matomerare_bamei_list⇒n_uma_pro 馬名で検索
            idx_harai = my_index(n_harai_matome_list, matome_data_list[i])  # 行番号を取得 matome_data_list⇒n_uma_race,n_harai_matome_list⇒n_harai　IDで検索
            # race
            if np.isnan(idx_race):  # NaNならTrue can't find the index
                moji_str01 = moji_str02 = moji_str03 = moji_str04 = moji_str05 = moji_str06 = moji_str07 = moji_str08 = moji_str09 = moji_str10 = moji_str11 = moji_str12\
                    = moji_str13 = moji_str15 = moji_str16 = moji_str17 = moji_str18 = moji_str19 = moji_str20 = moji_str21 = moji_str22 = moji_str23= moji_str24 \
                    = moji_str25 = moji_str26 = moji_str27 = moji_str28 = moji_str29 = moji_str30 = moji_str31 = moji_str32 = moji_str33 = moji_str34 = moji_str35 = moji_str36 = moji_str37\
                    = moji_str38 = moji_str39 = moji_str40 = moji_str41 = moji_str42 = moji_str43 = moji_str44 = moji_str45 = moji_str46 = moji_str47 = np.nan
            else:
                moji_str01 = gradecd_list[idx_race]
                moji_str02 = syubetu_list[idx_race]
                moji_str03 = jyokencd1_list[idx_race]
                moji_str04 = jyokencd2_list[idx_race]
                moji_str05 = jyokencd3_list[idx_race]
                moji_str06 = jyokencd4_list[idx_race]
                moji_str07 = jyokencd5_list[idx_race]
                moji_str08 = kyori_list[idx_race]
                moji_str09 = trackcd_list[idx_race]
                moji_str10 = tenkocd_list[idx_race]
                moji_str11 = sibababacd_list[idx_race]
                moji_str12 = dirtbabacd_list[idx_race]
                moji_str13 = kigocd_list[idx_race]

                moji_str15 = lap1_list[idx_race]
                moji_str16 = lap2_list[idx_race]
                moji_str17 = lap3_list[idx_race]
                moji_str18 = lap4_list[idx_race]
                moji_str19 = lap5_list[idx_race]
                moji_str20 = lap6_list[idx_race]
                moji_str21 = lap7_list[idx_race]
                moji_str22 = lap8_list[idx_race]
                moji_str23 = lap9_list[idx_race]
                moji_str24 = lap10_list[idx_race]
                moji_str25 = lap11_list[idx_race]
                moji_str26 = lap12_list[idx_race]
                moji_str27 = lap13_list[idx_race]
                moji_str28 = lap14_list[idx_race]
                moji_str29 = lap15_list[idx_race]
                moji_str30 = lap16_list[idx_race]
                moji_str31 = lap17_list[idx_race]
                moji_str32 = lap18_list[idx_race]
                moji_str33 = hassotime_list[idx_race]
                moji_str34 = syussotosu_list[idx_race]
                moji_str35 = corner1_list[idx_race]
                moji_str36 = syukaisu1_list[idx_race]
                moji_str37 = jyuni1_list[idx_race]
                moji_str38 = corner2_list[idx_race]
                moji_str39 = syukaisu2_list[idx_race]
                moji_str40 = jyuni2_list[idx_race]
                moji_str41 = corner3_list[idx_race]
                moji_str42 = syukaisu3_list[idx_race]
                moji_str43 = jyuni3_list[idx_race]
                moji_str44 = corner4_list[idx_race]
                moji_str45 = syukaisu4_list[idx_race]
                moji_str46 = jyuni4_list[idx_race]
                moji_str47 = ryakusyo6_list[idx_race]
            # 父親の馬名
            if np.isnan(idx_father):  # NaNならTrue can't find the index
                moji_str14 = np.nan
            else:
                moji_str14 = fathername_list[idx_father]
            # 払い戻し
            if np.isnan(idx_harai):  # NaNならTrue can't find the index
                moji_str48 = moji_str49 = moji_str50 = moji_str51 = moji_str52 = moji_str53 \
                    = moji_str54 = moji_str55 = moji_str56 = moji_str57 = moji_str58 = moji_str59 = moji_str60 = moji_str61 = moji_str62 = moji_str63 = np.nan
            else:
                moji_str48 = n_harai_matome_tanuma1[idx_harai]
                moji_str49 = n_harai_matome_tanpay1[idx_harai]
                moji_str50 = n_harai_matome_tanuma2[idx_harai]
                moji_str51 = n_harai_matome_tanpay2[idx_harai]
                moji_str52 = n_harai_matome_tanuma3[idx_harai]
                moji_str53 = n_harai_matome_tanpay3[idx_harai]
                moji_str54 = n_harai_matome_uma1[idx_harai]
                moji_str55 = n_harai_matome_pay1[idx_harai]
                moji_str56 = n_harai_matome_uma2[idx_harai]
                moji_str57 = n_harai_matome_pay2[idx_harai]
                moji_str58 = n_harai_matome_uma3[idx_harai]
                moji_str59 = n_harai_matome_pay3[idx_harai]
                moji_str60 = n_harai_matome_uma4[idx_harai]
                moji_str61 = n_harai_matome_pay4[idx_harai]
                moji_str62 = n_harai_matome_uma5[idx_harai]
                moji_str63 = n_harai_matome_pay5[idx_harai]

            # データをどういれるか
            a_gradecd += [moji_str01]
            a_syubetu += [moji_str02]
            a_jyokencd1 += [moji_str03]
            a_jyokencd2 += [moji_str04]
            a_jyokencd3 += [moji_str05]
            a_jyokencd4 += [moji_str06]
            a_jyokencd5 += [moji_str07]
            a_kyori += [moji_str08]
            a_trackcd += [moji_str09]
            a_tenkocd += [moji_str10]
            a_sibababacd += [moji_str11]
            a_dirtbabacd += [moji_str12]
            a_kigocd += [moji_str13]
            a_father += [moji_str14]
            a_lap1 += [moji_str15]
            a_lap2 += [moji_str16]
            a_lap3 += [moji_str17]
            a_lap4 += [moji_str18]
            a_lap5 += [moji_str19]
            a_lap6 += [moji_str20]
            a_lap7 += [moji_str21]
            a_lap8 += [moji_str22]
            a_lap9 += [moji_str23]
            a_lap10 += [moji_str24]
            a_lap11 += [moji_str25]
            a_lap12 += [moji_str26]
            a_lap13 += [moji_str27]
            a_lap14 += [moji_str28]
            a_lap15 += [moji_str29]
            a_lap16 += [moji_str30]
            a_lap17 += [moji_str31]
            a_lap18 += [moji_str32]
            a_hasso += [moji_str33]
            a_syussou += [moji_str34]
            a_corner1 += [moji_str35]
            a_syukaisu1 += [moji_str36]
            a_jyuni1 += [moji_str37]
            a_corner2 += [moji_str38]
            a_syukaisu2 += [moji_str39]
            a_jyuni2 += [moji_str40]
            a_corner3 += [moji_str41]
            a_syukaisu3 += [moji_str42]
            a_jyuni3 += [moji_str43]
            a_corner4 += [moji_str44]
            a_syukaisu4 += [moji_str45]
            a_jyuni4 += [moji_str46]
            a_ryakusyo6 += [moji_str47]
            a_tanuma1 += [moji_str48]
            a_tanpay1 += [moji_str49]
            a_tanuma2 += [moji_str50]
            a_tanpay2 += [moji_str51]
            a_tanuma3 += [moji_str52]
            a_tanpay3 += [moji_str53]
            a_uma1 += [moji_str54]
            a_pay1 += [moji_str55]
            a_uma2 += [moji_str56]
            a_pay2 += [moji_str57]
            a_uma3 += [moji_str58]
            a_pay3 += [moji_str59]
            a_uma4 += [moji_str60]
            a_pay4 += [moji_str61]
            a_uma5 += [moji_str62]
            a_pay5 += [moji_str63]
        # データの結合
        merge = pd.DataFrame(
            data={'gradecd': a_gradecd, 'syubetu': a_syubetu, 'jyokencd1': a_jyokencd1, 'jyokencd2': a_jyokencd2,
                  'jyokencd3': a_jyokencd3, 'jyokencd4': a_jyokencd4, 'jyokencd5': a_jyokencd5, 'kyori': a_kyori, 'trackcd': a_trackcd,
                  'tenkocd': a_tenkocd, 'sibababacd': a_sibababacd, 'dirtbabacd': a_dirtbabacd, 'kigocd': a_kigocd, 'father': a_father,
                  'lap1': a_lap1, 'lap2': a_lap2, 'lap3': a_lap3, 'lap4': a_lap4, 'lap5': a_lap5,
                  'lap6': a_lap6, 'lap7': a_lap7, 'lap8': a_lap8, 'lap9': a_lap9, 'lap10': a_lap10, 'lap11': a_lap11,
                  'lap12': a_lap12, 'lap13': a_lap13, 'lap14': a_lap14, 'lap15': a_lap15, 'lap16': a_lap16, 'lap17': a_lap17,
                  'lap18': a_lap18, 'hasso': a_hasso, 'syussou': a_syussou, 'corner1': a_corner1, 'syukaisu1': a_syukaisu1, 'jyuni1': a_jyuni1,
                  'corner2': a_corner2, 'syukaisu2': a_syukaisu2, 'jyuni2': a_jyuni2, 'corner3': a_corner3, 'syukaisu3': a_syukaisu3, 'jyuni3': a_jyuni3,
                  'corner4': a_corner4, 'syukaisu4': a_syukaisu4, 'jyuni4': a_jyuni4, 'ryakusyo6': a_ryakusyo6, 'tanuma1': a_tanuma1, 'tanpay1': a_tanpay1,
                  'tanuma2': a_tanuma2, 'tanpay2': a_tanpay2, 'tanuma3': a_tanuma3, 'tanpay3': a_tanpay3, 'fukuuma1': a_uma1, 'fukupay1': a_pay1,
                  'fukuuma2': a_uma2, 'fukupay2': a_pay2, 'fukuuma3': a_uma3, 'fukupay3': a_pay3, 'fukuuma4': a_uma4, 'fukupay4': a_pay4, 'fukuuma5': a_uma5, 'fukupay5': a_pay5},
            columns=['gradecd', 'syubetu', 'jyokencd1', 'jyokencd2', 'jyokencd3', 'jyokencd4', 'jyokencd5', 'kyori', 'trackcd',
                     'tenkocd', 'sibababacd', 'dirtbabacd', 'kigocd', 'father', 'lap1', 'lap2', 'lap3', 'lap4',
                     'lap5', 'lap6', 'lap7', 'lap8', 'lap9', 'lap10', 'lap11', 'lap12', 'lap13', 'lap14', 'lap15', 'lap16', 'lap17', 'lap18',
                     'hasso', 'syussou', 'corner1', 'syukaisu1', 'jyuni1', 'corner2', 'syukaisu2', 'jyuni2', 'corner3', 'syukaisu3', 'jyuni3',
                     'corner4', 'syukaisu4', 'jyuni4', 'ryakusyo6', 'tanuma1', 'tanpay1', 'tanuma2', 'tanpay2', 'tanuma3', 'tanpay3',
                     'fukuuma1', 'fukupay1', 'fukuuma2', 'fukupay2', 'fukuuma3', 'fukupay3', 'fukuuma4', 'fukupay4', 'fukuuma5', 'fukupay5'])

        saigo = pd.concat([matome_data, merge], axis=1)  # 水平結合
        saigo = saigo.reset_index() # index与える

        # 5分前データ結合処理 36min------------------------------------------
        a_index, a_happyotime, a_umaban, a_tanodds, a_tanninki = [], [], [], [], []
        # saigo=hoge1
        # saigo_1 = saigo.loc[:, ['index', 'year', 'monthday', 'jyocd', 'ID', 'hasso']]
        saigo_1 = saigo.loc[:, ['index', 'year', 'monthday', 'jyocd', 'ID', 'hasso']]
        saigo_1['hassotime'] = saigo_1['monthday'] + saigo_1['hasso']
        for year in range(2010, 2021):  # 2010-2020年まで
            print(year)
            for jyocd in range(1, 11):
                if jyocd == 10:
                    jyocd = str(jyocd)
                else:
                    jyocd = '0' + str(jyocd)
                print(jyocd)
                SQL = "SELECT year,monthday,jyocd,kaiji,nichiji,racenum,happyotime,umaban,tanodds,tanninki FROM public.n_jodds_tanpuku WHERE year='{0}' AND jyocd='{1}';".format(year, jyocd)
                conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
                cursor = conn.cursor()  # データベースを操作できるようにする
                # postgreからpandasに出力するデータを指定するSQL
                # DBのデータをpandasで取得
                n_tanodds = pd.read_sql(SQL, conn)  # sql:実行したいsql，conn:対象のdb名
                ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
                cursor.close()  # データベースの操作を終了する
                conn.commit()  # 変更をデータベースに保存
                conn.close()  # データベースを閉じる
                # データ抽出------------------------------------------
                n_tanodds['ID'] = n_tanodds['year'] + n_tanodds['monthday'] + n_tanodds['jyocd'] + n_tanodds['kaiji'] + n_tanodds['nichiji'] + n_tanodds['racenum']  # レースIDを追加
                saigo_2 = saigo_1[((saigo_1['year'] == str(year)) & (saigo_1['jyocd'] == jyocd))]  # 元データ抜き出し
                # IDで検索
                ID_all = saigo_2["ID"].unique()
                for IDnum in range(len(ID_all)):
                    ID_moto = ID_all[IDnum]
                    # IDで抽出
                    n_tanodds_1 = n_tanodds[n_tanodds['ID'] == ID_moto]
                    if len(n_tanodds_1) > 1:  # オッズデータあるとき　
                        # 時間で抽出
                        saigo_3 = saigo_2[saigo_2['ID'] == ID_moto]
                        n_tanodds_1['happyotime'] = n_tanodds_1['happyotime'].astype(int)
                        if type(saigo_3['hassotime'].unique()[0]) == str:  # オッズデータあるとき　
                            n_tanodds_2 = n_tanodds_1[n_tanodds_1['happyotime'] < int(saigo_3['hassotime'].unique())]  # 発走時間5分以前の単勝オッズ
                            kakuteimaeodds_gun = n_tanodds_2['happyotime'].unique()
                            kakuteimaeodds = kakuteimaeodds_gun[len(kakuteimaeodds_gun) - 1]
                            n_tanodds_3 = n_tanodds_2[n_tanodds_2['happyotime'] == kakuteimaeodds]
                            list_index = list(saigo_3['index'])
                            list_happyotime = list(n_tanodds_3['happyotime'])
                            list_umaban = list(n_tanodds_3['umaban'])
                            list_tanodds = list(n_tanodds_3['tanodds'])
                            list_tanninki = list(n_tanodds_3['tanninki'])
                            a_index += list_index
                            a_happyotime += list_happyotime
                            a_umaban += list_umaban
                            a_tanodds += list_tanodds
                            a_tanninki += list_tanninki
        # このリストを結合
        df_odds = pd.DataFrame({'index': a_index, 'happyotime': a_happyotime, 'a_umaban': a_umaban, 'tanodds': a_tanodds, 'tanninki': a_tanninki})
        df_odds = df_odds.sort_values('index')  # 昇順で並べ替え
        df_odds.index = df_odds['index']  # 列のindexデータを本当のindexにする
        data = pd.DataFrame(index=range(len(saigo)))  # 結合のために0～すべてのデータ元データを作成
        df_tempo = pd.concat([data, df_odds], axis=1)  # 結合のためのデータを作成
        df_last = pd.concat([saigo, df_tempo.loc[:, ['happyotime', 'a_umaban', 'tanodds', 'tanninki']]], axis=1)  # そして結合
        # DBへ出力
        # データpostgreへ
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする
        df_last.to_sql("df_moto", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
        # -------------実行ここまで
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる

        process_time = time.time() - start
        print(process_time / 60)  # 246
# endregion

# classの実行
# Output.moto()
# pickleファイルに
# pd.to_pickle(df_matome, "arr.pkl")#保存
# hoge = pd.read_pickle("arr.pkl") #読み出し

# ③-1：スピード指数class⇒スピード指数を作成する。
# region speed_index-1 class
class speed_index:
    @staticmethod
    def calclulate():
        """
        スピード指数を作成しDBに出力する関数
        Parameters:
        -----------

        Returns:
        -----------
        a_time1 : pandas.DataFrame
            スピード指数
        """
        start = time.time()
        # csv読み込み　データ準備
        # 距離書いただけのやつ読み込み　競馬場にどんな距離あるか示したもの 2010-2020で開催された距離のみ記載
        df_siba_1 = pd.read_csv('スピード指数 - 芝の距離書いただけのやつ.csv')
        df_dirt_1 = pd.read_csv('スピード指数 - ダートの距離書いただけのやつ.csv')
        # クラス指数　1勝クラス，2勝クラスとかで実力差を補正する指数
        class_1 = pd.read_csv('スピード指数 - クラス指数 - 簡易.csv')  # TODO 改善 クラスの差があまりでなくなってしまっている
        class3_1 = pd.read_csv('スピード指数 - クラス指数3歳 - 簡易.csv')  # TODO 改善
        # 距離指数　距離ごとに補正する指数　これは使っておらず自前で算出している
        # kyori_1=pd.read_csv('スピード指数 - 距離指数.csv')#https://team-d.club/about-speed-index/ このブログの距離指数を拝借したが使っていない。自分で算出したの使ってるがよいか再確認。
        # 元データをpostgreから取得---------------------------------------------------------------------
        # DBの初期設定
        DATABASE = 'postgresql'
        USER = 'postgres'
        PASSWORD = 'taku0703'
        HOST = 'localhost'
        PORT = '5432'
        DB_NAME = 'everydb2'
        CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする
        # postgreからpandasに出力するデータを指定するSQL
        sql_moto = 'SELECT * FROM public."df_moto" ORDER BY index ASC;'  # 実行SQL 払い戻し
        # DBのデータをpandasで取得
        a_time = pd.read_sql(sql_moto, conn)  # sql:実行したいsql，conn:対象のdb名
        ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる

        # データの前処理
        # 斤量を585⇒58.5みたいに直す
        def futan_henkan(x):
            return float(x[0:2] + '.' + x[2])

        # 走破時計を4桁の数字⇒秒になおす
        def henkan(x):
            if x[0] == '0':
                return float(x[1:3] + '.' + x[3])
            else:
                return 60 * int(x[0]) + float(x[1:3] + '.' + x[3])

        a_time = a_time.loc[:,
                 ['index', 'year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'bamei',
                  'futan', 'time', 'kakuteijyuni', 'ID', 'gradecd','syubetu','jyokencd1', 'jyokencd2', 'jyokencd3', 'jyokencd4', 'jyokencd5',
                  'kyori', 'trackcd', 'tenkocd', 'sibababacd', 'dirtbabacd', 'kigocd']]
        speed_data = a_time.copy()  # defaultはtrue copyにしないと参照渡しになって元データから変更になってしまう
        speed_data = speed_data.replace('', np.nan)  # 空をnanに置き換え
        speed_data['hiniti'] = speed_data['year'] + speed_data['monthday']  # 日にちデータの追加
        speed_data['futan_siyou'] = speed_data['futan'].apply(futan_henkan)
        speed_data['sectime'] = speed_data['time'].apply(henkan)
        speed_data['sectime'] = speed_data['sectime'].replace(0, np.nan)  # 走破時計0をNaNに置き換え
        speed_data['year'] = pd.to_numeric(speed_data["year"], errors='coerce')  # numericに型変換しつつ欠測があったらnanで埋める
        speed_data['kyori'] = pd.to_numeric(speed_data["kyori"], errors='coerce')  # numericに型変換しつつ欠測があったらnanで埋める 169161
        speed_data['jyocd'] = pd.to_numeric(speed_data["jyocd"], errors='coerce')  # numericに型変換しつつ欠測があったらnanで埋め
        speed_data = speed_data[speed_data['year'] >= 2010]  # 抽出　2010年～のデータ、バグデータの取り除き　892060 ⇒825827
        # ①基準タイムと距離指数の算出
        # 上記を算出するために元データとして天気：晴/曇り，馬場：良/稍，着順1～3着，条件：1～3勝クラス天気晴れのみのデータを抽出　825827⇒43429（36426 良だけだと）
        speed_data_hare = speed_data[((speed_data['tenkocd'] == '1') | (speed_data['tenkocd'] == '2')) & ((speed_data['sibababacd'] == '1') | (speed_data['dirtbabacd'] == '1') | (
                speed_data['sibababacd'] == '2') | (speed_data['dirtbabacd'] == '2')) & ((speed_data['kakuteijyuni'] == '01') | (speed_data['kakuteijyuni'] == '02') |
                (speed_data['kakuteijyuni'] == '03')) & ((speed_data['jyokencd5'] == '005') | (speed_data['jyokencd5'] == '010') | (speed_data['jyokencd5'] == '016'))]
        # 基準タイムと距離指数を格納する箱を作成　11年分を各年ごとに算出 芝72個、ダート56個
        today = datetime.date.today()
        year_range = today.year - 2010  # 何年分作成したいか
        kijyun_siba = [[] for torima in range(year_range)]  # 基準タイム用　芝
        kijyun_dirt = [[] for torima in range(year_range)]  # 基準タイム用　ダート
        kyori_siba = [[] for torima in range(year_range)]  # 距離指数用　芝
        kyori_dirt = [[] for torima in range(year_range)]  # 距離指数用　ダート
        count = 0  # 年度をカウントする用

        def cal_index(df_kyori_moto_D, df_moto_D, kyori_row_D, basyo_j_D, hajime_D, year_D):
            """
            スピード指数算出のための様々な指数を計算する(基準タイム，距離指数などなど)
            ----------
            Parameters
            df_kyori_moto_D(pandas):計算したい競馬場の距離参照用，df_moto_D(pandas):元データ。(speed_data_hareなど)，kyori_row_D(int):df_kyori_motoの知りたい行番号。
            basyo_j_D(int):競馬場コード，hajime_D(int):データ抽出の始まりのyear，year_D(int):データ抽出の終わりのyear
            -------
            Returns
            kijyun_t_D(float):基準タイム，kyori_s_D(float):距離指数
            """
            kyori_D = df_kyori_moto_D.iloc[kyori_row_D, basyo_j_D - 1]  # 対象コースでの距離が何mかを取得
            # 対象の距離，競馬場，集計年度の始まりの年，終わりの年より小さいデータを抽出2013なら2012
            syukei_D = df_moto_D[(df_moto_D['kyori'] == kyori_D) & (df_moto_D['jyocd'] == basyo_j_D) & (hajime_D <= df_moto_D['year']) & (df_moto_D['year'] < year_D)]  # データ抽出
            kijyun_t_D = round(np.nanmean(syukei_D['sectime']), 1)  # 基準タイムを計算
            kyori_s_D = round(1 / (10 * np.nanmean(syukei_D['sectime'])) * 1000, 2)  # 距離指数を算出　×10することで妥当になる　距離指数＝1/基準タイム　ここ妥当かなぞ
            return kijyun_t_D, kyori_s_D

        # for文で11年分の基準タイムと距離指数を作成していく　前年のデータを使用するので，2010年分は作成できない，2011年～
        for i in range(year_range):  # 2011-2021 11year　去年までの過去3年のデータを使用しデータを作成 元データは2010～2021の12年分
            year = 2011 + i  # i:0-10で2011～2021年の11年分 year年のデータを作成したい(year年より以前のデータを使用して)
            df_siba = df_siba_1.copy()  # 基準タイム芝用の元データをコピー
            df_dirt = df_dirt_1.copy()  # 基準タイムダート用の元データをコピー
            df_siba_kyori = df_siba_1.copy()  # 距離指数芝用の元データをコピー
            df_dirt_kyori = df_dirt_1.copy()  # 距離指数ダート用の元データをコピー
            # 過去の使用データについて年度ごとに場合分けを行う
            if year >= 2013:  # 2013年～は3年分の過去データを使用可能　2013年なら2010，2011，2012年の3年
                hajime = year - 3
            elif year == 2011:  # 2011年は2010年のみ
                hajime = year - 1
            else:  # 2012年は2010，2011年のみ
                hajime = year - 2
            # 競馬場ごとに基準タイムと距離指数を作成していく
            for j in range(1, 11):  # 競馬場コード　1-10
                for k in range(len(df_siba)):  # lenは行の大きさを取得　芝について基準タイムと距離指数を作成，格納
                    get = cal_index(df_siba, speed_data_hare, k, j, hajime, year)
                    df_siba.iloc[k, j - 1] = get[0]
                    df_siba_kyori.iloc[k, j - 1] = get[1]
                for k in range(len(df_dirt)):  # lenは行の大きさを取得　ダートについて基準タイムと距離指数を作成，格納
                    get = cal_index(df_dirt, speed_data_hare, k, j, hajime, year)
                    df_dirt.iloc[k, j - 1] = get[0]
                    df_dirt_kyori.iloc[k, j - 1] = get[1]
            # 年ごとに基準タイムを格納
            kijyun_siba[count] = df_siba  # 0に2011年のデータが入る（2010年のデータで作成したもの）。2011年のスピード指数算出したいときはこの基準タイムを使用する
            kijyun_dirt[count] = df_dirt  # 1に2012年のデータが入る（2010年～2011年のデータで作成したもの）
            # 年ごとに距離指数を格納
            kyori_siba[count] = df_siba_kyori  # 2に2013年のデータが入る（2010年～2012念のデータで作成したもの）
            kyori_dirt[count] = df_dirt_kyori  # 3に2014年のデータが入る（2011年～2013年のデータで作成したもの）
            count += 1

        # ②-①馬場指数の算出　日にち分発生する　距離が過去にないものだとエラーでる，中京芝3000とか
        sisuu_data = speed_data[speed_data['year'] >= 2011]  # 指数を出せるのは2011年のデータから。基準と距離指数が2011年分～しかないため。
        hiniti_data = sisuu_data['hiniti'].unique()  # 開催日時を取り出す
        spped_data_kakunou = []  # スピード指数格納用　芝
        index_kakunou = []  # スピード指数index格納用　ダート
        baba_kakunou_siba = []  # 芝馬場指数確認用
        baba_kakunou_dirt = []  # ダート馬場指数確認用
        for i in range(len(hiniti_data)):  # 開催日時ごとに指数を算出　開催日時でfor 10年で3369開催日あった i=2453で不良の秋天。
            siba_baba_hako = []  # 馬場指数格納用　芝
            dirt_baba_hako = []  # 馬場指数格納用　ダート
            hiniti_1 = hiniti_data[i]  # 日にちを1日取り出してその日の馬場指数を算出
            baba_index = sisuu_data[sisuu_data['hiniti'] == hiniti_1]  # 対象の日に行われたレースだけ抽出
            speed_index_moto = baba_index.copy()  # スピード指数作成用元データ　defaultはtrue copyにしないと参照渡しになって元データから変更になってしまう
            # 馬場指数用
            baba_index = baba_index[((baba_index['kakuteijyuni'] == '01') | (baba_index['kakuteijyuni'] == '02') | (baba_index['kakuteijyuni'] == '03'))
                        & ((baba_index['jyokencd5'] == '703') | (baba_index['jyokencd5'] == '005') | (baba_index['jyokencd5'] == '010') | (baba_index['jyokencd5'] == '016') | (
                    baba_index['jyokencd5'] == '999')) & ((baba_index['syubetu'] == '13') | (baba_index['syubetu'] == '14'))]  # 1～3着、未勝利～オープン、3・4歳上のレースを選択 3歳戦は削除
            # スピード指数用
            speed_index_moto = speed_index_moto[((speed_index_moto['syubetu'] == '11') | (speed_index_moto['syubetu'] == '12') | (speed_index_moto['syubetu'] == '13') |
                                                 (speed_index_moto['syubetu'] == '14')) & ((speed_index_moto['jyocd'] <= 10) & (speed_index_moto['jyocd'] > 0))]  # 中央の競馬で障害は除く
            jyo_data = baba_index['jyocd'].unique()  # 当日開催された競馬場コードを抽出　★
            for j in range(len(jyo_data)):  # まずは競馬場を指定　★
                jyo_data_1 = jyo_data[j]  # 競馬場コードを抽出
                baba_index_0 = baba_index[baba_index['jyocd'] == jyo_data_1]  # 競馬場コードが一致する行を抽出 馬場指数用
                speed_index_moto_0 = speed_index_moto[speed_index_moto['jyocd'] == jyo_data_1]  ##競馬場コードが一致する行を抽出 スピード指数用
                ID_data = baba_index_0['ID'].unique()  # 上記の条件を満たすレースIDを抽出
                for k in range(len(ID_data)):  # レースIDの数　その日の対象競馬場のレースIDでfor
                    ID_1 = ID_data[k]  # レースIDを抽出
                    baba_index_1 = baba_index_0[baba_index_0['ID'] == ID_1]  # 対象の馬だけ取得　1～3着
                    # 海外のレースID引っ張ると型変換エラーでるからtry-except文
                    try:
                        # 馬場指数の計算に必要な開催場所、距離、クラス、年度，芝orダ，何歳上，グレードの7つを抽出する 検索用に型変換もする　str->int
                        kaisai_d = int(baba_index_1['jyocd'].unique())  # 開催場所
                        kyori_d = int(baba_index_1['kyori'].unique())  # 距離
                        class_d = int(baba_index_1['jyokencd5'].unique())  # クラス
                        nendo_d = int(baba_index_1['year'].unique())  # 年度
                        sibadirt_d = int(baba_index_1['sibababacd'].unique())  # 芝(sibadirt_d=1)orダ(sibadirt_d=0)
                        nansaiue_d = int(baba_index_1['syubetu'].unique())  # 何歳上
                        grade_d = (baba_index_1['gradecd'].unique())[0]  # G3/G2/G1とか
                    except ValueError:
                        pass
                    else:  # 例外が発生しなかった場合の処理
                        # 上記の条件を使って，まずは馬場指数用基準タイム(＝ 基準タイム － (クラス指数 × 距離指数))を作成
                        # 基準タイム編 配列の何行目に位置するか取得 対象年度の対象競馬場の対象距離と芝/ダで決まる
                        # 列番号検索用
                        kijyun_d = kijyun_siba if sibadirt_d >= 1 else kijyun_dirt  # 芝かダートか判定して，その条件での基準タイムを取得
                        kijyun_d = kijyun_d[nendo_d - 2011]  # 対象年度のデータを抽出
                        # 行番号検索用
                        index_d = df_siba_1.iloc[:, kaisai_d - 1] if sibadirt_d >= 1 else df_dirt_1.iloc[:, kaisai_d - 1]  # まずは一致する開催場所列を抽出
                        index_d = np.where(index_d == kyori_d)  # 一致する行番号を取得⇒どこの開催場所でどの距離かが分かり，行列番号がわかった。
                        kijyun_time = kijyun_d.iloc[index_d[0][0], kaisai_d - 1]  # 基準タイム取り出し完了
                        # クラス指数編　配列の何行目に位置するか取得
                        class_index = class3_1 if nansaiue_d == 12 else class_1  # まずは3歳戦か3歳上のどちらのクラス指数使うか決める
                        # クラス条件をもとに行の取り出し
                        if class_d == 703:  # 未勝利
                            class_dd = class_index.iloc[0, 1]
                        elif class_d == 5:  # 1勝クラス
                            class_dd = class_index.iloc[1, 1]
                        elif class_d == 10:  # 2勝クラス
                            class_dd = class_index.iloc[2, 1]
                        elif class_d == 16:  # 3勝クラス
                            class_dd = class_index.iloc[3, 1]
                        elif grade_d == 'B' or grade_d == 'C':  # G3/G2クラス
                            class_dd = class_index.iloc[5, 1]
                        elif grade_d == 'A':  # G1
                            class_dd = class_index.iloc[6, 1]
                        else:  # OPクラス グレードのない重賞もここに入る
                            class_dd = class_index.iloc[4, 1]
                        # 距離指数編　配列の何行目に位置するか取得
                        kijyun_kyori = kyori_siba if sibadirt_d >= 1 else kyori_dirt  # 芝かダートか判定して，その条件での距離指数を取得
                        kijyun_kyori = kijyun_kyori[nendo_d - 2011]  # 対象年度のデータを抽出
                        kyori_index = kijyun_kyori.iloc[index_d[0][0], kaisai_d - 1]  # 距離指数取り出し完了
                        # 馬場指数用基準タイムの算出　馬場指数用基準タイム ＝ 基準タイム － (クラス指数 × 距離指数)
                        baba_kijyun = kijyun_time - (class_dd * kyori_index) / 10  # ここダメだったので修正。指数=10*タイムなので10で割る。
                        # 暫定馬場指数＝（馬場指数用基準タイム－該当レース上位３頭の平均タイム）× 距離指数。ここも修正。指数=10*タイムなので10倍して単位を合わせる。
                        baba_zantei = (10 * (np.nanmean(baba_index_1['sectime'])) - 10 * baba_kijyun) * kyori_index  # 平均ー基準に変更　★
                        # 芝/ダで分けてデータを格納
                        siba_baba_hako.append(baba_zantei) if sibadirt_d >= 1 else dirt_baba_hako.append(baba_zantei)  # 芝かダートか判定して，その条件での暫定馬場指数格納
                # その日の馬場指数算出
                baba_siba = np.nanmean(siba_baba_hako)  # 対象日の馬場指数芝
                baba_dirt = np.nanmean(dirt_baba_hako)  # 対象日の馬場指数ダート
                baba_kakunou_siba += [baba_siba]  # 馬場指数芝 確認用
                baba_kakunou_dirt += [baba_dirt]  # 馬場指数ダート 確認用

                # ②-②続けてスピード指数を算出
                for l in range(len(speed_index_moto_0)):  # 当日の全レースに対してスピード指数を算出
                    spped_uma = pd.DataFrame(speed_index_moto_0.iloc[l, :]).T  # 一行ずつ馬データを処理 なぜか転置されて出てくるから再転置する
                    # 海外のレースID引っ張ると型変換エラーでるからtry-except文
                    if (spped_uma['time'] != '0000').any():  # データバグ対策
                        try:
                            # 馬場指数の計算に必要な開催場所、距離、クラス、年度，芝orダ，何歳上，グレードの7つを抽出する 検索用に型変換もする　str->int
                            kaisai_d = int(spped_uma['jyocd'])  # 開催場所
                            kyori_d = int(spped_uma['kyori'])  # 距離
                            nendo_d = int(spped_uma['year'])  # 年度
                            sibadirt_d = int(spped_uma['sibababacd'])  # 芝(sibadirt_d=1)orダ(sibadirt_d=0)
                            futan = float(spped_uma['futan_siyou'])  # 斤量
                            pd_index = int(spped_uma['index'])  # 斤量
                        except ValueError:
                            pass
                        else:  # 例外が発生しなかった場合の処理
                            # 上記の条件を使って，まずは馬場指数用基準タイム(＝ 基準タイム － (クラス指数 × 距離指数))を作成
                            # 基準タイム編 配列の何行目に位置するか取得 対象年度の対象競馬場の対象距離と芝/ダで決まる
                            # 列番号検索用
                            kijyun_d = kijyun_siba if sibadirt_d >= 1 else kijyun_dirt  # 芝かダートか判定して，その条件での基準タイムを取得
                            kijyun_d = kijyun_d[nendo_d - 2011]  # 対象年度のデータを抽出
                            # 行番号検索用
                            index_d = df_siba_1.iloc[:, kaisai_d - 1] if sibadirt_d >= 1 else df_dirt_1.iloc[:, kaisai_d - 1]  # まずは一致する開催場所列を抽出
                            index_d = np.where(index_d == kyori_d)  # 一致する行番号を取得⇒どこの開催場所でどの距離かが分かり，行列番号がわかった。
                            kijyun_time = kijyun_d.iloc[index_d[0][0], kaisai_d - 1]  # 基準タイム取り出し完了
                            # クラス指数編　配列の何行目に位置するか取得
                            # 距離指数編　配列の何行目に位置するか取得
                            kijyun_kyori = kyori_siba if sibadirt_d >= 1 else kyori_dirt  # 芝かダートか判定して，その条件での距離指数を取得
                            kijyun_kyori = kijyun_kyori[nendo_d - 2011]  # 対象年度のデータを抽出
                            kyori_index = kijyun_kyori.iloc[index_d[0][0], kaisai_d - 1]  # 距離指数取り出し完了
                            # 馬場指数どっち使うか判定
                            baba_siyou = baba_siba if sibadirt_d >= 1 else baba_dirt  # 芝かダートか判定して，その条件での基準タイムを取得
                            # スピード指数を計算
                            speed_index = (10 * kijyun_time - 10 * float(spped_uma['sectime'].unique())) * kyori_index + baba_siyou + (futan - 55) * 2 + 80
                            # speed_index_moto.loc[pd_index,'speed_idx']=round(speed_index,1)#データを格納
                            # a_time1.loc[pd_index,'speed_idx']=round(speed_index,1)#データを格納
                            spped_data_kakunou += [round(speed_index, 1)]  # スピード指数を格納　あとでまとめて追加する
                            index_kakunou += [pd_index]  # indexを格納　あとでまとめて追加する
                    else:
                        pass
                        # ilocは列名の指定できないけど行番号の指定が取り出したものの何番目の行という考えかｔら。，locは指定できるけど行番号の指定がそいつがもともと持っている行番号になる。

        # ③スピード指数格納　時間すごいかかる 1時間くらい ⇒短縮に成功
        data = pd.DataFrame(index=range(len(a_time)))  # くっつけるために0～すべてのデータ元データを作成
        tempo = pd.DataFrame(spped_data_kakunou)
        tempo_new = tempo.rename(columns={0: 'speed_idx'})
        df_tempo = pd.concat([pd.DataFrame(index_kakunou), tempo_new], axis=1)
        df_tempo_1 = df_tempo.set_index(0)
        spped_append = pd.concat([data, df_tempo_1], axis=1)
        a_time1 = pd.concat([a_time, spped_append], axis=1)  # くっつけ
        # ④DBへ出力
        # データpostgreへ
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする
        a_time1.to_sql("speed_index", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
        # -------------実行ここまで
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる

        process_time = time.time() - start
        print(process_time / 60)  # 23.3min
# endregion

# classの実行
# speed_index.calclulate()

# ③-2：スピード指数class⇒スピード指数を出力する
# region speed_index-2 class
class speed_index:
    @staticmethod
    def output():
        """
        スピード指数を出力する関数
        Parameters:
        -----------

        Returns:
        -----------
        csvをフォルダに出力
        """
        start = time.time()
        # 元データをpostgreから取得---------------------------------------------------------------------
        # DBの初期設定
        DATABASE = 'postgresql'
        USER = 'postgres'
        PASSWORD = 'taku0703'
        HOST = 'localhost'
        PORT = '5432'
        DB_NAME = 'everydb2'
        CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする
        # postgreからpandasに出力するデータを指定するSQL
        sql_speedindex = 'SELECT * FROM public."speed_index_class" ORDER BY index ASC;'  # 実行SQL 払い戻し
        # DBのデータをpandasで取得
        spped_from_db = pd.read_sql(sql_speedindex, conn)  # sql:実行したいsql，conn:対象のdb名
        ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる

        # レースIDと日にちをpandasに追加
        spped_from_db1 = spped_from_db
        spped_from_db1['netID'] = spped_from_db1['year'] + spped_from_db1['jyocd'] + spped_from_db1['kaiji'] + spped_from_db1['nichiji'] + spped_from_db1['racenum']  # レースIDの作成
        spped_from_db1['hiniti'] = spped_from_db1['year'] + spped_from_db1['monthday']  # 日にち検索用
        # 対象日を選択する
        raceDAY = spped_from_db1['hiniti'].unique()  # 当日開催されたレースを抽出
        input_kensakuDAY = '20210111'  # 予測した日にちを選択 2021年1月11日の競馬のためにデータがほしいみたいな
        spped_from_db2 = spped_from_db1[spped_from_db1['hiniti'] == input_kensakuDAY]  # ほしいレースだけ取り出し
        allnetID = spped_from_db2['netID'].unique()  # 当日のレースIDを取り出し
        # 対象日の全レースについてcsv作成
        for i in range(len(allnetID)):  # 全レース指数取り出し
            motopandas = spped_from_db2[1:1]  # moto
            allnetID_1 = allnetID[i]  # ID
            spped_from_db3 = spped_from_db2[spped_from_db2['netID'] == allnetID_1]  # ほしいレースだけ取り出し
            name = spped_from_db3['bamei'].unique()  # 当日開催された競馬場コードを抽出　★
            for j in range(len(name)):  # 全馬に対して指数を取り出す
                name_1 = name[j]  # 馬名
                umadata = spped_from_db1[spped_from_db1['bamei'] == name_1]  # レース取り出し
                tasu = umadata.tail(5)  # 5走分
                motopandas = pd.concat([motopandas, tasu], axis=0)  # 結合
            # データをcsvで出力
            motopandas = motopandas.drop(['year', 'monthday', 'index', 'kaiji', 'nichiji', 'ID', 'gradecd', 'syubetu', 'jyokencd1', 'jyokencd2',
                                          'jyokencd3','jyokencd4', 'jyokencd5', 'trackcd', 'tenkocd', 'kigocd'], axis=1)  # いらん列削除
            motopandas = motopandas[motopandas['hiniti'] != input_kensakuDAY]  # 当日はデータないので削除
            kensakuID = ((umadata.tail(1)['year']).unique() + (umadata.tail(1)['monthday']).unique() + (umadata.tail(1)['jyocd']).unique() + (umadata.tail(1)['racenum']).unique())[0]
            # 日にちでフォルダ作成
            new_path = 'speed_hozon\{}'.format(input_kensakuDAY)
            if not os.path.exists(new_path):  # ディレクトリがなかったら
                os.mkdir(new_path)  # 作成したいフォルダ名を作成
            # csv出力
            hozonsaki = new_path + '\{}.csv'.format(kensakuID)
            motopandas.to_csv(hozonsaki, encoding='utf_8_sig', index=False)

        process_time = time.time() - start
        print(process_time / 60)  #
# endregion

# classの実行
# speed_index.output()


# ④特徴量作成class⇒targetencodingを意識した特徴量(統計量)を作成する。
# region target_encoding class
class target_encoding:
    @staticmethod
    def output():
        """
        targer-encoding特徴量を出力する関数
        Parameters:
        -----------

        Returns:
        -----------
        Tokutyo_data_new : pandas.DataFrame
            target_encoding特徴量をDBに出力
        """
        start = time.time()
        # 元データをpostgreから取得---------------------------------------------------------------------
        # DBの初期設定
        DATABASE = 'postgresql'
        USER = 'postgres'
        PASSWORD = 'taku0703'
        HOST = 'localhost'
        PORT = '5432'
        DB_NAME = 'everydb2'
        CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする
        # postgreからpandasに出力するデータを指定するSQL
        sql_moto = 'SELECT * FROM public."df_moto" ORDER BY index ASC;'  # 実行SQL
        # DBのデータをpandasで取得
        moto_df = pd.read_sql(sql_moto, conn)  # sql:実行したいsql，conn:対象のdb名
        ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる

        # データの前処理
        moto_df = moto_df.loc[:,
                 ['index', 'year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'umaban', 'bamei',
                  'chokyosiryakusyo', 'banusiname', 'kisyuryakusyo', 'kakuteijyuni', 'odds', 'ID', 'kyori', 'trackcd', 'sibababacd', 'dirtbabacd', 'father',
                  'tanuma1', 'tanpay1', 'tanuma2', 'tanpay2', 'tanuma3', 'tanpay3', 'fukuuma1', 'fukupay1', 'fukuuma2', 'fukupay2', 'fukuuma3', 'fukupay3',
                  'fukuuma4', 'fukupay4', 'fukuuma5', 'fukupay5']]
        # 変数の初期設定
        year_num = 11
        basyo_num = 10
        main_num = 50
        # 統計データを作成する
        moto_data = moto_df.copy()  # defaultはtrue copyにしないと参照渡しになって元データから変更になってしまう
        moto_data = moto_data.replace('', np.nan)  # 空をnanに置き換え
        # pandasでobject形式のデータをfloatにして入れ替える
        moto_data['kakuteijyuni'] = moto_data['kakuteijyuni'].astype(float)  # 確定順位をobjectからintに変換
        moto_data['fukuuma1'] = moto_data['fukuuma1'].astype(float)
        moto_data['fukupay1'] = moto_data['fukupay1'].astype(float)
        moto_data['fukuuma2'] = moto_data['fukuuma2'].astype(float)
        moto_data['fukupay2'] = moto_data['fukupay2'].astype(float)
        moto_data['fukuuma3'] = moto_data['fukuuma3'].astype(float)
        moto_data['fukupay3'] = moto_data['fukupay3'].astype(float)
        moto_data['fukuuma4'] = moto_data['fukuuma4'].astype(float)
        moto_data['fukupay4'] = moto_data['fukupay4'].astype(float)
        moto_data['fukuuma5'] = moto_data['fukuuma5'].astype(float)
        moto_data['fukupay5'] = moto_data['fukupay5'].astype(float)
        moto_data['tanuma1'] = moto_data['tanuma1'].astype(float)
        moto_data['tanpay1'] = moto_data['tanpay1'].astype(float)
        moto_data['tanuma2'] = moto_data['tanuma2'].astype(float)
        moto_data['tanpay2'] = moto_data['tanpay2'].astype(float)
        moto_data['tanuma3'] = moto_data['tanuma3'].astype(float)
        moto_data['tanpay3'] = moto_data['tanpay3'].astype(float)
        # 単勝払い戻しと複勝払い戻しを列に追加
        # 特徴量元データに単勝払い戻しと複勝払い戻しを列に追加編
        def harai_tan(x):
            if float(x.umaban) == x.tanuma1:
                return x.tanpay1
            elif float(x.umaban) == x.tanuma2:
                return x.tanpay2
            elif float(x.umaban) == x.tanuma3:
                return x.tanpay3
            else:
                return 0

        def harai_fuku(x):
            if float(x.umaban) == x.fukuuma1:
                return x.fukupay1
            elif float(x.umaban) == x.fukuuma2:
                return x.fukupay2
            elif float(x.umaban) == x.fukuuma3:
                return x.fukupay3
            elif float(x.umaban) == x.fukuuma4:
                return x.fukupay4
            elif float(x.umaban) == x.fukuuma5:
                return x.fukupay5
            else:
                return 0
        # applyで格納
        if not 'tan_harai' in moto_data.columns:
            moto_data['tan_harai'] = moto_data.apply(lambda x: harai_tan(x), axis=1)
            moto_data['fuku_harai'] = moto_data.apply(lambda x: harai_fuku(x), axis=1)
        else:
            pass
        # いらない列削除
        moto_data = moto_data.drop(
            ['odds', 'fukuuma1', 'fukupay1', 'fukuuma2', 'fukupay2', 'fukuuma3', 'fukupay3', 'fukuuma4', 'fukupay4', 'fukuuma5',
             'fukupay5', 'tanuma1', 'tanpay1', 'tanuma2', 'tanpay2', 'tanuma3', 'tanpay3'], axis=1)
        # 確定順位列を右端に移動させる
        col = moto_data.columns.tolist()  # 列名のリスト
        col.remove('kakuteijyuni')  # 't'を削除 ※列名は重複していないものとする
        col.append('kakuteijyuni')  # 末尾に`t`を追加
        moto_data = moto_data[col]
        moto_data_2 = moto_data
        moto_data_2['year'] = moto_data_2['year'].astype(int)  # 確定順位をobjectからintに変換
        # 特徴量を追加編
        # pandasのデータをfloat型にする　NaNもあるし，float型 競走中止とかは将来的に
        # 型変換と欠測処理　object⇒numericにして欠測はnanで埋める
        moto_data_2['year'] = pd.to_numeric(moto_data_2["year"], errors='coerce')
        moto_data_2["jyocd"] = pd.to_numeric(moto_data_2["jyocd"], errors='coerce')
        moto_data_2['umaban'] = pd.to_numeric(moto_data_2["umaban"], errors='coerce')
        moto_data_2['kyori'] = pd.to_numeric(moto_data_2["kyori"], errors='coerce')
        moto_data_2['trackcd'] = pd.to_numeric(moto_data_2["trackcd"], errors='coerce')
        moto_data_2['sibababacd'] = pd.to_numeric(moto_data_2["sibababacd"], errors='coerce')
        moto_data_2['dirtbabacd'] = pd.to_numeric(moto_data_2["dirtbabacd"], errors='coerce')
        moto_2010 = moto_data_2
        # TODO itertools.combinations これで変数の組み合わせわかる
        # 特徴量の条件を抽出
        # region Feature value
        # デフォルトデータ
        t0 = list(moto_2010.index)  # デフォルトデータ
        # 馬番関係
        t1 = list(moto_2010[(moto_2010['umaban'] < 9)].index)  # 馬番9より小さい　OK
        t61 = list(moto_2010[(moto_2010['umaban'] >= 9)].index)
        # 距離関係　短距離，中距離，長距離
        t209 = list(moto_2010[(moto_2010['kyori'] <= 1400)].index)  # 1400以下
        t210 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200))].index)  # 1422
        t211 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600))].index)  # 2236
        # 馬場状態良・重関係
        t254 = list(moto_2010[((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1))].index)  # 良
        t255 = list(moto_2010[((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1))].index)  # 重
        # 芝/ダ関係
        t264 = list(moto_2010[((moto_2010['sibababacd'] > 0))].index)  # 芝
        t265 = list(moto_2010[((moto_2010['sibababacd'] == 0))].index)  # ダ
        # 内/外周り(芝のみ)
        t266 = list(moto_2010[((moto_2010['sibababacd'] > 0) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 内まわり芝
        t267 = list(moto_2010[((moto_2010['sibababacd'] > 0) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 外まわり芝
        # endregion

        # 条件のindexをlistに格納
        jyo_list_pre = []
        jyo_list_pre.extend(
            [t0, t1, t61, t209, t210, t211, t254, t255, t264, t265, t266, t267])  # 全267条件⇒12条件

        jyo_list = []
        for i in range(len(jyo_list_pre)):
            t_check = jyo_list_pre[i]
            if len(t_check) >= 10000:  # 10000個以上データあれば格納
                jyo_list.append(t_check)

        # 払い戻しなどの集計用に必要な列（単勝/複勝払い戻し，確定順位）だけ抽出
        np_moto_2010 = np.array(moto_2010.loc[:, ['tan_harai', 'fuku_harai', 'kakuteijyuni']])
        # 集計データを格納する用のlistを作成　二次元配列（リストのリスト）11年×10場×50メイン
        # TODO 単勝率，複勝率，単勝回収率，複勝回収率4つも必要？ 複だけにして2つにするか？
        kisyu_box_tanharai = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        kisyu_box_fukuharai = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        kisyu_box_syouritu = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        kisyu_box_fukuritu = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        chokyo_box_tanharai = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        chokyo_box_fukuharai = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        chokyo_box_syouritu = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        chokyo_box_fukuritu = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        banu_box_tanharai = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        banu_box_fukuharai = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        banu_box_syouritu = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        banu_box_fukuritu = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        syu_box_tanharai = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        syu_box_fukuharai = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        syu_box_syouritu = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        syu_box_fukuritu = [[] for torima in range(year_num * basyo_num * main_num)]  # n_uma_race用
        # index番号把握用
        kisyu_index = [[] for torima in range(year_num * basyo_num * main_num)]  # 騎手用　★
        chokyo_index = [[] for torima in range(year_num * basyo_num * main_num)]  # 調教師用　★
        banu_index = [[] for torima in range(year_num * basyo_num * main_num)]  # 馬主用　★
        syu_index = [[] for torima in range(year_num * basyo_num * main_num)]  # 種牡馬用　★
        # サンプル数確認用
        kisyu_sample = [[] for torima in range(year_num * basyo_num * main_num)]  # 騎手用　★
        chokyo_sample = [[] for torima in range(year_num * basyo_num * main_num)]  # 調教師用　★
        banu_sample = [[] for torima in range(year_num * basyo_num * main_num)]  # 馬主用　★
        syu_sample = [[] for torima in range(year_num * basyo_num * main_num)]  # 種牡馬用　★
        # mainを追加するよう 11year
        kisyu_main_11 = [[] for torima in range(year_num)]  # 騎手用　★
        chokyo_main_11 = [[] for torima in range(year_num)]  # 調教師用　★
        banu_main_11 = [[] for torima in range(year_num)]  # 馬主用　★
        syu_main_11 = [[] for torima in range(year_num)]  # 種牡馬用　★
        # count用
        count = 0
        count_main = 0

        # データ作成 11年×10場×50個（メイン）＝5500個
        for i in range(year_num):  # 11年分
            # 年の範囲を指定する
            year_hani = 2011 + i  # 2011~2021でデータを作る　2011年までのデータは2012年に使う
            year_hani_low = year_hani - 3  # 2015なら2012
            year_hani_high = year_hani - 1  # 2015なら2014で2012-2014の3年間のデータを使用する
            print(year_hani)
            # 対象年以下を指定
            year_list = list(moto_2010[((year_hani_low <= moto_2010['year']) & (moto_2010['year'] <= year_hani_high))].index)  # 特徴量作成のための元データ 2015年のデータなら2012年から2014年のデータを使用
            tokuapply_list = list(moto_2010[(moto_2010['year'] == year_hani)].index)  # 特徴量をapplyする行 ↑の例なら2015年とか
            # メイン取得用
            moto_main = moto_2010[((1 <= moto_2010['jyocd']) & (moto_2010['jyocd'] <= 10))]  # 中央
            moto_main = moto_main[((year_hani_low <= moto_main['year']) & (moto_main['year'] <= year_hani_high))]  # year範囲
            # メインデータを抽出 data in last year 地方めちゃまぎれこむ　ほしいのは中央
            kisyu_data = list(moto_main['kisyuryakusyo'].value_counts().to_dict().keys())  # 騎手　辞書にしてキーをlistで取得
            chokyo_data = list(moto_main['chokyosiryakusyo'].value_counts().to_dict().keys())  # 調教師　辞書にしてキーをlistで取得
            banu_data = list(moto_main['banusiname'].value_counts().to_dict().keys())  # 馬主　辞書にしてキーをlistで取得
            syu_data = list(moto_main['father'].value_counts().to_dict().keys())  # 種牡馬　辞書にしてキーをlistで取得
            # メイン追加用
            kisyu_main = []
            chokyo_main = []
            banu_main = []
            syu_main = []
            for jyonum in range(1, 11):  # 競馬場コード10個 1-10
                print(jyonum)
                # 競馬場を指定
                basyo_list = list(moto_2010[(moto_2010['jyocd'] == jyonum)].index)
                yearbasyo_list = list(set(year_list) & set(basyo_list))  # 年と場所に関する条件
                # uma_data=list(moto_main['bamei'].value_counts().to_dict().keys())#bamei　辞書にしてキーをlistで取得
                for j in range(main_num):  # 4つのメインに対して50個分データを作成
                    # メインのindexを取り出し
                    kisyu_list = list(moto_2010[(moto_2010['kisyuryakusyo'] == kisyu_data[j])].index)
                    chokyo_list = list(moto_2010[(moto_2010['chokyosiryakusyo'] == chokyo_data[j])].index)
                    banu_list = list(moto_2010[(moto_2010['banusiname'] == banu_data[j])].index)
                    syu_list = list(moto_2010[(moto_2010['father'] == syu_data[j])].index)
                    # 追加
                    if jyonum == 1:  # １場だけ
                        print('できてます')
                        kisyu_main.append(kisyu_data[j])
                        chokyo_main.append(chokyo_data[j])
                        banu_main.append(banu_data[j])
                        syu_main.append(syu_data[j])
                    # 特徴量作成用のindex kisyu&year(以下のほう)&basyo
                    kisyu_index1 = list(set(kisyu_list) & set(yearbasyo_list))  # mainとyearとbasyoでindexを取得
                    chokyo_index1 = list(set(chokyo_list) & set(yearbasyo_list))
                    banu_list_index1 = list(set(banu_list) & set(yearbasyo_list))
                    syu_index1 = list(set(syu_list) & set(yearbasyo_list))
                    # list内包表記 特徴量作成用 mapの代わりになる このデータを　https://qiita.com/KTakahiro1729/items/c9cb757473de50652374
                    syukei_kisyu = [set(kisyu_index1) & set(i_nakami) for i_nakami in jyo_list]  # main×267条件で1×267配列誕生
                    syukei_chokyo = [set(chokyo_index1) & set(i_nakami) for i_nakami in jyo_list]
                    syukei_banu = [set(banu_list_index1) & set(i_nakami) for i_nakami in jyo_list]
                    syukei_syu = [set(syu_index1) & set(i_nakami) for i_nakami in jyo_list]
                    # 特徴量を適応する行のindex kisyu&year(=のほう)&basyo
                    kisyu_indexapp = list(set(kisyu_list) & set(tokuapply_list) & set(basyo_list))
                    chokyo_indexapp = list(set(chokyo_list) & set(tokuapply_list) & set(basyo_list))
                    banu_list_indexapp = list(set(banu_list) & set(tokuapply_list) & set(basyo_list))
                    syu_indexapp = list(set(syu_list) & set(tokuapply_list) & set(basyo_list))
                    # list内包表記 特徴量を適応する行 mapの代わりになる ここの行に入れる　https://qiita.com/KTakahiro1729/items/c9cb757473de50652374
                    syukei_kisyuapp = [list(set(kisyu_indexapp) & set(i_nakami)) for i_nakami in jyo_list]  # main×267条件で1×267配列誕生
                    syukei_chokyoapp = [list(set(chokyo_indexapp) & set(i_nakami)) for i_nakami in jyo_list]
                    syukei_banuapp = [list(set(banu_list_indexapp) & set(i_nakami)) for i_nakami in jyo_list]
                    syukei_syuapp = [list(set(syu_indexapp) & set(i_nakami)) for i_nakami in jyo_list]
                    # 格納
                    # 特徴量を適応する行のindexを格納 ここをいかに早く適応させるか
                    kisyu_index[count] = syukei_kisyuapp
                    chokyo_index[count] = syukei_chokyoapp
                    banu_index[count] = syukei_banuapp
                    syu_index[count] = syukei_syuapp
                    # 特徴量作成用 syukei_kisyuこれでオーケー
                    # 騎手
                    kisyu_box_tanharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 0]) for i_nakami in syukei_kisyu]
                    kisyu_box_fukuharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 1]) for i_nakami in syukei_kisyu]
                    kisyu_box_syouritu[count] = [np.nanmean(np_moto_2010[list(i_nakami), 2] == 1.0) * 100 for i_nakami in syukei_kisyu]
                    kisyu_box_fukuritu[count] = [np.nanmean((np_moto_2010[list(i_nakami), 2] >= 1) & (np_moto_2010[list(i_nakami), 2] <= 3)) * 100 for i_nakami in syukei_kisyu]
                    # 調教
                    chokyo_box_tanharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 0]) for i_nakami in syukei_chokyo]
                    chokyo_box_fukuharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 1]) for i_nakami in syukei_chokyo]
                    chokyo_box_syouritu[count] = [np.nanmean(np_moto_2010[list(i_nakami), 2] == 1.0) * 100 for i_nakami in syukei_chokyo]
                    chokyo_box_fukuritu[count] = [np.nanmean((np_moto_2010[list(i_nakami), 2] >= 1) & (np_moto_2010[list(i_nakami), 2] <= 3)) * 100 for i_nakami in syukei_chokyo]
                    # 馬主
                    banu_box_tanharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 0]) for i_nakami in syukei_banu]
                    banu_box_fukuharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 1]) for i_nakami in syukei_banu]
                    banu_box_syouritu[count] = [np.nanmean(np_moto_2010[list(i_nakami), 2] == 1.0) * 100 for i_nakami in syukei_banu]
                    banu_box_fukuritu[count] = [np.nanmean((np_moto_2010[list(i_nakami), 2] >= 1) & (np_moto_2010[list(i_nakami), 2] <= 3)) * 100 for i_nakami in syukei_banu]
                    # 種牡馬
                    syu_box_tanharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 0]) for i_nakami in syukei_syu]
                    syu_box_fukuharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 1]) for i_nakami in syukei_syu]
                    syu_box_syouritu[count] = [np.nanmean(np_moto_2010[list(i_nakami), 2] == 1.0) * 100 for i_nakami in syukei_syu]
                    syu_box_fukuritu[count] = [np.nanmean((np_moto_2010[list(i_nakami), 2] >= 1) & (np_moto_2010[list(i_nakami), 2] <= 3)) * 100 for i_nakami in syukei_syu]
                    # サンプル数確認用　★
                    kisyu_sample[count] = [len(v) for v in syukei_kisyu]  # サンプル数を格納
                    chokyo_sample[count] = [len(v) for v in syukei_chokyo]  # サンプル数を格納
                    banu_sample[count] = [len(v) for v in syukei_banu]  # サンプル数を格納
                    syu_sample[count] = [len(v) for v in syukei_syu]  # サンプル数を格納

                    count += 1  # 5500まで行く

            # 一年分追加
            kisyu_main_11[count_main] = kisyu_main  # mainを格納
            chokyo_main_11[count_main] = chokyo_main  # mainを格納
            banu_main_11[count_main] = banu_main  # mainを格納
            syu_main_11[count_main] = syu_main  # mainを格納
            count_main += 1  # 11年分まで行く

        # 4つのメインについての特徴量をpd.DataFrameに変換
        pdk1 = pd.DataFrame(kisyu_box_tanharai)
        pdk2 = pd.DataFrame(kisyu_box_fukuharai)
        pdk3 = pd.DataFrame(kisyu_box_syouritu)
        pdk4 = pd.DataFrame(kisyu_box_fukuritu)
        pdc1 = pd.DataFrame(chokyo_box_tanharai)
        pdc2 = pd.DataFrame(chokyo_box_fukuharai)
        pdc3 = pd.DataFrame(chokyo_box_syouritu)
        pdc4 = pd.DataFrame(chokyo_box_fukuritu)
        pdb1 = pd.DataFrame(banu_box_tanharai)
        pdb2 = pd.DataFrame(banu_box_fukuharai)
        pdb3 = pd.DataFrame(banu_box_syouritu)
        pdb4 = pd.DataFrame(banu_box_fukuritu)
        pds1 = pd.DataFrame(syu_box_tanharai)
        pds2 = pd.DataFrame(syu_box_fukuharai)
        pds3 = pd.DataFrame(syu_box_syouritu)
        pds4 = pd.DataFrame(syu_box_fukuritu)
        # index
        indexnum1 = pd.DataFrame(kisyu_index)
        indexnum2 = pd.DataFrame(chokyo_index)
        indexnum3 = pd.DataFrame(banu_index)
        indexnum4 = pd.DataFrame(syu_index)
        # サンプル数
        sample1 = pd.DataFrame(kisyu_sample)
        sample2 = pd.DataFrame(chokyo_sample)
        sample3 = pd.DataFrame(banu_sample)
        sample4 = pd.DataFrame(syu_sample)
        # メイン
        main1 = pd.DataFrame(kisyu_main_11)
        main2 = pd.DataFrame(chokyo_main_11)
        main3 = pd.DataFrame(banu_main_11)
        main4 = pd.DataFrame(syu_main_11)
        # index振る
        pdk10 = pdk1.reset_index()  # indexを与える
        pdk20 = pdk2.reset_index()  # indexを与える
        pdk30 = pdk3.reset_index()  # indexを与える
        pdk40 = pdk4.reset_index()  # indexを与える
        pdc10 = pdc1.reset_index()  # indexを与える
        pdc20 = pdc2.reset_index()  # indexを与える
        pdc30 = pdc3.reset_index()  # indexを与える
        pdc40 = pdc4.reset_index()  # indexを与える
        pdb10 = pdb1.reset_index()  # indexを与える
        pdb20 = pdb2.reset_index()  # indexを与える
        pdb30 = pdb3.reset_index()  # indexを与える
        pdb40 = pdb4.reset_index()  # indexを与える
        pds10 = pds1.reset_index()  # indexを与える
        pds20 = pds2.reset_index()  # indexを与える
        pds30 = pds3.reset_index()  # indexを与える
        pds40 = pds4.reset_index()  # indexを与える
        # indexも振る
        indexnum10 = indexnum1.reset_index()  # indexを与える
        indexnum20 = indexnum2.reset_index()  # indexを与える
        indexnum30 = indexnum3.reset_index()  # indexを与える
        indexnum40 = indexnum4.reset_index()  # indexを与える
        # サンプル数も振る
        sample10 = sample1.reset_index()  # indexを与える
        sample20 = sample2.reset_index()  # indexを与える
        sample30 = sample3.reset_index()  # indexを与える
        sample40 = sample4.reset_index()  # indexを与える
        # mainも振る
        main10 = main1.reset_index()  # indexを与える
        main20 = main2.reset_index()  # indexを与える
        main30 = main3.reset_index()  # indexを与える
        main40 = main4.reset_index()  # indexを与える
        # drop
        akisyu_box_tanharai1 = pdk10.drop(['index'], axis=1)  # index列削除
        akisyu_box_fukuharai1 = pdk20.drop(['index'], axis=1)  # index列削除
        akisyu_box_syouritu1 = pdk30.drop(['index'], axis=1)  # index列削除
        akisyu_box_fukuritu1 = pdk40.drop(['index'], axis=1)  # index列削除
        achokyo_box_tanharai1 = pdc10.drop(['index'], axis=1)  # index列削除
        achokyo_box_fukuharai1 = pdc20.drop(['index'], axis=1)  # index列削除
        achokyo_box_syouritu1 = pdc30.drop(['index'], axis=1)  # index列削除
        achokyo_box_fukuritu1 = pdc40.drop(['index'], axis=1)  # index列削除
        abanu_box_tanharai1 = pdb10.drop(['index'], axis=1)  # index列削除
        abanu_box_fukuharai1 = pdb20.drop(['index'], axis=1)  # index列削除
        abanu_box_syouritu1 = pdb30.drop(['index'], axis=1)  # index列削除
        abanu_box_fukuritu1 = pdb40.drop(['index'], axis=1)  # index列削除
        asyu_box_tanharai1 = pds10.drop(['index'], axis=1)  # index列削除
        asyu_box_fukuharai1 = pds20.drop(['index'], axis=1)  # index列削除
        asyu_box_syouritu1 = pds30.drop(['index'], axis=1)  # index列削除
        asyu_box_fukuritu1 = pds40.drop(['index'], axis=1)  # index列削除
        at_kisyu_sample1 = sample10.drop(['index'], axis=1)  # index列削除
        at_chokyo_sample1 = sample20.drop(['index'], axis=1)  # index列削除
        at_banu_sample1 = sample30.drop(['index'], axis=1)  # index列削除
        at_syu_sample1 = sample40.drop(['index'], axis=1)  # index列削除
        at_kisyu_main1 = main10.drop(['index'], axis=1)  # index列削除
        at_chokyo_main1 = main20.drop(['index'], axis=1)  # index列削除
        at_banu_main1 = main30.drop(['index'], axis=1)  # index列削除
        at_syu_main1 = main40.drop(['index'], axis=1)  # index列削除
        # サンプル数5以下をnanに変換
        thr = 5
        at_kisyu_sample2 = at_kisyu_sample1.where(at_kisyu_sample1 > thr, np.nan)  # 5以下をnanにする
        at_chokyo_sample2 = at_chokyo_sample1.where(at_kisyu_sample1 > thr, np.nan)
        at_banu_sample2 = at_banu_sample1.where(at_kisyu_sample1 > thr, np.nan)
        at_syu_sample2 = at_syu_sample1.where(at_kisyu_sample1 > thr, np.nan)
        # 数値データを1にする
        at_kisyu_sample3 = at_kisyu_sample2.where(at_kisyu_sample1 < thr, 1)  # 5以上を1にする
        at_chokyo_sample3 = at_chokyo_sample2.where(at_kisyu_sample1 < thr, 1)
        at_banu_sample3 = at_banu_sample2.where(at_kisyu_sample1 < thr, 1)
        at_syu_sample3 = at_syu_sample2.where(at_kisyu_sample1 < thr, 1)
        # df_bool=sum((at_kisyu_sample4==5.0).sum())#足し算
        # 特徴量データ×sampleデータして残すデータを決める
        akisyu_box_tanharai2 = akisyu_box_tanharai1 * at_kisyu_sample3
        akisyu_box_fukuharai2 = akisyu_box_fukuharai1 * at_kisyu_sample3
        akisyu_box_syouritu2 = akisyu_box_syouritu1 * at_kisyu_sample3
        akisyu_box_fukuritu2 = akisyu_box_fukuritu1 * at_kisyu_sample3
        achokyo_box_tanharai2 = achokyo_box_tanharai1 * at_chokyo_sample3
        achokyo_box_fukuharai2 = achokyo_box_fukuharai1 * at_chokyo_sample3
        achokyo_box_syouritu2 = achokyo_box_syouritu1 * at_chokyo_sample3
        achokyo_box_fukuritu2 = achokyo_box_fukuritu1 * at_chokyo_sample3
        abanu_box_tanharai2 = abanu_box_tanharai1 * at_banu_sample3
        abanu_box_fukuharai2 = abanu_box_fukuharai1 * at_banu_sample3
        abanu_box_syouritu2 = abanu_box_syouritu1 * at_banu_sample3
        abanu_box_fukuritu2 = abanu_box_fukuritu1 * at_banu_sample3
        asyu_box_tanharai2 = asyu_box_tanharai1 * at_syu_sample3
        asyu_box_fukuharai2 = asyu_box_fukuharai1 * at_syu_sample3
        asyu_box_syouritu2 = asyu_box_syouritu1 * at_syu_sample3
        asyu_box_fukuritu2 = asyu_box_fukuritu1 * at_syu_sample3
        # それぞれの列においてNANを残ったデータの平均で置き換え TODO 精度向上のため，今野は年単位で欠測処理行う
        akisyu_box_tanharai3 = akisyu_box_tanharai2.fillna(akisyu_box_tanharai2.mean())
        akisyu_box_fukuharai3 = akisyu_box_fukuharai2.fillna(akisyu_box_fukuharai2.mean())
        akisyu_box_syouritu3 = akisyu_box_syouritu2.fillna(akisyu_box_syouritu2.mean())
        akisyu_box_fukuritu3 = akisyu_box_fukuritu2.fillna(akisyu_box_fukuritu2.mean())
        achokyo_box_tanharai3 = achokyo_box_tanharai2.fillna(achokyo_box_tanharai2.mean())
        achokyo_box_fukuharai3 = achokyo_box_fukuharai2.fillna(achokyo_box_fukuharai2.mean())
        achokyo_box_syouritu3 = achokyo_box_syouritu2.fillna(achokyo_box_syouritu2.mean())
        achokyo_box_fukuritu3 = achokyo_box_fukuritu2.fillna(achokyo_box_fukuritu2.mean())
        abanu_box_tanharai3 = abanu_box_tanharai2.fillna(abanu_box_tanharai2.mean())
        abanu_box_fukuharai3 = abanu_box_fukuharai2.fillna(abanu_box_fukuharai2.mean())
        abanu_box_syouritu3 = abanu_box_syouritu2.fillna(abanu_box_syouritu2.mean())
        abanu_box_fukuritu3 = abanu_box_fukuritu2.fillna(abanu_box_fukuritu2.mean())
        asyu_box_tanharai3 = asyu_box_tanharai2.fillna(asyu_box_tanharai2.mean())
        asyu_box_fukuharai3 = asyu_box_fukuharai2.fillna(asyu_box_fukuharai2.mean())
        asyu_box_syouritu3 = asyu_box_syouritu2.fillna(asyu_box_syouritu2.mean())
        asyu_box_fukuritu3 = asyu_box_fukuritu2.fillna(asyu_box_fukuritu2.mean())
        # メインを11年分並べる，縦に
        # 騎手メイン
        kn_10_0 = (pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[0, :]))] * 10)).rename(columns={0: 'jockey'})
        kn_10_1 = pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[1, :]))] * 10).rename(columns={1: 'jockey'})
        kn_10_2 = pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[2, :]))] * 10).rename(columns={2: 'jockey'})
        kn_10_3 = pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[3, :]))] * 10).rename(columns={3: 'jockey'})
        kn_10_4 = pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[4, :]))] * 10).rename(columns={4: 'jockey'})
        kn_10_5 = pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[5, :]))] * 10).rename(columns={5: 'jockey'})
        kn_10_6 = pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[6, :]))] * 10).rename(columns={6: 'jockey'})
        kn_10_7 = pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[7, :]))] * 10).rename(columns={7: 'jockey'})
        kn_10_8 = pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[8, :]))] * 10).rename(columns={8: 'jockey'})
        kn_10_9 = pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[9, :]))] * 10).rename(columns={9: 'jockey'})
        kn_10_10 = pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[10, :]))] * 10).rename(columns={10: 'jockey'})
        kn_10_all = pd.concat([kn_10_0, kn_10_1, kn_10_2, kn_10_3, kn_10_4, kn_10_5, kn_10_6, kn_10_7, kn_10_8, kn_10_9, kn_10_10])  # 11年分複製
        kn_10_all = kn_10_all.reset_index(drop=True)
        # 調教師メイン
        cn_10_0 = (pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[0, :]))] * 10)).rename(columns={0: 'chokyo'})
        cn_10_1 = pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[1, :]))] * 10).rename(columns={1: 'chokyo'})
        cn_10_2 = pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[2, :]))] * 10).rename(columns={2: 'chokyo'})
        cn_10_3 = pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[3, :]))] * 10).rename(columns={3: 'chokyo'})
        cn_10_4 = pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[4, :]))] * 10).rename(columns={4: 'chokyo'})
        cn_10_5 = pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[5, :]))] * 10).rename(columns={5: 'chokyo'})
        cn_10_6 = pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[6, :]))] * 10).rename(columns={6: 'chokyo'})
        cn_10_7 = pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[7, :]))] * 10).rename(columns={7: 'chokyo'})
        cn_10_8 = pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[8, :]))] * 10).rename(columns={8: 'chokyo'})
        cn_10_9 = pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[9, :]))] * 10).rename(columns={9: 'chokyo'})
        cn_10_10 = pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[10, :]))] * 10).rename(columns={10: 'chokyo'})
        cn_10_all = pd.concat([cn_10_0, cn_10_1, cn_10_2, cn_10_3, cn_10_4, cn_10_5, cn_10_6, cn_10_7, cn_10_8, cn_10_9, cn_10_10])  # 11年分複製
        cn_10_all = cn_10_all.reset_index(drop=True)
        # 馬主メイン
        bn_10_0 = (pd.concat([(pd.DataFrame(at_banu_main1.iloc[0, :]))] * 10)).rename(columns={0: 'banushi'})
        bn_10_1 = pd.concat([(pd.DataFrame(at_banu_main1.iloc[1, :]))] * 10).rename(columns={1: 'banushi'})
        bn_10_2 = pd.concat([(pd.DataFrame(at_banu_main1.iloc[2, :]))] * 10).rename(columns={2: 'banushi'})
        bn_10_3 = pd.concat([(pd.DataFrame(at_banu_main1.iloc[3, :]))] * 10).rename(columns={3: 'banushi'})
        bn_10_4 = pd.concat([(pd.DataFrame(at_banu_main1.iloc[4, :]))] * 10).rename(columns={4: 'banushi'})
        bn_10_5 = pd.concat([(pd.DataFrame(at_banu_main1.iloc[5, :]))] * 10).rename(columns={5: 'banushi'})
        bn_10_6 = pd.concat([(pd.DataFrame(at_banu_main1.iloc[6, :]))] * 10).rename(columns={6: 'banushi'})
        bn_10_7 = pd.concat([(pd.DataFrame(at_banu_main1.iloc[7, :]))] * 10).rename(columns={7: 'banushi'})
        bn_10_8 = pd.concat([(pd.DataFrame(at_banu_main1.iloc[8, :]))] * 10).rename(columns={8: 'banushi'})
        bn_10_9 = pd.concat([(pd.DataFrame(at_banu_main1.iloc[9, :]))] * 10).rename(columns={9: 'banushi'})
        bn_10_10 = pd.concat([(pd.DataFrame(at_banu_main1.iloc[10, :]))] * 10).rename(columns={10: 'banushi'})
        bn_10_all = pd.concat([bn_10_0, bn_10_1, bn_10_2, bn_10_3, bn_10_4, bn_10_5, bn_10_6, bn_10_7, bn_10_8, bn_10_9, bn_10_10])  # 11年分複製
        bn_10_all = bn_10_all.reset_index(drop=True)
        # 種牡馬メイン
        sbn_10_0 = (pd.concat([(pd.DataFrame(at_syu_main1.iloc[0, :]))] * 10)).rename(columns={0: 'syuboba'})
        sbn_10_1 = pd.concat([(pd.DataFrame(at_syu_main1.iloc[1, :]))] * 10).rename(columns={1: 'syuboba'})
        sbn_10_2 = pd.concat([(pd.DataFrame(at_syu_main1.iloc[2, :]))] * 10).rename(columns={2: 'syuboba'})
        sbn_10_3 = pd.concat([(pd.DataFrame(at_syu_main1.iloc[3, :]))] * 10).rename(columns={3: 'syuboba'})
        sbn_10_4 = pd.concat([(pd.DataFrame(at_syu_main1.iloc[4, :]))] * 10).rename(columns={4: 'syuboba'})
        sbn_10_5 = pd.concat([(pd.DataFrame(at_syu_main1.iloc[5, :]))] * 10).rename(columns={5: 'syuboba'})
        sbn_10_6 = pd.concat([(pd.DataFrame(at_syu_main1.iloc[6, :]))] * 10).rename(columns={6: 'syuboba'})
        sbn_10_7 = pd.concat([(pd.DataFrame(at_syu_main1.iloc[7, :]))] * 10).rename(columns={7: 'syuboba'})
        sbn_10_8 = pd.concat([(pd.DataFrame(at_syu_main1.iloc[8, :]))] * 10).rename(columns={8: 'syuboba'})
        sbn_10_9 = pd.concat([(pd.DataFrame(at_syu_main1.iloc[9, :]))] * 10).rename(columns={9: 'syuboba'})
        sbn_10_10 = pd.concat([(pd.DataFrame(at_syu_main1.iloc[10, :]))] * 10).rename(columns={10: 'syuboba'})
        sbn_10_all = pd.concat([sbn_10_0, sbn_10_1, sbn_10_2, sbn_10_3, sbn_10_4, sbn_10_5, sbn_10_6, sbn_10_7, sbn_10_8, sbn_10_9,sbn_10_10])  # 11年分複製
        sbn_10_all = sbn_10_all.reset_index(drop=True)
        # 水平結合⇒これを元データとくっつける

        # データの欠測，補間処理
        def matome_index(matome, index):
            torima = pd.DataFrame((akisyu_box_tanharai3.index.values // 500) + 2011)
            torima = (torima.rename(columns={0: 'datayear'}))
            return pd.concat([matome, index, torima], axis=1)

        akisyu_box_tanharai4 = matome_index(akisyu_box_tanharai3, kn_10_all)
        akisyu_box_fukuharai4 = matome_index(akisyu_box_fukuharai3, kn_10_all)
        akisyu_box_syouritu4 = matome_index(akisyu_box_syouritu3, kn_10_all)
        akisyu_box_fukuritu4 = matome_index(akisyu_box_fukuritu3, kn_10_all)
        achokyo_box_tanharai4 = matome_index(achokyo_box_tanharai3, cn_10_all)
        achokyo_box_fukuharai4 = matome_index(achokyo_box_fukuharai3, cn_10_all)
        achokyo_box_syouritu4 = matome_index(achokyo_box_syouritu3, cn_10_all)
        achokyo_box_fukuritu4 = matome_index(achokyo_box_fukuritu3, cn_10_all)
        abanu_box_tanharai4 = matome_index(abanu_box_tanharai3, bn_10_all)
        abanu_box_fukuharai4 = matome_index(abanu_box_fukuharai3, bn_10_all)
        abanu_box_syouritu4 = matome_index(abanu_box_syouritu3, bn_10_all)
        abanu_box_fukuritu4 = matome_index(abanu_box_fukuritu3, bn_10_all)
        asyu_box_tanharai4 = matome_index(asyu_box_tanharai3, sbn_10_all)
        asyu_box_fukuharai4 = matome_index(asyu_box_fukuharai3, sbn_10_all)
        asyu_box_syouritu4 = matome_index(asyu_box_syouritu3, sbn_10_all)
        asyu_box_fukuritu4 = matome_index(asyu_box_fukuritu3, sbn_10_all)

        # ③どう結合させるのか賢いか？
        alldata = [akisyu_box_tanharai4, akisyu_box_fukuharai4, akisyu_box_syouritu4, akisyu_box_fukuritu4,
                   achokyo_box_tanharai4, achokyo_box_fukuharai4, achokyo_box_syouritu4, achokyo_box_fukuritu4,
                   abanu_box_tanharai4, abanu_box_fukuharai4, abanu_box_syouritu4, abanu_box_fukuritu4,
                   asyu_box_tanharai4, asyu_box_fukuharai4, asyu_box_syouritu4, asyu_box_fukuritu4]  # 4mainの勝率，回収率をまとめる

        for z in range(len(alldata)):  # 16個分
            print(z)
            torima_maindata = alldata[z].iloc[:, 0:len(alldata[z].columns) - 2]  # 列取り出し
            # どのindex使うか
            if 0 <= z < 4:  # 騎手
                ifdata = indexnum10
            elif 4 <= z < 8:  # 調教
                ifdata = indexnum20
            elif 8 <= z < 12:  # 馬主
                ifdata = indexnum30
            else:  # 種牡馬
                ifdata = indexnum40

            torima_indexdata = ifdata.iloc[:, 1:len(ifdata.columns)]  # 列取り出し 1:268
            def_motodata = pd.DataFrame(index=range(len(moto_2010)),
                                        columns=range(len(torima_indexdata.columns)))  # 空データを作成 914907×267

            # indexdata 5500*267の全セルに対してfor文を回す itertoolsを使えばfor2つが1つで済む ここエラー
            for i, j in itertools.product(range(len(torima_indexdata)), range(len(torima_indexdata.columns))):  # 5500*267
                toridashi_data = torima_indexdata.iloc[i, j]  # 行データが格納されているlistを取り出し
                for k in range(len(toridashi_data)):  # list内のデータ数だけ実行
                    def_motodata.iloc[toridashi_data[k], j] = torima_maindata.iloc[i, j]  # TODO ここが時間かかる numpyにする？
            # 2011~2020年の合計10年分のデータを使用する
            # index振って，DBに格納
            def_motodata = def_motodata.reset_index()
            conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
            cursor = conn.cursor()  # データベースを操作できるようにする
            def_motodata.to_sql(str(z) + "Tokutyo_data_new", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
            cursor.close()  # データベースの操作を終了する
            conn.commit()  # 変更をデータベースに保存
            conn.close()  # データベースを閉じる

        process_time = time.time() - start
        print(process_time / 60)  #


# classの実行
# target_encoding.output()

# ④stan用データ作成class
# region target_encoding class
class data_for_stan:
    @staticmethod
    def output():
        """
            stan用のcsvファイルを出力する関数
            Parameters:
            -----------

            Returns:
            -----------
            data_for_stan : csv
                 stan用データファイルをcsvに出力（Rで使用）
             """
        start = time.time()
        # 元データをpostgreから取得---------------------------------------------------------------------
        # DBの初期設定
        DATABASE = 'postgresql'
        USER = 'postgres'
        PASSWORD = 'taku0703'
        HOST = 'localhost'
        PORT = '5432'
        DB_NAME = 'everydb2'
        CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする
        # postgreからpandasに出力するデータを指定するSQL
        sql_moto = 'SELECT * FROM public."df_moto" ORDER BY index ASC;'  # 実行SQL
        # DBのデータをpandasで取得
        moto_df = pd.read_sql(sql_moto, conn)  # sql:実行したいsql，conn:対象のdb名
        ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる

        # データの前処理
        moto_df = moto_df.loc[:,['index', 'year', 'monthday', 'jyocd', 'trackcd', 'ID', 'kakuteijyuni', 'kettonum', 'kisyuryakusyo']]
        # 初期入力
        year_list = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
        month_list = [1, 4, 7, 10]
        babatra_list = [0, 1]  # 芝orダート

        for year_v in range(len(year_list)):
            year = year_list[year_v]
            for month_v in range(len(month_list)):
                month = month_list[month_v]
                for babatra_v in range(len(babatra_list)):
                    babatra = babatra_list[babatra_v]  # 0：芝,1：ダート,芝10-22,ダート23-26
                    # 処理開始
                    if month == 1:
                        year_low = year - 1
                        year_high = year - 1
                        month_low = month
                        month_high = 12
                    else:
                        year_low = year - 1
                        year_high = year
                        month_low = month
                        month_high = month - 1

                    if babatra == 0:
                        babatra_low = 10
                        babatra_high = 22
                    else:
                        babatra_low = 23
                        babatra_high = 26
                    # データフィルタリング
                    n_in = moto_df.copy()
                    n_in['monthday'] = n_in['monthday'].str[0:2]
                    n_in['monthday'] = n_in['year'] + n_in['monthday']
                    n_in['monthday'] = pd.to_numeric(n_in["monthday"], errors='coerce')
                    # 0をつける処理
                    if month_low == 1 or month_low == 4 or month_low == 7:
                        month_low = '0' + str(month_low)
                    if month_low == '04' or month_low == '07' or month_low == 10:
                        month_high = '0' + str(month_high)
                    n_in = n_in[((int(str(year_low) + str(month_low)) <= n_in['monthday'])
                                 & (n_in['monthday'] <= int(str(year_high) + str(month_high))))]
                    n_in['jyocd'] = pd.to_numeric(n_in["jyocd"], errors='coerce')
                    n_in = n_in[((1 <= n_in['jyocd']) & (n_in['jyocd'] <= 10))]  # 中央
                    n_in['trackcd'] = pd.to_numeric(n_in["trackcd"], errors='coerce')
                    n_in = n_in[((babatra_low <= n_in['trackcd']) & (n_in['trackcd'] <= babatra_high))]
                    n_in = n_in.reset_index(drop=True)  # index振りなおす
                    n_in['year'] = n_in['year'].astype(str)
                    n_in['jyocd'] = n_in['jyocd'].astype(str)
                    n_in['trackcd'] = n_in['trackcd'].astype(str)
                    n_in = n_in.loc[:, ['ID', 'kakuteijyuni', 'kettonum', 'kisyuryakusyo']]  # ベイズモデリングに必要なデータだけ取り出し
                    n_in['kakuteijyuni'] = n_in['kakuteijyuni'].astype(int)
                    df_new = n_in.rename(columns={'ID': 'RaceID', 'kakuteijyuni': 'OoA', 'kettonum': 'horseID', 'kisyuryakusyo': 'jockeyID'})
                    # 中止の馬は削除する，中止の場合の強さははかれないため
                    df_new = df_new[df_new['OoA'] != 0]
                    # 同着の馬は順位を1ずらし，順位を昇順にする,データ振りなおし
                    df0 = pd.DataFrame(index=[], columns=['RaceID', 'OoA', 'horseID', 'jockeyID'])
                    i = 0
                    for raceID, sdf in df_new.groupby('RaceID'):
                        if len(sdf) >= 5:  # 5頭以上なら
                            i = i + 1
                            sdf = sdf.sort_values('OoA')  # 着順ソート
                            if any(sdf.duplicated(subset='OoA')):  # 重複あれば 20476行目重複
                                sdf.loc[:, 'OoA'] = np.arange(1, len(sdf) + 1)
                            sdf['RaceID'] = i
                            df0 = df0.append(sdf, ignore_index=True)
                    # 血統番号を振りなおす→ここで血統番号と騎手IDの対応表作っておく
                    df0_hozon = df0.loc[:, ['horseID', 'jockeyID']]
                    from sklearn import preprocessing
                    le = preprocessing.LabelEncoder()  # LabelEncoder()は，文字列や数値で表されたラベルを，0~(ラベル種類数-1)までの数値に変換してくれるもの
                    le.fit(df0['horseID'])
                    df0['horseID'] = le.transform(df0['horseID'])
                    df0['horseID'] = df0['horseID'] + 1
                    le.fit(df0['jockeyID'])
                    df0['jockeyID'] = le.transform(df0['jockeyID'])
                    df0['jockeyID'] = df0['jockeyID'] + 1

                    # 対応表保存
                    df0_hozon = pd.concat([df0_hozon, df0.loc[:, ['horseID', 'jockeyID']]], axis=1)  # 横方向の連結
                    # indexを1はじまりにする
                    df0.index = np.arange(1, len(df0) + 1)

                    # CSVで出力
                    import os  # フォルダ作成用
                    fold_name = 'stan'
                    fold_name = 'moto1'
                    fold_name1 = 'hikaku1'
                    # 日にちでフォルダ作成
                    new_path = 'data_forR\stan\{}'.format(fold_name)
                    new_path1 = 'data_forR\stan\{}'.format(fold_name1)
                    stanlabel = 'stan' + str(int(year)) + '-' + str(int(month)) + '-' + str(int(babatra))
                    complabel = 'comp' + str(int(year)) + '-' + str(int(month)) + '-' + str(int(year_low)) + '-' + str(int(month_low)) + '-' \
                                + str(int(year_high)) + '-' + str(int(month_high)) + '-' + str(int(babatra))
                    if not os.path.exists(new_path):  # ディレクトリがなかったら
                        os.mkdir(new_path)  # 作成したいフォルダ名を作成
                    if not os.path.exists(new_path1):  # ディレクトリがなかったら
                        os.mkdir(new_path1)  # 作成したいフォルダ名を作成
                    # csv出力
                    csv_name_stan = new_path + '\{}.csv'.format(stanlabel)
                    csv_name_comp = new_path1 + '\{}.csv'.format(complabel)
                    df0.to_csv(csv_name_stan, encoding='utf-8', index=False)  # utf-8-sigボムあり，utf-8-なし
                    df0_hozon.to_csv(csv_name_comp, encoding='utf-8', index=False)  # utf-8-sigボムあり，utf-8-なし

        process_time = time.time() - start
        print(process_time / 60)  # 8min

# classの実行
# data_for_stan.output()

# ⑤inputデータ作成class⇒LGBMに入力するデータを作成する。過去6走データ。
# ⑥LGBM class⇒LGBMで各馬の勝率を算出するclass。その勝率をもとにシミュレーション行う。