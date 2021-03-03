# region postgre_connector:postgreとのデータをやり取りするスクリプト OK
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import numpy as np

# ①初期設定
DATABASE = 'postgresql'
USER = 'postgres'
PASSWORD = 'taku0703'
HOST = 'localhost'
PORT = '5432'
DB_NAME = 'everydb2'
CONNECT_STR = '{}://{}:{}@{}:{}/{}'.format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)
# connect postgreSQL　ポスグレ接続
conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
cursor = conn.cursor()  # データベースを操作できるようにする

#  cur.execute('SQL') SQL実行
# ------------- 実行ここから
# postgreからpandasにデータを出力
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
sql15 = 'SELECT * FROM public."4Input_Data_Uma"; ORDER BY index ASC'  # 教師データ
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
# スピード指数作成用データ
sql45 = 'SELECT * FROM public."a_time" ORDER BY index ASC;'  # 教師データ
# スピード指数データ
sql46 = 'SELECT * FROM public."speed_index" ORDER BY index ASC;'  # 教師データ

# pandasで読み込み---------------------------------------------------------------
# 元データ
n_uma_pro = pd.read_sql(sql1, conn)  # sql:実行したいsql，conn:対象のdb名
n_uma_race = pd.read_sql(sql2, conn)  # sql:実行したいsql，conn:対象のdb名
n_race = pd.read_sql(sql3, conn)  # sql:実行したいsql，conn:対象のdb名
n_harai = pd.read_sql(sql4, conn)  # sql:実行したいsql，conn:対象のdb名
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
akisyu_box_tanharai = pd.read_sql(sql21, conn)  # sql:実行したいsql，conn:対象のdb名
akisyu_box_fukuharai = pd.read_sql(sql22, conn)  # sql:実行したいsql，conn:対象のdb名
akisyu_box_syouritu = pd.read_sql(sql23, conn)  # sql:実行したいsql，conn:対象のdb名
akisyu_box_fukuritu = pd.read_sql(sql24, conn)  # sql:実行したいsql，conn:対象のdb名
achokyo_box_tanharai = pd.read_sql(sql25, conn)  # sql:実行したいsql，conn:対象のdb名
achokyo_box_fukuharai = pd.read_sql(sql26, conn)  # sql:実行したいsql，conn:対象のdb名
achokyo_box_syouritu = pd.read_sql(sql27, conn)  # sql:実行したいsql，conn:対象のdb名
achokyo_box_fukuritu = pd.read_sql(sql28, conn)  # sql:実行したいsql，conn:対象のdb名
abanu_box_tanharai = pd.read_sql(sql29, conn)  # sql:実行したいsql，conn:対象のdb名
abanu_box_fukuharai = pd.read_sql(sql30, conn)  # sql:実行したいsql，conn:対象のdb名
abanu_box_syouritu = pd.read_sql(sql31, conn)  # sql:実行したいsql，conn:対象のdb名
abanu_box_fukuritu = pd.read_sql(sql32, conn)  # sql:実行したいsql，conn:対象のdb名
asyu_box_tanharai = pd.read_sql(sql33, conn)  # sql:実行したいsql，conn:対象のdb名
asyu_box_fukuharai = pd.read_sql(sql34, conn)  # sql:実行したいsql，conn:対象のdb名
asyu_box_syouritu = pd.read_sql(sql35, conn)  # sql:実行したいsql，conn:対象のdb名
asyu_box_fukuritu = pd.read_sql(sql36, conn)  # sql:実行したいsql，conn:対象のdb名
at_kisyu_sample = pd.read_sql(sql37, conn)  # sql:実行したいsql，conn:対象のdb名
at_chokyo_sample = pd.read_sql(sql38, conn)  # sql:実行したいsql，conn:対象のdb名
at_banu_sample = pd.read_sql(sql39, conn)  # sql:実行したいsql，conn:対象のdb名
at_syu_sample = pd.read_sql(sql40, conn)  # sql:実行したいsql，conn:対象のdb名
at_kisyu_main = pd.read_sql(sql41, conn)  # sql:実行したいsql，conn:対象のdb名
at_chokyo_main = pd.read_sql(sql42, conn)  # sql:実行したいsql，conn:対象のdb名
at_banu_main = pd.read_sql(sql43, conn)  # sql:実行したいsql，conn:対象のdb名
at_syu_main = pd.read_sql(sql44, conn)  # sql:実行したいsql，conn:対象のdb名
# スピード指数作成用データ
a_time = pd.read_sql(sql45, conn)#sql:実行したいsql，conn:対象のdb名
# スピード指数データ
spped_from_db= pd.read_sql(sql46, conn)#sql:実行したいsql，conn:対象のdb名
# -------------実行ここまで
# pandasからpostgreにデータを出力
ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
# -------------実行ここまで
# test1().to_sql("test_uma", ENGINE,if_exists='replace',index=False)#postgreに出力 df2の内容をtestテーブルとして出力　存在してたらreplace
# test2().to_sql("test_uma_race", ENGINE,if_exists='replace',index=False)#postgreに出力 df2の内容をtestテーブルとして出力　存在してたらreplace
# test3().to_sql("test_harai", ENGINE,if_exists='replace',index=False)#postgreに出力 df2の内容をtestテーブルとして出力　存在してたらreplace
# cre_data.to_sql("Input_Data", ENGINE,if_exists='replace',index=False)#postgreに出力 df2の内容をtestテーブルとして出力　存在してたらreplace
# -------------実行ここまで
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる
# endregion

