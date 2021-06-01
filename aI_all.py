# region postgre_connector:postgreとのデータをやり取りするスクリプト コードの最適化までOK
# ⓪ライブラリのインポート
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import numpy as np
# ①DBの初期設定
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
# 元データ
sql1 = "SELECT * FROM public.n_uma;"  # 実行SQL 競走馬マスタ
sql2 = "SELECT * FROM public.n_uma_race;"  # 実行SQL 馬毎レース情報
sql3 = "SELECT * FROM public.n_race;"  # 実行SQL レース詳細
sql4 = "SELECT * FROM public.n_harai;"  # 実行SQL 払い戻し
sql5 = "SELECT * FROM public.n_kisyu_seiseki;"  # 実行SQL　騎手成績
sql6 = "SELECT * FROM public.n_kisyu;"  # 実行SQL　騎手成績
# 5走分データ
sql7 = 'SELECT * FROM public."0Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql8 = 'SELECT * FROM public."0Input_Data_Race" ORDER BY index ASC;'  # 教師データ
sql9 = 'SELECT * FROM public."1Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql10 = 'SELECT * FROM public."1Input_Data_Race" ORDER BY index ASC;'  # 教師データ
sql11 = 'SELECT * FROM public."2Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql12 = 'SELECT * FROM public."2Input_Data_Race" ORDER BY index ASC;'  # 教師データ
sql13 = 'SELECT * FROM public."3Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql14 = 'SELECT * FROM public."3Input_Data_Race" ORDER BY index ASC;'  # 教師データ
sql15 = 'SELECT * FROM public."4Input_Data_Uma" ORDER BY index ASC'  # 教師データ
sql16 = 'SELECT * FROM public."4Input_Data_Race" ORDER BY index ASC;'  # 教師データ
sql17 = 'SELECT * FROM public."5Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql18 = 'SELECT * FROM public."5Input_Data_Race" ORDER BY index ASC;'  # 教師データ
# 特徴量作成用データ
sql19 = 'SELECT * FROM public."data_sakuseiyou" ORDER BY index ASC;'  # 教師データ
# sql20 = 'SELECT * FROM public."tmp";'#教師データ
sql20 = 'SELECT * FROM public."tokutyo_moto" ORDER BY index ASC;'  # 教師データ
# 特徴量データ
sql21 = 'SELECT * FROM public."t_kisyu_box_tanharai" ORDER BY index ASC;'  # 教師データ
sql22 = 'SELECT * FROM public."t_kisyu_box_fukuharai" ORDER BY index ASC;'  # 教師データ
sql23 = 'SELECT * FROM public."t_kisyu_box_syouritu" ORDER BY index ASC;'  # 教師データ
sql24 = 'SELECT * FROM public."t_kisyu_box_fukuritu" ORDER BY index ASC;'  # 教師データ
sql25 = 'SELECT * FROM public."t_chokyo_box_tanharai" ORDER BY index ASC;'  # 教師データ
sql26 = 'SELECT * FROM public."t_chokyo_box_fukuharai" ORDER BY index ASC;'  # 教師データ
sql27 = 'SELECT * FROM public."t_chokyo_box_syouritu" ORDER BY index ASC;'  # 教師データ
sql28 = 'SELECT * FROM public."t_chokyo_box_fukuritu" ORDER BY index ASC;'  # 教師データ
sql29 = 'SELECT * FROM public."t_banu_box_tanharai" ORDER BY index ASC;'  # 教師データ
sql30 = 'SELECT * FROM public."t_banu_box_fukuharai" ORDER BY index ASC;'  # 教師データ
sql31 = 'SELECT * FROM public."t_banu_box_syouritu" ORDER BY index ASC;'  # 教師データ
sql32 = 'SELECT * FROM public."t_banu_box_fukuritu" ORDER BY index ASC;'  # 教師データ
sql33 = 'SELECT * FROM public."t_syu_box_tanharai" ORDER BY index ASC;'  # 教師データ
sql34 = 'SELECT * FROM public."t_syu_box_fukuharai" ORDER BY index ASC;'  # 教師データ
sql35 = 'SELECT * FROM public."t_syu_box_syouritu" ORDER BY index ASC;'  # 教師データ
sql36 = 'SELECT * FROM public."t_syu_box_fukuritu" ORDER BY index ASC;'  # 教師データ
sql37 = 'SELECT * FROM public."t_kisyu_sample" ORDER BY index ASC;'  # サンプル数
sql38 = 'SELECT * FROM public."t_chokyo_sample" ORDER BY index ASC;'  # サンプル数
sql39 = 'SELECT * FROM public."t_banu_sample" ORDER BY index ASC;'  # サンプル数
sql40 = 'SELECT * FROM public."t_syu_sample" ORDER BY index ASC;'  # サンプル数
sql41 = 'SELECT * FROM public."t_kisyu_main" ORDER BY index ASC;'  # サンプル数
sql42 = 'SELECT * FROM public."t_chokyo_main" ORDER BY index ASC;'  # サンプル数
sql43 = 'SELECT * FROM public."t_banu_main" ORDER BY index ASC;'  # サンプル数
sql44 = 'SELECT * FROM public."t_syu_main" ORDER BY index ASC;'  # サンプル数
sql45 = 'SELECT * FROM public."t_kisyu_indexnum" ORDER BY index ASC;'  # 対象index番号
sql46 = 'SELECT * FROM public."t_chokyo_indexnum" ORDER BY index ASC;'  # 対象index番号
sql47 = 'SELECT * FROM public."t_banu_indexnum" ORDER BY index ASC;'  # 対象index番号
sql48 = 'SELECT * FROM public."t_syu_indexnum" ORDER BY index ASC;'  # 対象index番号
# スピード指数作成用データ
sql49 = 'SELECT * FROM public."a_time" ORDER BY index ASC;'  # 教師データ
# スピード指数データ
sql50 = 'SELECT * FROM public."speed_index" ORDER BY index ASC;'  # 教師データ
# target-encoding 特徴量
sql51 = 'SELECT * FROM public."0Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql52 = 'SELECT * FROM public."1Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql53 = 'SELECT * FROM public."2Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql54 = 'SELECT * FROM public."3Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql55 = 'SELECT * FROM public."4Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql56 = 'SELECT * FROM public."5Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql57 = 'SELECT * FROM public."6Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql58 = 'SELECT * FROM public."7Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql59 = 'SELECT * FROM public."8Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql60 = 'SELECT * FROM public."9Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql61 = 'SELECT * FROM public."10Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql62 = 'SELECT * FROM public."11Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql63 = 'SELECT * FROM public."12Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql64 = 'SELECT * FROM public."13Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql65 = 'SELECT * FROM public."14Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
sql66 = 'SELECT * FROM public."15Tokutyo_data" ORDER BY index ASC;'  # 対象index番号
# DBのデータをpandasで取得---------------------------------------------------------------
# 元データ
n_uma_pro = pd.read_sql(sql1, conn)  # sql:実行したいsql，conn:対象のdb名
# n_uma_race = pd.read_sql(sql2, conn)  # sql:実行したいsql，conn:対象のdb名
# n_race = pd.read_sql(sql3, conn)  # sql:実行したいsql，conn:対象のdb名
# n_harai = pd.read_sql(sql4, conn)  # sql:実行したいsql，conn:対象のdb名
# n_kisyu_sei = pd.read_sql(sql5, conn)#sql:実行したいsql，conn:対象のdb名
# n_kisyu = pd.read_sql(sql6, conn)#sql:実行したいsql，conn:対象のdb名
# 5走分データ 全部取得するとメモリ95％とかになる
# n_input_0uma = pd.read_sql(sql7, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_0race = pd.read_sql(sql8, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_1uma = pd.read_sql(sql9, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_1race = pd.read_sql(sql10, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_2uma = pd.read_sql(sql11, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_2race = pd.read_sql(sql12, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_3uma = pd.read_sql(sql13, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_3race = pd.read_sql(sql14, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_4uma = pd.read_sql(sql15, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_4race = pd.read_sql(sql16, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_5uma = pd.read_sql(sql17, conn)#sql:実行したいsql，conn:対象のdb名
# n_input_5race = pd.read_sql(sql18, conn)#sql:実行したいsql，conn:対象のdb名
# 特徴量作成用データ
# data_sakuseiyou = pd.read_sql(sql19, conn)#sql:実行したいsql，conn:対象のdb名
tokutyo_moto = pd.read_sql(sql20, conn)  # sql:実行したいsql，conn:対象のdb名
# 特徴量データ
# akisyu_box_tanharai = pd.read_sql(sql21, conn)  # sql:実行したいsql，conn:対象のdb名
# akisyu_box_fukuharai = pd.read_sql(sql22, conn)  # sql:実行したいsql，conn:対象のdb名
# akisyu_box_syouritu = pd.read_sql(sql23, conn)  # sql:実行したいsql，conn:対象のdb名
# akisyu_box_fukuritu = pd.read_sql(sql24, conn)  # sql:実行したいsql，conn:対象のdb名
# achokyo_box_tanharai = pd.read_sql(sql25, conn)  # sql:実行したいsql，conn:対象のdb名
# achokyo_box_fukuharai = pd.read_sql(sql26, conn)  # sql:実行したいsql，conn:対象のdb名
# achokyo_box_syouritu = pd.read_sql(sql27, conn)  # sql:実行したいsql，conn:対象のdb名
# achokyo_box_fukuritu = pd.read_sql(sql28, conn)  # sql:実行したいsql，conn:対象のdb名
# abanu_box_tanharai = pd.read_sql(sql29, conn)  # sql:実行したいsql，conn:対象のdb名
# abanu_box_fukuharai = pd.read_sql(sql30, conn)  # sql:実行したいsql，conn:対象のdb名
# abanu_box_syouritu = pd.read_sql(sql31, conn)  # sql:実行したいsql，conn:対象のdb名
# abanu_box_fukuritu = pd.read_sql(sql32, conn)  # sql:実行したいsql，conn:対象のdb名
# asyu_box_tanharai = pd.read_sql(sql33, conn)  # sql:実行したいsql，conn:対象のdb名
# asyu_box_fukuharai = pd.read_sql(sql34, conn)  # sql:実行したいsql，conn:対象のdb名
# asyu_box_syouritu = pd.read_sql(sql35, conn)  # sql:実行したいsql，conn:対象のdb名
# asyu_box_fukuritu = pd.read_sql(sql36, conn)  # sql:実行したいsql，conn:対象のdb名
# at_kisyu_sample = pd.read_sql(sql37, conn)  # sql:実行したいsql，conn:対象のdb名
# at_chokyo_sample = pd.read_sql(sql38, conn)  # sql:実行したいsql，conn:対象のdb名
# at_banu_sample = pd.read_sql(sql39, conn)  # sql:実行したいsql，conn:対象のdb名
# at_syu_sample = pd.read_sql(sql40, conn)  # sql:実行したいsql，conn:対象のdb名
# at_kisyu_main = pd.read_sql(sql41, conn)  # sql:実行したいsql，conn:対象のdb名
# at_chokyo_main = pd.read_sql(sql42, conn)  # sql:実行したいsql，conn:対象のdb名
# at_banu_main = pd.read_sql(sql43, conn)  # sql:実行したいsql，conn:対象のdb名
# at_syu_main = pd.read_sql(sql44, conn)  # sql:実行したいsql，conn:対象のdb名
# akisyu_indexnum = pd.read_sql(sql45, conn)  # sql:実行したいsql，conn:対象のdb名
# achokyo_indexnum = pd.read_sql(sql46, conn)  # sql:実行したいsql，conn:対象のdb名a
# abanu_indexnum = pd.read_sql(sql47, conn)  # sql:実行したいsql，conn:対象のdb名
# syu_indexnum = pd.read_sql(sql48, conn)  # sql:実行したいsql，conn:対象のdb名
# スピード指数作成用データ
# a_time = pd.read_sql(sql49, conn)  # sql:実行したいsql，conn:対象のdb名
# スピード指数データ
# spped_from_db = pd.read_sql(sql50, conn)  # sql:実行したいsql，conn:対象のdb名
# target-encoding 特徴量
# Tokutyo0 = (pd.read_sql(sql51, conn))#listにするとメモリすごい食う　7ギガくらいの差ある　pandas7.0GB,list14GB,np13.8GB 0
# Tokutyo1 = (pd.read_sql(sql52, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo2 = (pd.read_sql(sql53, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo3 = (pd.read_sql(sql54, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo4 = (pd.read_sql(sql55, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo5 = (pd.read_sql(sql56, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo6 = (pd.read_sql(sql57, conn)).values.tolist() # sql:実行したいsql，conn:対象のdb名
# Tokutyo7 = (pd.read_sql(sql58, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo8 = (pd.read_sql(sql59, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo9 = (pd.read_sql(sql60, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo10 = (pd.read_sql(sql61, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo11 = (pd.read_sql(sql62, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo12 = (pd.read_sql(sql63, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo13 = (pd.read_sql(sql64, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo14 = (pd.read_sql(sql65, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# Tokutyo15 = (pd.read_sql(sql66, conn)).values.tolist()  # sql:実行したいsql，conn:対象のdb名
# finish the cursor
ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる
# endregion