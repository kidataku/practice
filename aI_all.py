# AI_all 競馬予測用プログラムをすべてまとめてここに
# TODO Output.moto()の実行 fuku@ayなおすため

# 20250624保存　リファクタリング前のもの


# 1.ライブラリの読み込み
# region ライブラリの読み込み

# 標準ライブラリ
import os
import time
import datetime
import itertools

# サードパーティライブラリ
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error, r2_score
import category_encoders as ce
import psycopg2
from sqlalchemy import create_engine

# endregion


# 2.元データclass⇒特徴量作成用の元データを作る。Rstan用データ機能もここに。
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
            特徴量作成用に様々な元データをひとまとめにしたものをDBに出力する
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
        # DBのデータをpandasで取得
        n_uma_pro = pd.read_sql(sql1, conn)  # sql:実行したいsql，conn:対象のdb名
        n_uma_race = pd.read_sql(sql2, conn)  # sql:実行したいsql，conn:対象のdb名
        n_race = pd.read_sql(sql3, conn)  # sql:実行したいsql，conn:対象のdb名
        n_harai = pd.read_sql(sql4, conn)  # sql:実行したいsql，conn:対象のdb名
        ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる

        print('finished connection of DB line68')

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
        n_uma_pro_matome = n_uma_pro.loc[:,['bamei', 'ketto3infobamei1', 'ketto3infobamei2', 'ketto3infobamei3',
        'ketto3infobamei4', 'ketto3infobamei5', 'ketto3infobamei6']] # 馬名，父名，母名，父父，父母，母父，母母を追加　20220911※
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
        fathername_list2 = list(n_uma_pro_matome['ketto3infobamei2']) # 20220911追加
        fathername_list3 = list(n_uma_pro_matome['ketto3infobamei3']) # 20220911追加
        fathername_list4 = list(n_uma_pro_matome['ketto3infobamei4']) # 20220911追加
        fathername_list5 = list(n_uma_pro_matome['ketto3infobamei5']) # 20220911追加
        fathername_list6 = list(n_uma_pro_matome['ketto3infobamei6']) # 20220911追加
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
        a_gradecd, a_syubetu, a_jyokencd1, a_jyokencd2, a_jyokencd3, a_jyokencd4, a_jyokencd5, a_kyori, a_trackcd, a_tenkocd, a_sibababacd, a_dirtbabacd, a_kigocd, \
            a_father,a_father_2,a_father_3,a_father_4,a_father_5,a_father_6 = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [] #20220911追加
        # raceデータをlistに格納し高速化
        a_lap1, a_lap2, a_lap3, a_lap4, a_lap5, a_lap6, a_lap7, a_lap8, a_lap9, a_lap10, a_lap11, a_lap12, a_lap13, a_lap14, a_lap15, a_lap16, a_lap17, a_lap18 = \
            [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
        # raceデータをlistに格納し高速化
        a_hasso, a_syussou, a_corner1, a_syukaisu1, a_jyuni1, a_corner2, a_syukaisu2, a_jyuni2, a_corner3, a_syukaisu3, a_jyuni3, a_corner4, a_syukaisu4, a_jyuni4, a_ryakusyo6 = \
            [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
        # haraiデータをlistに格納し高速化
        a_tanuma1, a_tanpay1, a_tanuma2, a_tanpay2, a_tanuma3, a_tanpay3 = [], [], [], [], [], []
        a_uma1, a_pay1, a_uma2, a_pay2, a_uma3, a_pay3, a_uma4, a_pay4, a_uma5, a_pay5 = [], [], [], [], [], [], [], [], [], []
        
        print('finished to list line194')

        # 行番号を探す関数を定義
        def my_index(l, x, default=np.nan):
            if x in l:  # Lにxがあれば
                return l.index(x)  # 一致するデータがあるときはindexを返す
            else:
                return default  # ないときはNaNを返す
        # for文でデータを抽出
        for i in range(len(matome_data)):
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
                moji_str14 = moji_str14_2 = moji_str14_3 = moji_str14_4 = moji_str14_5 = moji_str14_6 = np.nan # 20220911追加
            else:
                moji_str14 = fathername_list[idx_father]
                moji_str14_2 = fathername_list2[idx_father] # 20220911追加
                moji_str14_3 = fathername_list3[idx_father] # 20220911追加
                moji_str14_4 = fathername_list4[idx_father] # 20220911追加
                moji_str14_5 = fathername_list5[idx_father] # 20220911追加
                moji_str14_6 = fathername_list6[idx_father] # 20220911追加
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
            a_father_2 += [moji_str14_2] # 20220911追加
            a_father_3 += [moji_str14_3] # 20220911追加
            a_father_4 += [moji_str14_4] # 20220911追加
            a_father_5 += [moji_str14_5] # 20220911追加
            a_father_6 += [moji_str14_6] # 20220911追加
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
        # データの結合 20220911追加
        merge = pd.DataFrame(
            data={'gradecd': a_gradecd, 'syubetu': a_syubetu, 'jyokencd1': a_jyokencd1, 'jyokencd2': a_jyokencd2,
                  'jyokencd3': a_jyokencd3, 'jyokencd4': a_jyokencd4, 'jyokencd5': a_jyokencd5, 'kyori': a_kyori, 'trackcd': a_trackcd,
                  'tenkocd': a_tenkocd, 'sibababacd': a_sibababacd, 'dirtbabacd': a_dirtbabacd, 'kigocd': a_kigocd,
                  'father': a_father,'mother': a_father_2,'father_f': a_father_3,'father_m': a_father_4,'mother_f': a_father_5,'mother_m': a_father_6,
                  'lap1': a_lap1, 'lap2': a_lap2, 'lap3': a_lap3, 'lap4': a_lap4, 'lap5': a_lap5,
                  'lap6': a_lap6, 'lap7': a_lap7, 'lap8': a_lap8, 'lap9': a_lap9, 'lap10': a_lap10, 'lap11': a_lap11,
                  'lap12': a_lap12, 'lap13': a_lap13, 'lap14': a_lap14, 'lap15': a_lap15, 'lap16': a_lap16, 'lap17': a_lap17,
                  'lap18': a_lap18, 'hasso': a_hasso, 'syussou': a_syussou, 'corner1': a_corner1, 'syukaisu1': a_syukaisu1, 'jyuni1': a_jyuni1,
                  'corner2': a_corner2, 'syukaisu2': a_syukaisu2, 'jyuni2': a_jyuni2, 'corner3': a_corner3, 'syukaisu3': a_syukaisu3, 'jyuni3': a_jyuni3,
                  'corner4': a_corner4, 'syukaisu4': a_syukaisu4, 'jyuni4': a_jyuni4, 'ryakusyo6': a_ryakusyo6, 'tanuma1': a_tanuma1, 'tanpay1': a_tanpay1,
                  'tanuma2': a_tanuma2, 'tanpay2': a_tanpay2, 'tanuma3': a_tanuma3, 'tanpay3': a_tanpay3, 'fukuuma1': a_uma1, 'fukupay1': a_pay1,
                  'fukuuma2': a_uma2, 'fukupay2': a_pay2, 'fukuuma3': a_uma3, 'fukupay3': a_pay3, 'fukuuma4': a_uma4, 'fukupay4': a_pay4, 'fukuuma5': a_uma5, 'fukupay5': a_pay5},
            columns=['gradecd', 'syubetu', 'jyokencd1', 'jyokencd2', 'jyokencd3', 'jyokencd4', 'jyokencd5', 'kyori', 'trackcd',
                     'tenkocd', 'sibababacd', 'dirtbabacd', 'kigocd', 'father', 'mother', 'father_f', 'father_m', 'mother_f', 'mother_m', 'lap1', 'lap2', 'lap3', 'lap4',
                     'lap5', 'lap6', 'lap7', 'lap8', 'lap9', 'lap10', 'lap11', 'lap12', 'lap13', 'lap14', 'lap15', 'lap16', 'lap17', 'lap18',
                     'hasso', 'syussou', 'corner1', 'syukaisu1', 'jyuni1', 'corner2', 'syukaisu2', 'jyuni2', 'corner3', 'syukaisu3', 'jyuni3',
                     'corner4', 'syukaisu4', 'jyuni4', 'ryakusyo6', 'tanuma1', 'tanpay1', 'tanuma2', 'tanpay2', 'tanuma3', 'tanpay3',
                     'fukuuma1', 'fukupay1', 'fukuuma2', 'fukupay2', 'fukuuma3', 'fukupay3', 'fukuuma4', 'fukupay4', 'fukuuma5', 'fukupay5'])

        saigo = pd.concat([matome_data, merge], axis=1)  # 水平結合
        saigo = saigo.reset_index() # index与える

        print('finished crating saigo line388')

        # 5分前データ結合処理 36min------------------------------------------
        a_index, a_happyotime, a_umaban, a_tanodds, a_tanninki, a_fukuoddslow, a_fukuoddshigh, a_fukuninki = [], [], [], [], [], [], [], [] # 20220911追加
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
                SQL = "SELECT year,monthday,jyocd,kaiji,nichiji,racenum,happyotime,umaban,tanodds,tanninki,fukuoddslow,fukuoddshigh,fukuninki FROM public.n_jodds_tanpuku WHERE year='{0}' AND jyocd='{1}';".format(year, jyocd) #20220911追加
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
                            list_fukuoddslow = list(n_tanodds_3['fukuoddslow']) #20220911追加
                            list_fukuoddshigh = list(n_tanodds_3['fukuoddshigh']) #20220911追加
                            list_fukuninki = list(n_tanodds_3['fukuninki']) #20220911追加

                            a_index += list_index
                            a_happyotime += list_happyotime
                            a_umaban += list_umaban
                            a_tanodds += list_tanodds
                            a_tanninki += list_tanninki
                            a_fukuoddslow += list_fukuoddslow #20220911追加
                            a_fukuoddshigh += list_fukuoddshigh #20220911追加
                            a_fukuninki += list_fukuninki #20220911追加
        # このリストを結合
        df_odds = pd.DataFrame({'index': a_index, 'happyotime': a_happyotime, 'a_umaban': a_umaban, 'tanodds': a_tanodds, 'tanninki': a_tanninki,
        'fukuoddslow': a_fukuoddslow, 'fukuoddshigh': a_fukuoddshigh, 'fukuninki': a_fukuninki}) #20220911追加
        df_odds = df_odds.sort_values('index')  # 昇順で並べ替え
        df_odds.index = df_odds['index']  # 列のindexデータを本当のindexにする
        data = pd.DataFrame(index=range(len(saigo)))  # 結合のために0～すべてのデータ元データを作成
        df_tempo = pd.concat([data, df_odds], axis=1)  # 結合のためのデータを作成
        df_last = pd.concat([saigo, df_tempo.loc[:, ['happyotime', 'a_umaban', 'tanodds', 'tanninki','fukuoddslow','fukuoddshigh','fukuninki']]], axis=1)  # そして結合 20220911追加

        print('finished crating df_last line458')

        # DBへ出力
        # データpostgreへ
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする
        df_last.to_sql("df_moto_test", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
        # -------------実行ここまで
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる

        process_time = time.time() - start
        print(process_time / 60)  # 248min
# endregion

# classの実行
# Output.moto()







# pickleファイルに出力する場合はこれ。
# pd.to_pickle(df_matome, "arr.pkl")#保存
# hoge = pd.read_pickle("arr.pkl") #読み出し

# 3-1：スピード指数class⇒スピード指数を作成する。
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
            スピード指数をDBに出力
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
        sql_moto = 'SELECT * FROM public."df_moto_test" ORDER BY index ASC;'  # 実行SQL 払い戻し
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
        print(process_time / 60)  # 16.6min 20220917
# endregion

# classの実行
# speed_index.calclulate()

# 3-2：スピード指数class⇒スピード指数を出力する
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

# 4-1stan用データ作成class
# region data_for_stan class
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
        sql_moto = 'SELECT * FROM public."df_moto_test" ORDER BY index ASC;'  # 実行SQL
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
# endregion

# classの実行
# data_for_stan.output()

# 4-2stan用データ結合class stanデータ同じ値が入ってきてないか確認する。具体的にはキアロスクーロの20200412と20200425で同じのが入ってないか確認する。
# region mix_stan class
class mix_stan:
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
        sql_moto = 'SELECT * FROM public."df_moto_test" ORDER BY index ASC;'  # 実行SQL
        # DBのデータをpandasで取得
        moto_df0 = pd.read_sql(sql_moto, conn)  # sql:実行したいsql，conn:対象のdb名
        ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる
        # データの前処理
        start = time.time()
        moto_df = moto_df0.loc[:, ['index', 'year', 'monthday', 'jyocd', 'trackcd', 'ID', 'kakuteijyuni', 'kettonum', 'kisyuryakusyo']]
        # 初期入力
        year_list = [2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
        month_list = [1, 4, 7, 10]
        babatra_list = [0, 1]  # 芝orダート
        # 格納list
        horse_power_list = []
        jockey_power_list = []
        n_in_index_list = []
        # forで格納していく
        for year_v in range(len(year_list)):
            year = year_list[year_v]
            for month_v in range(len(month_list)):
                month = month_list[month_v]
                for babatra_v in range(len(babatra_list)):
                    babatra = babatra_list[babatra_v]  # 0：芝,1：ダート,芝10-22,ダート23-26
                    # 処理開始
                    year_low = year
                    year_high = year
                    month_low = month
                    month_high = month + 2

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
                        month_high = '0' + str(month_high)
                    n_in = n_in[((int(str(year_low) + str(month_low)) <= n_in['monthday'])
                                 & (n_in['monthday'] <= int(str(year_high) + str(month_high))))]
                    n_in['jyocd'] = pd.to_numeric(n_in["jyocd"], errors='coerce')
                    n_in = n_in[((1 <= n_in['jyocd']) & (n_in['jyocd'] <= 10))]  # 中央
                    n_in['trackcd'] = pd.to_numeric(n_in["trackcd"], errors='coerce')
                    n_in = n_in[((babatra_low <= n_in['trackcd']) & (n_in['trackcd'] <= babatra_high))]
                    # n_in = n_in.reset_index(drop=True)  # index振りなおす
                    n_in = n_in.loc[:, ['index', 'kettonum', 'kisyuryakusyo']]  # ベイズモデリングに必要なデータだけ取り出し
                    # stanデータの前処理
                    if month == 1:
                        year_low1 = year - 1
                        year_high1 = year - 1
                        month_low1 = month
                        month_high1 = 12
                    else:
                        year_low1 = year - 1
                        year_high1 = year
                        month_low1 = month
                        month_high1 = month - 1

                    if month_low1 == 1 or month_low1 == 4 or month_low1 == 7:
                        month_low1 = '0' + str(month_low1)
                    if month_low1 == '04' or month_low1 == '07' or month_low1 == 10:
                        month_high1 = '0' + str(month_high1)

                    fold_name = 'moto'
                    fold_name1 = 'hikaku'
                    fold_name2 = 'output'
                    # 日にちでフォルダ作成
                    new_path = 'data_forR\stan\{}'.format(fold_name)
                    new_path1 = 'data_forR\stan\{}'.format(fold_name1)
                    new_path2 = 'data_forR\{}'.format(fold_name2)
                    stanlabel = 'stan' + str(int(year)) + '-' + str(int(month)) + '-' + str(int(babatra))
                    complabel = 'comp' + str(int(year)) + '-' + str(int(month)) + '-' + str(int(year_low1)) + '-' + str(int(month_low1)) + '-' \
                                + str(int(year_high1)) + '-' + str(int(month_high1)) + '-' + str(int(babatra))
                    outputlabel = 'stan_output' + str(int(year)) + '-' + str(int(month)) + '-' + str(int(babatra))
                    csv_name_stan = new_path + '\{}.csv'.format(stanlabel)
                    csv_name_comp = new_path1 + '\{}.csv'.format(complabel)
                    csv_name_out = new_path2 + '\{}.txt'.format(outputlabel)
                    df_moto = pd.read_csv(csv_name_stan)
                    df_hikaku = pd.read_csv(csv_name_comp)
                    data_output = pd.read_table(csv_name_out, 'r')  # 区切りいれる
                    data_output['name'] = data_output['\tmean\tse_mean\tsd\tX2.5.\tX25.\tX50.\tX75.\tX97.5.\tn_eff\tRhat'].str.split(pat='\t', expand=True)[0]
                    data_output['mean'] = data_output['\tmean\tse_mean\tsd\tX2.5.\tX25.\tX50.\tX75.\tX97.5.\tn_eff\tRhat'].str.split(pat='\t', expand=True)[1]
                    data_output = data_output.drop('\tmean\tse_mean\tsd\tX2.5.\tX25.\tX50.\tX75.\tX97.5.\tn_eff\tRhat', axis=1)
                    df_horse = df_hikaku.loc[:, ['horseID', 'horseID.1']]
                    df_jockey = df_hikaku.loc[:, ['jockeyID', 'jockeyID.1']]
                    df_horse = df_horse.drop_duplicates()
                    df_jockey = df_jockey.drop_duplicates()
                    df_horse = df_horse.sort_values('horseID.1')  # 昇順で並べ替え
                    df_jockey = df_jockey.sort_values('jockeyID.1')  # 昇順で並べ替え
                    df_horse = df_horse.reset_index(drop=True)  # index振りなおす
                    df_jockey = df_jockey.reset_index(drop=True)  # index振りなおす
                    df_horse['horse_power'] = data_output['mean'][data_output['name'].str.contains('mu_h')]
                    df_jockey['jockey_power'] = data_output['mean'][data_output['name'].str.contains('mu_j')].reset_index(drop=True)
                    df_horse['horse_power'] = df_horse['horse_power'].astype('float16')
                    df_jockey['jockey_power'] = df_jockey['jockey_power'].astype('float16')
                    df_horse = df_horse.drop(columns='horseID.1')
                    df_jockey = df_jockey.drop(columns='jockeyID.1')
                    # listの準備
                    df_horseID_list = list(df_horse['horseID'])  # レースIDをlistで取得
                    df_jockeyID_list = list(df_jockey['jockeyID'])  # レースIDをlistで取得
                    n_in_horseID_list = list(n_in['kettonum'])  # レースIDをlistで取得
                    n_in_jockeyID_list = list(n_in['kisyuryakusyo'])  # レースIDをlistで取得
                    n_in_column_list = n_in['index'].tolist()

                    for i in range(len(n_in)):
                        df_horse1 = df_horse[(df_horse['horseID'] == int(n_in_horseID_list[i]))]
                        df_jockey1 = df_jockey[(df_jockey['jockeyID'] == n_in_jockeyID_list[i])]
                        horse_power_list += list(df_horse1.horse_power if df_horse1.empty != 1 else pd.Series(-1000))
                        jockey_power_list += list(df_jockey1.jockey_power if df_jockey1.empty != 1 else pd.Series(-1000))
                        n_in_index_list += list(pd.Series(n_in_column_list[i]))

        # 元データと結合
        data = pd.DataFrame(index=range(len(moto_df)))  # くっつけるために0～すべてのデータ元データを作成
        tempo_new = pd.DataFrame(data={'nindex': n_in_index_list, 'horse_p': horse_power_list, 'jockey_p': jockey_power_list},columns=['nindex', 'horse_p', 'jockey_p'])
        df_tempo_1 = tempo_new.set_index('nindex')
        appendpower_df = pd.concat([data, df_tempo_1], axis=1)
        appendpower_df = appendpower_df.replace(-1000, np.nan)

        moto_df0 = pd.concat([moto_df0, appendpower_df], axis=1)
        # データpostgreへ
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする
        moto_df0.to_sql("df_moto_test", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
        # -------------実行ここまで
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる

        process_time = time.time() - start
        print(process_time / 60)  # 10min
# endregion

# classの実行
# mix_stan.output()

# 5-1.umaデータ作成class umaデータ作成のための過去20走データ作成する。
# region uma_data_moto class
class uma_data_moto:
    @staticmethod
    def output():
        # pd.set_option('display.max_columns', 200)
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
        sql_moto = 'SELECT * FROM public."df_moto_test" ORDER BY index ASC;'  # 実行SQL
        # スピード指数データ
        sql50 = 'SELECT * FROM public."speed_index" ORDER BY index ASC;'  # 教師データ
        # DBのデータをpandasで取得
        moto_df = pd.read_sql(sql_moto, conn)  # sql:実行したいsql，conn:対象のdb名
        spped_from_db = pd.read_sql(sql50, conn)  # sql:実行したいsql，conn:対象のdb名
        ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる
        # データの前処理
        # スピード指数も取り出してデータの結合行う
        moto_df = pd.concat([moto_df, spped_from_db['speed_idx']], axis=1)  # 結合　914907 rows × 38 columns
        moto_df = moto_df.loc[:,
                ['index', 'year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'umaban','kettonum','bamei','horse_p','sexcd','barei','tozaicd','futan',
                'chokyosiryakusyo', 'banusiname', 'kisyuryakusyo', 'jockey_p','bataijyu','time','speed_idx','kakuteijyuni','jyuni4c','odds','ninki',
                'honsyokin','harontimel3','timediff','kyakusitukubun',
                'ID','jyokencd5', 'kyori','trackcd', 'sibababacd', 'dirtbabacd','syussou',
                'father','mother','father_f','father_m','mother_f','mother_m','tanodds',
                'tanuma1', 'tanpay1', 'tanuma2', 'tanpay2', 'tanuma3', 'tanpay3', 'fukuuma1', 'fukupay1', 'fukuuma2', 'fukupay2', 'fukuuma3', 'fukupay3',
                'fukuuma4', 'fukupay4', 'fukuuma5', 'fukupay5']]
        # 上がり3Fを正規化
        # レースを同じレースごとにまとめる
        n_uma_race_a0_1 = moto_df.loc[:,['ID','time','kakuteijyuni','harontimel3']]
        n_uma_race_a0_1 = n_uma_race_a0_1.reset_index() #indexいれないと変にソートされる
        ID_seiki_list = [[] for torima in range(n_uma_race_a0_1['ID'].nunique())]  # testデータをレース単位に区分したものを格納するlist
        mem = 0
        for ID, sdf in n_uma_race_a0_1.groupby('ID'):
            if len(sdf) > 3: # 要素数が4より大きいとき
                sdf['mediantime'] = ((sdf['time'].astype('float16'))/(sdf['time'].astype('float16').median()))
                sdf['meankakuteijyuni'] = ((sdf['kakuteijyuni'].astype('float16'))/(len(sdf)))
                sdf['medianharon3'] = ((sdf['harontimel3'].astype('float16'))/(sdf['harontimel3'].astype('float16').median()))
                ID_seiki_list[mem] = sdf.loc[:,['index','mediantime','meankakuteijyuni','medianharon3']]  # 分割したデータをlistに保存
                mem += 1

        da_all = pd.concat([ID_seiki_list[i] for i in range(mem)],axis=0)
        # 空フレームとたして欠測うめてくっつける
        kara_da_all = pd.DataFrame(index=range(len(moto_df)),columns=['index','mediantime','meankakuteijyuni','medianharon3'])  # 空データを作成 914907×267
        kara_da_all.fillna(0, inplace=True)
        eeureka = kara_da_all+da_all
        eeureka = eeureka.drop(columns='index')
        eeureka = eeureka.astype('str')
        # 元データと結合
        moto_df = pd.concat([moto_df, eeureka], axis=1)  # 結合　914907 rows × 38 columns
        # debug=moto_df[moto_df["ID"] == "2020122709060812"] #確認用，ただしい列になってるかの
        # debug.loc[:,["time","kakuteijyuni","harontimel3","mediantime","meankakuteijyuni","medianharon3"]]

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
        moto_data_2['year'] = moto_data_2['year'].astype(int)  # 確定順位をobjectからintに変換.

        # 特徴量を追加編
        # pandasのデータをfloat型にする　NaNもあるし，float型 競走中止とかは将来的に
        # 型変換と欠測処理　object⇒numericにして欠測はnanで埋める
        moto_data_2['year'] = pd.to_numeric(moto_data_2["year"], errors='coerce')
        # moto_data_2['monthday'] = pd.to_numeric(moto_data_2["monthday"], errors='coerce')
        moto_data_2["jyocd"] = pd.to_numeric(moto_data_2["jyocd"], errors='coerce')
        moto_data_2["kaiji"] = pd.to_numeric(moto_data_2["kaiji"], errors='coerce')
        moto_data_2["nichiji"] = pd.to_numeric(moto_data_2["nichiji"], errors='coerce')
        moto_data_2["racenum"] = pd.to_numeric(moto_data_2["racenum"], errors='coerce')
        moto_data_2['umaban'] = pd.to_numeric(moto_data_2["umaban"], errors='coerce')
        moto_data_2['horse_p'] = pd.to_numeric(moto_data_2["horse_p"], errors='coerce')
        moto_data_2['sexcd'] = pd.to_numeric(moto_data_2["sexcd"], errors='coerce')
        moto_data_2['barei'] = pd.to_numeric(moto_data_2["barei"], errors='coerce')
        moto_data_2['tozaicd'] = pd.to_numeric(moto_data_2["tozaicd"], errors='coerce')
        moto_data_2['futan'] = pd.to_numeric(moto_data_2["futan"], errors='coerce')
        moto_data_2['jockey_p'] = pd.to_numeric(moto_data_2["jockey_p"], errors='coerce')
        moto_data_2['bataijyu'] = pd.to_numeric(moto_data_2["bataijyu"], errors='coerce')
        moto_data_2['time'] = pd.to_numeric(moto_data_2["time"], errors='coerce')
        moto_data_2['speed_idx'] = pd.to_numeric(moto_data_2["speed_idx"], errors='coerce')
        moto_data_2['jyuni4c'] = pd.to_numeric(moto_data_2["jyuni4c"], errors='coerce')
        moto_data_2['ninki'] = pd.to_numeric(moto_data_2["ninki"], errors='coerce')
        moto_data_2['honsyokin'] = pd.to_numeric(moto_data_2["honsyokin"], errors='coerce')
        moto_data_2['harontimel3'] = pd.to_numeric(moto_data_2["harontimel3"], errors='coerce')
        moto_data_2['timediff'] = pd.to_numeric(moto_data_2["timediff"], errors='coerce')
        moto_data_2['kyakusitukubun'] = pd.to_numeric(moto_data_2["kyakusitukubun"], errors='coerce')
        # moto_data_2['ID'] = pd.to_numeric(moto_data_2["ID"], errors='coerce')
        moto_data_2['jyokencd5'] = pd.to_numeric(moto_data_2["jyokencd5"], errors='coerce')
        moto_data_2['kyori'] = pd.to_numeric(moto_data_2["kyori"], errors='coerce')
        moto_data_2['timediff'] = pd.to_numeric(moto_data_2["timediff"], errors='coerce')
        moto_data_2['trackcd'] = pd.to_numeric(moto_data_2["trackcd"], errors='coerce')
        moto_data_2['sibababacd'] = pd.to_numeric(moto_data_2["sibababacd"], errors='coerce')
        moto_data_2['dirtbabacd'] = pd.to_numeric(moto_data_2["dirtbabacd"], errors='coerce')
        moto_data_2['syussou'] = pd.to_numeric(moto_data_2["syussou"], errors='coerce')
        moto_data_2['mediantime'] = pd.to_numeric(moto_data_2["mediantime"], errors='coerce')
        moto_data_2['meankakuteijyuni'] = pd.to_numeric(moto_data_2["meankakuteijyuni"], errors='coerce')
        moto_data_2['medianharon3'] = pd.to_numeric(moto_data_2["medianharon3"], errors='coerce')
        moto_data_2['tan_harai'] = pd.to_numeric(moto_data_2["tan_harai"], errors='coerce')
        moto_data_2['fuku_harai'] = pd.to_numeric(moto_data_2["fuku_harai"], errors='coerce')
        moto_data_2['kakuteijyuni'] = pd.to_numeric(moto_data_2["kakuteijyuni"], errors='coerce')
        moto_data_2['tanodds'] = pd.to_numeric(moto_data_2["tanodds"], errors='coerce')
        moto_2010 = moto_data_2

        #元データの作成
        # 2011年～2020年の中央競馬結果一覧 これに対してデータ集計する 493674 rows × 46 columns
        moto_2010_uma_pre = moto_2010[((moto_2010['year'] >= 2011) & (moto_2010['year'] <= 2020) & (moto_2010['jyocd'] >= 1) & (moto_2010['jyocd'] <= 10))]
        # 馬データ集計のために必要なデータのみのデータフレームを作成する
        # 2011年～2020年の中央競馬結果一覧 これに対してumaデータ集計する 493674 rows × 46 columns
        moto_2010_uma = moto_2010_uma_pre
        # 必要な列だけ抽出
        moto_2010_uma = moto_2010_uma.loc[:,
                ['index', 'year', 'monthday', 'jyocd','umaban','kettonum','bamei','horse_p','sexcd',
                'speed_idx','kyori','trackcd','timediff','jyuni4c','ninki','tanodds','medianharon3','mediantime','meankakuteijyuni',
                'honsyokin','syussou','sibababacd','dirtbabacd','tan_harai','fuku_harai','kakuteijyuni']]
        moto_2010_uma_rename = moto_2010_uma.rename(columns={'index': 'index_moto'}) # indexの名前変える
        chuo_df_col_len = len(moto_2010_uma_rename.columns)  # 特徴量の数
        # pandasをnumpyに変換する,ここからデータを抽出 高速化用
        np_uma_race = np.array(moto_2010_uma_rename)
        np_map_ketto_test2 = np.array(moto_2010_uma_rename['kettonum'])
        np_map_index_moto = np.array(moto_2010_uma_rename['index_moto'])
        # 格納するlist作成
        list_list = [[] for torima in range(chuo_df_col_len * 21)]  # n_uma_race用 対象レース＋過去20レース
        # n1.columns.to_list()

        # DB格納用データ作成編
        # ①馬柱データの作成
        for i in range(len(moto_2010_uma_rename)):  # 2010年からのレースについて馬柱の作成を実行する(493674, 17),10000につき10分⇒493674で493分⇒9時間⇒諸々10時間
            if i % 10000 == 0:
                print(i)
            # ①-①n_uma_raceについての処理　馬データ
            ketto_index = (np.where(np_map_ketto_test2 == np_map_ketto_test2[i]))[0] # 全レース(n_uma_race)から対象の馬のレースが存在する行のindexを全て取得 np.whereはなるべく少ない列でここでかなり短縮できた
            ketto_index_list= list(ketto_index[ketto_index <= i])
            ketto_index_list[0:0] = [-1]* (21-len(ketto_index_list)) # 想定より少ないサンプルしかなかったらそのぶん-1いれる
            if len(ketto_index_list) >= 22: #要素が多いとき，対象＋過去21戦以上のとき
                ketto_index_list = ketto_index_list[-21:] # 21戦にする
            # uma_raceの処理
            data_0 = list(np_uma_race[(ketto_index_list[20])]) if ketto_index_list[20] >= 0 else [np.nan] * chuo_df_col_len  # 0走前のデータを行で取
            data_1 = list(np_uma_race[(ketto_index_list[19])]) if ketto_index_list[19]  >= 0 else [np.nan] * chuo_df_col_len
            data_2 = list(np_uma_race[(ketto_index_list[18])]) if ketto_index_list[18]  >= 0 else [np.nan] * chuo_df_col_len
            data_3 = list(np_uma_race[(ketto_index_list[17])]) if ketto_index_list[17]  >= 0 else [np.nan] * chuo_df_col_len
            data_4 = list(np_uma_race[(ketto_index_list[16])]) if ketto_index_list[16]  >= 0 else [np.nan] * chuo_df_col_len
            data_5 = list(np_uma_race[(ketto_index_list[15])]) if ketto_index_list[15]  >= 0 else [np.nan] * chuo_df_col_len
            data_6 = list(np_uma_race[(ketto_index_list[14])]) if ketto_index_list[14] >= 0 else [np.nan] * chuo_df_col_len  # 0走前のデータを行で取
            data_7 = list(np_uma_race[(ketto_index_list[13])]) if ketto_index_list[13]  >= 0 else [np.nan] * chuo_df_col_len
            data_8 = list(np_uma_race[(ketto_index_list[12])]) if ketto_index_list[12]  >= 0 else [np.nan] * chuo_df_col_len
            data_9 = list(np_uma_race[(ketto_index_list[11])]) if ketto_index_list[11]  >= 0 else [np.nan] * chuo_df_col_len
            data_10 = list(np_uma_race[(ketto_index_list[10])]) if ketto_index_list[10]  >= 0 else [np.nan] * chuo_df_col_len
            data_11 = list(np_uma_race[(ketto_index_list[9])]) if ketto_index_list[9]  >= 0 else [np.nan] * chuo_df_col_len
            data_12 = list(np_uma_race[(ketto_index_list[8])]) if ketto_index_list[8] >= 0 else [np.nan] * chuo_df_col_len  # 0走前のデータを行で取
            data_13 = list(np_uma_race[(ketto_index_list[7])]) if ketto_index_list[7]  >= 0 else [np.nan] * chuo_df_col_len
            data_14 = list(np_uma_race[(ketto_index_list[6])]) if ketto_index_list[6]  >= 0 else [np.nan] * chuo_df_col_len
            data_15 = list(np_uma_race[(ketto_index_list[5])]) if ketto_index_list[5]  >= 0 else [np.nan] * chuo_df_col_len
            data_16 = list(np_uma_race[(ketto_index_list[4])]) if ketto_index_list[4]  >= 0 else [np.nan] * chuo_df_col_len
            data_17 = list(np_uma_race[(ketto_index_list[3])]) if ketto_index_list[3]  >= 0 else [np.nan] * chuo_df_col_len
            data_18 = list(np_uma_race[(ketto_index_list[2])]) if ketto_index_list[2] >= 0 else [np.nan] * chuo_df_col_len  # 0走前のデータを行で取
            data_19 = list(np_uma_race[(ketto_index_list[1])]) if ketto_index_list[1]  >= 0 else [np.nan] * chuo_df_col_len
            data_20 = list(np_uma_race[(ketto_index_list[0])]) if ketto_index_list[0]  >= 0 else [np.nan] * chuo_df_col_len
            data_mix = data_0 + data_1 + data_2 + data_3 + data_4 + data_5 + data_6 + data_7 + data_8 + data_9 + data_10 + data_11 + data_12 + data_13 + data_14 + data_15 + data_16 + data_17 + data_18 + data_19 + data_20
            # 縦になってるlistの要素をdataframe用に分割していく
            for torima in range(chuo_df_col_len * 21):  # 特徴量×6回分（0～5走）ここ時間かかるか
                list_list[torima] += [data_mix[torima]]

        # DB編
        # ②-①Input_Data_UmaデータをDBに格納
        for bango in range(21):  # 0～5走前　ここは手動要素あり
            kasan = chuo_df_col_len * bango  # listのどこからとるか指定
            print(bango)
            cre_data = pd.DataFrame(
                data={str(bango) + 'index_moto': list_list[0 + kasan], str(bango) + 'year': list_list[1 + kasan],
                    str(bango) + 'monthday': list_list[2 + kasan], str(bango) + 'jyocd': list_list[3 + kasan],
                    str(bango) + 'umaban': list_list[4 + kasan],str(bango) + 'kettonum': list_list[5 + kasan],
                    str(bango) + 'bamei': list_list[6 + kasan], str(bango) + 'horse_p': list_list[7 + kasan],
                    str(bango) + 'sexcd': list_list[8 + kasan], str(bango) + 'speed_idx': list_list[9 + kasan],
                    str(bango) + 'kyori': list_list[10 + kasan], str(bango) + 'trackcd': list_list[11 + kasan],
                    str(bango) + 'timediff': list_list[12 + kasan], str(bango) + 'jyuni4c': list_list[13 + kasan],
                    str(bango) + 'ninki': list_list[14 + kasan], str(bango) + 'tanodds': list_list[15 + kasan],
                    str(bango) + 'medianharon3': list_list[16 + kasan], str(bango) + 'mediantime': list_list[17 + kasan],
                    str(bango) + 'meankakuteijyuni': list_list[18 + kasan], str(bango) + 'honsyokin': list_list[19 + kasan],
                    str(bango) + 'syussou': list_list[20 + kasan],str(bango) + 'sibababacd': list_list[21 + kasan],
                    str(bango) + 'dirtbabacd': list_list[22 + kasan],str(bango) + 'tan_harai': list_list[23 + kasan],
                    str(bango) + 'fuku_harai': list_list[24 + kasan],str(bango) + 'kakuteijyuni': list_list[25 + kasan]},
                columns=[str(bango) + 'index_moto', str(bango) + 'year', str(bango) + 'monthday', str(bango) + 'jyocd',
                        str(bango) + 'umaban', str(bango) + 'kettonum', str(bango) + 'bamei',str(bango) + 'horse_p',
                        str(bango) + 'sexcd', str(bango) + 'speed_idx', str(bango) + 'kyori', str(bango) + 'trackcd',
                        str(bango) + 'timediff', str(bango) + 'jyuni4c', str(bango) + 'ninki', str(bango) + 'tanodds',
                        str(bango) + 'medianharon3', str(bango) + 'mediantime', str(bango) + 'meankakuteijyuni', str(bango) + 'honsyokin',
                        str(bango) + 'syussou',str(bango) + 'sibababacd',str(bango) + 'dirtbabacd',
                        str(bango) + 'tan_harai', str(bango) + 'fuku_harai', str(bango) + 'kakuteijyuni'])
            # indexを与える
            cre_data_1 = cre_data.reset_index()
            # データpostgreへ
            conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
            cursor = conn.cursor()  # データベースを操作できるようにする
            cre_data_1.to_sql(str(bango) + "uma_syukei", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
            # -------------実行ここまで
            cursor.close()  # データベースの操作を終了する
            conn.commit()  # 変更をデータベースに保存
            conn.close()  # データベースを閉じる

        process_time = time.time() - start
        print(process_time / 60)  # 431min
# endregion

# classの実行
# uma_data_moto.output()

# 5-2.umaデータ作成する。=target_5data.
# region target_umadata class
class target_umadata:
    @staticmethod
    def output():
        # pd.set_option('display.max_columns', 200)
        start = time.time()
        # ①DB初期設定
        DATABASE = 'postgresql'
        USER = 'postgres'
        PASSWORD = 'taku0703'
        HOST = 'localhost'
        PORT = '5432'
        DB_NAME = 'everydb2'
        CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)
        # ポスグレ接続
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする

        # ②元データの取得　抽出するデータについての条件を決定、抽出データを小さくし、メモリの節約
        sql7 = 'SELECT * FROM public."0Input_Data_Uma_test" ORDER BY index ASC;'  # 教師データ

        sql_0uma = 'SELECT * FROM public."0uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_1uma = 'SELECT * FROM public."1uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_2uma = 'SELECT * FROM public."2uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_3uma = 'SELECT * FROM public."3uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_4uma = 'SELECT * FROM public."4uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_5uma = 'SELECT * FROM public."5uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_6uma = 'SELECT * FROM public."6uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_7uma = 'SELECT * FROM public."7uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_8uma = 'SELECT * FROM public."8uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_9uma = 'SELECT * FROM public."9uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_10uma = 'SELECT * FROM public."10uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_11uma = 'SELECT * FROM public."11uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_12uma = 'SELECT * FROM public."12uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_13uma = 'SELECT * FROM public."13uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_14uma = 'SELECT * FROM public."14uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_15uma = 'SELECT * FROM public."15uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_16uma = 'SELECT * FROM public."16uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_17uma = 'SELECT * FROM public."17uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_18uma = 'SELECT * FROM public."18uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_19uma = 'SELECT * FROM public."19uma_syukei" ORDER BY index ASC;'  # 教師データ
        sql_20uma = 'SELECT * FROM public."20uma_syukei" ORDER BY index ASC;'  # 教師データ
        # read_sql
        uma_syukei_0 = pd.read_sql(sql_0uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_1 = pd.read_sql(sql_1uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_2 = pd.read_sql(sql_2uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_3 = pd.read_sql(sql_3uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_4 = pd.read_sql(sql_4uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_5 = pd.read_sql(sql_5uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_6 = pd.read_sql(sql_6uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_7 = pd.read_sql(sql_7uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_8 = pd.read_sql(sql_8uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_9 = pd.read_sql(sql_9uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_10 = pd.read_sql(sql_10uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_11 = pd.read_sql(sql_11uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_12 = pd.read_sql(sql_12uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_13 = pd.read_sql(sql_13uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_14 = pd.read_sql(sql_14uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_15 = pd.read_sql(sql_15uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_16 = pd.read_sql(sql_16uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_17 = pd.read_sql(sql_17uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_18 = pd.read_sql(sql_18uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_19 = pd.read_sql(sql_19uma, conn)  # sql:実行したいsql，conn:対象のdb名
        uma_syukei_20 = pd.read_sql(sql_20uma, conn)  # sql:実行したいsql，conn:対象のdb名
        n0_u = pd.read_sql(sql7, conn)  # sql:実行したいsql，conn:対象のdb名 列数取得用 TODO 847228 rowsは不変か？
        ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる
        print('finished data acquisition') #9.6G⇒30.3GB
        # %%
        # フラグ用元データの作成
        # 芝・ダ用
        uma_baba_0=uma_syukei_0['0sibababacd'] #要素の個数0.0,242397,1.0,199390,2.0,34579,3.0,13026,4.0,3971,NaN,311
        uma_baba_1=uma_syukei_1['1sibababacd']
        uma_baba_2=uma_syukei_2['2sibababacd']
        uma_baba_3=uma_syukei_3['3sibababacd']
        uma_baba_4=uma_syukei_4['4sibababacd']
        uma_baba_5=uma_syukei_5['5sibababacd']
        uma_baba_6=uma_syukei_6['6sibababacd']
        uma_baba_7=uma_syukei_7['7sibababacd']
        uma_baba_8=uma_syukei_8['8sibababacd']
        uma_baba_9=uma_syukei_9['9sibababacd']
        uma_baba_10=uma_syukei_10['10sibababacd'] #要素の個数0.0,75296,1.0,73491,2.0,11888,3.0,4422,4.0,1290,NaN,327287
        uma_baba_11=uma_syukei_11['11sibababacd']
        uma_baba_12=uma_syukei_12['12sibababacd']
        uma_baba_13=uma_syukei_13['13sibababacd']
        uma_baba_14=uma_syukei_14['14sibababacd']
        uma_baba_15=uma_syukei_15['15sibababacd']
        uma_baba_16=uma_syukei_16['16sibababacd']
        uma_baba_17=uma_syukei_17['17sibababacd']
        uma_baba_18=uma_syukei_18['18sibababacd']
        uma_baba_19=uma_syukei_19['19sibababacd']
        uma_baba_20=uma_syukei_20['20sibababacd']
        # 馬場用
        uma_babadirt_0=uma_syukei_0['0dirtbabacd'] #要素の個数0.0,245144,1.0,152038,2.0,48933,3.0,29307,4.0,17941,NaN,311
        uma_babadirt_1=uma_syukei_1['1dirtbabacd']
        uma_babadirt_2=uma_syukei_2['2dirtbabacd']
        uma_babadirt_3=uma_syukei_3['3dirtbabacd']
        uma_babadirt_4=uma_syukei_4['4dirtbabacd']
        uma_babadirt_5=uma_syukei_5['5dirtbabacd']
        uma_babadirt_6=uma_syukei_6['6dirtbabacd']
        uma_babadirt_7=uma_syukei_7['7dirtbabacd']
        uma_babadirt_8=uma_syukei_8['8dirtbabacd']
        uma_babadirt_9=uma_syukei_9['9dirtbabacd']
        uma_babadirt_10=uma_syukei_10['10dirtbabacd'] #要素の個数0.0,90113,1.0,47045,2.0,14973,3.0,9127,4.0,5129,NaN,327287
        uma_babadirt_11=uma_syukei_11['11dirtbabacd']
        uma_babadirt_12=uma_syukei_12['12dirtbabacd']
        uma_babadirt_13=uma_syukei_13['13dirtbabacd']
        uma_babadirt_14=uma_syukei_14['14dirtbabacd']
        uma_babadirt_15=uma_syukei_15['15dirtbabacd']
        uma_babadirt_16=uma_syukei_16['16dirtbabacd']
        uma_babadirt_17=uma_syukei_17['17dirtbabacd']
        uma_babadirt_18=uma_syukei_18['18dirtbabacd']
        uma_babadirt_19=uma_syukei_19['19dirtbabacd']
        uma_babadirt_20=uma_syukei_20['20dirtbabacd']
        # 競馬場フラグ用
        uma_jyocd_0=uma_syukei_0['0jyocd'] #1.0,17864,2.0,20171,3.0,33192,4.0,49176,5.0,78088,6.0,70835,7.0,39831,8.0,74551,9.0,70373,10.0,39593
        uma_jyocd_1=uma_syukei_1['1jyocd']
        uma_jyocd_2=uma_syukei_2['2jyocd']
        uma_jyocd_3=uma_syukei_3['3jyocd']
        uma_jyocd_4=uma_syukei_4['4jyocd']
        uma_jyocd_5=uma_syukei_5['5jyocd']
        uma_jyocd_6=uma_syukei_6['6jyocd']
        uma_jyocd_7=uma_syukei_7['7jyocd']
        uma_jyocd_8=uma_syukei_8['8jyocd']
        uma_jyocd_9=uma_syukei_9['9jyocd']
        uma_jyocd_10=uma_syukei_10['10jyocd'] #1.0,5596,2.0,6471,3.0,9514,4.0,14462,5.0,26638,6.0,22797,7.0,13409,8.0,29343,9.0,25328,10.0,12931,NaN,327185
        uma_jyocd_11=uma_syukei_11['11jyocd']
        uma_jyocd_12=uma_syukei_12['12jyocd']
        uma_jyocd_13=uma_syukei_13['13jyocd']
        uma_jyocd_14=uma_syukei_14['14jyocd']
        uma_jyocd_15=uma_syukei_15['15jyocd']
        uma_jyocd_16=uma_syukei_16['16jyocd']
        uma_jyocd_17=uma_syukei_17['17jyocd']
        uma_jyocd_18=uma_syukei_18['18jyocd']
        uma_jyocd_19=uma_syukei_19['19jyocd']
        uma_jyocd_20=uma_syukei_20['20jyocd']
        # 距離フラグ用
        uma_kyori_0=uma_syukei_0['0kyori']# 1000-4250まである，nanなし
        uma_kyori_1=uma_syukei_1['1kyori']
        uma_kyori_2=uma_syukei_2['2kyori']
        uma_kyori_3=uma_syukei_3['3kyori']
        uma_kyori_4=uma_syukei_4['4kyori']
        uma_kyori_5=uma_syukei_5['5kyori']
        uma_kyori_6=uma_syukei_6['6kyori']
        uma_kyori_7=uma_syukei_7['7kyori']
        uma_kyori_8=uma_syukei_8['8kyori']
        uma_kyori_9=uma_syukei_9['9kyori']
        uma_kyori_10=uma_syukei_10['10kyori']# 1000-4250まである，nan 327287
        uma_kyori_11=uma_syukei_11['11kyori']
        uma_kyori_12=uma_syukei_12['12kyori']
        uma_kyori_13=uma_syukei_13['13kyori']
        uma_kyori_14=uma_syukei_14['14kyori']
        uma_kyori_15=uma_syukei_15['15kyori']
        uma_kyori_16=uma_syukei_16['16kyori']
        uma_kyori_17=uma_syukei_17['17kyori']
        uma_kyori_18=uma_syukei_18['18kyori']
        uma_kyori_19=uma_syukei_19['19kyori']
        uma_kyori_20=uma_syukei_20['20kyori']
        # 馬番フラグ用
        uma_umaban_0=uma_syukei_0['0umaban']
        uma_umaban_1=uma_syukei_1['1umaban']
        uma_umaban_2=uma_syukei_2['2umaban']
        uma_umaban_3=uma_syukei_3['3umaban']
        uma_umaban_4=uma_syukei_4['4umaban']
        uma_umaban_5=uma_syukei_5['5umaban']
        uma_umaban_6=uma_syukei_6['6umaban']
        uma_umaban_7=uma_syukei_7['7umaban']
        uma_umaban_8=uma_syukei_8['8umaban']
        uma_umaban_9=uma_syukei_9['9umaban']
        uma_umaban_10=uma_syukei_10['10umaban'] #1-18までほとんどだが99が5個ある。nan 327185
        uma_umaban_11=uma_syukei_11['11umaban']
        uma_umaban_12=uma_syukei_12['12umaban']
        uma_umaban_13=uma_syukei_13['13umaban']
        uma_umaban_14=uma_syukei_14['14umaban']
        uma_umaban_15=uma_syukei_15['15umaban']
        uma_umaban_16=uma_syukei_16['16umaban']
        uma_umaban_17=uma_syukei_17['17umaban']
        uma_umaban_18=uma_syukei_18['18umaban']
        uma_umaban_19=uma_syukei_19['19umaban']
        uma_umaban_20=uma_syukei_20['20umaban']
        # 夏・冬フラグ用
        uma_monthday_0=uma_syukei_0['0monthday'].str[:2]
        uma_monthday_1=uma_syukei_1['1monthday'].str[:2]
        uma_monthday_2=uma_syukei_2['2monthday'].str[:2]
        uma_monthday_3=uma_syukei_3['3monthday'].str[:2]
        uma_monthday_4=uma_syukei_4['4monthday'].str[:2]
        uma_monthday_5=uma_syukei_5['5monthday'].str[:2]
        uma_monthday_6=uma_syukei_6['6monthday'].str[:2]
        uma_monthday_7=uma_syukei_7['7monthday'].str[:2]
        uma_monthday_8=uma_syukei_8['8monthday'].str[:2]
        uma_monthday_9=uma_syukei_9['9monthday'].str[:2]
        uma_monthday_10=uma_syukei_10['10monthday'].str[:2]#01-12まで，nan327185
        uma_monthday_11=uma_syukei_11['11monthday'].str[:2]
        uma_monthday_12=uma_syukei_12['12monthday'].str[:2]
        uma_monthday_13=uma_syukei_13['13monthday'].str[:2]
        uma_monthday_14=uma_syukei_14['14monthday'].str[:2]
        uma_monthday_15=uma_syukei_15['15monthday'].str[:2]
        uma_monthday_16=uma_syukei_16['16monthday'].str[:2]
        uma_monthday_17=uma_syukei_17['17monthday'].str[:2]
        uma_monthday_18=uma_syukei_18['18monthday'].str[:2]
        uma_monthday_19=uma_syukei_19['19monthday'].str[:2]
        uma_monthday_20=uma_syukei_20['20monthday'].str[:2]
        # %%
        # 各フラグの作成
        # 芝・ダflag
        uma_baba_shiba_pre = pd.concat([uma_baba_0,uma_baba_1,uma_baba_2,uma_baba_3,uma_baba_4,uma_baba_5,uma_baba_6,uma_baba_7,uma_baba_8,uma_baba_9,
                                    uma_baba_10,uma_baba_11,uma_baba_12,uma_baba_13,uma_baba_14,uma_baba_15,uma_baba_16,uma_baba_17,uma_baba_18,
                                    uma_baba_19,uma_baba_20],axis=1)
        #1以上は（良，稍重，重，不良）は1にする。未設定・未整備時（地方競馬・海外）の初期値として0混じるがほぼ混じらないはず。
        #芝で1以上ならそれは芝レースということ。0だったらそれはダートのレース。これで芝・ダ判定する。
        uma_baba_shiba = uma_baba_shiba_pre.applymap(lambda x: 1 if x >= 1 else x)
        # 0sibababacd参照してTrue,False決める,未設定・未整備時の初期値として0混じる。
        uma_baba_flag_1=uma_baba_shiba['0sibababacd'] == uma_baba_shiba['1sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる,1==nan is false
        uma_baba_flag_2=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['2sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_3=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['3sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_4=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['4sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_5=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['5sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_6=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['6sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_7=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['7sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_8=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['8sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_9=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['9sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_10=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['10sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_11=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['11sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_12=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['12sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_13=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['13sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_14=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['14sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_15=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['15sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_16=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['16sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_17=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['17sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_18=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['18sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_19=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['19sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_baba_flag_20=uma_baba_shiba['0sibababacd']  == uma_baba_shiba['20sibababacd'] # 数字かけるとFalseは0，Trueは1として扱われる

        # 馬場フラグ
        uma_ryoomo_0=uma_syukei_0['0dirtbabacd']+uma_syukei_0['0sibababacd']
        uma_ryoomo_1=uma_syukei_1['1dirtbabacd']+uma_syukei_1['1sibababacd']
        uma_ryoomo_2=uma_syukei_2['2dirtbabacd']+uma_syukei_2['2sibababacd']
        uma_ryoomo_3=uma_syukei_3['3dirtbabacd']+uma_syukei_3['3sibababacd']
        uma_ryoomo_4=uma_syukei_4['4dirtbabacd']+uma_syukei_4['4sibababacd']
        uma_ryoomo_5=uma_syukei_5['5dirtbabacd']+uma_syukei_5['5sibababacd']
        uma_ryoomo_6=uma_syukei_6['6dirtbabacd']+uma_syukei_6['6sibababacd']
        uma_ryoomo_7=uma_syukei_7['7dirtbabacd']+uma_syukei_7['7sibababacd']
        uma_ryoomo_8=uma_syukei_8['8dirtbabacd']+uma_syukei_8['8sibababacd']
        uma_ryoomo_9=uma_syukei_9['9dirtbabacd']+uma_syukei_9['9sibababacd']
        uma_ryoomo_10=uma_syukei_10['10dirtbabacd']+uma_syukei_10['10sibababacd'] #nan + nan shitemo nanの数は変わらない
        uma_ryoomo_11=uma_syukei_11['11dirtbabacd']+uma_syukei_11['11sibababacd']
        uma_ryoomo_12=uma_syukei_12['12dirtbabacd']+uma_syukei_12['12sibababacd']
        uma_ryoomo_13=uma_syukei_13['13dirtbabacd']+uma_syukei_13['13sibababacd']
        uma_ryoomo_14=uma_syukei_14['14dirtbabacd']+uma_syukei_14['14sibababacd']
        uma_ryoomo_15=uma_syukei_15['15dirtbabacd']+uma_syukei_15['15sibababacd']
        uma_ryoomo_16=uma_syukei_16['16dirtbabacd']+uma_syukei_16['16sibababacd']
        uma_ryoomo_17=uma_syukei_17['17dirtbabacd']+uma_syukei_17['17sibababacd']
        uma_ryoomo_18=uma_syukei_18['18dirtbabacd']+uma_syukei_18['18sibababacd']
        uma_ryoomo_19=uma_syukei_19['19dirtbabacd']+uma_syukei_19['19sibababacd']
        uma_ryoomo_20=uma_syukei_20['20dirtbabacd']+uma_syukei_20['20sibababacd']
        uma_ryoomo_pre = pd.concat([uma_ryoomo_0,uma_ryoomo_1,uma_ryoomo_2,uma_ryoomo_3,uma_ryoomo_4,uma_ryoomo_5,uma_ryoomo_6,uma_ryoomo_7,uma_ryoomo_8,uma_ryoomo_9,
                                    uma_ryoomo_10,uma_ryoomo_11,uma_ryoomo_12,uma_ryoomo_13,uma_ryoomo_14,uma_ryoomo_15,uma_ryoomo_16,uma_ryoomo_17,uma_ryoomo_18,
                                    uma_ryoomo_19,uma_ryoomo_20],axis=1)
        #良は1,1より大きいもの（稍重，重，不良）は2にする,未設定・未整備時の初期値として0混じる。
        uma_ryoomo = uma_ryoomo_pre.applymap(lambda x: 2 if x > 1 else x)
        # 0sibababacd参照してTrue,False決める
        uma_ryoomo_flag_1=uma_ryoomo[0] == uma_ryoomo[1] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_2=uma_ryoomo[0] == uma_ryoomo[2] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_3=uma_ryoomo[0] == uma_ryoomo[3] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_4=uma_ryoomo[0] == uma_ryoomo[4] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_5=uma_ryoomo[0] == uma_ryoomo[5] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_6=uma_ryoomo[0] == uma_ryoomo[6] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_7=uma_ryoomo[0] == uma_ryoomo[7] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_8=uma_ryoomo[0] == uma_ryoomo[8] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_9=uma_ryoomo[0] == uma_ryoomo[9] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_10=uma_ryoomo[0] == uma_ryoomo[10] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_11=uma_ryoomo[0] == uma_ryoomo[11] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_12=uma_ryoomo[0] == uma_ryoomo[12] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_13=uma_ryoomo[0] == uma_ryoomo[13] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_14=uma_ryoomo[0] == uma_ryoomo[14] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_15=uma_ryoomo[0] == uma_ryoomo[15] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_16=uma_ryoomo[0] == uma_ryoomo[16] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_17=uma_ryoomo[0] == uma_ryoomo[17] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_18=uma_ryoomo[0] == uma_ryoomo[18] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_19=uma_ryoomo[0] == uma_ryoomo[19] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_ryoomo_flag_20=uma_ryoomo[0] == uma_ryoomo[20] # 数字かけるとFalseは0，Trueは1として扱われる

        # 競馬場フラグ(中山，東京，etc)
        uma_jyocd_flag_1=uma_jyocd_0 == uma_jyocd_1 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_2=uma_jyocd_0 == uma_jyocd_2 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_3=uma_jyocd_0 == uma_jyocd_3 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_4=uma_jyocd_0 == uma_jyocd_4 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_5=uma_jyocd_0 == uma_jyocd_5 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_6=uma_jyocd_0 == uma_jyocd_6 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_7=uma_jyocd_0 == uma_jyocd_7 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_8=uma_jyocd_0 == uma_jyocd_8 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_9=uma_jyocd_0 == uma_jyocd_9 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_10=uma_jyocd_0 == uma_jyocd_10 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_11=uma_jyocd_0 == uma_jyocd_11 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_12=uma_jyocd_0 == uma_jyocd_12 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_13=uma_jyocd_0 == uma_jyocd_13 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_14=uma_jyocd_0 == uma_jyocd_14 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_15=uma_jyocd_0 == uma_jyocd_15 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_16=uma_jyocd_0 == uma_jyocd_16 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_17=uma_jyocd_0 == uma_jyocd_17 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_18=uma_jyocd_0 == uma_jyocd_18 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_19=uma_jyocd_0 == uma_jyocd_19 # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocd_flag_20=uma_jyocd_0 == uma_jyocd_20 # 数字かけるとFalseは0，Trueは1として扱われる

        # 距離フラグ
        def kyori_cate(x):
            if x <= 1400:
                return 0
            elif x > 1400 and x <= 2200:
                return 1
            elif x > 2200 and x <= 3600:
                return 2
            else:
                return 3
        uma_kyori_pre = pd.concat([uma_kyori_0,uma_kyori_1,uma_kyori_2,uma_kyori_3,uma_kyori_4,uma_kyori_5,uma_kyori_6,uma_kyori_7,uma_kyori_8,uma_kyori_9,
                                    uma_kyori_10,uma_kyori_11,uma_kyori_12,uma_kyori_13,uma_kyori_14,uma_kyori_15,uma_kyori_16,uma_kyori_17,uma_kyori_18,
                                    uma_kyori_19,uma_kyori_20],axis=1)
        # 短距離，中距離，長距離で分類
        uma_kyori = uma_kyori_pre.applymap(kyori_cate)
        # kyori参照してTrue,False決める
        uma_kyori_flag_1=uma_kyori['0kyori'] == uma_kyori['1kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_2=uma_kyori['0kyori'] == uma_kyori['2kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_3=uma_kyori['0kyori'] == uma_kyori['3kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_4=uma_kyori['0kyori'] == uma_kyori['4kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_5=uma_kyori['0kyori'] == uma_kyori['5kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_6=uma_kyori['0kyori'] == uma_kyori['6kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_7=uma_kyori['0kyori'] == uma_kyori['7kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_8=uma_kyori['0kyori'] == uma_kyori['8kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_9=uma_kyori['0kyori'] == uma_kyori['9kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_10=uma_kyori['0kyori'] == uma_kyori['10kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_11=uma_kyori['0kyori'] == uma_kyori['11kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_12=uma_kyori['0kyori'] == uma_kyori['12kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_13=uma_kyori['0kyori'] == uma_kyori['13kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_14=uma_kyori['0kyori'] == uma_kyori['14kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_15=uma_kyori['0kyori'] == uma_kyori['15kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_16=uma_kyori['0kyori'] == uma_kyori['16kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_17=uma_kyori['0kyori'] == uma_kyori['17kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_18=uma_kyori['0kyori'] == uma_kyori['18kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_19=uma_kyori['0kyori'] == uma_kyori['19kyori'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_20=uma_kyori['0kyori'] == uma_kyori['20kyori'] # 数字かけるとFalseは0，Trueは1として扱われる

        # 馬番フラグ
        def umaban_cate(x):
            if x < 9:
                return 1
            elif x >= 9:
                return 2
            else: #nan,99
                return 3
        uma_umaban_pre= pd.concat([uma_umaban_0,uma_umaban_1,uma_umaban_2,uma_umaban_3,uma_umaban_4,uma_umaban_5,uma_umaban_6,uma_umaban_7,uma_umaban_8,uma_umaban_9,
                                    uma_umaban_10,uma_umaban_11,uma_umaban_12,uma_umaban_13,uma_umaban_14,uma_umaban_15,uma_umaban_16,uma_umaban_17,uma_umaban_18,
                                    uma_umaban_19,uma_umaban_20],axis=1)
        # 馬番で分類
        uma_umaban = uma_umaban_pre.applymap(umaban_cate)
        # 馬番で分類
        uma_umaban_flag_1=uma_umaban['0umaban'] == uma_umaban['1umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_2=uma_umaban['0umaban'] == uma_umaban['2umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_3=uma_umaban['0umaban'] == uma_umaban['3umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_4=uma_umaban['0umaban'] == uma_umaban['4umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_5=uma_umaban['0umaban'] == uma_umaban['5umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_6=uma_umaban['0umaban'] == uma_umaban['6umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_7=uma_umaban['0umaban'] == uma_umaban['7umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_8=uma_umaban['0umaban'] == uma_umaban['8umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_9=uma_umaban['0umaban'] == uma_umaban['9umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_10=uma_umaban['0umaban'] == uma_umaban['10umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_11=uma_umaban['0umaban'] == uma_umaban['11umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_12=uma_umaban['0umaban'] == uma_umaban['12umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_13=uma_umaban['0umaban'] == uma_umaban['13umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_14=uma_umaban['0umaban'] == uma_umaban['14umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_15=uma_umaban['0umaban'] == uma_umaban['15umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_16=uma_umaban['0umaban'] == uma_umaban['16umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_17=uma_umaban['0umaban'] == uma_umaban['17umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_18=uma_umaban['0umaban'] == uma_umaban['18umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_19=uma_umaban['0umaban'] == uma_umaban['19umaban'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_umaban_flag_20=uma_umaban['0umaban'] == uma_umaban['20umaban'] # 数字かけるとFalseは0，Trueは1として扱われる

        # 右・左フラグ
        def mawari_cate(x):
            if x == 1 or x == 2 or x == 3 or x == 6 or x == 8 or x == 9 or x == 10 :
                return 0
            elif x == 4 or x == 5 or x == 7:
                return 1
            else: #nan
                return 99
        uma_jyocd_pre = pd.concat([uma_jyocd_0,uma_jyocd_1,uma_jyocd_2,uma_jyocd_3,uma_jyocd_4,uma_jyocd_5,uma_jyocd_6,uma_jyocd_7,uma_jyocd_8,uma_jyocd_9,
                                    uma_jyocd_10,uma_jyocd_11,uma_jyocd_12,uma_jyocd_13,uma_jyocd_14,uma_jyocd_15,uma_jyocd_16,uma_jyocd_17,uma_jyocd_18,
                                    uma_jyocd_19,uma_jyocd_20],axis=1)
        # 右・左周りで分類
        uma_jyocd = uma_jyocd_pre.applymap(mawari_cate)
        # jyocd参照してTrue,False決める
        uma_jyocdb_flag_1=uma_jyocd['0jyocd'] == uma_jyocd['1jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_2=uma_jyocd['0jyocd'] == uma_jyocd['2jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_3=uma_jyocd['0jyocd'] == uma_jyocd['3jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_4=uma_jyocd['0jyocd'] == uma_jyocd['4jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_5=uma_jyocd['0jyocd'] == uma_jyocd['5jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_6=uma_jyocd['0jyocd'] == uma_jyocd['6jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_7=uma_jyocd['0jyocd'] == uma_jyocd['7jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_8=uma_jyocd['0jyocd'] == uma_jyocd['8jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_9=uma_jyocd['0jyocd'] == uma_jyocd['9jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_10=uma_jyocd['0jyocd'] == uma_jyocd['10jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_11=uma_jyocd['0jyocd'] == uma_jyocd['11jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_12=uma_jyocd['0jyocd'] == uma_jyocd['12jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_13=uma_jyocd['0jyocd'] == uma_jyocd['13jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_14=uma_jyocd['0jyocd'] == uma_jyocd['14jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_15=uma_jyocd['0jyocd'] == uma_jyocd['15jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_16=uma_jyocd['0jyocd'] == uma_jyocd['16jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_17=uma_jyocd['0jyocd'] == uma_jyocd['17jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_18=uma_jyocd['0jyocd'] == uma_jyocd['18jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_19=uma_jyocd['0jyocd'] == uma_jyocd['19jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocdb_flag_20=uma_jyocd['0jyocd'] == uma_jyocd['20jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる

        # 平坦・坂フラグ
        def saka_cate(x):
            if x == 1 or x == 2 or x == 3 or x == 4 or x == 8 or x == 10:
                return 0
            elif x == 5 or x == 6 or x == 7 or x == 9:
                return 1
            else: #nan
                return 99
        # 平坦・坂で分類
        uma_jyocd_pre = pd.concat([uma_jyocd_0,uma_jyocd_1,uma_jyocd_2,uma_jyocd_3,uma_jyocd_4,uma_jyocd_5,uma_jyocd_6,uma_jyocd_7,uma_jyocd_8,uma_jyocd_9,
                                    uma_jyocd_10,uma_jyocd_11,uma_jyocd_12,uma_jyocd_13,uma_jyocd_14,uma_jyocd_15,uma_jyocd_16,uma_jyocd_17,uma_jyocd_18,
                                    uma_jyocd_19,uma_jyocd_20],axis=1)
        uma_jyocda = uma_jyocd_pre.applymap(saka_cate)
        # jyocda参照してTrue,False決める
        uma_jyocda_flag_1=uma_jyocda['0jyocd'] == uma_jyocda['1jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_2=uma_jyocda['0jyocd'] == uma_jyocda['2jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_3=uma_jyocda['0jyocd'] == uma_jyocda['3jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_4=uma_jyocda['0jyocd'] == uma_jyocda['4jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_5=uma_jyocda['0jyocd'] == uma_jyocda['5jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_6=uma_jyocda['0jyocd'] == uma_jyocda['6jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_7=uma_jyocda['0jyocd'] == uma_jyocda['7jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_8=uma_jyocda['0jyocd'] == uma_jyocda['8jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_9=uma_jyocda['0jyocd'] == uma_jyocda['9jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_10=uma_jyocda['0jyocd'] == uma_jyocda['10jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_11=uma_jyocda['0jyocd'] == uma_jyocda['11jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_12=uma_jyocda['0jyocd'] == uma_jyocda['12jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_13=uma_jyocda['0jyocd'] == uma_jyocda['13jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_14=uma_jyocda['0jyocd'] == uma_jyocda['14jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_15=uma_jyocda['0jyocd'] == uma_jyocda['15jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_16=uma_jyocda['0jyocd'] == uma_jyocda['16jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_17=uma_jyocda['0jyocd'] == uma_jyocda['17jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_18=uma_jyocda['0jyocd'] == uma_jyocda['18jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_19=uma_jyocda['0jyocd'] == uma_jyocda['19jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_jyocda_flag_20=uma_jyocda['0jyocd'] == uma_jyocda['20jyocd'] # 数字かけるとFalseは0，Trueは1として扱われる

        # 夏冬フラグ ひと手間
        def season_cate(x):
            if int(x)>= 5 and int(x) <= 10:# 夏 5-10
                return 1
            elif int(x)> 0 and int(x) < 5:# 冬 1-4
                return 2
            elif int(x) > 10:# 冬 11,12
                return 2
            else:
                return 0
        uma_monthday_pre = pd.concat([uma_monthday_0,uma_monthday_1,uma_monthday_2,uma_monthday_3,uma_monthday_4,uma_monthday_5,uma_monthday_6,uma_monthday_7,uma_monthday_8,uma_monthday_9,
                                    uma_monthday_10,uma_monthday_11,uma_monthday_12,uma_monthday_13,uma_monthday_14,uma_monthday_15,uma_monthday_16,uma_monthday_17,uma_monthday_18,
                                    uma_monthday_19,uma_monthday_20],axis=1)
        uma_monthday_pre = uma_monthday_pre.fillna(0) #nanを0で埋める
        uma_monthday = uma_monthday_pre.applymap(season_cate)
        # monthday参照してTrue,False決める
        uma_monthday_flag_1=uma_monthday['0monthday'] == uma_monthday['1monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_2=uma_monthday['0monthday'] == uma_monthday['2monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_3=uma_monthday['0monthday'] == uma_monthday['3monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_4=uma_monthday['0monthday'] == uma_monthday['4monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_5=uma_monthday['0monthday'] == uma_monthday['5monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_6=uma_monthday['0monthday'] == uma_monthday['6monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_7=uma_monthday['0monthday'] == uma_monthday['7monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_8=uma_monthday['0monthday'] == uma_monthday['8monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_9=uma_monthday['0monthday'] == uma_monthday['9monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_10=uma_monthday['0monthday'] == uma_monthday['10monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_11=uma_monthday['0monthday'] == uma_monthday['11monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_12=uma_monthday['0monthday'] == uma_monthday['12monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_13=uma_monthday['0monthday'] == uma_monthday['13monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_14=uma_monthday['0monthday'] == uma_monthday['14monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_15=uma_monthday['0monthday'] == uma_monthday['15monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_16=uma_monthday['0monthday'] == uma_monthday['16monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_17=uma_monthday['0monthday'] == uma_monthday['17monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_18=uma_monthday['0monthday'] == uma_monthday['18monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_19=uma_monthday['0monthday'] == uma_monthday['19monthday'] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_monthday_flag_20=uma_monthday['0monthday'] == uma_monthday['20monthday'] # 数字かけるとFalseは0，Trueは1として扱われる

        # 距離延長・短縮
        uma_kyori_0_a=uma_kyori_0-uma_kyori_1
        uma_kyori_1_a=uma_kyori_1-uma_kyori_2
        uma_kyori_2_a=uma_kyori_2-uma_kyori_3
        uma_kyori_3_a=uma_kyori_3-uma_kyori_4
        uma_kyori_4_a=uma_kyori_4-uma_kyori_5
        uma_kyori_5_a=uma_kyori_5-uma_kyori_6
        uma_kyori_6_a=uma_kyori_6-uma_kyori_7
        uma_kyori_7_a=uma_kyori_7-uma_kyori_8
        uma_kyori_8_a=uma_kyori_8-uma_kyori_9
        uma_kyori_9_a=uma_kyori_9-uma_kyori_10
        uma_kyori_10_a=uma_kyori_10-uma_kyori_11
        uma_kyori_11_a=uma_kyori_11-uma_kyori_12
        uma_kyori_12_a=uma_kyori_12-uma_kyori_13
        uma_kyori_13_a=uma_kyori_13-uma_kyori_14
        uma_kyori_14_a=uma_kyori_14-uma_kyori_15
        uma_kyori_15_a=uma_kyori_15-uma_kyori_16
        uma_kyori_16_a=uma_kyori_16-uma_kyori_17
        uma_kyori_17_a=uma_kyori_17-uma_kyori_18
        uma_kyori_18_a=uma_kyori_18-uma_kyori_19
        uma_kyori_19_a=uma_kyori_19-uma_kyori_20
        def kyori_en_cate(x):
            if x > 0: #延長
                return 0
            elif x < 0:
                return 1
            elif x == 0:
                return 2
            else:
                return 3
        uma_route_pre = pd.concat([uma_kyori_0_a,uma_kyori_1_a,uma_kyori_2_a,uma_kyori_3_a,uma_kyori_4_a,uma_kyori_5_a,uma_kyori_6_a,uma_kyori_7_a,uma_kyori_8_a,uma_kyori_9_a,
                                    uma_kyori_10_a,uma_kyori_11_a,uma_kyori_12_a,uma_kyori_13_a,uma_kyori_14_a,uma_kyori_15_a,uma_kyori_16_a,uma_kyori_17_a,uma_kyori_18_a,
                                    uma_kyori_19_a],axis=1)
        uma_route = uma_route_pre.applymap(kyori_en_cate)
        # kyori参照してTrue,False決める 2だったら延長と短縮の平均をとる？
        uma_kyori_flag_1_route=uma_route[0] == uma_route[1] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_2_route=uma_route[0] == uma_route[2] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_3_route=uma_route[0] == uma_route[3] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_4_route=uma_route[0] == uma_route[4] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_5_route=uma_route[0] == uma_route[5] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_6_route=uma_route[0] == uma_route[6] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_7_route=uma_route[0] == uma_route[7] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_8_route=uma_route[0] == uma_route[8] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_9_route=uma_route[0] == uma_route[9] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_10_route=uma_route[0] == uma_route[10] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_11_route=uma_route[0] == uma_route[11] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_12_route=uma_route[0] == uma_route[12] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_13_route=uma_route[0] == uma_route[13] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_14_route=uma_route[0] == uma_route[14] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_15_route=uma_route[0] == uma_route[15] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_16_route=uma_route[0] == uma_route[16] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_17_route=uma_route[0] == uma_route[17] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_18_route=uma_route[0] == uma_route[18] # 数字かけるとFalseは0，Trueは1として扱われる
        uma_kyori_flag_19_route=uma_route[0] == uma_route[19] # 数字かけるとFalseは0，Trueは1として扱われる

        # %%
        # 各項目の集計
        # 過去5走着順の平均値（予測レースが芝なら芝のみ）
        # 結合して0はnanにしてnanmean
        ave_chaku_5_pre_pre = pd.concat([uma_syukei_1['1kakuteijyuni']*uma_baba_flag_1,uma_syukei_2['2kakuteijyuni']*uma_baba_flag_2,
                                        uma_syukei_3['3kakuteijyuni']*uma_baba_flag_3,uma_syukei_4['4kakuteijyuni']*uma_baba_flag_4,
                                        uma_syukei_5['5kakuteijyuni']*uma_baba_flag_5], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_chaku_5 = ave_chaku_5_pre.mean(axis=1,skipna=True)
        # TODO 儲かる馬ということで過去5走の単勝回収率，複勝回収率も求めるべきか

        # 過去対象馬場別着順の平均値（予測レースが芝重なら芝重のみ）
        n1 = uma_syukei_1['1kakuteijyuni']*uma_baba_flag_1*uma_ryoomo_flag_1
        n2 = uma_syukei_2['2kakuteijyuni']*uma_baba_flag_2*uma_ryoomo_flag_2
        n3 = uma_syukei_3['3kakuteijyuni']*uma_baba_flag_3*uma_ryoomo_flag_3
        n4 = uma_syukei_4['4kakuteijyuni']*uma_baba_flag_4*uma_ryoomo_flag_4
        n5 = uma_syukei_5['5kakuteijyuni']*uma_baba_flag_5*uma_ryoomo_flag_5
        n6 = uma_syukei_6['6kakuteijyuni']*uma_baba_flag_6*uma_ryoomo_flag_6
        n7 = uma_syukei_7['7kakuteijyuni']*uma_baba_flag_7*uma_ryoomo_flag_7
        n8 = uma_syukei_8['8kakuteijyuni']*uma_baba_flag_8*uma_ryoomo_flag_8
        n9 = uma_syukei_9['9kakuteijyuni']*uma_baba_flag_9*uma_ryoomo_flag_9
        n10 = uma_syukei_10['10kakuteijyuni']*uma_baba_flag_10*uma_ryoomo_flag_10
        n11 = uma_syukei_11['11kakuteijyuni']*uma_baba_flag_11*uma_ryoomo_flag_11
        n12 = uma_syukei_12['12kakuteijyuni']*uma_baba_flag_12*uma_ryoomo_flag_12
        n13 = uma_syukei_13['13kakuteijyuni']*uma_baba_flag_13*uma_ryoomo_flag_13
        n14 = uma_syukei_14['14kakuteijyuni']*uma_baba_flag_14*uma_ryoomo_flag_14
        n15 = uma_syukei_15['15kakuteijyuni']*uma_baba_flag_15*uma_ryoomo_flag_15
        n16 = uma_syukei_16['16kakuteijyuni']*uma_baba_flag_16*uma_ryoomo_flag_16
        n17 = uma_syukei_17['17kakuteijyuni']*uma_baba_flag_17*uma_ryoomo_flag_17
        n18 = uma_syukei_18['18kakuteijyuni']*uma_baba_flag_18*uma_ryoomo_flag_18
        n19 = uma_syukei_19['19kakuteijyuni']*uma_baba_flag_19*uma_ryoomo_flag_19
        n20 = uma_syukei_20['20kakuteijyuni']*uma_baba_flag_20*uma_ryoomo_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_chaku_baba_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去対象競馬場着順の平均値（予測レースが中山芝なら中山芝のみ）
        n1 = uma_syukei_1['1kakuteijyuni']*uma_baba_flag_1*uma_jyocd_flag_1
        n2 = uma_syukei_2['2kakuteijyuni']*uma_baba_flag_2*uma_jyocd_flag_2
        n3 = uma_syukei_3['3kakuteijyuni']*uma_baba_flag_3*uma_jyocd_flag_3
        n4 = uma_syukei_4['4kakuteijyuni']*uma_baba_flag_4*uma_jyocd_flag_4
        n5 = uma_syukei_5['5kakuteijyuni']*uma_baba_flag_5*uma_jyocd_flag_5
        n6 = uma_syukei_6['6kakuteijyuni']*uma_baba_flag_6*uma_jyocd_flag_6
        n7 = uma_syukei_7['7kakuteijyuni']*uma_baba_flag_7*uma_jyocd_flag_7
        n8 = uma_syukei_8['8kakuteijyuni']*uma_baba_flag_8*uma_jyocd_flag_8
        n9 = uma_syukei_9['9kakuteijyuni']*uma_baba_flag_9*uma_jyocd_flag_9
        n10 = uma_syukei_10['10kakuteijyuni']*uma_baba_flag_10*uma_jyocd_flag_10
        n11 = uma_syukei_11['11kakuteijyuni']*uma_baba_flag_11*uma_jyocd_flag_11
        n12 = uma_syukei_12['12kakuteijyuni']*uma_baba_flag_12*uma_jyocd_flag_12
        n13 = uma_syukei_13['13kakuteijyuni']*uma_baba_flag_13*uma_jyocd_flag_13
        n14 = uma_syukei_14['14kakuteijyuni']*uma_baba_flag_14*uma_jyocd_flag_14
        n15 = uma_syukei_15['15kakuteijyuni']*uma_baba_flag_15*uma_jyocd_flag_15
        n16 = uma_syukei_16['16kakuteijyuni']*uma_baba_flag_16*uma_jyocd_flag_16
        n17 = uma_syukei_17['17kakuteijyuni']*uma_baba_flag_17*uma_jyocd_flag_17
        n18 = uma_syukei_18['18kakuteijyuni']*uma_baba_flag_18*uma_jyocd_flag_18
        n19 = uma_syukei_19['19kakuteijyuni']*uma_baba_flag_19*uma_jyocd_flag_19
        n20 = uma_syukei_20['20kakuteijyuni']*uma_baba_flag_20*uma_jyocd_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_chaku_jyo_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去対象距離別着順の平均値（予測レースが中山芝なら中山芝のみ）
        n1 = uma_syukei_1['1kakuteijyuni']*uma_baba_flag_1*uma_kyori_flag_1
        n2 = uma_syukei_2['2kakuteijyuni']*uma_baba_flag_2*uma_kyori_flag_2
        n3 = uma_syukei_3['3kakuteijyuni']*uma_baba_flag_3*uma_kyori_flag_3
        n4 = uma_syukei_4['4kakuteijyuni']*uma_baba_flag_4*uma_kyori_flag_4
        n5 = uma_syukei_5['5kakuteijyuni']*uma_baba_flag_5*uma_kyori_flag_5
        n6 = uma_syukei_6['6kakuteijyuni']*uma_baba_flag_6*uma_kyori_flag_6
        n7 = uma_syukei_7['7kakuteijyuni']*uma_baba_flag_7*uma_kyori_flag_7
        n8 = uma_syukei_8['8kakuteijyuni']*uma_baba_flag_8*uma_kyori_flag_8
        n9 = uma_syukei_9['9kakuteijyuni']*uma_baba_flag_9*uma_kyori_flag_9
        n10 = uma_syukei_10['10kakuteijyuni']*uma_baba_flag_10*uma_kyori_flag_10
        n11 = uma_syukei_11['11kakuteijyuni']*uma_baba_flag_11*uma_kyori_flag_11
        n12 = uma_syukei_12['12kakuteijyuni']*uma_baba_flag_12*uma_kyori_flag_12
        n13 = uma_syukei_13['13kakuteijyuni']*uma_baba_flag_13*uma_kyori_flag_13
        n14 = uma_syukei_14['14kakuteijyuni']*uma_baba_flag_14*uma_kyori_flag_14
        n15 = uma_syukei_15['15kakuteijyuni']*uma_baba_flag_15*uma_kyori_flag_15
        n16 = uma_syukei_16['16kakuteijyuni']*uma_baba_flag_16*uma_kyori_flag_16
        n17 = uma_syukei_17['17kakuteijyuni']*uma_baba_flag_17*uma_kyori_flag_17
        n18 = uma_syukei_18['18kakuteijyuni']*uma_baba_flag_18*uma_kyori_flag_18
        n19 = uma_syukei_19['19kakuteijyuni']*uma_baba_flag_19*uma_kyori_flag_19
        n20 = uma_syukei_20['20kakuteijyuni']*uma_baba_flag_20*uma_kyori_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_chaku_kyori_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去対象内外別着順の平均値（予測レースが中山芝なら中山芝のみ）
        n1 = uma_syukei_1['1kakuteijyuni']*uma_baba_flag_1*uma_umaban_flag_1
        n2 = uma_syukei_2['2kakuteijyuni']*uma_baba_flag_2*uma_umaban_flag_2
        n3 = uma_syukei_3['3kakuteijyuni']*uma_baba_flag_3*uma_umaban_flag_3
        n4 = uma_syukei_4['4kakuteijyuni']*uma_baba_flag_4*uma_umaban_flag_4
        n5 = uma_syukei_5['5kakuteijyuni']*uma_baba_flag_5*uma_umaban_flag_5
        n6 = uma_syukei_6['6kakuteijyuni']*uma_baba_flag_6*uma_umaban_flag_6
        n7 = uma_syukei_7['7kakuteijyuni']*uma_baba_flag_7*uma_umaban_flag_7
        n8 = uma_syukei_8['8kakuteijyuni']*uma_baba_flag_8*uma_umaban_flag_8
        n9 = uma_syukei_9['9kakuteijyuni']*uma_baba_flag_9*uma_umaban_flag_9
        n10 = uma_syukei_10['10kakuteijyuni']*uma_baba_flag_10*uma_umaban_flag_10
        n11 = uma_syukei_11['11kakuteijyuni']*uma_baba_flag_11*uma_umaban_flag_11
        n12 = uma_syukei_12['12kakuteijyuni']*uma_baba_flag_12*uma_umaban_flag_12
        n13 = uma_syukei_13['13kakuteijyuni']*uma_baba_flag_13*uma_umaban_flag_13
        n14 = uma_syukei_14['14kakuteijyuni']*uma_baba_flag_14*uma_umaban_flag_14
        n15 = uma_syukei_15['15kakuteijyuni']*uma_baba_flag_15*uma_umaban_flag_15
        n16 = uma_syukei_16['16kakuteijyuni']*uma_baba_flag_16*uma_umaban_flag_16
        n17 = uma_syukei_17['17kakuteijyuni']*uma_baba_flag_17*uma_umaban_flag_17
        n18 = uma_syukei_18['18kakuteijyuni']*uma_baba_flag_18*uma_umaban_flag_18
        n19 = uma_syukei_19['19kakuteijyuni']*uma_baba_flag_19*uma_umaban_flag_19
        n20 = uma_syukei_20['20kakuteijyuni']*uma_baba_flag_20*uma_umaban_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_chaku_umaban_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去対象右・左回り別着順の平均値（予測レースが中山芝なら中山芝のみ）
        n1 = uma_syukei_1['1kakuteijyuni']*uma_baba_flag_1*uma_jyocdb_flag_1
        n2 = uma_syukei_2['2kakuteijyuni']*uma_baba_flag_2*uma_jyocdb_flag_2
        n3 = uma_syukei_3['3kakuteijyuni']*uma_baba_flag_3*uma_jyocdb_flag_3
        n4 = uma_syukei_4['4kakuteijyuni']*uma_baba_flag_4*uma_jyocdb_flag_4
        n5 = uma_syukei_5['5kakuteijyuni']*uma_baba_flag_5*uma_jyocdb_flag_5
        n6 = uma_syukei_6['6kakuteijyuni']*uma_baba_flag_6*uma_jyocdb_flag_6
        n7 = uma_syukei_7['7kakuteijyuni']*uma_baba_flag_7*uma_jyocdb_flag_7
        n8 = uma_syukei_8['8kakuteijyuni']*uma_baba_flag_8*uma_jyocdb_flag_8
        n9 = uma_syukei_9['9kakuteijyuni']*uma_baba_flag_9*uma_jyocdb_flag_9
        n10 = uma_syukei_10['10kakuteijyuni']*uma_baba_flag_10*uma_jyocdb_flag_10
        n11 = uma_syukei_11['11kakuteijyuni']*uma_baba_flag_11*uma_jyocdb_flag_11
        n12 = uma_syukei_12['12kakuteijyuni']*uma_baba_flag_12*uma_jyocdb_flag_12
        n13 = uma_syukei_13['13kakuteijyuni']*uma_baba_flag_13*uma_jyocdb_flag_13
        n14 = uma_syukei_14['14kakuteijyuni']*uma_baba_flag_14*uma_jyocdb_flag_14
        n15 = uma_syukei_15['15kakuteijyuni']*uma_baba_flag_15*uma_jyocdb_flag_15
        n16 = uma_syukei_16['16kakuteijyuni']*uma_baba_flag_16*uma_jyocdb_flag_16
        n17 = uma_syukei_17['17kakuteijyuni']*uma_baba_flag_17*uma_jyocdb_flag_17
        n18 = uma_syukei_18['18kakuteijyuni']*uma_baba_flag_18*uma_jyocdb_flag_18
        n19 = uma_syukei_19['19kakuteijyuni']*uma_baba_flag_19*uma_jyocdb_flag_19
        n20 = uma_syukei_20['20kakuteijyuni']*uma_baba_flag_20*uma_jyocdb_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_chaku_migihidari_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去対象平坦坂別着順の平均値（予測レースが中山芝なら中山芝のみ）
        n1 = uma_syukei_1['1kakuteijyuni']*uma_baba_flag_1*uma_jyocda_flag_1
        n2 = uma_syukei_2['2kakuteijyuni']*uma_baba_flag_2*uma_jyocda_flag_2
        n3 = uma_syukei_3['3kakuteijyuni']*uma_baba_flag_3*uma_jyocda_flag_3
        n4 = uma_syukei_4['4kakuteijyuni']*uma_baba_flag_4*uma_jyocda_flag_4
        n5 = uma_syukei_5['5kakuteijyuni']*uma_baba_flag_5*uma_jyocda_flag_5
        n6 = uma_syukei_6['6kakuteijyuni']*uma_baba_flag_6*uma_jyocda_flag_6
        n7 = uma_syukei_7['7kakuteijyuni']*uma_baba_flag_7*uma_jyocda_flag_7
        n8 = uma_syukei_8['8kakuteijyuni']*uma_baba_flag_8*uma_jyocda_flag_8
        n9 = uma_syukei_9['9kakuteijyuni']*uma_baba_flag_9*uma_jyocda_flag_9
        n10 = uma_syukei_10['10kakuteijyuni']*uma_baba_flag_10*uma_jyocda_flag_10
        n11 = uma_syukei_11['11kakuteijyuni']*uma_baba_flag_11*uma_jyocda_flag_11
        n12 = uma_syukei_12['12kakuteijyuni']*uma_baba_flag_12*uma_jyocda_flag_12
        n13 = uma_syukei_13['13kakuteijyuni']*uma_baba_flag_13*uma_jyocda_flag_13
        n14 = uma_syukei_14['14kakuteijyuni']*uma_baba_flag_14*uma_jyocda_flag_14
        n15 = uma_syukei_15['15kakuteijyuni']*uma_baba_flag_15*uma_jyocda_flag_15
        n16 = uma_syukei_16['16kakuteijyuni']*uma_baba_flag_16*uma_jyocda_flag_16
        n17 = uma_syukei_17['17kakuteijyuni']*uma_baba_flag_17*uma_jyocda_flag_17
        n18 = uma_syukei_18['18kakuteijyuni']*uma_baba_flag_18*uma_jyocda_flag_18
        n19 = uma_syukei_19['19kakuteijyuni']*uma_baba_flag_19*uma_jyocda_flag_19
        n20 = uma_syukei_20['20kakuteijyuni']*uma_baba_flag_20*uma_jyocda_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_chaku_heitansaka_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 夏冬フラグ
        n1 = uma_syukei_1['1kakuteijyuni']*uma_baba_flag_1*uma_monthday_flag_1
        n2 = uma_syukei_2['2kakuteijyuni']*uma_baba_flag_2*uma_monthday_flag_2
        n3 = uma_syukei_3['3kakuteijyuni']*uma_baba_flag_3*uma_monthday_flag_3
        n4 = uma_syukei_4['4kakuteijyuni']*uma_baba_flag_4*uma_monthday_flag_4
        n5 = uma_syukei_5['5kakuteijyuni']*uma_baba_flag_5*uma_monthday_flag_5
        n6 = uma_syukei_6['6kakuteijyuni']*uma_baba_flag_6*uma_monthday_flag_6
        n7 = uma_syukei_7['7kakuteijyuni']*uma_baba_flag_7*uma_monthday_flag_7
        n8 = uma_syukei_8['8kakuteijyuni']*uma_baba_flag_8*uma_monthday_flag_8
        n9 = uma_syukei_9['9kakuteijyuni']*uma_baba_flag_9*uma_monthday_flag_9
        n10 = uma_syukei_10['10kakuteijyuni']*uma_baba_flag_10*uma_monthday_flag_10
        n11 = uma_syukei_11['11kakuteijyuni']*uma_baba_flag_11*uma_monthday_flag_11
        n12 = uma_syukei_12['12kakuteijyuni']*uma_baba_flag_12*uma_monthday_flag_12
        n13 = uma_syukei_13['13kakuteijyuni']*uma_baba_flag_13*uma_monthday_flag_13
        n14 = uma_syukei_14['14kakuteijyuni']*uma_baba_flag_14*uma_monthday_flag_14
        n15 = uma_syukei_15['15kakuteijyuni']*uma_baba_flag_15*uma_monthday_flag_15
        n16 = uma_syukei_16['16kakuteijyuni']*uma_baba_flag_16*uma_monthday_flag_16
        n17 = uma_syukei_17['17kakuteijyuni']*uma_baba_flag_17*uma_monthday_flag_17
        n18 = uma_syukei_18['18kakuteijyuni']*uma_baba_flag_18*uma_monthday_flag_18
        n19 = uma_syukei_19['19kakuteijyuni']*uma_baba_flag_19*uma_monthday_flag_19
        n20 = uma_syukei_20['20kakuteijyuni']*uma_baba_flag_20*uma_monthday_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_chaku_natufuyu_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 距離延長・短縮フラグ
        n1 = uma_syukei_1['1kakuteijyuni']*uma_baba_flag_1*uma_kyori_flag_1_route
        n2 = uma_syukei_2['2kakuteijyuni']*uma_baba_flag_2*uma_kyori_flag_2_route
        n3 = uma_syukei_3['3kakuteijyuni']*uma_baba_flag_3*uma_kyori_flag_3_route
        n4 = uma_syukei_4['4kakuteijyuni']*uma_baba_flag_4*uma_kyori_flag_4_route
        n5 = uma_syukei_5['5kakuteijyuni']*uma_baba_flag_5*uma_kyori_flag_5_route
        n6 = uma_syukei_6['6kakuteijyuni']*uma_baba_flag_6*uma_kyori_flag_6_route
        n7 = uma_syukei_7['7kakuteijyuni']*uma_baba_flag_7*uma_kyori_flag_7_route
        n8 = uma_syukei_8['8kakuteijyuni']*uma_baba_flag_8*uma_kyori_flag_8_route
        n9 = uma_syukei_9['9kakuteijyuni']*uma_baba_flag_9*uma_kyori_flag_9_route
        n10 = uma_syukei_10['10kakuteijyuni']*uma_baba_flag_10*uma_kyori_flag_10_route
        n11 = uma_syukei_11['11kakuteijyuni']*uma_baba_flag_11*uma_kyori_flag_11_route
        n12 = uma_syukei_12['12kakuteijyuni']*uma_baba_flag_12*uma_kyori_flag_12_route
        n13 = uma_syukei_13['13kakuteijyuni']*uma_baba_flag_13*uma_kyori_flag_13_route
        n14 = uma_syukei_14['14kakuteijyuni']*uma_baba_flag_14*uma_kyori_flag_14_route
        n15 = uma_syukei_15['15kakuteijyuni']*uma_baba_flag_15*uma_kyori_flag_15_route
        n16 = uma_syukei_16['16kakuteijyuni']*uma_baba_flag_16*uma_kyori_flag_16_route
        n17 = uma_syukei_17['17kakuteijyuni']*uma_baba_flag_17*uma_kyori_flag_17_route
        n18 = uma_syukei_18['18kakuteijyuni']*uma_baba_flag_18*uma_kyori_flag_18_route
        n19 = uma_syukei_19['19kakuteijyuni']*uma_baba_flag_19*uma_kyori_flag_19_route
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_chaku_kyoriencho_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去５走S指数の平均値（予測レースが芝なら芝のみ）
        ave_chaku_5_pre_pre = pd.concat([uma_syukei_1['1speed_idx']*uma_baba_flag_1,uma_syukei_2['2speed_idx']*uma_baba_flag_2,
                                        uma_syukei_3['3speed_idx']*uma_baba_flag_3,uma_syukei_4['4speed_idx']*uma_baba_flag_4,
                                        uma_syukei_5['5speed_idx']*uma_baba_flag_5], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_speed_5 = ave_chaku_5_pre.mean(axis=1,skipna=True)
        # TODO 儲かる馬ということで過去5走の単勝回収率，複勝回収率も求めるべきか

        # 過去対象競馬場でのS指数の平均値（予測レースが芝なら芝のみ）
        n1 = uma_syukei_1['1speed_idx']*uma_baba_flag_1*uma_jyocd_flag_1
        n2 = uma_syukei_2['2speed_idx']*uma_baba_flag_2*uma_jyocd_flag_2
        n3 = uma_syukei_3['3speed_idx']*uma_baba_flag_3*uma_jyocd_flag_3
        n4 = uma_syukei_4['4speed_idx']*uma_baba_flag_4*uma_jyocd_flag_4
        n5 = uma_syukei_5['5speed_idx']*uma_baba_flag_5*uma_jyocd_flag_5
        n6 = uma_syukei_6['6speed_idx']*uma_baba_flag_6*uma_jyocd_flag_6
        n7 = uma_syukei_7['7speed_idx']*uma_baba_flag_7*uma_jyocd_flag_7
        n8 = uma_syukei_8['8speed_idx']*uma_baba_flag_8*uma_jyocd_flag_8
        n9 = uma_syukei_9['9speed_idx']*uma_baba_flag_9*uma_jyocd_flag_9
        n10 = uma_syukei_10['10speed_idx']*uma_baba_flag_10*uma_jyocd_flag_10
        n11 = uma_syukei_11['11speed_idx']*uma_baba_flag_11*uma_jyocd_flag_11
        n12 = uma_syukei_12['12speed_idx']*uma_baba_flag_12*uma_jyocd_flag_12
        n13 = uma_syukei_13['13speed_idx']*uma_baba_flag_13*uma_jyocd_flag_13
        n14 = uma_syukei_14['14speed_idx']*uma_baba_flag_14*uma_jyocd_flag_14
        n15 = uma_syukei_15['15speed_idx']*uma_baba_flag_15*uma_jyocd_flag_15
        n16 = uma_syukei_16['16speed_idx']*uma_baba_flag_16*uma_jyocd_flag_16
        n17 = uma_syukei_17['17speed_idx']*uma_baba_flag_17*uma_jyocd_flag_17
        n18 = uma_syukei_18['18speed_idx']*uma_baba_flag_18*uma_jyocd_flag_18
        n19 = uma_syukei_19['19speed_idx']*uma_baba_flag_19*uma_jyocd_flag_19
        n20 = uma_syukei_20['20speed_idx']*uma_baba_flag_20*uma_jyocd_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_speed_jyo_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去対象距離でのS指数の平均値（予測レースが芝なら芝のみ）
        n1 = uma_syukei_1['1speed_idx']*uma_baba_flag_1*uma_kyori_flag_1
        n2 = uma_syukei_2['2speed_idx']*uma_baba_flag_2*uma_kyori_flag_2
        n3 = uma_syukei_3['3speed_idx']*uma_baba_flag_3*uma_kyori_flag_3
        n4 = uma_syukei_4['4speed_idx']*uma_baba_flag_4*uma_kyori_flag_4
        n5 = uma_syukei_5['5speed_idx']*uma_baba_flag_5*uma_kyori_flag_5
        n6 = uma_syukei_6['6speed_idx']*uma_baba_flag_6*uma_kyori_flag_6
        n7 = uma_syukei_7['7speed_idx']*uma_baba_flag_7*uma_kyori_flag_7
        n8 = uma_syukei_8['8speed_idx']*uma_baba_flag_8*uma_kyori_flag_8
        n9 = uma_syukei_9['9speed_idx']*uma_baba_flag_9*uma_kyori_flag_9
        n10 = uma_syukei_10['10speed_idx']*uma_baba_flag_10*uma_kyori_flag_10
        n11 = uma_syukei_11['11speed_idx']*uma_baba_flag_11*uma_kyori_flag_11
        n12 = uma_syukei_12['12speed_idx']*uma_baba_flag_12*uma_kyori_flag_12
        n13 = uma_syukei_13['13speed_idx']*uma_baba_flag_13*uma_kyori_flag_13
        n14 = uma_syukei_14['14speed_idx']*uma_baba_flag_14*uma_kyori_flag_14
        n15 = uma_syukei_15['15speed_idx']*uma_baba_flag_15*uma_kyori_flag_15
        n16 = uma_syukei_16['16speed_idx']*uma_baba_flag_16*uma_kyori_flag_16
        n17 = uma_syukei_17['17speed_idx']*uma_baba_flag_17*uma_kyori_flag_17
        n18 = uma_syukei_18['18speed_idx']*uma_baba_flag_18*uma_kyori_flag_18
        n19 = uma_syukei_19['19speed_idx']*uma_baba_flag_19*uma_kyori_flag_19
        n20 = uma_syukei_20['20speed_idx']*uma_baba_flag_20*uma_kyori_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_speed_kyori_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去対象馬場でのS指数の平均値（予測レースが芝なら芝のみ）
        n1 = uma_syukei_1['1speed_idx']*uma_baba_flag_1*uma_ryoomo_flag_1
        n2 = uma_syukei_2['2speed_idx']*uma_baba_flag_2*uma_ryoomo_flag_2
        n3 = uma_syukei_3['3speed_idx']*uma_baba_flag_3*uma_ryoomo_flag_3
        n4 = uma_syukei_4['4speed_idx']*uma_baba_flag_4*uma_ryoomo_flag_4
        n5 = uma_syukei_5['5speed_idx']*uma_baba_flag_5*uma_ryoomo_flag_5
        n6 = uma_syukei_6['6speed_idx']*uma_baba_flag_6*uma_ryoomo_flag_6
        n7 = uma_syukei_7['7speed_idx']*uma_baba_flag_7*uma_ryoomo_flag_7
        n8 = uma_syukei_8['8speed_idx']*uma_baba_flag_8*uma_ryoomo_flag_8
        n9 = uma_syukei_9['9speed_idx']*uma_baba_flag_9*uma_ryoomo_flag_9
        n10 = uma_syukei_10['10speed_idx']*uma_baba_flag_10*uma_ryoomo_flag_10
        n11 = uma_syukei_11['11speed_idx']*uma_baba_flag_11*uma_ryoomo_flag_11
        n12 = uma_syukei_12['12speed_idx']*uma_baba_flag_12*uma_ryoomo_flag_12
        n13 = uma_syukei_13['13speed_idx']*uma_baba_flag_13*uma_ryoomo_flag_13
        n14 = uma_syukei_14['14speed_idx']*uma_baba_flag_14*uma_ryoomo_flag_14
        n15 = uma_syukei_15['15speed_idx']*uma_baba_flag_15*uma_ryoomo_flag_15
        n16 = uma_syukei_16['16speed_idx']*uma_baba_flag_16*uma_ryoomo_flag_16
        n17 = uma_syukei_17['17speed_idx']*uma_baba_flag_17*uma_ryoomo_flag_17
        n18 = uma_syukei_18['18speed_idx']*uma_baba_flag_18*uma_ryoomo_flag_18
        n19 = uma_syukei_19['19speed_idx']*uma_baba_flag_19*uma_ryoomo_flag_19
        n20 = uma_syukei_20['20speed_idx']*uma_baba_flag_20*uma_ryoomo_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_speed_baba_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去５走stanの平均値（予測レースが芝なら芝のみ）
        horse_p_pre = pd.concat([uma_syukei_1['1horse_p']*uma_baba_flag_1,uma_syukei_2['2horse_p']*uma_baba_flag_2,
                                        uma_syukei_3['3horse_p']*uma_baba_flag_3,uma_syukei_4['4horse_p']*uma_baba_flag_4,
                                        uma_syukei_5['5horse_p']*uma_baba_flag_5], axis=1)
        horse_p = horse_p_pre.replace([0], np.nan)
        ave_stan_5 = horse_p.mean(axis=1,skipna=True)
        # TODO 儲かる馬ということで過去5走の単勝回収率，複勝回収率も求めるべきか

        # 過去対象競馬場でのstanの平均値（予測レースが芝なら芝のみ）
        n1 = uma_syukei_1['1horse_p']*uma_baba_flag_1*uma_jyocd_flag_1
        n2 = uma_syukei_2['2horse_p']*uma_baba_flag_2*uma_jyocd_flag_2
        n3 = uma_syukei_3['3horse_p']*uma_baba_flag_3*uma_jyocd_flag_3
        n4 = uma_syukei_4['4horse_p']*uma_baba_flag_4*uma_jyocd_flag_4
        n5 = uma_syukei_5['5horse_p']*uma_baba_flag_5*uma_jyocd_flag_5
        n6 = uma_syukei_6['6horse_p']*uma_baba_flag_6*uma_jyocd_flag_6
        n7 = uma_syukei_7['7horse_p']*uma_baba_flag_7*uma_jyocd_flag_7
        n8 = uma_syukei_8['8horse_p']*uma_baba_flag_8*uma_jyocd_flag_8
        n9 = uma_syukei_9['9horse_p']*uma_baba_flag_9*uma_jyocd_flag_9
        n10 = uma_syukei_10['10horse_p']*uma_baba_flag_10*uma_jyocd_flag_10
        n11 = uma_syukei_11['11horse_p']*uma_baba_flag_11*uma_jyocd_flag_11
        n12 = uma_syukei_12['12horse_p']*uma_baba_flag_12*uma_jyocd_flag_12
        n13 = uma_syukei_13['13horse_p']*uma_baba_flag_13*uma_jyocd_flag_13
        n14 = uma_syukei_14['14horse_p']*uma_baba_flag_14*uma_jyocd_flag_14
        n15 = uma_syukei_15['15horse_p']*uma_baba_flag_15*uma_jyocd_flag_15
        n16 = uma_syukei_16['16horse_p']*uma_baba_flag_16*uma_jyocd_flag_16
        n17 = uma_syukei_17['17horse_p']*uma_baba_flag_17*uma_jyocd_flag_17
        n18 = uma_syukei_18['18horse_p']*uma_baba_flag_18*uma_jyocd_flag_18
        n19 = uma_syukei_19['19horse_p']*uma_baba_flag_19*uma_jyocd_flag_19
        n20 = uma_syukei_20['20horse_p']*uma_baba_flag_20*uma_jyocd_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_stan_jyo_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去対象距離でのstanの平均値（予測レースが芝なら芝のみ）
        n1 = uma_syukei_1['1horse_p']*uma_baba_flag_1*uma_kyori_flag_1
        n2 = uma_syukei_2['2horse_p']*uma_baba_flag_2*uma_kyori_flag_2
        n3 = uma_syukei_3['3horse_p']*uma_baba_flag_3*uma_kyori_flag_3
        n4 = uma_syukei_4['4horse_p']*uma_baba_flag_4*uma_kyori_flag_4
        n5 = uma_syukei_5['5horse_p']*uma_baba_flag_5*uma_kyori_flag_5
        n6 = uma_syukei_6['6horse_p']*uma_baba_flag_6*uma_kyori_flag_6
        n7 = uma_syukei_7['7horse_p']*uma_baba_flag_7*uma_kyori_flag_7
        n8 = uma_syukei_8['8horse_p']*uma_baba_flag_8*uma_kyori_flag_8
        n9 = uma_syukei_9['9horse_p']*uma_baba_flag_9*uma_kyori_flag_9
        n10 = uma_syukei_10['10horse_p']*uma_baba_flag_10*uma_kyori_flag_10
        n11 = uma_syukei_11['11horse_p']*uma_baba_flag_11*uma_kyori_flag_11
        n12 = uma_syukei_12['12horse_p']*uma_baba_flag_12*uma_kyori_flag_12
        n13 = uma_syukei_13['13horse_p']*uma_baba_flag_13*uma_kyori_flag_13
        n14 = uma_syukei_14['14horse_p']*uma_baba_flag_14*uma_kyori_flag_14
        n15 = uma_syukei_15['15horse_p']*uma_baba_flag_15*uma_kyori_flag_15
        n16 = uma_syukei_16['16horse_p']*uma_baba_flag_16*uma_kyori_flag_16
        n17 = uma_syukei_17['17horse_p']*uma_baba_flag_17*uma_kyori_flag_17
        n18 = uma_syukei_18['18horse_p']*uma_baba_flag_18*uma_kyori_flag_18
        n19 = uma_syukei_19['19horse_p']*uma_baba_flag_19*uma_kyori_flag_19
        n20 = uma_syukei_20['20horse_p']*uma_baba_flag_20*uma_kyori_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_stan_kyori_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去対象馬場でのstanの平均値（予測レースが芝なら芝のみ）
        n1 = uma_syukei_1['1horse_p']*uma_baba_flag_1*uma_ryoomo_flag_1
        n2 = uma_syukei_2['2horse_p']*uma_baba_flag_2*uma_ryoomo_flag_2
        n3 = uma_syukei_3['3horse_p']*uma_baba_flag_3*uma_ryoomo_flag_3
        n4 = uma_syukei_4['4horse_p']*uma_baba_flag_4*uma_ryoomo_flag_4
        n5 = uma_syukei_5['5horse_p']*uma_baba_flag_5*uma_ryoomo_flag_5
        n6 = uma_syukei_6['6horse_p']*uma_baba_flag_6*uma_ryoomo_flag_6
        n7 = uma_syukei_7['7horse_p']*uma_baba_flag_7*uma_ryoomo_flag_7
        n8 = uma_syukei_8['8horse_p']*uma_baba_flag_8*uma_ryoomo_flag_8
        n9 = uma_syukei_9['9horse_p']*uma_baba_flag_9*uma_ryoomo_flag_9
        n10 = uma_syukei_10['10horse_p']*uma_baba_flag_10*uma_ryoomo_flag_10
        n11 = uma_syukei_11['11horse_p']*uma_baba_flag_11*uma_ryoomo_flag_11
        n12 = uma_syukei_12['12horse_p']*uma_baba_flag_12*uma_ryoomo_flag_12
        n13 = uma_syukei_13['13horse_p']*uma_baba_flag_13*uma_ryoomo_flag_13
        n14 = uma_syukei_14['14horse_p']*uma_baba_flag_14*uma_ryoomo_flag_14
        n15 = uma_syukei_15['15horse_p']*uma_baba_flag_15*uma_ryoomo_flag_15
        n16 = uma_syukei_16['16horse_p']*uma_baba_flag_16*uma_ryoomo_flag_16
        n17 = uma_syukei_17['17horse_p']*uma_baba_flag_17*uma_ryoomo_flag_17
        n18 = uma_syukei_18['18horse_p']*uma_baba_flag_18*uma_ryoomo_flag_18
        n19 = uma_syukei_19['19horse_p']*uma_baba_flag_19*uma_ryoomo_flag_19
        n20 = uma_syukei_20['20horse_p']*uma_baba_flag_20*uma_ryoomo_flag_20
        ave_chaku_5_pre_pre = pd.concat([n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20], axis=1)
        ave_chaku_5_pre = ave_chaku_5_pre_pre.replace([0], np.nan)
        ave_stan_baba_20 = ave_chaku_5_pre.mean(axis=1,skipna=True)

        # 過去５走走破時差の平均値（予測レースが芝なら芝のみ）
        uma_baba_flag_1a = uma_baba_flag_1.replace([False], np.nan)
        uma_baba_flag_2a = uma_baba_flag_2.replace([False], np.nan)
        uma_baba_flag_3a = uma_baba_flag_3.replace([False], np.nan)
        uma_baba_flag_4a = uma_baba_flag_4.replace([False], np.nan)
        uma_baba_flag_5a = uma_baba_flag_5.replace([False], np.nan)
        horse_p_pre = pd.concat([uma_syukei_1['1timediff']*uma_baba_flag_1a,uma_syukei_2['2timediff']*uma_baba_flag_2a,
                                        uma_syukei_3['3timediff']*uma_baba_flag_3a,uma_syukei_4['4timediff']*uma_baba_flag_4a,
                                        uma_syukei_5['5timediff']*uma_baba_flag_5a], axis=1)
        ave_timediff_5 = horse_p_pre.mean(axis=1,skipna=True)

        # 過去５走４角順位の平均値（予測レースが芝なら芝のみ）
        horse_p_pre = pd.concat([uma_syukei_1['1jyuni4c']*uma_baba_flag_1,uma_syukei_2['2jyuni4c']*uma_baba_flag_2,
                                        uma_syukei_3['3jyuni4c']*uma_baba_flag_3,uma_syukei_4['4jyuni4c']*uma_baba_flag_4,
                                        uma_syukei_5['5jyuni4c']*uma_baba_flag_5], axis=1)
        horse_p = horse_p_pre.replace([0], np.nan)
        ave_jyuni4c_5 = horse_p.mean(axis=1,skipna=True)

        # 過去５走人気の平均値（予測レースが芝なら芝のみ）
        horse_p_pre = pd.concat([uma_syukei_1['1ninki']*uma_baba_flag_1,uma_syukei_2['2ninki']*uma_baba_flag_2,
                                        uma_syukei_3['3ninki']*uma_baba_flag_3,uma_syukei_4['4ninki']*uma_baba_flag_4,
                                        uma_syukei_5['5ninki']*uma_baba_flag_5], axis=1)
        horse_p = horse_p_pre.replace([0], np.nan)
        ave_ninki_5 = horse_p.mean(axis=1,skipna=True)

        # 過去５走単勝オッズの平均値（予測レースが芝なら芝のみ
        horse_p_pre = pd.concat([uma_syukei_1['1tanodds']*uma_baba_flag_1,uma_syukei_2['2tanodds']*uma_baba_flag_2,
                                        uma_syukei_3['3tanodds']*uma_baba_flag_3,uma_syukei_4['4tanodds']*uma_baba_flag_4,
                                        uma_syukei_5['5tanodds']*uma_baba_flag_5], axis=1)
        horse_p = horse_p_pre.replace([0], np.nan)
        ave_tanodds_5 = horse_p.mean(axis=1,skipna=True)

        # 過去５走上がり３Fの平均値（予測レースが芝なら芝のみ）
        horse_p_pre = pd.concat([uma_syukei_1['1medianharon3']*uma_baba_flag_1,uma_syukei_2['2medianharon3']*uma_baba_flag_2,
                                        uma_syukei_3['3medianharon3']*uma_baba_flag_3,uma_syukei_4['4medianharon3']*uma_baba_flag_4,
                                        uma_syukei_5['5medianharon3']*uma_baba_flag_5], axis=1)
        horse_p = horse_p_pre.replace([0], np.nan)
        ave_medianharon3_5 = horse_p.mean(axis=1,skipna=True)

        # 過去５走正規化着順の平均値（予測レースが芝なら芝のみ）
        horse_p_pre = pd.concat([uma_syukei_1['1meankakuteijyuni']*uma_baba_flag_1,uma_syukei_2['2meankakuteijyuni']*uma_baba_flag_2,
                                        uma_syukei_3['3meankakuteijyuni']*uma_baba_flag_3,uma_syukei_4['4meankakuteijyuni']*uma_baba_flag_4,
                                        uma_syukei_5['5meankakuteijyuni']*uma_baba_flag_5], axis=1)
        horse_p = horse_p_pre.replace([0], np.nan)
        ave_meankakuteijyuni_5 = horse_p.mean(axis=1,skipna=True)

        # 過去５走正規化走破時計の平均値（予測レースが芝なら芝のみ）
        horse_p_pre = pd.concat([uma_syukei_1['1mediantime']*uma_baba_flag_1,uma_syukei_2['2mediantime']*uma_baba_flag_2,
                                        uma_syukei_3['3mediantime']*uma_baba_flag_3,uma_syukei_4['4mediantime']*uma_baba_flag_4,
                                        uma_syukei_5['5mediantime']*uma_baba_flag_5], axis=1)
        horse_p = horse_p_pre.replace([0], np.nan)
        ave_mediantime_5 = horse_p.mean(axis=1,skipna=True)

        # 過去５走賞金の平均値（予測レースが芝なら芝のみ）
        uma_baba_flag_1a = uma_baba_flag_1.replace([False], np.nan)
        uma_baba_flag_2a = uma_baba_flag_2.replace([False], np.nan)
        uma_baba_flag_3a = uma_baba_flag_3.replace([False], np.nan)
        uma_baba_flag_4a = uma_baba_flag_4.replace([False], np.nan)
        uma_baba_flag_5a = uma_baba_flag_5.replace([False], np.nan)
        horse_p_pre = pd.concat([uma_syukei_1['1honsyokin']*uma_baba_flag_1a,uma_syukei_2['2honsyokin']*uma_baba_flag_2a,
                                        uma_syukei_3['3honsyokin']*uma_baba_flag_3a,uma_syukei_4['4honsyokin']*uma_baba_flag_4a,
                                        uma_syukei_5['5honsyokin']*uma_baba_flag_5a], axis=1)
        ave_honsyokin_5 = horse_p_pre.mean(axis=1,skipna=True)

        # 過去５走出走頭数の平均値
        horse_p_pre = pd.concat([uma_syukei_1['1syussou']*uma_baba_flag_1,uma_syukei_2['2syussou']*uma_baba_flag_2,
                                        uma_syukei_3['3syussou']*uma_baba_flag_3,uma_syukei_4['4syussou']*uma_baba_flag_4,
                                        uma_syukei_5['5syussou']*uma_baba_flag_5], axis=1)
        horse_p = horse_p_pre.replace([0], np.nan)
        ave_syussou_5 = horse_p.mean(axis=1,skipna=True)

        #%%
        # データは本当は800000行くらいあるからその欠けを埋めてDBへ
        da_all = pd.concat([uma_syukei_0['0index_moto'],ave_chaku_5,ave_chaku_baba_20,ave_chaku_jyo_20,ave_chaku_kyori_20,ave_chaku_umaban_20,ave_chaku_migihidari_20,
                            ave_chaku_heitansaka_20,ave_chaku_natufuyu_20,ave_chaku_kyoriencho_20,ave_speed_5,ave_speed_jyo_20,ave_speed_kyori_20,
                            ave_speed_baba_20,ave_stan_5,ave_stan_jyo_20,ave_stan_kyori_20,ave_stan_baba_20,ave_timediff_5,ave_jyuni4c_5,
                            ave_ninki_5,ave_tanodds_5,ave_medianharon3_5,ave_meankakuteijyuni_5,ave_mediantime_5,ave_honsyokin_5,ave_syussou_5],axis=1)

        da_all=da_all.rename(columns={'0index_moto':'index',0:'ave_chaku_5',0:'ave_chaku_5',1:'ave_chaku_baba_20',2:'ave_chaku_jyo_20',3:'ave_chaku_kyori_20',4:'ave_chaku_umaban_20',
                            5:'ave_chaku_migihidari_20',6:'ave_chaku_heitansaka_20',7:'ave_chaku_natufuyu_20',8:'ave_chaku_kyoriencho_20',9:'ave_speed_5',
                            10:'ave_speed_jyo_20',11:'ave_speed_kyori_20',12:'ave_speed_baba_20',13:'ave_stan_5',14:'ave_stan_jyo_20',
                            15:'ave_stan_kyori_20',16:'ave_stan_baba_20',17:'ave_timediff_5',18:'ave_jyuni4c_5',19:'ave_ninki_5',
                            20:'ave_tanodds_5',21:'ave_medianharon3_5',22:'ave_meankakuteijyuni_5',23:'ave_mediantime_5',24:'ave_honsyokin_5',
                            25:'ave_syussou_5'})
        da_all = da_all.set_index('index')
        # 空フレームとたして欠測うめてくっつける
        kara_da_all = pd.DataFrame(index=range(len(n0_u)),columns=['index','ave_chaku_5','ave_chaku_baba_20','ave_chaku_jyo_20',
                                                                'ave_chaku_kyori_20','ave_chaku_umaban_20','ave_chaku_migihidari_20',
                                                                'ave_chaku_heitansaka_20','ave_chaku_natufuyu_20','ave_chaku_kyoriencho_20',
                                                                'ave_speed_5','ave_speed_jyo_20','ave_speed_kyori_20','ave_speed_baba_20',
                                                                'ave_stan_5','ave_stan_jyo_20','ave_stan_kyori_20','ave_stan_baba_20','ave_timediff_5',
                                                                'ave_jyuni4c_5','ave_ninki_5','ave_tanodds_5','ave_medianharon3_5','ave_meankakuteijyuni_5',
                                                                'ave_mediantime_5','ave_honsyokin_5','ave_syussou_5'])  # 空データを作成 914907×267
        kara_da_all.fillna(0, inplace=True)
        eeureka_pre = kara_da_all+da_all
        eeureka_pre = eeureka_pre.drop(columns='index')
        # indexを与える
        eeureka = eeureka_pre.reset_index()
        #n1.columns.to_list()
        #n1_u['1kakuteijyuni'].unique()

        # 「前走着順ー前走人気」ー「今回人気」とか追加，処理がおかしくないか全体チェック
        #n1.columns.to_list()
        #n1_u['1kakuteijyuni'].unique()

        # %%
        # DBへ出力
        # データpostgreへ
        conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
        cursor = conn.cursor()  # データベースを操作できるようにする
        eeureka.to_sql("uma_20_5_syukei", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
        # -------------実行ここまで
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる

        process_time = time.time() - start
        print(process_time / 60)  # 3.8min
# endregion

# classの実行
# target_umadata.output()

# 5-3.kisyu,chokyo,banushi,etcなどのtargetencoding意識のデータ作成する。=test_4_targetencoding_1
# 6.inputデータ作成する=test_5_input_data
# 7.LGBMする=LGBM

# 5.特徴量作成class⇒targetencodingを意識した特徴量(統計量)を作成する。
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
        sql_moto = 'SELECT * FROM public."df_moto_test" ORDER BY index ASC;'  # 実行SQL
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
        # 変数の初期設定
        year_num = 11
        basyo_num = 10
        main_num = 50
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
        at_chokyo_sample2 = at_chokyo_sample1.where(at_kisyu_sample1 > thr, np.nan) #間違いのはず　chokyoで統一？
        at_banu_sample2 = at_banu_sample1.where(at_kisyu_sample1 > thr, np.nan)#間違いのはず
        at_syu_sample2 = at_syu_sample1.where(at_kisyu_sample1 > thr, np.nan)#間違いのはず
        # 数値データを1にする
        at_kisyu_sample3 = at_kisyu_sample2.where(at_kisyu_sample1 < thr, 1)  # 5以上を1にする
        at_chokyo_sample3 = at_chokyo_sample2.where(at_kisyu_sample1 < thr, 1)#間違いのはず
        at_banu_sample3 = at_banu_sample2.where(at_kisyu_sample1 < thr, 1)#間違いのはず
        at_syu_sample3 = at_syu_sample2.where(at_kisyu_sample1 < thr, 1)#間違いのはず
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
        # それぞれの列においてNANを残ったデータの平均で置き換え TODO leak防止のため，今後は年単位で欠測処理行う ,とりあえずまずは置き換えない。年だけでなく競馬場データも混じるので
        # akisyu_box_tanharai3 = akisyu_box_tanharai2.fillna(akisyu_box_tanharai2.mean())
        # akisyu_box_fukuharai3 = akisyu_box_fukuharai2.fillna(akisyu_box_fukuharai2.mean())
        # akisyu_box_syouritu3 = akisyu_box_syouritu2.fillna(akisyu_box_syouritu2.mean())
        # akisyu_box_fukuritu3 = akisyu_box_fukuritu2.fillna(akisyu_box_fukuritu2.mean())
        # achokyo_box_tanharai3 = achokyo_box_tanharai2.fillna(achokyo_box_tanharai2.mean())
        # achokyo_box_fukuharai3 = achokyo_box_fukuharai2.fillna(achokyo_box_fukuharai2.mean())
        # achokyo_box_syouritu3 = achokyo_box_syouritu2.fillna(achokyo_box_syouritu2.mean())
        # achokyo_box_fukuritu3 = achokyo_box_fukuritu2.fillna(achokyo_box_fukuritu2.mean())
        # abanu_box_tanharai3 = abanu_box_tanharai2.fillna(abanu_box_tanharai2.mean())
        # abanu_box_fukuharai3 = abanu_box_fukuharai2.fillna(abanu_box_fukuharai2.mean())
        # abanu_box_syouritu3 = abanu_box_syouritu2.fillna(abanu_box_syouritu2.mean())
        # abanu_box_fukuritu3 = abanu_box_fukuritu2.fillna(abanu_box_fukuritu2.mean())
        # asyu_box_tanharai3 = asyu_box_tanharai2.fillna(asyu_box_tanharai2.mean())
        # asyu_box_fukuharai3 = asyu_box_fukuharai2.fillna(asyu_box_fukuharai2.mean())
        # asyu_box_syouritu3 = asyu_box_syouritu2.fillna(asyu_box_syouritu2.mean())
        # asyu_box_fukuritu3 = asyu_box_fukuritu2.fillna(asyu_box_fukuritu2.mean())
        akisyu_box_tanharai3 = akisyu_box_tanharai2
        akisyu_box_fukuharai3 = akisyu_box_fukuharai2
        akisyu_box_syouritu3 = akisyu_box_syouritu2
        akisyu_box_fukuritu3 = akisyu_box_fukuritu2
        achokyo_box_tanharai3 = achokyo_box_tanharai2
        achokyo_box_fukuharai3 = achokyo_box_fukuharai2
        achokyo_box_syouritu3 = achokyo_box_syouritu2
        achokyo_box_fukuritu3 = achokyo_box_fukuritu2
        abanu_box_tanharai3 = abanu_box_tanharai2
        abanu_box_fukuharai3 = abanu_box_fukuharai2
        abanu_box_syouritu3 = abanu_box_syouritu2
        abanu_box_fukuritu3 = abanu_box_fukuritu2
        asyu_box_tanharai3 = asyu_box_tanharai2
        asyu_box_fukuharai3 = asyu_box_fukuharai2
        asyu_box_syouritu3 = asyu_box_syouritu2
        asyu_box_fukuritu3 = asyu_box_fukuritu2
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
# endregion

# classの実行
# target_encoding.output()

# 6.inputデータ作成class⇒LGBMに入力するデータを作成する。過去6走データ。
# 対象レースの馬柱（0走前）⇒1走前⇒2走前⇒3走前⇒4走前⇒5走前
# 対応する詳細⇒1走前対応する詳細⇒2走前対応する詳細⇒3走前対応する詳細⇒4走前対応する詳細⇒5走前対応する詳細
# region input_data class
class input_data:
    @staticmethod
    def output():
        """
            input_dataを出力する関数
            Parameters:
            -----------

            Returns:
            -----------
            Input_Data_Uma : pandas.DataFrame
            Input_Data_Race : pandas.DataFrame
                 inputデータを出力
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
        sql_moto = 'SELECT * FROM public."df_moto_test" ORDER BY index ASC;'  # 実行SQL
        # スピード指数データ
        sql50 = 'SELECT * FROM public."speed_index" ORDER BY index ASC;'  # 教師データ
        # target-encoding 特徴量
        sql52 = 'SELECT * FROM public."1Tokutyo_data_new_test" ORDER BY index ASC;'  # 対象index番号
        sql54 = 'SELECT * FROM public."3Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
        sql56 = 'SELECT * FROM public."5Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
        sql58 = 'SELECT * FROM public."7Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
        sql60 = 'SELECT * FROM public."9Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
        sql62 = 'SELECT * FROM public."11Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
        sql64 = 'SELECT * FROM public."13Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
        sql66 = 'SELECT * FROM public."15Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
        # DBのデータをpandasで取得
        moto_df = pd.read_sql(sql_moto, conn)  # sql:実行したいsql，conn:対象のdb名
        spped_from_db = pd.read_sql(sql50, conn)  # sql:実行したいsql，conn:対象のdb名
        # target-encoding 特徴量
        Tokutyo1 = (pd.read_sql(sql52, conn))  # sql:実行したいsql，conn:対象のdb名
        Tokutyo3 = (pd.read_sql(sql54, conn))  # sql:実行したいsql，conn:対象のdb名
        Tokutyo5 = (pd.read_sql(sql56, conn))  # sql:実行したいsql，conn:対象のdb名
        Tokutyo7 = (pd.read_sql(sql58, conn))  # sql:実行したいsql，conn:対象のdb名
        Tokutyo9 = (pd.read_sql(sql60, conn))  # sql:実行したいsql，conn:対象のdb名
        Tokutyo11 = (pd.read_sql(sql62, conn))  # sql:実行したいsql，conn:対象のdb名
        Tokutyo13 = (pd.read_sql(sql64, conn))  # sql:実行したいsql，conn:対象のdb名
        Tokutyo15 = (pd.read_sql(sql66, conn))  # sql:実行したいsql，conn:対象のdb名
        ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
        cursor.close()  # データベースの操作を終了する
        conn.commit()  # 変更をデータベースに保存
        conn.close()  # データベースを閉じる
        # index 削除
        Tokutyo1 = Tokutyo1.drop(columns='index')
        Tokutyo3 = Tokutyo3.drop(columns='index')
        Tokutyo3 = Tokutyo3.rename(columns={'0': '12', '1': '13', '2': '14', '3': '15', '4': '16', '5': '17', '6': '18', '7': '19', '8': '20', '9': '21', '10': '22', '11': '23'})
        Tokutyo5 = Tokutyo5.drop(columns='index')
        Tokutyo5 = Tokutyo5.rename(columns={'0': '24', '1': '25', '2': '26', '3': '27', '4': '28', '5': '29', '6': '30', '7': '31', '8': '32', '9': '33', '10': '34', '11': '35'})
        Tokutyo7 = Tokutyo7.drop(columns='index')
        Tokutyo7 = Tokutyo7.rename(columns={'0': '36', '1': '37', '2': '38', '3': '39', '4': '40', '5': '41', '6': '42', '7': '43', '8': '44', '9': '45', '10': '46', '11': '47'})
        Tokutyo9 = Tokutyo9.drop(columns='index')
        Tokutyo9 = Tokutyo9.rename(columns={'0': '48', '1': '49', '2': '50', '3': '51', '4': '52', '5': '53', '6': '54', '7': '55', '8': '56', '9': '57', '10': '58', '11': '59'})
        Tokutyo11 = Tokutyo11.drop(columns='index')
        Tokutyo11 = Tokutyo11.rename(columns={'0': '60', '1': '61', '2': '62', '3': '63', '4': '64', '5': '65', '6': '66', '7': '67', '8': '68', '9': '69', '10': '70', '11': '71'})
        Tokutyo13 = Tokutyo13.drop(columns='index')
        Tokutyo13 = Tokutyo13.rename(columns={'0': '72', '1': '73', '2': '74', '3': '75', '4': '76', '5': '77', '6': '78', '7': '79', '8': '80', '9': '81', '10': '82', '11': '83'})
        Tokutyo15 = Tokutyo15.drop(columns='index')
        Tokutyo15 = Tokutyo15.rename(columns={'0': '84', '1': '85', '2': '86', '3': '87', '4': '88', '5': '89', '6': '90', '7': '91', '8': '92', '9': '93', '10': '94', '11': '95'})
        tokupandas = pd.concat([Tokutyo1, Tokutyo3, Tokutyo5, Tokutyo7, Tokutyo9, Tokutyo11, Tokutyo13, Tokutyo15], axis=1)  # 結合　914907 rows × 38 columns
        del Tokutyo1, Tokutyo3, Tokutyo5, Tokutyo7, Tokutyo9, Tokutyo11, Tokutyo13, Tokutyo15  # データを格納する用のlist作成，listの中にlistが222個，228個存在
        # スピード指数も取り出してデータの結合行う
        moto_df1 = pd.concat([moto_df, spped_from_db['speed_idx'], tokupandas], axis=1)  # 結合　914907 rows × 38 columns
        # いらない変数削除
        del spped_from_db
        moto_df1['happyotime'] = moto_df1['happyotime'].fillna(0)
        moto_df1['happyotime'] = moto_df1['happyotime'].astype(str)
        # 走破時計を4桁の数字⇒秒になおす
        def time_henkan(x):
            if len(x) == 7: # 7桁なら
                return '0' + x
        moto_df1['happyotime'] = moto_df1['happyotime'].apply(time_henkan)

        # moto_df1をn_uma_raceとn_raceに分割
        # n_uma_race
        n_uma_race_a0 = moto_df1.loc[:,
                        ['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'wakuban', 'umaban', 'a_umaban', 'kettonum', 'bamei', 'horse_p', 'father', 'sexcd', 'barei',
                         'tozaicd', 'futan', 'chokyosiryakusyo', 'banusiname', 'kisyuryakusyo', 'jockey_p', 'bataijyu', 'zogenfugo', 'zogensa', 'ijyocd', 'time', 'speed_idx',
                         'kakuteijyuni', 'chakusacd', 'jyuni1c', 'jyuni2c', 'jyuni3c', 'jyuni4c', 'odds', 'tanodds', 'ninki', 'tanninki', 'honsyokin', 'harontimel3', 'kettonum1',
                         'bamei1', 'timediff', 'kyakusitukubun', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20',
                         '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46',
                         '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63', '64', '65', '66', '67', '68', '69', '70', '71', '72',
                         '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95', 'ID']]
        n_uma_race_col_len = len(n_uma_race_a0.columns)  # 特徴量の数
        # n_race
        n_race_0 = moto_df1.loc[:,
                   ['hasso', 'happyotime', 'gradecd', 'syubetu', 'jyokencd5', 'kyori', 'trackcd', 'tenkocd', 'sibababacd', 'dirtbabacd', 'kigocd', 'lap1', 'lap2', 'lap3',
                    'lap4', 'lap5', 'lap6', 'lap7', 'lap8', 'lap9', 'lap10', 'lap11', 'lap12', 'lap13', 'lap14', 'lap15', 'lap16', 'lap17', 'lap18', 'syussou', 'corner1',
                    'syukaisu1', 'jyuni1', 'corner2', 'syukaisu2', 'jyuni2', 'corner3', 'syukaisu3', 'jyuni3', 'corner4', 'syukaisu4', 'jyuni4', 'ryakusyo6', 'tanuma1',
                    'tanpay1', 'tanuma2', 'tanpay2', 'tanuma3', 'tanpay3', 'fukuuma1', 'fukupay1', 'fukuuma2', 'fukupay2', 'fukuuma3', 'fukupay3', 'fukuuma4', 'fukupay4',
                    'fukuuma5', 'fukupay5', 'ID']]
        n_race_1_col_len = len(n_race_0.columns)  # 特徴量の数

        # 全馬の血統番号だけをn_uma_race_1から抽出，これで馬を検索する
        map_ketto = n_uma_race_a0.loc[:, ['kettonum']]
        # pandasをnumpyに変換する　ここからデータを抽出 高速化用
        np_uma_race = np.array(n_uma_race_a0)
        np_race = np.array(n_race_0)
        np_map_ketto = np.array(map_ketto)
        # レースIDの一覧を2つ作成　n_raceから一致するデータを取得する用
        raceID_uma = np.array(n_uma_race_a0['ID'])
        raceID_race = np.array(n_race_0['ID'])
        # 格納するlist作成
        list_list = [[] for torima in range(n_uma_race_col_len * 6)]  # n_uma_race用
        list_match = [[] for torima in range(n_race_1_col_len * 6)]  # n_race用

        # DB格納用データ作成編
        # ①馬柱データの作成
        for i in range(len(n_uma_race_a0)):  # 2010年からのレースについて馬柱の作成を実行する　914907 rows × 38 columns　10000につき12分
            if i % 100000 == 0:
                print(i)
            # ①-①n_uma_raceについての処理　馬データ
            ketto_index = np.where(np_map_ketto == np_map_ketto[i])  # 全レース(n_uma_race)から対象の馬のレースが存在する行のindexを全て取得
            ketto_basyo = (list(ketto_index[0]).index(i))  # 対象の馬のレースが全レース(n_uma_race)のなかで何番目に位置するかを取得 5とでれば理想
            # pandas用のデータはlistで取得する
            # データあれば対象の馬情報をすべて取得、なければnan 0走前
            flag_0 = ketto_index[0][ketto_basyo - 0] if ketto_basyo - 0 >= 0 else -10  # 0走前のindexの場所を取得　
            data_0 = list(np_uma_race[(flag_0)]) if ketto_basyo - 0 >= 0 else [np.nan] * n_uma_race_col_len  # 0走前のデータを行で取得　
            # データあれば対象の馬情報をすべて取得、なければnan 1走前
            flag_1 = ketto_index[0][ketto_basyo - 1] if ketto_basyo - 1 >= 0 else -10  # indexの場所を取得
            data_1 = list(np_uma_race[(flag_1)]) if ketto_basyo - 1 >= 0 else [np.nan] * n_uma_race_col_len
            # データあれば対象の馬情報をすべて取得、なければnan 2走前
            flag_2 = ketto_index[0][ketto_basyo - 2] if ketto_basyo - 2 >= 0 else -10  # indexの場所を取得
            data_2 = list(np_uma_race[(flag_2)]) if ketto_basyo - 2 >= 0 else [np.nan] * n_uma_race_col_len
            # データあれば対象の馬情報をすべて取得、なければnan 3走前
            flag_3 = ketto_index[0][ketto_basyo - 3] if ketto_basyo - 3 >= 0 else -10  # indexの場所を取得
            data_3 = list(np_uma_race[(flag_3)]) if ketto_basyo - 3 >= 0 else [np.nan] * n_uma_race_col_len
            # データあれば対象の馬情報をすべて取得、なければnan 4走前
            flag_4 = ketto_index[0][ketto_basyo - 4] if ketto_basyo - 4 >= 0 else -10  # indexの場所を取得
            data_4 = list(np_uma_race[(flag_4)]) if ketto_basyo - 4 >= 0 else [np.nan] * n_uma_race_col_len
            # データあれば対象の馬情報をすべて取得、なければnan 5走前
            flag_5 = ketto_index[0][ketto_basyo - 5] if ketto_basyo - 5 >= 0 else -10  # indexの場所を取得
            data_5 = list(np_uma_race[(flag_5)]) if ketto_basyo - 5 >= 0 else [np.nan] * n_uma_race_col_len
            # リストの結合 222列存在
            data_mix = data_0 + data_1 + data_2 + data_3 + data_4 + data_5
            # リスト内リストに馬柱データを格納する
            for torima in range(n_uma_race_col_len * 6):  # 特徴量×6回分（0～5走）
                list_list[torima] += [data_mix[torima]]

            # ①-②n_raceについての処理 レース　74157レース
            # データを格納する
            if flag_0 != -10 and (raceID_uma[flag_0] == raceID_race).any():  # データが存在し、n_umaのレースがm_raceにあるかを確認している
                ket = np.where(raceID_race == raceID_uma[flag_0])  # 同じ馬を取得n_umaがn_raceでどの行に存在するかを取得
                match_0 = list(np_race[ket[0][0]])  # 対象データを行で取得
            else:
                match_0 = [np.nan] * n_race_1_col_len
            if flag_1 != -10 and (raceID_uma[flag_1] == raceID_race).any():
                ket = np.where(raceID_race == raceID_uma[flag_1])  # 同じ馬を取得
                match_1 = list(np_race[ket[0][0]])  # 対象データの取得
            else:
                match_1 = [np.nan] * n_race_1_col_len
            if flag_2 != -10 and (raceID_uma[flag_2] == raceID_race).any():
                ket = np.where(raceID_race == raceID_uma[flag_2])  # 同じ馬を取得
                match_2 = list(np_race[ket[0][0]])  # 対象データの取得
            else:
                match_2 = [np.nan] * n_race_1_col_len
            if flag_3 != -10 and (raceID_uma[flag_3] == raceID_race).any():
                ket = np.where(raceID_race == raceID_uma[flag_3])  # 同じ馬を取得
                match_3 = list(np_race[ket[0][0]])  # 対象データの取得
            else:
                match_3 = [np.nan] * n_race_1_col_len
            if flag_4 != -10 and (raceID_uma[flag_4] == raceID_race).any():
                ket = np.where(raceID_race == raceID_uma[flag_4])  # 同じ馬を取得
                match_4 = list(np_race[ket[0][0]])  # 対象データの取得
            else:
                match_4 = [np.nan] * n_race_1_col_len
            if flag_5 != -10 and (raceID_uma[flag_5] == raceID_race).any():
                ket = np.where(raceID_race == raceID_uma[flag_5])  # 同じ馬を取得
                match_5 = list(np_race[ket[0][0]])  # 対象データの取得
            else:
                match_5 = [np.nan] * n_race_1_col_len
                # リストの結合 228列存在
            match_mix = match_0 + match_1 + match_2 + match_3 + match_4 + match_5
            # リスト内リストにn_raceデータを格納する
            for torima in range(n_race_1_col_len * 6):
                list_match[torima] += [match_mix[torima]]

        # いらない変数削除
        del n_uma_race_a0, n_race_0, map_ketto, np_uma_race, np_map_ketto, np_race, raceID_uma, raceID_race

        # DB編
        # ②-①Input_Data_UmaデータをDBに格納
        for bango in range(6):  # 0～5走前　ここは手動要素あり
            kasan = n_uma_race_col_len * bango  # listのどこからとるか指定
            print(bango)

            cre_data = pd.DataFrame(
                data={str(bango) + 'year': list_list[0 + kasan], str(bango) + 'monthday': list_list[1 + kasan],
                      str(bango) + 'jyocd': list_list[2 + kasan], str(bango) + 'kaiji': list_list[3 + kasan],
                      str(bango) + 'nichiji': list_list[4 + kasan],str(bango) + 'racenum': list_list[5 + kasan],
                      str(bango) + 'wakuban': list_list[6 + kasan], str(bango) + 'umaban': list_list[7 + kasan],
                      str(bango) + 'a_umaban': list_list[8 + kasan], str(bango) + 'kettonum': list_list[9 + kasan],
                      str(bango) + 'bamei': list_list[10 + kasan], str(bango) + 'horse_p': list_list[11 + kasan],
                      str(bango) + 'father': list_list[12 + kasan], str(bango) + 'sexcd': list_list[13 + kasan],
                      str(bango) + 'barei': list_list[14 + kasan], str(bango) + 'tozaicd': list_list[15 + kasan],
                      str(bango) + 'futan': list_list[16 + kasan], str(bango) + 'chokyosiryakusyo': list_list[17 + kasan],
                      str(bango) + 'banusiname': list_list[18 + kasan], str(bango) + 'kisyuryakusyo': list_list[19 + kasan],
                      str(bango) + 'jockey_p': list_list[20 + kasan], str(bango) + 'bataijyu': list_list[21 + kasan],
                      str(bango) + 'zogenfugo': list_list[22 + kasan], str(bango) + 'zogensa': list_list[23 + kasan],
                      str(bango) + 'ijyocd': list_list[24 + kasan], str(bango) + 'time': list_list[25 + kasan],
                      str(bango) + 'speed_idx': list_list[26 + kasan], str(bango) + 'kakuteijyuni': list_list[27 + kasan],
                      str(bango) + 'chakusacd': list_list[28 + kasan], str(bango) + 'jyuni1c': list_list[29 + kasan],
                      str(bango) + 'jyuni2c': list_list[30 + kasan], str(bango) + 'jyuni3c': list_list[31 + kasan],
                      str(bango) + 'jyuni4c': list_list[32 + kasan], str(bango) + 'odds': list_list[33 + kasan],
                      str(bango) + 'tanodds': list_list[34 + kasan], str(bango) + 'ninki': list_list[35 + kasan],
                      str(bango) + 'tanninki': list_list[36 + kasan], str(bango) + 'honsyokin': list_list[37 + kasan],
                      str(bango) + 'harontimel3': list_list[38 + kasan], str(bango) + 'kettonum1': list_list[39 + kasan],
                      str(bango) + 'bamei1': list_list[40 + kasan], str(bango) + 'timediff': list_list[41 + kasan],
                      str(bango) + 'kyakusitukubun': list_list[42 + kasan],
                      str(bango) + 't0': list_list[43 + kasan], str(bango) + 't1': list_list[44 + kasan],
                      str(bango) + 't2': list_list[45 + kasan], str(bango) + 't3': list_list[46 + kasan],
                      str(bango) + 't4': list_list[47 + kasan], str(bango) + 't5': list_list[48 + kasan],
                      str(bango) + 't6': list_list[49 + kasan], str(bango) + 't7': list_list[50 + kasan],
                      str(bango) + 't8': list_list[51 + kasan], str(bango) + 't9': list_list[52 + kasan],
                      str(bango) + 't10': list_list[53 + kasan], str(bango) + 't11': list_list[54 + kasan],
                      str(bango) + 't12': list_list[55 + kasan], str(bango) + 't13': list_list[56 + kasan],
                      str(bango) + 't14': list_list[57 + kasan], str(bango) + 't15': list_list[58 + kasan],
                      str(bango) + 't16': list_list[59 + kasan], str(bango) + 't17': list_list[60 + kasan],
                      str(bango) + 't18': list_list[61 + kasan], str(bango) + 't19': list_list[62 + kasan],
                      str(bango) + 't20': list_list[63 + kasan], str(bango) + 't21': list_list[64 + kasan],
                      str(bango) + 't22': list_list[65 + kasan], str(bango) + 't23': list_list[66 + kasan],
                      str(bango) + 't24': list_list[67 + kasan], str(bango) + 't25': list_list[68 + kasan],
                      str(bango) + 't26': list_list[69 + kasan], str(bango) + 't27': list_list[70 + kasan],
                      str(bango) + 't28': list_list[71 + kasan], str(bango) + 't29': list_list[72 + kasan],
                      str(bango) + 't30': list_list[73 + kasan], str(bango) + 't31': list_list[74 + kasan],
                      str(bango) + 't32': list_list[75 + kasan], str(bango) + 't33': list_list[76 + kasan],
                      str(bango) + 't34': list_list[77 + kasan], str(bango) + 't35': list_list[78 + kasan],
                      str(bango) + 't36': list_list[79 + kasan], str(bango) + 't37': list_list[80 + kasan],
                      str(bango) + 't38': list_list[81 + kasan], str(bango) + 't39': list_list[82 + kasan],
                      str(bango) + 't40': list_list[83 + kasan], str(bango) + 't41': list_list[84 + kasan],
                      str(bango) + 't42': list_list[85 + kasan], str(bango) + 't43': list_list[86 + kasan],
                      str(bango) + 't44': list_list[87 + kasan], str(bango) + 't45': list_list[88 + kasan],
                      str(bango) + 't46': list_list[89 + kasan], str(bango) + 't47': list_list[90 + kasan],
                      str(bango) + 't48': list_list[91 + kasan], str(bango) + 't49': list_list[92 + kasan],
                      str(bango) + 't50': list_list[93 + kasan], str(bango) + 't51': list_list[94 + kasan],
                      str(bango) + 't52': list_list[95 + kasan], str(bango) + 't53': list_list[96 + kasan],
                      str(bango) + 't54': list_list[97 + kasan], str(bango) + 't55': list_list[98 + kasan],
                      str(bango) + 't56': list_list[99 + kasan], str(bango) + 't57': list_list[100 + kasan],
                      str(bango) + 't58': list_list[101 + kasan], str(bango) + 't59': list_list[102 + kasan],
                      str(bango) + 't60': list_list[103 + kasan], str(bango) + 't61': list_list[104 + kasan],
                      str(bango) + 't62': list_list[105 + kasan], str(bango) + 't63': list_list[106 + kasan],
                      str(bango) + 't64': list_list[107 + kasan], str(bango) + 't65': list_list[108 + kasan],
                      str(bango) + 't66': list_list[109 + kasan], str(bango) + 't67': list_list[110 + kasan],
                      str(bango) + 't68': list_list[111 + kasan], str(bango) + 't69': list_list[112 + kasan],
                      str(bango) + 't70': list_list[113 + kasan], str(bango) + 't71': list_list[114 + kasan],
                      str(bango) + 't72': list_list[115 + kasan], str(bango) + 't73': list_list[116 + kasan],
                      str(bango) + 't74': list_list[117 + kasan], str(bango) + 't75': list_list[118 + kasan],
                      str(bango) + 't76': list_list[119 + kasan], str(bango) + 't77': list_list[120 + kasan],
                      str(bango) + 't78': list_list[121 + kasan], str(bango) + 't79': list_list[122 + kasan],
                      str(bango) + 't80': list_list[123 + kasan], str(bango) + 't81': list_list[124 + kasan],
                      str(bango) + 't82': list_list[125 + kasan], str(bango) + 't83': list_list[126 + kasan],
                      str(bango) + 't84': list_list[127 + kasan], str(bango) + 't85': list_list[128 + kasan],
                      str(bango) + 't86': list_list[129 + kasan], str(bango) + 't87': list_list[130 + kasan],
                      str(bango) + 't88': list_list[131 + kasan], str(bango) + 't89': list_list[132 + kasan],
                      str(bango) + 't90': list_list[133 + kasan], str(bango) + 't91': list_list[134 + kasan],
                      str(bango) + 't92': list_list[135 + kasan], str(bango) + 't93': list_list[136 + kasan],
                      str(bango) + 't94': list_list[137 + kasan], str(bango) + 't95': list_list[138 + kasan],
                      str(bango) + 'ID': list_list[139 + kasan]},
                columns=[str(bango) + 'year', str(bango) + 'monthday', str(bango) + 'jyocd', str(bango) + 'kaiji',
                         str(bango) + 'nichiji', str(bango) + 'racenum', str(bango) + 'wakuban',
                         str(bango) + 'umaban', str(bango) + 'a_umaban', str(bango) + 'kettonum', str(bango) + 'bamei', str(bango) + 'horse_p',
                         str(bango) + 'father',str(bango) + 'sexcd',str(bango) + 'barei', str(bango) + 'tozaicd', str(bango) + 'futan',
                         str(bango) + 'chokyosiryakusyo', str(bango) + 'banusiname', str(bango) + 'kisyuryakusyo', str(bango) + 'jockey_p', str(bango) + 'bataijyu',
                         str(bango) + 'zogenfugo', str(bango) + 'zogensa', str(bango) + 'ijyocd', str(bango) + 'time', str(bango) + 'speed_idx',
                         str(bango) + 'kakuteijyuni', str(bango) + 'chakusacd', str(bango) + 'jyuni1c',
                         str(bango) + 'jyuni2c', str(bango) + 'jyuni3c', str(bango) + 'jyuni4c',
                         str(bango) + 'odds', str(bango) + 'tanodds', str(bango) + 'ninki', str(bango) + 'tanninki',
                         str(bango) + 'honsyokin', str(bango) + 'harontimel3', str(bango) + 'kettonum1',
                         str(bango) + 'bamei1', str(bango) + 'timediff', str(bango) + 'kyakusitukubun',
                         str(bango) + 't0', str(bango) + 't1', str(bango) + 't2', str(bango) + 't3',
                         str(bango) + 't4', str(bango) + 't5', str(bango) + 't6', str(bango) + 't7', str(bango) + 't8',
                         str(bango) + 't9', str(bango) + 't10', str(bango) + 't11', str(bango) + 't12', str(bango) + 't13',
                         str(bango) + 't14', str(bango) + 't15', str(bango) + 't16', str(bango) + 't17', str(bango) + 't18',
                         str(bango) + 't19', str(bango) + 't20', str(bango) + 't21', str(bango) + 't22', str(bango) + 't23',
                         str(bango) + 't24', str(bango) + 't25', str(bango) + 't26', str(bango) + 't27', str(bango) + 't28',
                         str(bango) + 't29', str(bango) + 't30', str(bango) + 't31', str(bango) + 't32', str(bango) + 't33',
                         str(bango) + 't34', str(bango) + 't35', str(bango) + 't36', str(bango) + 't37', str(bango) + 't38',
                         str(bango) + 't39', str(bango) + 't40', str(bango) + 't41', str(bango) + 't42', str(bango) + 't43',
                         str(bango) + 't44', str(bango) + 't45', str(bango) + 't46', str(bango) + 't47', str(bango) + 't48',
                         str(bango) + 't49', str(bango) + 't50', str(bango) + 't51', str(bango) + 't52', str(bango) + 't53',
                         str(bango) + 't54', str(bango) + 't55', str(bango) + 't56', str(bango) + 't57', str(bango) + 't58',
                         str(bango) + 't59', str(bango) + 't60', str(bango) + 't61', str(bango) + 't62', str(bango) + 't63',
                         str(bango) + 't64', str(bango) + 't65', str(bango) + 't66', str(bango) + 't67', str(bango) + 't68',
                         str(bango) + 't69', str(bango) + 't70', str(bango) + 't71', str(bango) + 't72', str(bango) + 't73',
                         str(bango) + 't74', str(bango) + 't75', str(bango) + 't76', str(bango) + 't77', str(bango) + 't78',
                         str(bango) + 't79', str(bango) + 't80', str(bango) + 't81', str(bango) + 't82', str(bango) + 't83',
                         str(bango) + 't84', str(bango) + 't85', str(bango) + 't86', str(bango) + 't87', str(bango) + 't88',
                         str(bango) + 't89', str(bango) + 't90', str(bango) + 't91', str(bango) + 't92', str(bango) + 't93',
                         str(bango) + 't94', str(bango) + 't95', str(bango) + 'ID'])
            # indexを与える
            cre_data_1 = cre_data.reset_index()
            # データpostgreへ
            conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
            cursor = conn.cursor()  # データベースを操作できるようにする
            cre_data_1.to_sql(str(bango) + "Input_Data_Uma", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
            # -------------実行ここまで
            cursor.close()  # データベースの操作を終了する
            conn.commit()  # 変更をデータベースに保存
            conn.close()  # データベースを閉じる

            # いらない変数削除
            del cre_data, cre_data_1

        # ②-②Input_Data_RaceデータをDBに格納
        for bango in range(6):  # 0～5
            kasan = n_race_1_col_len * bango  # listのどこからとるか指定
            print(bango)

            cre_data = pd.DataFrame(
                data={str(bango) + 'hasso': list_match[0 + kasan], str(bango) + 'happyotime': list_match[1 + kasan],
                      str(bango) + 'gradecd': list_match[2 + kasan], str(bango) + 'syubetu': list_match[3 + kasan],
                      str(bango) + 'jyokencd5': list_match[4 + kasan], str(bango) + 'kyori': list_match[5 + kasan],
                      str(bango) + 'trackcd': list_match[6 + kasan], str(bango) + 'tenkocd': list_match[7 + kasan],
                      str(bango) + 'sibababacd': list_match[8 + kasan], str(bango) + 'dirtbabacd': list_match[9 + kasan],
                      str(bango) + 'kigocd': list_match[10 + kasan], str(bango) + 'laptime1': list_match[11 + kasan],
                      str(bango) + 'laptime2': list_match[12 + kasan], str(bango) + 'laptime3': list_match[13 + kasan],
                      str(bango) + 'laptime4': list_match[14 + kasan],str(bango) + 'laptime5': list_match[15 + kasan],
                      str(bango) + 'laptime6': list_match[16 + kasan], str(bango) + 'laptime7': list_match[17 + kasan],
                      str(bango) + 'laptime8': list_match[18 + kasan], str(bango) + 'laptime9': list_match[19 + kasan],
                      str(bango) + 'laptime10': list_match[20 + kasan], str(bango) + 'laptime11': list_match[21 + kasan], \
                      str(bango) + 'laptime12': list_match[22 + kasan], str(bango) + 'laptime13': list_match[23 + kasan],
                      str(bango) + 'laptime14': list_match[24 + kasan], str(bango) + 'laptime15': list_match[25 + kasan], \
                      str(bango) + 'laptime16': list_match[26 + kasan], str(bango) + 'laptime17': list_match[27 + kasan],
                      str(bango) + 'laptime18': list_match[28 + kasan], str(bango) + 'syussotosu': list_match[29 + kasan], \
                      str(bango) + 'corner1': list_match[30 + kasan], str(bango) + 'syukaisu1': list_match[31 + kasan],
                      str(bango) + 'jyuni1': list_match[32 + kasan], str(bango) + 'corner2': list_match[33 + kasan], \
                      str(bango) + 'syukaisu2': list_match[34 + kasan], str(bango) + 'jyuni2': list_match[35 + kasan],
                      str(bango) + 'corner3': list_match[36 + kasan],str(bango) + 'syukaisu3': list_match[37 + kasan],
                      str(bango)+ 'jyuni3': list_match[38 + kasan], str(bango) + 'corner4': list_match[39 + kasan],
                      str(bango) + 'syukaisu4': list_match[40 + kasan], str(bango) + 'jyuni4': list_match[41 + kasan],
                      str(bango) + 'ryakusyo6': list_match[42 + kasan], str(bango) + 'tanuma1': list_match[43 + kasan],
                      str(bango) + 'tanpay1': list_match[44 + kasan], str(bango) + 'tanuma2': list_match[45 + kasan],
                      str(bango) + 'tanpay2': list_match[46 + kasan], str(bango) + 'tanuma3': list_match[47 + kasan],
                      str(bango) + 'tanpay3': list_match[48 + kasan], str(bango) + 'fukuuma1': list_match[49 + kasan],
                      str(bango) + 'fukupay1': list_match[50 + kasan], str(bango) + 'fukuuma2': list_match[51 + kasan],
                      str(bango) + 'fukupay2': list_match[52 + kasan], str(bango) + 'fukuuma3': list_match[53 + kasan],
                      str(bango) + 'fukupay3': list_match[54 + kasan], str(bango) + 'fukuuma4': list_match[55 + kasan],
                      str(bango) + 'fukupay4': list_match[56 + kasan], str(bango) + 'fukuuma5': list_match[57 + kasan],
                      str(bango) + 'fukupay5': list_match[58 + kasan], str(bango) + 'ID': list_match[59 + kasan]},
                columns=[str(bango) + 'hasso', str(bango) + 'happyotime', str(bango) + 'gradecd', str(bango) + 'syubetu',
                         str(bango) + 'jyokencd5', str(bango) + 'kyori', str(bango) + 'trackcd', str(bango) + 'tenkocd',
                         str(bango) + 'sibababacd', str(bango) + 'dirtbabacd', str(bango) + 'kigocd', str(bango) + 'laptime1',
                         str(bango) + 'laptime2', str(bango) + 'laptime3', str(bango) + 'laptime4', str(bango) + 'laptime5',
                         str(bango) + 'laptime6', str(bango) + 'laptime7', str(bango) + 'laptime8', str(bango) + 'laptime9',
                         str(bango) + 'laptime10', str(bango) + 'laptime11', str(bango) + 'laptime12', str(bango) + 'laptime13',
                         str(bango) + 'laptime14', str(bango) + 'laptime15', str(bango) + 'laptime16', str(bango) + 'laptime17',
                         str(bango) + 'laptime18', str(bango) + 'syussotosu', str(bango) + 'corner1', str(bango) + 'syukaisu1',
                         str(bango) + 'jyuni1', str(bango) + 'corner2', str(bango) + 'syukaisu2', str(bango) + 'jyuni2',
                         str(bango) + 'corner3', str(bango) + 'syukaisu3', str(bango) + 'jyuni3', str(bango) + 'corner4',
                         str(bango) + 'syukaisu4', str(bango) + 'jyuni4', str(bango) + 'ryakusyo6', str(bango) + 'tanuma1', str(bango) + 'tanpay1',
                         str(bango) + 'tanuma2', str(bango) + 'tanpay2', str(bango) + 'tanuma3', str(bango) + 'tanpay3', str(bango) + 'fukuuma1',
                         str(bango) + 'fukupay1', str(bango) + 'fukuuma2', str(bango) + 'fukupay2', str(bango) + 'fukuuma3', str(bango) + 'fukupay3',
                         str(bango) + 'fukuuma4', str(bango) + 'fukupay4', str(bango) + 'fukuuma5', str(bango) + 'fukupay5', str(bango) + 'ID'])

            # indexを与える
            cre_data_1 = cre_data.reset_index()
            # データpostgreへ
            conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
            cursor = conn.cursor()  # データベースを操作できるようにする
            cre_data_1.to_sql(str(bango) + "Input_Data_Race", ENGINE, if_exists='replace',index=False)  # postgreに作成データを出力，存在してたらreplace
            # -------------実行ここまで
            cursor.close()  # データベースの操作を終了する
            conn.commit()  # 変更をデータベースに保存
            conn.close()  # データベースを閉じる

            # いらない変数削除
            del cre_data, cre_data_1

        process_time = time.time() - start
        print(process_time / 60)  # 850min

# endregion

# classの実行
# input_data.output()

# 7.LGBM class⇒LGBMで各馬の勝率を算出するclass。その勝率をもとにシミュレーション行う。このファイルは別ファイル。