# region speed_generator_moto_0:スピード指数作成のための元データを作成してDBに出力するスクリプト OK
# ⓪騎手・調教師・血統・馬主・生産者ごとの勝率・複勝率・単勝回収率・回収率などの特徴量を作成
# uma_raceから必要な馬の情報の取り出す
import numpy as np
matome_data = n_uma_race.loc[:,['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'bamei', 'futan', 'time', 'kakuteijyuni']]
matome_data['ID'] = n_uma_race['year'] + n_uma_race['monthday'] + n_uma_race['jyocd'] + n_uma_race['kaiji'] +n_uma_race['nichiji'] + n_uma_race['racenum']  # レースIDの作成
# raceから必要なレースの情報の取り出す
matomerare_race = n_race.loc[:,['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'gradecd', 'syubetucd', 'jyokencd1','jyokencd2', 'jyokencd3', 'jyokencd4',
'jyokencd5', 'kyori', 'trackcd', 'tenkocd', 'sibababacd', 'dirtbabacd', 'kigocd']]
matomerare_race['ID'] = n_race['year'] + n_race['monthday'] + n_race['jyocd'] + n_race['kaiji'] + n_race['nichiji'] +n_race['racenum']  # レースIDの作成
# レースIDをlistにして検索しやすいようにする
matome_data_list = list(matome_data['ID'])  # レースIDをlistで取得
matomerare_race_list = list(matomerare_race['ID'])  # レースIDをlistで取得
# 準備 必要なものだけlist化
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

# 行番号を探す関数
def my_index(l, x, default=np.nan):
    if x in l:
        return l.index(x)  # 一致するデータがあるときはindexを返す
    else:
        return default  # ないときはNaNを返す

# データはlistに入れて高速化
a_gradecd, a_syubetu, a_jyokencd1, a_jyokencd2, a_jyokencd3, a_jyokencd4, a_jyokencd5, a_kyori, a_trackcd, a_tenkocd, a_sibababacd, a_dirtbabacd, a_kigocd = [], [], [], [], [], [], [], [], [], [], [], [], []
# for文でデータを抽出
for i in range(len(matome_data)):
    if i % 100000 == 0:
        print(i)
    idx = my_index(matomerare_race_list, matome_data_list[i])  # 行番号を取得
    # レースID
    if np.isnan(idx):  # NaNならTrue
        moji_str0a = np.nan
        moji_str1a = np.nan
        moji_str1b = np.nan
        moji_str1c = np.nan
        moji_str1d = np.nan
        moji_str1e = np.nan
        moji_str1f = np.nan
        moji_str1g = np.nan
        moji_str1h = np.nan
        moji_str1i = np.nan
        moji_str1j = np.nan
        moji_str1k = np.nan
        moji_str1l = np.nan
    else:
        moji_str0a = gradecd_list[idx]
        moji_str1a = syubetu_list[idx]
        moji_str1b = jyokencd1_list[idx]
        moji_str1c = jyokencd2_list[idx]
        moji_str1d = jyokencd3_list[idx]
        moji_str1e = jyokencd4_list[idx]
        moji_str1f = jyokencd5_list[idx]
        moji_str1g = kyori_list[idx]
        moji_str1h = trackcd_list[idx]
        moji_str1i = tenkocd_list[idx]
        moji_str1j = sibababacd_list[idx]
        moji_str1k = dirtbabacd_list[idx]
        moji_str1l = kigocd_list[idx]

    # データをどういれるか
    a_gradecd += [moji_str0a]
    a_syubetu += [moji_str1a]
    a_jyokencd1 += [moji_str1b]
    a_jyokencd2 += [moji_str1c]
    a_jyokencd3 += [moji_str1d]
    a_jyokencd4 += [moji_str1e]
    a_jyokencd5 += [moji_str1f]
    a_kyori += [moji_str1g]
    a_trackcd += [moji_str1h]
    a_tenkocd += [moji_str1i]
    a_sibababacd += [moji_str1j]
    a_dirtbabacd += [moji_str1k]
    a_kigocd += [moji_str1l]

# データの結合
merge = pd.DataFrame(
    data={'gradecd': a_gradecd, 'syubetu': a_syubetu, 'jyokencd1': a_jyokencd1, 'jyokencd2': a_jyokencd2,
          'jyokencd3': a_jyokencd3,'jyokencd4': a_jyokencd4, 'jyokencd5': a_jyokencd5, 'kyori': a_kyori, 'trackcd': a_trackcd,
          'tenkocd': a_tenkocd, 'sibababacd': a_sibababacd,'dirtbabacd': a_dirtbabacd, 'kigocd': a_kigocd},
    columns=['gradecd', 'syubetu', 'jyokencd1', 'jyokencd2', 'jyokencd3', 'jyokencd4', 'jyokencd5', 'kyori', 'trackcd',
             'tenkocd', 'sibababacd', 'dirtbabacd', 'dirtbabacd', 'kigocd'])
saigo = pd.concat([matome_data, merge], axis=1)
# データpostgreへ
cre_data_1 = saigo.reset_index()  # indexを与える
conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
cursor = conn.cursor()  # データベースを操作できるようにする
cre_data_1.to_sql("a_time", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
# -------------実行ここまで
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる
# endregion

# region speed_generator_1:スピード指数を作成してDBに格納するスクリプト　Wall time: 1h 17min 3s OK
# ⓪データの前処理
# csv読み込み　データ準備
# 距離書いただけのやつ読み込み　競馬場にどんな距離あるか示したもの 2010-2020で開催された距離のみ記載
df_siba_1 = pd.read_csv('スピード指数 - 芝の距離書いただけのやつ.csv')
df_dirt_1 = pd.read_csv('スピード指数 - ダートの距離書いただけのやつ.csv')
# クラス指数　1勝クラス，2勝クラスとかで実力差を補正する指数
class_1 = pd.read_csv('スピード指数 - クラス指数 - 簡易.csv')  # TODO 改善 クラスの差があまりでなくなってしまっている
class3_1 = pd.read_csv('スピード指数 - クラス指数3歳 - 簡易.csv')  # TODO 改善
# 距離指数　距離ごとに補正する指数　これは使っておらず自前で算出している
# kyori_1=pd.read_csv('スピード指数 - 距離指数.csv')#https://team-d.club/about-speed-index/ このブログの距離指数を拝借したが使っていない。自分で算出したの使ってるがよいか再確認。

# データの前処理　スピード指数の元となるtableを前処理
speed_data = a_time.copy()  # defaultはtrue copyにしないと参照渡しになって元データから変更になってしまう
speed_data = speed_data.replace('', np.nan)  # 空をnanに置き換え
speed_data['hiniti'] = speed_data['year'] + speed_data['monthday']  # 日にちデータの追加

# 斤量を585⇒58.5みたいに直す
def futan_henkan(x):
    return float(x[0:2] + '.' + x[2])

# 走破時計を4桁の数字⇒秒になおす
def henkan(x):
    if x[0] == '0':
        return float(x[1:3] + '.' + x[3])
    else:
        return 60 * int(x[0]) + float(x[1:3] + '.' + x[3])

speed_data['futan_siyou'] = speed_data['futan'].apply(futan_henkan)
speed_data['sectime'] = speed_data['time'].apply(henkan)
speed_data['sectime'] = speed_data['sectime'].replace(0, np.nan)  # 走破時計0をNaNに置き換え
speed_data['year'] = pd.to_numeric(speed_data["year"], errors='coerce')  # numericに型変換しつつ欠測があったらnanで埋める
speed_data['kyori'] = pd.to_numeric(speed_data["kyori"], errors='coerce')  # numericに型変換しつつ欠測があったらnanで埋める
speed_data['jyocd'] = pd.to_numeric(speed_data["jyocd"], errors='coerce')  # numericに型変換しつつ欠測があったらnanで埋める
speed_data = speed_data[speed_data['year'] >= 2010]  # 2010年～のデータを抽出、バグデータの取り除き　892060 ⇒825827

# ①基準タイムと距離指数の算出
# 上記を算出するために天気：晴/曇り，馬場：良/稍，着順1～3着，条件：1～3勝クラス天気晴れのみのデータを抽出　825827⇒43429（36426 良だけだと）
speed_data_hare = speed_data[((speed_data['tenkocd'] == '1') | (speed_data['tenkocd'] == '2'))& ((speed_data['sibababacd'] == '1') | (speed_data['dirtbabacd'] == '1') | (
speed_data['sibababacd'] == '2') | (speed_data['dirtbabacd'] == '2'))& ((speed_data['kakuteijyuni'] == '01') | (speed_data['kakuteijyuni'] == '02') | (speed_data['kakuteijyuni'] == '03'))
& ((speed_data['jyokencd5'] == '005') | (speed_data['jyokencd5'] == '010') | (speed_data['jyokencd5'] == '016'))]
# 基準タイムと距離指数を格納する箱を作成　11年分を各年ごとに算出 芝72個、ダート56個
kijyun_siba = [[] for torima in range(11)]  # 基準タイム用　芝
kijyun_dirt = [[] for torima in range(11)]  # 基準タイム用　ダート
kyori_siba = [[] for torima in range(11)]  # 距離指数用　芝
kyori_dirt = [[] for torima in range(11)]  # 距離指数用　ダート
count = 0  # 年度をカウントする用
# for文で11年分の基準タイムと距離指数を作成していく　2010年分は作成できない，2011年～
for i in range(11):  # 2011-2021 11year　去年までの過去3年のデータを使用しデータを作成 元データは2010～2021の12年分
    year = 2011 + i  # i:0-10で2011～2021年の11年分
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
        for k in range(len(df_siba)):  # lenは行の大きさを取得　芝について基準タイムと距離指数を作成
            siba_kyori = df_siba.iloc[k, j - 1]  # 値を取得　対象のコースでの距離の値が格納される
            # 対象の距離，競馬場，集計年度の始まりの年，終わりの年より小さいデータを抽出2013なら2012
            syukei = speed_data_hare[(speed_data_hare['kyori'] == siba_kyori) & (speed_data_hare['jyocd'] == j) & (hajime <= speed_data_hare['year']) & (speed_data_hare['year'] < year)]
            df_siba.iloc[k, j - 1] = round(np.nanmean(syukei['sectime']), 1)  # 条件に一致した走破時計を平均して，df_sibaに格納する　基準タイムが求まった
            df_siba_kyori.iloc[k, j - 1] = round(1 / (10 * np.nanmean(syukei['sectime'])) * 1000,2)  # 距離指数を算出　×10することで妥当になる　距離指数＝1/基準タイム　ここ妥当かなぞ
        for k in range(len(df_dirt)):  # lenは行の大きさを取得　ダートについて基準タイムと距離指数を作成
            dirt_kyori = df_dirt.iloc[k, j - 1]  # 値を取得　対象のコースでの距離の値が格納される
            # 対象の距離，競馬場，集計年度の始まりの年，終わりの年より小さいデータを抽出2013なら2012
            syukei = speed_data_hare[(speed_data_hare['kyori'] == dirt_kyori) & (speed_data_hare['jyocd'] == j) & (hajime <= speed_data_hare['year']) & (speed_data_hare['year'] < year)]
            df_dirt.iloc[k, j - 1] = round(np.nanmean(syukei['sectime']), 1)  # 条件に一致した走破時計を平均して，df_sibaに格納する　基準タイムが求まった
            df_dirt_kyori.iloc[k, j - 1] = round(1 / (10 * np.nanmean(syukei['sectime'])) * 1000,2)  # 距離指数を算出　×10することで妥当になる　距離指数＝1/基準タイム　ここ妥当かなぞ
    # 年ごとに基準タイムを格納
    kijyun_siba[count] = df_siba  # 0に2011年のデータが入る（2010年のデータで作成したもの）。2011年のスピード指数算出したいときはこの基準タイムを使用する
    kijyun_dirt[count] = df_dirt  # 1に2012年のデータが入る（2010年～2011年のデータで作成したもの）
    # 年ごとに距離指数
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
                baba_index['jyokencd5'] == '999'))& ((baba_index['syubetu'] == '13') | (baba_index['syubetu'] == '14'))]  # 1～3着、未勝利～オープン、3・4歳上のレースを選択 3歳戦は削除
    # スピード指数用
    speed_index_moto = speed_index_moto[((speed_index_moto['syubetu'] == '11') | (speed_index_moto['syubetu'] == '12') | (speed_index_moto['syubetu'] == '13') |
                    (speed_index_moto['syubetu'] == '14'))& ((speed_index_moto['jyocd'] <= 10) & (speed_index_moto['jyocd'] > 0))]  # 中央の競馬で障害は除く
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
                index_d = df_siba_1.iloc[:, kaisai_d - 1] if sibadirt_d >= 1 else df_dirt_1.iloc[:,kaisai_d - 1]  # まずは一致する開催場所列を抽出
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
                    index_d = df_siba_1.iloc[:, kaisai_d - 1] if sibadirt_d >= 1 else df_dirt_1.iloc[:,kaisai_d - 1]  # まずは一致する開催場所列を抽出
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
                    spped_data_kakunou += [round(speed_index, 1)]  # indexを格納　あとでまとめて追加する
                    index_kakunou += [pd_index]  # スピード指数を格納　あとでまとめて追加する
            else:
                pass
                # ilocは列名の指定できないけど行番号の指定が取り出したものの何番目の行という考えかｔら。，locは指定できるけど行番号の指定がそいつがもともと持っている行番号になる。

# ③スピード指数格納　時間すごいかかる 1時間くらい
for i in range(len(spped_data_kakunou)):
    a_time.loc[index_kakunou[i], 'speed_idx'] = spped_data_kakunou[i]
    if i % 10000 == 0:
        print(i)
# ④DBへ出力
# データpostgreへ
conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
cursor = conn.cursor()  # データベースを操作できるようにする
a_time.to_sql("speed_index", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
# -------------実行ここまで
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる
# endregion

# region speed_index_output:対象日のレースの馬のスピード指数を出力するスクリプト OK
# speed_index_output:対象日のレースの馬のスピード指数を出力するスクリプト
import os  # フォルダ作成用

# データのindex整理
spped_from_db = spped_from_db.sort_values('index')  # indexがおかしいので，昇順で並べ替え
spped_from_db1 = spped_from_db.reset_index(drop=True)  # 一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
# レースIDと日にちを作成する
spped_from_db1['netID'] = spped_from_db1['year'] + spped_from_db1['jyocd'] + spped_from_db1['kaiji'] + spped_from_db1['nichiji'] + spped_from_db1['racenum']  # レースIDの作成
spped_from_db1['hiniti'] = spped_from_db1['year'] + spped_from_db1['monthday']  # 日にち検索用
# 対象日を選択する
raceDAY = spped_from_db1['hiniti'].unique()  # 当日開催されたレースを抽出
input_kensakuDAY = '20210111'  # 検索したい日にちを指定
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
    motopandas = motopandas.drop(
        ['year', 'monthday', 'index', 'kaiji', 'nichiji', 'ID', 'gradecd', 'syubetu', 'jyokencd1', 'jyokencd2',
         'jyokencd3',
         'jyokencd4', 'jyokencd5', 'trackcd', 'tenkocd', 'kigocd'], axis=1)  # いらん列削除
    motopandas = motopandas[motopandas['hiniti'] != input_kensakuDAY]  # 当日はデータないので削除
    kensakuID = ((umadata.tail(1)['year']).unique() + (umadata.tail(1)['monthday']).unique() + (
    umadata.tail(1)['jyocd']).unique() + (umadata.tail(1)['racenum']).unique())[0]
    # 日にちでフォルダ作成
    new_path = 'speed_hozon\{}'.format(input_kensakuDAY)
    if not os.path.exists(new_path):  # ディレクトリがなかったら
        os.mkdir(new_path)  # 作成したいフォルダ名を作成
    # csv出力
    hozonsaki = new_path + '\{}.csv'.format(kensakuID)
    motopandas.to_csv(hozonsaki, encoding='utf_8_sig', index=False)
# endregion

# region tokutyou_generator_moto_0:特徴量作成のために，払い戻しなども含めた元データを作成するスクリプトWall time: 3h 13min 38s
# tokutyou_generator_moto_0:特徴量作成のために，払い戻しなども含めた元データを作成するスクリプト
# ⓪騎手・調教師・血統・馬主・生産者ごとの勝率・複勝率・単勝回収率・回収率などの特徴量を作成
# まとめて
# uma_raceから必要な馬の情報の取り出す
matome_data = n_uma_race.loc[:,['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'umaban', 'bamei', 'chokyosiryakusyo','banusiname', 'kisyuryakusyo', 'kakuteijyuni', 'odds']]
matome_data['ID'] = n_uma_race['year'] + n_uma_race['monthday'] + n_uma_race['jyocd'] + n_uma_race['kaiji'] + n_uma_race['nichiji'] + n_uma_race['racenum']  # レースIDの作成
# raceから必要なレースの情報の取り出す
matomerare_race = n_race.loc[:,['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'kyori', 'trackcd', 'sibababacd','dirtbabacd']]
matomerare_race['ID'] = n_race['year'] + n_race['monthday'] + n_race['jyocd'] + n_race['kaiji'] + n_race['nichiji'] +n_race['racenum']  # レースIDの作成
# n_haraiから必要な馬の情報の取り出す
n_harai_matome = n_harai.loc[:,['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'paytansyoumaban1', 'paytansyopay1',
'paytansyoumaban2', 'paytansyopay2', 'paytansyoumaban3', 'paytansyopay3', 'payfukusyoumaban1','payfukusyopay1',
'payfukusyoumaban2', 'payfukusyopay2', 'payfukusyoumaban3', 'payfukusyopay3', 'payfukusyoumaban4','payfukusyopay4', 'payfukusyoumaban5', 'payfukusyopay5', ]]
n_harai_matome['ID'] = n_harai['year'] + n_harai['monthday'] + n_harai['jyocd'] + n_harai['kaiji'] + n_harai['nichiji'] + n_harai['racenum']  # レースIDの作成
# レースIDをlistにして検索しやすいようにする
matome_data_list = list(matome_data['ID'])  # レースIDをlistで取得
matomerare_race_list = list(matomerare_race['ID'])  # レースIDをlistで取得
n_harai_matome_idlist = list(n_harai_matome['ID'])  # レースIDをlistで取得
# 馬名をlistに
matome_bamei_list = list(matome_data['bamei'])  # レースIDをlistで取得
matomerare_bamei_list = list(n_uma_pro['bamei'])  # レースIDをlistで取得
# 準備 必要なものだけlist化
kyori_list = list(matomerare_race['kyori'])
trackcd_list = list(matomerare_race['trackcd'])
sibababacd_list = list(matomerare_race['sibababacd'])
dirtbabacd_list = list(matomerare_race['dirtbabacd'])
fathername_list = list(n_uma_pro['ketto3infobamei1'])
# 払い戻し，馬番をlistに
# 単勝
n_harai_matome_tanuma1 = list(n_harai_matome['paytansyoumaban1'])  # レースIDをlistで取得
n_harai_matome_tanpay1 = list(n_harai_matome['paytansyopay1'])  # レースIDをlistで取得
n_harai_matome_tanuma2 = list(n_harai_matome['paytansyoumaban2'])  # レースIDをlistで取得
n_harai_matome_tanpay2 = list(n_harai_matome['paytansyopay2'])  # レースIDをlistで取得
n_harai_matome_tanuma3 = list(n_harai_matome['paytansyoumaban3'])  # レースIDをlistで取得
n_harai_matome_tanpay3 = list(n_harai_matome['paytansyopay3'])  # レースIDをlistで取得
# 複勝
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

# 行番号を探す関数
def my_index(l, x, default=np.nan):
    if x in l:
        return l.index(x)  # 一致するデータがあるときはindexを返す
    else:
        return default  # ないときはNaNを返す

# データはlistに入れて高速化
a_kyori = []
a_trackcd = []
a_sibababacd = []
a_dirtbabacd = []
a_father = []
# データはlistに入れて高速化
a_tanuma1 = []
a_tanpay1 = []
a_tanuma2 = []
a_tanpay2 = []
a_tanuma3 = []
a_tanpay3 = []
a_uma1 = []
a_pay1 = []
a_uma2 = []
a_pay2 = []
a_uma3 = []
a_pay3 = []
a_uma4 = []
a_pay4 = []
a_uma5 = []
a_pay5 = []
# for文でデータを抽出
for i in range(len(matome_data)):
    if i % 100000 == 0:
        print(i)
    idx = my_index(matomerare_race_list, matome_data_list[i])  # 行番号を取得
    idx_father = my_index(matomerare_bamei_list, matome_bamei_list[i])  # 行番号を取得
    idx1 = my_index(n_harai_matome_idlist, matome_data_list[i])  # 行番号を取得
    # レースID
    if np.isnan(idx):  # NaNならTrue
        moji_str1a = np.nan
        moji_str1b = np.nan
        moji_str1c = np.nan
        moji_str1d = np.nan
    else:
        moji_str1a = kyori_list[idx]
        moji_str1b = trackcd_list[idx]
        moji_str1c = sibababacd_list[idx]
        moji_str1d = dirtbabacd_list[idx]
    # 父親の馬名
    if np.isnan(idx_father):  # NaNならTrue
        moji_str1e = np.nan
    else:
        moji_str1e = fathername_list[idx_father]
    # 払い戻し
    if np.isnan(idx1):  # NaNならTrue
        moji_str0a = np.nan
        moji_str0b = np.nan
        moji_str0c = np.nan
        moji_str0d = np.nan
        moji_str0e = np.nan
        moji_str0f = np.nan
        moji_stra = np.nan
        moji_strb = np.nan
        moji_strc = np.nan
        moji_strd = np.nan
        moji_stre = np.nan
        moji_strf = np.nan
        moji_strg = np.nan
        moji_strh = np.nan
        moji_stri = np.nan
        moji_strj = np.nan
    else:
        moji_str0a = n_harai_matome_tanuma1[idx1]
        moji_str0b = n_harai_matome_tanpay1[idx1]
        moji_str0c = n_harai_matome_tanuma2[idx1]
        moji_str0d = n_harai_matome_tanpay2[idx1]
        moji_str0e = n_harai_matome_tanuma3[idx1]
        moji_str0f = n_harai_matome_tanpay3[idx1]
        moji_stra = n_harai_matome_uma1[idx1]
        moji_strb = n_harai_matome_pay1[idx1]
        moji_strc = n_harai_matome_uma2[idx1]
        moji_strd = n_harai_matome_pay2[idx1]
        moji_stre = n_harai_matome_uma3[idx1]
        moji_strf = n_harai_matome_pay3[idx1]
        moji_strg = n_harai_matome_uma4[idx1]
        moji_strh = n_harai_matome_pay4[idx1]
        moji_stri = n_harai_matome_uma5[idx1]
        moji_strj = n_harai_matome_pay5[idx1]

    # データをどういれるか
    a_kyori += [moji_str1a]
    a_trackcd += [moji_str1b]
    a_sibababacd += [moji_str1c]
    a_dirtbabacd += [moji_str1d]
    a_father += [moji_str1e]
    a_tanuma1 += [moji_str0a]
    a_tanpay1 += [moji_str0b]
    a_tanuma2 += [moji_str0c]
    a_tanpay2 += [moji_str0d]
    a_tanuma3 += [moji_str0e]
    a_tanpay3 += [moji_str0f]
    a_uma1 += [moji_stra]
    a_pay1 += [moji_strb]
    a_uma2 += [moji_strc]
    a_pay2 += [moji_strd]
    a_uma3 += [moji_stre]
    a_pay3 += [moji_strf]
    a_uma4 += [moji_strg]
    a_pay4 += [moji_strh]
    a_uma5 += [moji_stri]
    a_pay5 += [moji_strj]

# データの結合
merge = pd.DataFrame(
    data={'kyori': a_kyori, 'trackcd': a_trackcd, 'sibababacd': a_sibababacd, 'dirtbabacd': a_dirtbabacd,
          'father': a_father, 'tanuma1': a_tanuma1, \
          'tanpay1': a_tanpay1, 'tanuma2': a_tanuma2, 'tanpay2': a_tanpay2, 'tanuma3': a_tanuma3, 'tanpay3': a_tanpay3,
          'fukuuma1': a_uma1, 'fukupay1': a_pay1, 'fukuuma2': a_uma2,
          'fukupay2': a_pay2, 'fukuuma3': a_uma3, 'fukupay3': a_pay3, 'fukuuma4': a_uma4, 'fukupay4': a_pay4,
          'fukuuma5': a_uma5, 'fukupay5': a_pay5}, \
    columns=['kyori', 'trackcd', 'sibababacd', 'dirtbabacd', 'father', 'tanuma1', 'tanpay1', 'tanuma2', 'tanpay2',
             'tanuma3', 'tanpay3', 'fukuuma1', 'fukupay1', 'fukuuma2', \
             'fukupay2', 'fukuuma3', 'fukupay3', 'fukuuma4', 'fukupay4', 'fukuuma5', 'fukupay5'])
saigo = pd.concat([matome_data, merge], axis=1)
# データpostgreへ
cre_data_1 = saigo.reset_index()  # indexを与える
conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
cursor = conn.cursor()  # データベースを操作できるようにする
cre_data_1.to_sql("tokutyo_moto", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
# -------------実行ここまで
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる
# endregion

# region tokutyou_generator_moto_1:特徴量元データに単勝払い戻しと複勝払い戻しを列に追加するスクリプトWall time: 1min 28s
# tokutyou_generator_moto_1:特徴量元データに単勝払い戻しと複勝払い戻しを列に追加するスクリプト
# 統計データを作成する
tmp_1 = tokutyo_moto.sort_values('index')  # indexがおかしいので，昇順で並べ替え
tmp_2 = tmp_1.reset_index(drop=True)  # 一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
moto_data = tmp_2.copy()  # defaultはtrue copyにしないと参照渡しになって元データから変更になってしまう
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
    ['odds', 'fukuuma1', 'fukupay1', 'fukuuma2', 'fukupay2', 'fukuuma3', 'fukupay3', 'fukuuma4', 'fukupay4', 'fukuuma5', \
     'fukupay5', 'tanuma1', 'tanpay1', 'tanuma2', 'tanpay2', 'tanuma3', 'tanpay3'], axis=1)
# 確定順位列を右端に移動させる
col = moto_data.columns.tolist()  # 列名のリスト
col.remove('kakuteijyuni')  # 't'を削除 ※列名は重複していないものとする
col.append('kakuteijyuni')  # 末尾に`t`を追加
moto_data = moto_data[col]

# 時系列で並べ替え
moto_data['nara'] = moto_data['ID'] + moto_data['umaban']  # 並べ替え用
moto_data_1 = moto_data.sort_values('nara')  # indexがおかしいので，昇順で並べ替え
# index振りなおし
moto_data_1 = moto_data_1.drop('index', axis=1)
moto_data_2 = moto_data_1.reset_index(drop=True)  # 一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
moto_data_2 = moto_data_2.reset_index(drop=False)  # 一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
# 表示
moto_data_2['year'] = moto_data_2['year'].astype(int)  # 確定順位をobjectからintに変換
# endregion

# region tokutyou_generator_2:10000個くらいの特徴量をtarget-encodingで作成するスクリプト Wall time: 4h 58min 30s
# tokutyou_generator_2:10000個くらいの特徴量をtarget-encodingで作成するスクリプト Wall time: 4h 58min 30s
# pandasのデータをfloat型にする　NaNもあるし，float型
# 競走中止とかは将来的に
# サンプル数は確認して、あまりにも少ないときは平均値などで置き換えを検討すべきかも
# 型変換と欠測処理　object⇒numericにして欠測はnanで埋める
moto_data_2['year'] = pd.to_numeric(moto_data_2["year"], errors='coerce')
moto_data_2["jyocd"] = pd.to_numeric(moto_data_2["jyocd"], errors='coerce')
moto_data_2['umaban'] = pd.to_numeric(moto_data_2["umaban"], errors='coerce')
moto_data_2['kyori'] = pd.to_numeric(moto_data_2["kyori"], errors='coerce')
moto_data_2['trackcd'] = pd.to_numeric(moto_data_2["trackcd"], errors='coerce')
moto_data_2['sibababacd'] = pd.to_numeric(moto_data_2["sibababacd"], errors='coerce')
moto_data_2['dirtbabacd'] = pd.to_numeric(moto_data_2["dirtbabacd"], errors='coerce')
moto_2010 = moto_data_2[moto_data_2['year'] >= 2010]  # 2010年以降のデータだけにする。moto_data_2⇒moto_2010
# umadataの抽出，2000年以降に産まれた馬だけを選択
n_uma_pro['birthdate'] = pd.to_numeric(n_uma_pro["birthdate"], errors='coerce')
n_uma_pro = n_uma_pro[n_uma_pro['birthdate'] >= 20000001]  # 2000年からの馬を集計　10万頭くらい
# 様々な条件でのindexを取得⇒ここは一つの条件でindex様々に取得して，その様々なindexのかつをしたほうがおしゃれかも
# region various condition
t1 = list(moto_2010[((moto_2010['umaban'] < 9))].index)  # 馬番9より小さい　OK
t2 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400))].index)  # 馬番9より小さいかつ距離1400以下　OK
t3 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200))].index)  # 馬番9より小さいかつ距離1400~2200　OK
t4 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600))].index)  # 馬番9より小さいかつ距離2200~3600　OK
t5 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 馬番9より小さいかつ良馬場　OK
t6 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 馬番9より小さいかつ重馬場　OK
t7 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ芝　OK
t8 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつダート　OK
t9 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 馬番9より小さいかつ1400以下かつ良馬場　OK
t10 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 馬番9より小さいかつ1400~2200かつ良馬場　OK？
t11 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 馬番9より小さいかつ2200~3600かつ良馬場　OK？
t12 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 馬番9より小さいかつ1400以下かつ重馬場　OK？
t13 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 馬番9より小さいかつ1400~2200かつ重馬場　OK？
t14 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 馬番9より小さいかつ2200~3600かつ重馬場　OK？
t15 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ1400以下かつ芝　OK？
t16 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ1400～2200かつ芝　OK？
t17 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ2200～3600かつ芝　OK？
t18 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつ1400以下かつダート　OK？
t19 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつ1400～2200かつダート　OK？
t20 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつ2200～3600かつダート　OK？
t21 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['sibababacd'] > 0) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 馬番9より小さいかつ芝でコースが11か17(内回り　OK？
t22 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['sibababacd'] > 0) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 馬番9より小さいかつ芝でコースが12か18(外回り　OK？
t23 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ良馬場かつ芝　OK？
t24 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ重馬場かつ芝　OK？
t25 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつ良馬場かつダート　OK？
t26 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつ重馬場かつダート　OK？
t27 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下かつ1400以下良かつ芝　OK？
t28 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下14-22かつ良かつ芝？
t29 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下22-36かつ良かつ芝？
t30 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下かつ1400以下重かつ芝　OK？
t31 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下14-22かつ重かつ芝？
t32 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下22-36かつ重かつ芝？
t33 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下かつ1400以下良かつダ　OK？
t34 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下14-22かつ良かつダ？
t35 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下22-36かつ良かつダ？
t36 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下かつ1400以下重かつダ　OK？
t37 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下14-22かつ重かつダ？
t38 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下24-36かつ重かつダ？
t39 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下1400以下　芝　内回り？
t40 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下14-22　芝　内回り？
t41 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下24-36　芝　内回り?
t42 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下1400以下　芝　外回り？
t43 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下14-22　芝　外回り？
t44 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下22-36　芝　外回り？
t45 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下　良　芝　内回り？
t46 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下　重　芝　外回り？
t47 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下　重　芝　外回り？
t48 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下　重　芝　内回り？
t49 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下14良芝内
t50 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下1422良芝内)
t51 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下2232良芝内)
t52 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下1422良芝外
t53 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下1422良芝外
t54 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下2232良芝外
t55 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下14重芝内
t56 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下1422重芝内
t57 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下32重芝内
t58 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下14重芝外
t59 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下1422重芝外
t60 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下36重芝外
# 馬番関係
t61 = list(moto_2010[((moto_2010['umaban'] >= 9))].index)
t62 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400))].index)
t63 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200))].index)
t64 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600))].index)
t65 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)
t66 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)
t67 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] > 0)))].index)
t68 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] == 0)))].index)
t69 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)
t70 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)
t71 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)
t72 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)
t73 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)
t74 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)
t75 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)))].index)
t76 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)))].index)
t77 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)))].index)
t78 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] == 0)))].index)
t79 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] == 0)))].index)
t80 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] == 0)))].index)
t81 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)) & ((moto_2010['sibababacd'] > 0)))].index)
t82 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)) & ((moto_2010['sibababacd'] > 0)))].index)
t83 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t84 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t85 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t86 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t87 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t88 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t89 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t90 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t91 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t92 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t93 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t94 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t95 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t96 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t97 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t98 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t99 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t100 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t101 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t102 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t103 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t104 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t105 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t106 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t107 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t108 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t109 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t110 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t111 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t112 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t113 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t114 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t115 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t116 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t117 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t118 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t119 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t120 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
# 馬番関係
t121 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1000) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t122 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1150) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t123 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t124 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1300) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t125 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t126 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1500) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t127 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t128 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1700) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t129 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1800) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t130 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1900) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t131 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2000) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t132 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2100) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t133 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t134 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2300) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t135 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t136 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2500) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t137 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t138 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2800) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t139 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3000) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t140 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t141 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t142 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t143 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1000) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t144 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1150) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t145 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1200) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t146 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1300) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t147 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1400) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t148 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1500) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t149 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1600) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t150 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1700) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t151 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1800) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t152 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1900) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t153 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2000) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t154 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2100) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t155 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2200) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t156 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2300) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t157 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2400) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t158 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2500) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t159 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2600) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t160 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2800) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t161 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3000) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t162 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3200) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t163 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3400) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t164 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3600) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t165 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1000) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t166 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1150) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t167 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t168 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1300) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t169 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t170 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1500) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t171 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t172 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1700) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t173 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1800) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t174 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1900) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t175 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2000) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t176 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2100) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t177 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t178 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2300) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t179 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t180 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2500) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t181 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t182 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2800) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t183 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3000) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t184 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t185 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t186 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t187 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1000) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t188 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1150) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t189 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1200) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t190 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1300) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t191 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1400) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t192 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1500) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t193 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1600) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t194 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1700) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t195 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1800) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t196 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1900) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t197 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2000) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t198 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2100) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t199 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2200) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t200 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2300) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t201 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2400) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t202 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2500) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t203 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2600) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t204 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2800) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t205 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3000) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t206 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3200) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t207 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3400) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t208 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3600) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
# 距離関係
t209 = list(moto_2010[((moto_2010['kyori'] <= 1400))].index)  # 1400以下
t210 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200))].index)  # 1422
t211 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600))].index)  # 2236
t212 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 14良
t213 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 1422良
t214 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 2236良
t215 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 14重
t216 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 1422重
t217 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 2236重
t218 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)))].index)  # 14芝
t219 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)))].index)  # 1422芝
t220 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)))].index)  # 2236芝
t221 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] == 0)))].index)  # 14ダ
t222 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] == 0)))].index)  # 1422ダ
t223 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] == 0)))].index)  # 2236ダ
t224 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 14良芝
t225 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 1422良芝
t226 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 2236良芝
t227 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 14重芝
t228 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 1422重芝
t229 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 2236重芝
t230 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 14良ダ
t231 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 1422良ダ
t232 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 2236良ダ
t233 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 14重ダ
t234 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 1422重ダ
t235 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 2236重ダ
t236 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 14芝内
t237 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 1422芝内
t238 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 2236芝内
t239 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 14芝外
t240 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 1422芝外
t241 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 2236芝外
t242 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 14良芝内
t243 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 1422良芝内
t244 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 2236良芝内
t245 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 14良芝外
t246 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 1422良芝外
t247 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 2236良芝外
t248 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 14重芝内
t249 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 1422重芝内
t250 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 2236重芝内
t251 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 14重芝外
t252 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 1422重芝内
t253 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 2236重芝内
# 馬場状態良・重関係
t254 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 良
t255 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 重
t256 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 良芝
t257 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 重芝
t258 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 良ダ
t259 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 重ダ
t260 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 良芝内
t261 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 重芝外
t262 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 良芝外
t263 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 重芝内
# 芝/ダ関係
t264 = list(moto_2010[(((moto_2010['sibababacd'] > 0)))].index)  # 芝
t265 = list(moto_2010[(((moto_2010['sibababacd'] == 0)))].index)  # ダ
t266 = list(moto_2010[(((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 内芝
t267 = list(moto_2010[(((moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 外芝
# endregion
# 条件のindexをlistに格納
jyo_list = []
jyo_list.extend(
    [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25,t26,
     t27, t28, t29, t30, t31, t32, t33, t34, t35, t36, t37, t38, t39, t40, t41, t42, t43, t44, t45, t46, t47, t48, t49,t50, t51, t52, t53, t54,
     t55, t56, t57, t58, t59, t60, t61, t62, t63, t64, t65, t66, t67, t68, t69, t70, t71, t72, t73, t74, t75, t76, t77,t78, t79, t80, t81, t82,
     t83, t84, t85, t86, t87, t88, t89, t90, t91, t92, t93, t94, t95, t96, t97, t98, t99, t100, t101, t102, t103, t104,t105, t106, t107, t108,
     t109, t110, t111, t112, t113, t114, t115, t116, t117, t118, t119, t120, t121, t122, t123, t124, t125, t126, t127,t128, t129, t130, t131,
     t132, t133, t134, t135, t136, t137, t138, t139, t140, t141, t142, t143, t144, t145, t146, t147, t148, t149, t150,t151, t152, t153, t154,
     t155, t156, t157, t158, t159, t160, t161, t162, t163, t164, t165, t166, t167, t168, t169, t170, t171, t172, t173,t174, t175, t176, t177,
     t178, t179, t180, t181, t182, t183, t184, t185, t186, t187, t188, t189, t190, t191, t192, t193, t194, t195, t196,t197, t198, t199, t200,
     t201, t202, t203, t204, t205, t206, t207, t208, t209, t210, t211, t212, t213, t214, t215, t216, t217, t218, t219,t220, t221, t222, t223,
     t224, t225, t226, t227, t228, t229, t230, t231, t232, t233, t234, t235, t236, t237, t238, t239, t240, t241, t242,t243, t244, t245, t246,
     t247, t248, t249, t250, t251, t252, t253, t254, t255, t256, t257, t258, t259, t260, t261, t262, t263, t264, t265,t266, t267])  # 全267条件
# 払い戻しなどの集計用に必要な列（単勝/複勝払い戻し，確定順位）だけ抽出
np_moto_2010 = np.array(moto_data_2.loc[:, ['tan_harai', 'fuku_harai', 'kakuteijyuni']])  # Wall time: 46.3 ms to numpy
# 集計データを格納する用のlistを作成　二次元配列（リストのリスト）11年×10場×50メイン
kisyu_box_tanharai = [[] for torima in range(5500)]  # n_uma_race用
kisyu_box_fukuharai = [[] for torima in range(5500)]  # n_uma_race用
kisyu_box_syouritu = [[] for torima in range(5500)]  # n_uma_race用
kisyu_box_fukuritu = [[] for torima in range(5500)]  # n_uma_race用
chokyo_box_tanharai = [[] for torima in range(5500)]  # n_uma_race用
chokyo_box_fukuharai = [[] for torima in range(5500)]  # n_uma_race用
chokyo_box_syouritu = [[] for torima in range(5500)]  # n_uma_race用
chokyo_box_fukuritu = [[] for torima in range(5500)]  # n_uma_race用
banu_box_tanharai = [[] for torima in range(5500)]  # n_uma_race用
banu_box_fukuharai = [[] for torima in range(5500)]  # n_uma_race用
banu_box_syouritu = [[] for torima in range(5500)]  # n_uma_race用
banu_box_fukuritu = [[] for torima in range(5500)]  # n_uma_race用
syu_box_tanharai = [[] for torima in range(5500)]  # n_uma_race用
syu_box_fukuharai = [[] for torima in range(5500)]  # n_uma_race用
syu_box_syouritu = [[] for torima in range(5500)]  # n_uma_race用
syu_box_fukuritu = [[] for torima in range(5500)]  # n_uma_race用
# サンプル数確認用
kisyu_sample = [[] for torima in range(5500)]  # 騎手用　★
chokyo_sample = [[] for torima in range(5500)]  # 調教師用　★
banu_sample = [[] for torima in range(5500)]  # 馬主用　★
syu_sample = [[] for torima in range(5500)]  # 種牡馬用　★
# uma
# uma_box_tanharai=[[] for torima in range(100*len(uma_data))]#n_uma_race用 100000くらい
# uma_box_fukuharai=[[] for torima in range(100*len(uma_data))]#n_uma_race用
# uma_box_syouritu=[[] for torima in range(100*len(uma_data))]#n_uma_race用
# uma_box_fukuritu=[[] for torima in range(100*len(uma_data))]#n_uma_race用
# mainを追加するよう 11year
kisyu_main_11 = [[] for torima in range(11)]  # 騎手用　★
chokyo_main_11 = [[] for torima in range(11)]  # 調教師用　★
banu_main_11 = [[] for torima in range(11)]  # 馬主用　★
syu_main_11 = [[] for torima in range(11)]  # 種牡馬用　★
# count用
count = 0
count_uma = 0
count_main = 0
# nanのnp作成
mat = np.zeros([1, len(jyo_list)])
mat[:, :] = np.nan
# データ作成 11年×10場×50個（メイン）＝5500個
for i in range(11):  # 11年分
    year_hani = 2011 + i  # 2011~2021でデータを作る　2011年のデータは2012年に使う
    print(year_hani)
    # 対象年以下を指定
    year_list = list(moto_2010[(((moto_2010['year'] <= year_hani)))].index)
    # メイン取得用
    moto_main = moto_2010[moto_2010['year'] <= year_hani]
    # メインデータを抽出 data in last year
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
        basyo_list = list(moto_2010[(((moto_2010['jyocd'] == jyonum)))].index)
        yearbasyo_list = list(set(year_list) & set(basyo_list))  # 年と場所に関する条件
        # uma_data=list(moto_main['bamei'].value_counts().to_dict().keys())#bamei　辞書にしてキーをlistで取得
        for j in range(50):  # 4つのメインに対して50個分データを作成
            # メインを指定
            kisyu_list = list(moto_2010[(((moto_2010['kisyuryakusyo'] == kisyu_data[j])))].index)
            chokyo_list = list(moto_2010[(((moto_2010['chokyosiryakusyo'] == chokyo_data[j])))].index)
            banu_list = list(moto_2010[(((moto_2010['banusiname'] == banu_data[j])))].index)
            syu_list = list(moto_2010[(((moto_2010['father'] == syu_data[j])))].index)
            # 追加
            if jyonum == 1:  # １場だけ
                print('できてます')
                kisyu_main.append(kisyu_data[j])
                chokyo_main.append(chokyo_data[j])
                banu_main.append(banu_data[j])
                syu_main.append(syu_data[j])
            # 条件を指定
            kisyu_index1 = list(set(kisyu_list) & set(yearbasyo_list))
            chokyo_index1 = list(set(chokyo_list) & set(yearbasyo_list))
            banu_list_index1 = list(set(banu_list) & set(yearbasyo_list))
            syu_index1 = list(set(syu_list) & set(yearbasyo_list))
            # list内包表記 mapの代わりになる　https://qiita.com/KTakahiro1729/items/c9cb757473de50652374
            syukei_kisyu = [set(kisyu_index1) & set(i_nakami) for i_nakami in
                            jyo_list]  # 大list=list×267，それぞれのlistの中にindexが格納されている
            syukei_chokyo = [set(chokyo_index1) & set(i_nakami) for i_nakami in jyo_list]
            syukei_banu = [set(banu_list_index1) & set(i_nakami) for i_nakami in jyo_list]
            syukei_syu = [set(syu_index1) & set(i_nakami) for i_nakami in jyo_list]
            # サンプル少ないデータを平均値などで置き換えるかどうか
            # 格納
            # 騎手
            kisyu_box_tanharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 0]) for i_nakami in syukei_kisyu]
            kisyu_box_fukuharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 1]) for i_nakami in syukei_kisyu]
            kisyu_box_syouritu[count] = [np.nanmean(np_moto_2010[list(i_nakami), 2] == 1.0) * 100 for i_nakami in
                                         syukei_kisyu]
            kisyu_box_fukuritu[count] = [
                np.nanmean((np_moto_2010[list(i_nakami), 2] >= 1) & (np_moto_2010[list(i_nakami), 2] <= 3)) * 100 for
                i_nakami in syukei_kisyu]
            # 調教
            chokyo_box_tanharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 0]) for i_nakami in syukei_chokyo]
            chokyo_box_fukuharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 1]) for i_nakami in syukei_chokyo]
            chokyo_box_syouritu[count] = [np.nanmean(np_moto_2010[list(i_nakami), 2] == 1.0) * 100 for i_nakami in
                                          syukei_chokyo]
            chokyo_box_fukuritu[count] = [
                np.nanmean((np_moto_2010[list(i_nakami), 2] >= 1) & (np_moto_2010[list(i_nakami), 2] <= 3)) * 100 for
                i_nakami in syukei_chokyo]
            # 馬主
            banu_box_tanharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 0]) for i_nakami in syukei_banu]
            banu_box_fukuharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 1]) for i_nakami in syukei_banu]
            banu_box_syouritu[count] = [np.nanmean(np_moto_2010[list(i_nakami), 2] == 1.0) * 100 for i_nakami in
                                        syukei_banu]
            banu_box_fukuritu[count] = [
                np.nanmean((np_moto_2010[list(i_nakami), 2] >= 1) & (np_moto_2010[list(i_nakami), 2] <= 3)) * 100 for
                i_nakami in syukei_banu]
            # 種牡馬
            syu_box_tanharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 0]) for i_nakami in syukei_syu]
            syu_box_fukuharai[count] = [np.nanmean(np_moto_2010[list(i_nakami), 1]) for i_nakami in syukei_syu]
            syu_box_syouritu[count] = [np.nanmean(np_moto_2010[list(i_nakami), 2] == 1.0) * 100 for i_nakami in
                                       syukei_syu]
            syu_box_fukuritu[count] = [
                np.nanmean((np_moto_2010[list(i_nakami), 2] >= 1) & (np_moto_2010[list(i_nakami), 2] <= 3)) * 100 for
                i_nakami in syukei_syu]
            # データないものは成績悪めのデータで置き換え？
            # サンプル数確認用　★
            kisyu_sample[count] = [len(v) for v in syukei_kisyu]  # サンプル数を格納
            chokyo_sample[count] = [len(v) for v in syukei_chokyo]  # サンプル数を格納
            banu_sample[count] = [len(v) for v in syukei_banu]  # サンプル数を格納
            syu_sample[count] = [len(v) for v in syukei_syu]  # サンプル数を格納
            #
            count += 1  # 5000まで行く

        '''
        for j in range(len(uma_data)):#馬ごとの特徴量を作成する。しかし全馬に対してデータを作成すると時間がかかりすぎるので，コメントアウト
            #メインを指定
            uma_list=list(moto_2010[(((moto_2010['bamei']==uma_data[j])))].index)
            #条件を指定
            uma_index1=list(set(uma_list)&set(yearbasyo_list))
            if len(uma_index1)==0:#馬いないとき
                uma_box_tanharai[count_uma]=mat
                uma_box_fukuharai[count_uma]=mat
                uma_box_syouritu[count_uma]=mat
                uma_box_fukuritu[count_uma]=mat
            else:
            #list内包表記 mapの代わりになる　https://qiita.com/KTakahiro1729/items/c9cb757473de50652374
                syukei_uma=[set(uma_index1)&set(i_nakami) for i_nakami in jyo_list]
                #サンプル少ないデータを平均値などで置き換えるかどうか
                #格納
                #騎手
                uma_box_tanharai[count_uma]=[np.nanmean(np_moto_2010[list(i_nakami),0]) for i_nakami in syukei_uma]
                uma_box_fukuharai[count_uma]=[np.nanmean(np_moto_2010[list(i_nakami),1]) for i_nakami in syukei_uma]
                uma_box_syouritu[count_uma]=[np.nanmean(np_moto_2010[list(i_nakami),2]==1.0)*100 for i_nakami in syukei_uma]
                uma_box_fukuritu[count_uma]=[np.nanmean((np_moto_2010[list(i_nakami),2]>=1)&(np_moto_2010[list(i_nakami),2]<=3))*100 for i_nakami in syukei_uma]
            #データないものは成績悪めのデータで置き換え？
            count_uma+=1
        '''
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
# データpostgreへ
conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
cursor = conn.cursor()  # データベースを操作できるようにする
# ↓はDBに出力済み
pdk10.to_sql("t_kisyu_box_tanharai", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdk20.to_sql("t_kisyu_box_fukuharai", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdk30.to_sql("t_kisyu_box_syouritu", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdk40.to_sql("t_kisyu_box_fukuritu", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdc10.to_sql("t_chokyo_box_tanharai", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdc20.to_sql("t_chokyo_box_fukuharai", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdc30.to_sql("t_chokyo_box_syouritu", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdc40.to_sql("t_chokyo_box_fukuritu", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdb10.to_sql("t_banu_box_tanharai", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdb20.to_sql("t_banu_box_fukuharai", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdb30.to_sql("t_banu_box_syouritu", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pdb40.to_sql("t_banu_box_fukuritu", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pds10.to_sql("t_syu_box_tanharai", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pds20.to_sql("t_syu_box_fukuharai", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pds30.to_sql("t_syu_box_syouritu", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
pds40.to_sql("t_syu_box_fukuritu", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
sample10.to_sql("t_kisyu_sample", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
sample20.to_sql("t_chokyo_sample", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
sample30.to_sql("t_banu_sample", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
sample40.to_sql("t_syu_sample", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
main10.to_sql("t_kisyu_main", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
main20.to_sql("t_chokyo_main", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
main30.to_sql("t_banu_main", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
main40.to_sql("t_syu_main", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
# -------------実行ここまで
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる
# endregion

# region targetencodingのデータを欠測処理して，使いやすい形にする 5s たぶんこれはいらなくなった
#targetencodingのデータを欠測処理して，使いやすい形にする
#index直し
import time
start = time.time()

akisyu_box_tanharai = akisyu_box_tanharai.sort_values('index')#indexがおかしいので，昇順で並べ替え
akisyu_box_tanharai1 = akisyu_box_tanharai.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
akisyu_box_tanharai1 = akisyu_box_tanharai1.drop(['index'], axis=1)#index列削除
akisyu_box_fukuharai = akisyu_box_fukuharai.sort_values('index')#indexがおかしいので，昇順で並べ替え
akisyu_box_fukuharai1 = akisyu_box_fukuharai.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
akisyu_box_fukuharai1 = akisyu_box_fukuharai1.drop(['index'], axis=1)#index列削除
akisyu_box_syouritu = akisyu_box_syouritu.sort_values('index')#indexがおかしいので，昇順で並べ替え
akisyu_box_syouritu1 = akisyu_box_syouritu.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
akisyu_box_syouritu1 = akisyu_box_syouritu1.drop(['index'], axis=1)#index列削除
akisyu_box_fukuritu = akisyu_box_fukuritu.sort_values('index')#indexがおかしいので，昇順で並べ替え
akisyu_box_fukuritu1 = akisyu_box_fukuritu.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
akisyu_box_fukuritu1 = akisyu_box_fukuritu1.drop(['index'], axis=1)#index列削除
achokyo_box_tanharai = achokyo_box_tanharai.sort_values('index')#indexがおかしいので，昇順で並べ替え
achokyo_box_tanharai1 = achokyo_box_tanharai.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
achokyo_box_tanharai1 = achokyo_box_tanharai1.drop(['index'], axis=1)#index列削除
achokyo_box_fukuharai = achokyo_box_fukuharai.sort_values('index')#indexがおかしいので，昇順で並べ替え
achokyo_box_fukuharai1 = achokyo_box_fukuharai.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
achokyo_box_fukuharai1 = achokyo_box_fukuharai1.drop(['index'], axis=1)#index列削除
achokyo_box_syouritu = achokyo_box_syouritu.sort_values('index')#indexがおかしいので，昇順で並べ替え
achokyo_box_syouritu1 = achokyo_box_syouritu.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
achokyo_box_syouritu1 = achokyo_box_syouritu1.drop(['index'], axis=1)#index列削除
achokyo_box_fukuritu = achokyo_box_fukuritu.sort_values('index')#indexがおかしいので，昇順で並べ替え
achokyo_box_fukuritu1 = achokyo_box_fukuritu.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
achokyo_box_fukuritu1 = achokyo_box_fukuritu1.drop(['index'], axis=1)#index列削除
abanu_box_tanharai = abanu_box_tanharai.sort_values('index')#indexがおかしいので，昇順で並べ替え
abanu_box_tanharai1 = abanu_box_tanharai.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
abanu_box_tanharai1 = abanu_box_tanharai1.drop(['index'], axis=1)#index列削除
abanu_box_fukuharai = abanu_box_fukuharai.sort_values('index')#indexがおかしいので，昇順で並べ替え
abanu_box_fukuharai1 = abanu_box_fukuharai.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
abanu_box_fukuharai1 = abanu_box_fukuharai1.drop(['index'], axis=1)#index列削除
abanu_box_syouritu = abanu_box_syouritu.sort_values('index')#indexがおかしいので，昇順で並べ替え
abanu_box_syouritu1 = abanu_box_syouritu.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
abanu_box_syouritu1 = abanu_box_syouritu1.drop(['index'], axis=1)#index列削除
abanu_box_fukuritu = abanu_box_fukuritu.sort_values('index')#indexがおかしいので，昇順で並べ替え
abanu_box_fukuritu1 = abanu_box_fukuritu.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
abanu_box_fukuritu1 = abanu_box_fukuritu1.drop(['index'], axis=1)#index列削除
asyu_box_tanharai = asyu_box_tanharai.sort_values('index')#indexがおかしいので，昇順で並べ替え
asyu_box_tanharai1 = asyu_box_tanharai.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
asyu_box_tanharai1 = asyu_box_tanharai1.drop(['index'], axis=1)#index列削除
asyu_box_fukuharai = asyu_box_fukuharai.sort_values('index')#indexがおかしいので，昇順で並べ替え
asyu_box_fukuharai1 = asyu_box_fukuharai.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
asyu_box_fukuharai1 = asyu_box_fukuharai1.drop(['index'], axis=1)#index列削除
asyu_box_syouritu = asyu_box_syouritu.sort_values('index')#indexがおかしいので，昇順で並べ替え
asyu_box_syouritu1 = asyu_box_syouritu.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
asyu_box_syouritu1 = asyu_box_syouritu1.drop(['index'], axis=1)#index列削除
asyu_box_fukuritu = asyu_box_fukuritu.sort_values('index')#indexがおかしいので，昇順で並べ替え
asyu_box_fukuritu1 = asyu_box_fukuritu.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
asyu_box_fukuritu1 = asyu_box_fukuritu1.drop(['index'], axis=1)#index列削除
at_kisyu_sample = at_kisyu_sample.sort_values('index')#indexがおかしいので，昇順で並べ替え
at_kisyu_sample1 = at_kisyu_sample.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
at_kisyu_sample1 = at_kisyu_sample1.drop(['index'], axis=1)#index列削除
at_chokyo_sample = at_chokyo_sample.sort_values('index')#indexがおかしいので，昇順で並べ替え
at_chokyo_sample1 = at_chokyo_sample.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
at_chokyo_sample1 = at_chokyo_sample1.drop(['index'], axis=1)#index列削除
at_banu_sample = at_banu_sample.sort_values('index')#indexがおかしいので，昇順で並べ替え
at_banu_sample1 = at_banu_sample.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
at_banu_sample1 = at_banu_sample1.drop(['index'], axis=1)#index列削除
at_syu_sample = at_syu_sample.sort_values('index')#indexがおかしいので，昇順で並べ替え
at_syu_sample1 = at_syu_sample.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
at_syu_sample1 = at_syu_sample1.drop(['index'], axis=1)#index列削除
at_kisyu_main = at_kisyu_main.sort_values('index')#indexがおかしいので，昇順で並べ替え
at_kisyu_main1 = at_kisyu_main.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
at_kisyu_main1 = at_kisyu_main1.drop(['index'], axis=1)#index列削除
at_chokyo_main = at_chokyo_main.sort_values('index')#indexがおかしいので，昇順で並べ替え
at_chokyo_main1 = at_chokyo_main.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
at_chokyo_main1 = at_chokyo_main1.drop(['index'], axis=1)#index列削除
at_banu_main = at_banu_main.sort_values('index')#indexがおかしいので，昇順で並べ替え
at_banu_main1 = at_banu_main.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
at_banu_main1 = at_banu_main1.drop(['index'], axis=1)#index列削除
at_syu_main = at_syu_main.sort_values('index')#indexがおかしいので，昇順で並べ替え
at_syu_main1 = at_syu_main.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
at_syu_main1 = at_syu_main1.drop(['index'], axis=1)#index列削除
#サンプル数5以下をnanに変換
at_kisyu_sample2=at_kisyu_sample1.where(at_kisyu_sample1>5, np.nan)#5以下をnanにする
at_chokyo_sample2=at_chokyo_sample1.where(at_kisyu_sample1>5, np.nan)
at_banu_sample2=at_banu_sample1.where(at_kisyu_sample1>5, np.nan)
at_syu_sample2=at_syu_sample1.where(at_kisyu_sample1>5, np.nan)
#数値データを1にする
at_kisyu_sample3=at_kisyu_sample2.where(at_kisyu_sample1<5, 1)#5以上を1にする
at_chokyo_sample3=at_chokyo_sample2.where(at_kisyu_sample1<5, 1)
at_banu_sample3=at_banu_sample2.where(at_kisyu_sample1<5, 1)
at_syu_sample3=at_syu_sample2.where(at_kisyu_sample1<5, 1)
#df_bool=sum((at_kisyu_sample4==5.0).sum())#足し算
#特徴量データ×sampleデータして残すデータを決める
akisyu_box_tanharai2=akisyu_box_tanharai1*at_kisyu_sample3
akisyu_box_fukuharai2=akisyu_box_fukuharai1*at_kisyu_sample3
akisyu_box_syouritu2=akisyu_box_syouritu1*at_kisyu_sample3
akisyu_box_fukuritu2=akisyu_box_fukuritu1*at_kisyu_sample3
achokyo_box_tanharai2=achokyo_box_tanharai1*at_chokyo_sample3
achokyo_box_fukuharai2=achokyo_box_fukuharai1*at_chokyo_sample3
achokyo_box_syouritu2=achokyo_box_syouritu1*at_chokyo_sample3
achokyo_box_fukuritu2=achokyo_box_fukuritu1*at_chokyo_sample3
abanu_box_tanharai2=abanu_box_tanharai1*at_banu_sample3
abanu_box_fukuharai2=abanu_box_fukuharai1*at_banu_sample3
abanu_box_syouritu2=abanu_box_syouritu1*at_banu_sample3
abanu_box_fukuritu2=abanu_box_fukuritu1*at_banu_sample3
asyu_box_tanharai2=asyu_box_tanharai1*at_syu_sample3
asyu_box_fukuharai2=asyu_box_fukuharai1*at_syu_sample3
asyu_box_syouritu2=asyu_box_syouritu1*at_syu_sample3
asyu_box_fukuritu2=asyu_box_fukuritu1*at_syu_sample3
#それぞれの列においてNANを残ったデータの平均で置き換え
akisyu_box_tanharai3=akisyu_box_tanharai2.fillna(akisyu_box_tanharai2.mean())
akisyu_box_fukuharai3=akisyu_box_fukuharai2.fillna(akisyu_box_fukuharai2.mean())
akisyu_box_syouritu3=akisyu_box_syouritu2.fillna(akisyu_box_syouritu2.mean())
akisyu_box_fukuritu3=akisyu_box_fukuritu2.fillna(akisyu_box_fukuritu2.mean())
achokyo_box_tanharai3=achokyo_box_tanharai2.fillna(achokyo_box_tanharai2.mean())
achokyo_box_fukuharai3=achokyo_box_fukuharai2.fillna(achokyo_box_fukuharai2.mean())
achokyo_box_syouritu3=achokyo_box_syouritu2.fillna(achokyo_box_syouritu2.mean())
achokyo_box_fukuritu3=achokyo_box_fukuritu2.fillna(achokyo_box_fukuritu2.mean())
abanu_box_tanharai3=abanu_box_tanharai2.fillna(abanu_box_tanharai2.mean())
abanu_box_fukuharai3=abanu_box_fukuharai2.fillna(abanu_box_fukuharai2.mean())
abanu_box_syouritu3=abanu_box_syouritu2.fillna(abanu_box_syouritu2.mean())
abanu_box_fukuritu3=abanu_box_fukuritu2.fillna(abanu_box_fukuritu2.mean())
asyu_box_tanharai3=asyu_box_tanharai2.fillna(asyu_box_tanharai2.mean())
asyu_box_fukuharai3=asyu_box_fukuharai2.fillna(asyu_box_fukuharai2.mean())
asyu_box_syouritu3=asyu_box_syouritu2.fillna(asyu_box_syouritu2.mean())
asyu_box_fukuritu3=asyu_box_fukuritu2.fillna(asyu_box_fukuritu2.mean())
#メインを11年分並べる，縦に
#騎手メイン
kn_10_0=(pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[0,:]))]*10)).rename(columns={0: 'jockey'})
kn_10_1=pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[1,:]))]*10).rename(columns={1: 'jockey'})
kn_10_2=pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[2,:]))]*10).rename(columns={2: 'jockey'})
kn_10_3=pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[3,:]))]*10).rename(columns={3: 'jockey'})
kn_10_4=pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[4,:]))]*10).rename(columns={4: 'jockey'})
kn_10_5=pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[5,:]))]*10).rename(columns={5: 'jockey'})
kn_10_6=pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[6,:]))]*10).rename(columns={6: 'jockey'})
kn_10_7=pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[7,:]))]*10).rename(columns={7: 'jockey'})
kn_10_8=pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[8,:]))]*10).rename(columns={8: 'jockey'})
kn_10_9=pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[9,:]))]*10).rename(columns={9: 'jockey'})
kn_10_10=pd.concat([(pd.DataFrame(at_kisyu_main1.iloc[10,:]))]*10).rename(columns={10: 'jockey'})
kn_10_all=pd.concat([kn_10_0,kn_10_1,kn_10_2,kn_10_3,kn_10_4,kn_10_5,kn_10_6,kn_10_7,kn_10_8,kn_10_9,kn_10_10])#11年分複製
kn_10_all=kn_10_all.reset_index(drop=True)
#調教師メイン
cn_10_0=(pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[0,:]))]*10)).rename(columns={0: 'chokyo'})
cn_10_1=pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[1,:]))]*10).rename(columns={1: 'chokyo'})
cn_10_2=pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[2,:]))]*10).rename(columns={2: 'chokyo'})
cn_10_3=pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[3,:]))]*10).rename(columns={3: 'chokyo'})
cn_10_4=pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[4,:]))]*10).rename(columns={4: 'chokyo'})
cn_10_5=pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[5,:]))]*10).rename(columns={5: 'chokyo'})
cn_10_6=pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[6,:]))]*10).rename(columns={6: 'chokyo'})
cn_10_7=pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[7,:]))]*10).rename(columns={7: 'chokyo'})
cn_10_8=pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[8,:]))]*10).rename(columns={8: 'chokyo'})
cn_10_9=pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[9,:]))]*10).rename(columns={9: 'chokyo'})
cn_10_10=pd.concat([(pd.DataFrame(at_chokyo_main1.iloc[10,:]))]*10).rename(columns={10: 'chokyo'})
cn_10_all=pd.concat([cn_10_0,cn_10_1,cn_10_2,cn_10_3,cn_10_4,cn_10_5,cn_10_6,cn_10_7,cn_10_8,cn_10_9,cn_10_10])#11年分複製
cn_10_all=cn_10_all.reset_index(drop=True)
#馬主メイン
bn_10_0=(pd.concat([(pd.DataFrame(at_banu_main1.iloc[0,:]))]*10)).rename(columns={0: 'banushi'})
bn_10_1=pd.concat([(pd.DataFrame(at_banu_main1.iloc[1,:]))]*10).rename(columns={1: 'banushi'})
bn_10_2=pd.concat([(pd.DataFrame(at_banu_main1.iloc[2,:]))]*10).rename(columns={2: 'banushi'})
bn_10_3=pd.concat([(pd.DataFrame(at_banu_main1.iloc[3,:]))]*10).rename(columns={3: 'banushi'})
bn_10_4=pd.concat([(pd.DataFrame(at_banu_main1.iloc[4,:]))]*10).rename(columns={4: 'banushi'})
bn_10_5=pd.concat([(pd.DataFrame(at_banu_main1.iloc[5,:]))]*10).rename(columns={5: 'banushi'})
bn_10_6=pd.concat([(pd.DataFrame(at_banu_main1.iloc[6,:]))]*10).rename(columns={6: 'banushi'})
bn_10_7=pd.concat([(pd.DataFrame(at_banu_main1.iloc[7,:]))]*10).rename(columns={7: 'banushi'})
bn_10_8=pd.concat([(pd.DataFrame(at_banu_main1.iloc[8,:]))]*10).rename(columns={8: 'banushi'})
bn_10_9=pd.concat([(pd.DataFrame(at_banu_main1.iloc[9,:]))]*10).rename(columns={9: 'banushi'})
bn_10_10=pd.concat([(pd.DataFrame(at_banu_main1.iloc[10,:]))]*10).rename(columns={10: 'banushi'})
bn_10_all=pd.concat([bn_10_0,bn_10_1,bn_10_2,bn_10_3,bn_10_4,bn_10_5,bn_10_6,bn_10_7,bn_10_8,bn_10_9,bn_10_10])#11年分複製
bn_10_all=bn_10_all.reset_index(drop=True)
#種牡馬メイン
sbn_10_0=(pd.concat([(pd.DataFrame(at_syu_main1.iloc[0,:]))]*10)).rename(columns={0: 'syuboba'})
sbn_10_1=pd.concat([(pd.DataFrame(at_syu_main1.iloc[1,:]))]*10).rename(columns={1: 'syuboba'})
sbn_10_2=pd.concat([(pd.DataFrame(at_syu_main1.iloc[2,:]))]*10).rename(columns={2: 'syuboba'})
sbn_10_3=pd.concat([(pd.DataFrame(at_syu_main1.iloc[3,:]))]*10).rename(columns={3: 'syuboba'})
sbn_10_4=pd.concat([(pd.DataFrame(at_syu_main1.iloc[4,:]))]*10).rename(columns={4: 'syuboba'})
sbn_10_5=pd.concat([(pd.DataFrame(at_syu_main1.iloc[5,:]))]*10).rename(columns={5: 'syuboba'})
sbn_10_6=pd.concat([(pd.DataFrame(at_syu_main1.iloc[6,:]))]*10).rename(columns={6: 'syuboba'})
sbn_10_7=pd.concat([(pd.DataFrame(at_syu_main1.iloc[7,:]))]*10).rename(columns={7: 'syuboba'})
sbn_10_8=pd.concat([(pd.DataFrame(at_syu_main1.iloc[8,:]))]*10).rename(columns={8: 'syuboba'})
sbn_10_9=pd.concat([(pd.DataFrame(at_syu_main1.iloc[9,:]))]*10).rename(columns={9: 'syuboba'})
sbn_10_10=pd.concat([(pd.DataFrame(at_syu_main1.iloc[10,:]))]*10).rename(columns={10: 'syuboba'})
sbn_10_all=pd.concat([sbn_10_0,sbn_10_1,sbn_10_2,sbn_10_3,sbn_10_4,sbn_10_5,sbn_10_6,sbn_10_7,sbn_10_8,sbn_10_9,sbn_10_10])#11年分複製
sbn_10_all=sbn_10_all.reset_index(drop=True)
#水平結合 yearも
def matome_index(matome,index):
    torima=pd.DataFrame((akisyu_box_tanharai3.index.values//500)+2011)
    torima=(torima.rename(columns={0: 'datayear'}))
    return pd.concat([matome,index,torima],axis=1)

akisyu_box_tanharai4=matome_index(akisyu_box_tanharai3,kn_10_all)
akisyu_box_fukuharai4=matome_index(akisyu_box_fukuharai3,kn_10_all)
akisyu_box_syouritu4=matome_index(akisyu_box_syouritu3,kn_10_all)
akisyu_box_fukuritu4=matome_index(akisyu_box_fukuritu3,kn_10_all)
achokyo_box_tanharai4=matome_index(achokyo_box_tanharai3,cn_10_all)
achokyo_box_fukuharai4=matome_index(achokyo_box_fukuharai3,cn_10_all)
achokyo_box_syouritu4=matome_index(achokyo_box_syouritu3,cn_10_all)
achokyo_box_fukuritu4=matome_index(achokyo_box_fukuritu3,cn_10_all)
abanu_box_tanharai4=matome_index(abanu_box_tanharai3,bn_10_all)
abanu_box_fukuharai4=matome_index(abanu_box_fukuharai3,bn_10_all)
abanu_box_syouritu4=matome_index(abanu_box_syouritu3,bn_10_all)
abanu_box_fukuritu4=matome_index(abanu_box_fukuritu3,bn_10_all)
asyu_box_tanharai4=matome_index(asyu_box_tanharai3,sbn_10_all)
asyu_box_fukuharai4=matome_index(asyu_box_fukuharai3,sbn_10_all)
asyu_box_syouritu4=matome_index(asyu_box_syouritu3,sbn_10_all)
asyu_box_fukuritu4=matome_index(asyu_box_fukuritu3,sbn_10_all)
#AI学習用データの作成，総まとめ編
#u_umaとかとくっつけて(index,year,kisyu,banu,sho,syu)，それを5走の形にしてデータ作成
tokutyo_moto0 = tokutyo_moto.sort_values('index')#indexがおかしいので，昇順で並べ替え
tokutyo_moto1 = tokutyo_moto0.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
tokutyo_moto1 = tokutyo_moto1.drop(['index'], axis=1)#index列削除
tokutyo_moto1=tokutyo_moto1.reset_index()#indexを与える
tokutyo_moto2=tokutyo_moto1.loc[:, ['index','year', 'chokyosiryakusyo','banusiname', 'kisyuryakusyo','father']]

#今後の予定列の名前みて，akisyu_box_tanharai4などを水平に結合する　これやる

process_time = time.time() - start
print(process_time)
# endregion

# region inputdata_generator:inputdataを過去5走分作成してDBに出力するスクリプト　もともと②だったやつ スピード指数はここに格納　Wall time: 20h 18min 39s
# inputdata_generator:inputdataを過去5走分作成してDBに出力するスクリプト　もともと②だったやつ スピード指数はここに格納　Wall time: 20h 18min 39s
# ②　AI用のデータセットを作成し下記12回に分割してDBに保存する。6走分の馬柱を作成するイメージ
# 対象レースの馬柱（0走前）⇒1走前⇒2走前⇒3走前⇒4走前⇒5走前
# 対応する詳細⇒1走前対応する詳細⇒2走前対応する詳細⇒3走前対応する詳細⇒4走前対応する詳細⇒5走前対応する詳細

# ⓪データの準備　Wall time: 14.6 s
# データを格納する用のlist作成，listの中にlistが222個，228個存在
# n_uma_raceから必要なデータを抽出し，並べ替えを行う
n_uma_race_a0 = n_uma_race.loc[:,['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'wakuban', 'umaban', 'kettonum', 'bamei','sexcd','barei', 'tozaicd', 'chokyosiryakusyo', 'banusiname', 'futan', 'kisyuryakusyo', 'bataijyu', \
'zogenfugo', 'zogensa', 'ijyocd', 'kakuteijyuni', 'time', 'chakusacd', 'jyuni1c', 'jyuni2c', 'jyuni3c','jyuni4c','odds', 'ninki', 'honsyokin', 'zogensa', 'harontimel3',
'kettonum1', 'bamei1', 'timediff','kyakusitukubun']]
# スピード指数も取り出してデータの結合行う
spped_from_db = spped_from_db.sort_values('index')  # indexがおかしいので，昇順で並べ替え
spped_from_db1 = spped_from_db.reset_index(drop=True)  # 一番左のindexをindexに合わせて振りなおし。
n_uma_race_a = pd.concat([n_uma_race_a0, spped_from_db1['speed_idx']], axis=1)  # 結合　914907 rows × 38 columns
# いらない変数削除
del n_uma_race_a0, spped_from_db1
del spped_from_db  # ちょっと回すときはコメントアウト
# データをレース順で並びかえる，まずは並べ替え用データを作成する はやくなったはず
n_uma_race_a['tuika'] = n_uma_race_a['year'] + n_uma_race_a['monthday'] + n_uma_race_a['jyocd'] + n_uma_race_a['nichiji'] + n_uma_race_a['racenum'] + n_uma_race_a['umaban']
n_uma_race_b = n_uma_race_a.sort_values('tuika')  # 昇順で並べ替え
n_uma_race_c = n_uma_race_b.reset_index()  # index振りなおす
n_uma_race_1 = n_uma_race_c.drop(columns=['tuika'])  # いらん列削除で並べ替え完了
n_uma_race_1['index1'] = n_uma_race_1['index']  # 最終列にindex追加
n_uma_race_1 = n_uma_race_1.drop('index', axis=1)  # index列消す
n_uma_race_col_len = len(n_uma_race_1.columns)  # 特徴量の数
# いらない変数削除
del n_uma_race_a, n_uma_race_b, n_uma_race_c
# n_raceから必要なデータを抽出する
n_race_0 = n_race.loc[:,
           ['jyokencd5', 'trackcd', 'kyori', 'sibababacd', 'dirtbabacd', 'monthday', 'laptime1', 'laptime2', 'laptime3',
            'laptime4', 'laptime5', 'laptime6', 'laptime7', 'laptime8', 'laptime9', 'laptime10', 'laptime11',
            'laptime12', 'laptime13','laptime14', 'laptime15', 'laptime16', 'laptime17', 'laptime18', 'syussotosu', 'corner1', 'syukaisu1',
            'jyuni1','corner2', 'syukaisu2', 'jyuni2', 'corner3', 'syukaisu3', 'jyuni3', 'corner4', 'syukaisu4', 'jyuni4','ryakusyo6']]
n_race_1 = n_race_0.reset_index()  # index振りなおす
n_race_1['index1'] = n_race_1['index']  # 最終列にindex追加
n_race_1 = n_race_1.drop('index', axis=1)  # index列消す
n_race_1_col_len = len(n_race_1.columns)  # 特徴量の数
# いらない変数削除
del n_race_0
# 全馬の血統番号だけをn_uma_race_1から抽出，これで馬を検索する
map_ketto = n_uma_race_1.loc[:, ['kettonum']]
# pandasをnumpyに変換する　ここからデータを抽出 高速化用
np_uma_race = np.array(n_uma_race_1)
np_race = np.array(n_race_1)
np_map_ketto = np.array(map_ketto)
# レースIDの一覧を2つ作成　n_raceから一致するデータを取得する用
raceID_uma = np.array(
    n_uma_race_1['year'] + n_uma_race_1['monthday'] + n_uma_race_1['jyocd'] + n_uma_race_1['kaiji'] + n_uma_race_1[
        'nichiji'] + n_uma_race_1['racenum'])
raceID_race = np.array(
    n_race['year'] + n_race['monthday'] + n_race['jyocd'] + n_race['kaiji'] + n_race['nichiji'] + n_race['racenum'])
# 格納するlist作成
list_list = [[] for torima in range(n_uma_race_col_len * 6)]  # n_uma_race用
list_match = [[] for torima in range(n_race_1_col_len * 6)]  # n_race用

# ①馬柱データの作成
for i in range(len(n_uma_race_1)):  # 2010年からのレースについて馬柱の作成を実行する　914907 rows × 38 columns　10000につき12分
    if i % 100000 == 0:
        print(i)
    # ①-①n_uma_raceについての処理
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
    # リスト内リストに格納する
    for torima in range(n_uma_race_col_len * 6):  # 特徴量×6回分（0～5走）
        list_list[torima] += [data_mix[torima]]

    # ①-②n_raceについての処理
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
    # リスト内リストに格納する
    for torima in range(n_race_1_col_len * 6):
        list_match[torima] += [match_mix[torima]]

# いらない変数削除
del n_uma_race, n_race, n_uma_race_1, n_race_1, map_ketto, np_uma_race, np_map_ketto, np_race, raceID_uma, raceID_race

# ②-①Input_Data_UmaデータをDBに格納
for bango in range(6):  # 0～5走前　ここは手動要素あり
    kasan = n_uma_race_col_len * bango  # listのどこからとるか指定

    cre_data = pd.DataFrame(
        data={str(bango) + 'year': list_list[0 + kasan], str(bango) + 'monthday': list_list[1 + kasan],
              str(bango) + 'jyocd': list_list[2 + kasan], \
              str(bango) + 'kaiji': list_list[3 + kasan], str(bango) + 'nichiji': list_list[4 + kasan],
              str(bango) + 'racenum': list_list[5 + kasan], str(bango) + 'wakuban': list_list[6 + kasan], \
              str(bango) + 'umaban': list_list[7 + kasan], str(bango) + 'kettonum': list_list[8 + kasan],
              str(bango) + 'bamei': list_list[9 + kasan], str(bango) + 'sexcd': list_list[10 + kasan], \
              str(bango) + 'barei': list_list[11 + kasan], str(bango) + 'tozaicd': list_list[12 + kasan],
              str(bango) + 'chokyosiryakusyo': list_list[13 + kasan], str(bango) + 'banusiname': list_list[14 + kasan], \
              str(bango) + 'futan': list_list[15 + kasan], str(bango) + 'kisyuryakusyo': list_list[16 + kasan],
              str(bango) + 'bataijyu': list_list[17 + kasan], \
              str(bango) + 'zogenfugo': list_list[18 + kasan], str(bango) + 'zogensa': list_list[19 + kasan],
              str(bango) + 'ijyocd': list_list[20 + kasan], str(bango) + 'kakuteijyuni': list_list[21 + kasan], \
              str(bango) + 'time': list_list[22 + kasan], str(bango) + 'chakusacd': list_list[23 + kasan],
              str(bango) + 'jyuni1c': list_list[24 + kasan], str(bango) + 'jyuni2c': list_list[25 + kasan], \
              str(bango) + 'jyuni3c': list_list[26 + kasan], str(bango) + 'jyuni4c': list_list[27 + kasan],
              str(bango) + 'odds': list_list[28 + kasan], str(bango) + 'ninki': list_list[29 + kasan], \
              str(bango) + 'honsyokin': list_list[30 + kasan], str(bango) + 'zogensa': list_list[31 + kasan],
              str(bango) + 'harontimel3': list_list[32 + kasan], str(bango) + 'kettonum1': list_list[33 + kasan], \
              str(bango) + 'bamei1': list_list[34 + kasan], str(bango) + 'timediff': list_list[35 + kasan],
              str(bango) + 'kyakusitukubun': list_list[36 + kasan],
              str(bango) + 'speedidx': list_list[37 + kasan], str(bango) + 'index': list_list[38 + kasan]},
        columns=[str(bango) + 'year', str(bango) + 'monthday', str(bango) + 'jyocd', str(bango) + 'kaiji',
                 str(bango) + 'nichiji', str(bango) + 'racenum', str(bango) + 'wakuban', \
                 str(bango) + 'umaban', str(bango) + 'kettonum', str(bango) + 'bamei', str(bango) + 'sexcd',
                 str(bango) + 'barei', str(bango) + 'tozaicd', str(bango) + 'chokyosiryakusyo', \
                 str(bango) + 'banusiname', str(bango) + 'futan', str(bango) + 'kisyuryakusyo', str(bango) + 'bataijyu',
                 str(bango) + 'zogenfugo', str(bango) + 'zogensa', str(bango) + 'ijyocd', \
                 str(bango) + 'kakuteijyuni', str(bango) + 'time', str(bango) + 'chakusacd', str(bango) + 'jyuni1c',
                 str(bango) + 'jyuni2c', str(bango) + 'jyuni3c', str(bango) + 'jyuni4c', \
                 str(bango) + 'odds', str(bango) + 'ninki', str(bango) + 'honsyokin', str(bango) + 'zogensa',
                 str(bango) + 'harontimel3', str(bango) + 'kettonum1', \
                 str(bango) + 'bamei1', str(bango) + 'timediff', str(bango) + 'kyakusitukubun', str(bango) + 'speedidx',
                 str(bango) + 'index'])

    # indexを与える
    cre_data_1 = cre_data.reset_index()
    # データpostgreへ
    conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
    cursor = conn.cursor()  # データベースを操作できるようにする
    cre_data_1.to_sql(str(bango) + "Input_Data_Uma", ENGINE, if_exists='replace',
                      index=False)  # postgreに作成データを出力，存在してたらreplace
    # -------------実行ここまで
    cursor.close()  # データベースの操作を終了する
    conn.commit()  # 変更をデータベースに保存
    conn.close()  # データベースを閉じる

    # いらない変数削除
    del cre_data, cre_data_1

# ②-②Input_Data_RaceデータをDBに格納
for bango in range(6):  # 0～5
    kasan = n_race_1_col_len * bango  # listのどこからとるか指定

    cre_data = pd.DataFrame(
        data={str(bango) + 'jyokencd5': list_match[0 + kasan], str(bango) + 'trackcd': list_match[1 + kasan],
              str(bango) + 'kyori': list_match[2 + kasan], \
              str(bango) + 'sibababacd': list_match[3 + kasan], str(bango) + 'dirtbabacd': list_match[4 + kasan],
              str(bango) + 'monthday': list_match[5 + kasan], \
              str(bango) + 'laptime1': list_match[6 + kasan], str(bango) + 'laptime2': list_match[7 + kasan],
              str(bango) + 'laptime3': list_match[8 + kasan], str(bango) + 'laptime4': list_match[9 + kasan], \
              str(bango) + 'laptime5': list_match[10 + kasan], str(bango) + 'laptime6': list_match[11 + kasan],
              str(bango) + 'laptime7': list_match[12 + kasan], \
              str(bango) + 'laptime8': list_match[13 + kasan], str(bango) + 'laptime9': list_match[14 + kasan],
              str(bango) + 'laptime10': list_match[15 + kasan], str(bango) + 'laptime11': list_match[16 + kasan], \
              str(bango) + 'laptime12': list_match[17 + kasan], str(bango) + 'laptime13': list_match[18 + kasan],
              str(bango) + 'laptime14': list_match[19 + kasan], str(bango) + 'laptime15': list_match[20 + kasan], \
              str(bango) + 'laptime16': list_match[21 + kasan], str(bango) + 'laptime17': list_match[22 + kasan],
              str(bango) + 'laptime18': list_match[23 + kasan], str(bango) + 'syussotosu': list_match[24 + kasan], \
              str(bango) + 'corner1': list_match[25 + kasan], str(bango) + 'syukaisu1': list_match[26 + kasan],
              str(bango) + 'jyuni1': list_match[27 + kasan], str(bango) + 'corner2': list_match[28 + kasan], \
              str(bango) + 'syukaisu2': list_match[29 + kasan], str(bango) + 'jyuni2': list_match[30 + kasan],
              str(bango) + 'corner3': list_match[31 + kasan], \
              str(bango) + 'syukaisu3': list_match[32 + kasan], 'str(bango)+jyuni3': list_match[33 + kasan],
              str(bango) + 'corner4': list_match[34 + kasan], str(bango) + 'syukaisu4': list_match[35 + kasan], \
              str(bango) + 'jyuni4': list_match[36 + kasan], str(bango) + 'ryakusyo6': list_match[37 + kasan],
              str(bango) + 'index': list_match[38 + kasan]}, \
        columns=[str(bango) + 'jyokencd5', str(bango) + 'trackcd', str(bango) + 'kyori', str(bango) + 'sibababacd',
                 str(bango) + 'dirtbabacd', str(bango) + 'monthday', str(bango) + 'laptime1', \
                 str(bango) + 'laptime2', str(bango) + 'laptime3', str(bango) + 'laptime4', str(bango) + 'laptime5',
                 str(bango) + 'laptime6', str(bango) + 'laptime7', str(bango) + 'laptime8', str(bango) + 'laptime9', \
                 str(bango) + 'laptime10', str(bango) + 'laptime11', str(bango) + 'laptime12', str(bango) + 'laptime13',
                 str(bango) + 'laptime14', str(bango) + 'laptime15', str(bango) + 'laptime16', str(bango) + 'laptime17', \
                 str(bango) + 'laptime18', str(bango) + 'syussotosu', str(bango) + 'corner1', str(bango) + 'syukaisu1',
                 str(bango) + 'jyuni1', str(bango) + 'corner2', str(bango) + 'syukaisu2', str(bango) + 'jyuni2', \
                 str(bango) + 'corner3', str(bango) + 'syukaisu3', str(bango) + 'jyuni3', str(bango) + 'corner4',
                 str(bango) + 'syukaisu4', str(bango) + 'jyuni4', str(bango) + 'ryakusyo6', str(bango) + 'index'])

    # indexを与える
    cre_data_1 = cre_data.reset_index()
    # データpostgreへ
    conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
    cursor = conn.cursor()  # データベースを操作できるようにする
    cre_data_1.to_sql(str(bango) + "Input_Data_Race", ENGINE, if_exists='replace',
                      index=False)  # postgreに作成データを出力，存在してたらreplace
    # -------------実行ここまで
    cursor.close()  # データベースの操作を終了する
    conn.commit()  # 変更をデータベースに保存
    conn.close()  # データベースを閉じる

    # いらない変数削除
    del cre_data, cre_data_1
# endregion