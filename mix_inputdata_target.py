# -------------------------------------------------------------------------------------
# region postgre_connector:postgreとのデータをやり取りするスクリプト コードの最適化までOK ここあまり使ってない
# ⓪ライブラリのインポート
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import numpy as np

import time
start = time.time()

# SQL Data
# 5走分データ
sql7 = 'SELECT * FROM public."0Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql9 = 'SELECT * FROM public."1Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql11 = 'SELECT * FROM public."2Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql13 = 'SELECT * FROM public."3Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql15 = 'SELECT * FROM public."4Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql17 = 'SELECT * FROM public."5Input_Data_Uma" ORDER BY index ASC;'  # 教師データ

# target-encoding 特徴量
sql51 = 'SELECT * FROM public."0Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql52 = 'SELECT * FROM public."1Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql53 = 'SELECT * FROM public."2Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql54 = 'SELECT * FROM public."3Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql55 = 'SELECT * FROM public."4Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql56 = 'SELECT * FROM public."5Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql57 = 'SELECT * FROM public."6Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql58 = 'SELECT * FROM public."7Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql59 = 'SELECT * FROM public."8Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql60 = 'SELECT * FROM public."9Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql61 = 'SELECT * FROM public."10Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql62 = 'SELECT * FROM public."11Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql63 = 'SELECT * FROM public."12Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql64 = 'SELECT * FROM public."13Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql65 = 'SELECT * FROM public."14Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号
sql66 = 'SELECT * FROM public."15Tokutyo_data_new" ORDER BY index ASC;'  # 対象index番号

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
ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない

n_input_0uma = pd.read_sql(sql7, conn) #sql:実行したいsql，conn:対象のdb名
n_input_0uma=list(n_input_0uma.iloc[:,len(n_input_0uma.columns)-1])#index
n_input_1uma = pd.read_sql(sql9, conn) #sql:実行したいsql，conn:対象のdb名
n_input_1uma=list(n_input_1uma.iloc[:,len(n_input_1uma.columns)-1])#index
n_input_2uma = pd.read_sql(sql11, conn) #sql:実行したいsql，conn:対象のdb名
n_input_2uma=list(n_input_2uma.iloc[:,len(n_input_2uma.columns)-1])#index
n_input_3uma = pd.read_sql(sql13, conn) #sql:実行したいsql，conn:対象のdb名
n_input_3uma=list(n_input_3uma.iloc[:,len(n_input_3uma.columns)-1])#index
n_input_4uma = pd.read_sql(sql15, conn) #sql:実行したいsql，conn:対象のdb名
n_input_4uma=list(n_input_4uma.iloc[:,len(n_input_4uma.columns)-1])#index
n_input_5uma = pd.read_sql(sql17, conn)#sql:実行したいsql，conn:対象のdb名
n_input_5uma=list(n_input_5uma.iloc[:,len(n_input_5uma.columns)-1])#index

Uma_roop=[n_input_0uma,n_input_1uma,n_input_2uma,n_input_3uma,n_input_4uma,n_input_4uma]

Uma_roop1=[sql7,sql9,sql11,sql13,sql15,sql17]
Toku_roop=[sql51,sql52,sql53,sql54,sql55,sql56,sql57,sql58,sql59,sql60,sql61,sql62,sql63,sql64,sql65,sql66]

# 結合処理
for i in range(len(Uma_roop)):# number of Uma_roop
    conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
    cursor = conn.cursor()  # データベースを操作できるようにする
    ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
    print(i)
    col_name = Uma_roop[i]
    for j in range(len(Toku_roop)):# number of Toku_roop
        print('j:',j)
        Toku_panda = pd.read_sql(Toku_roop[j], conn).values.tolist()    # sql:実行したいsql，conn:対象のdb名
        # listd = list(uma_panda[col_name[len(col_name) - 1]])  # お尻にindex存在するのでtargetデータと結合
        #Toku_list = Toku_panda.values.tolist()  # pandasデータをlistにして軽量化
        sort_list = [[] for torima in range(len(col_name))]  # 行のサイズ
        for k in range(len(Toku_panda)):
            if np.isnan(col_name[k]) == 1:# nanの時はnanデータを追加
                sort_list[k] = [np.nan] * len((Toku_panda[0]))
                # torima = [np.nan] * len(Toku_panda.columns)
            else:
                sort_list[k] = Toku_panda[int(col_name[k])]#対象行のデータを格納
                # torima = Toku_list[int(Toku_list[k][len(Toku_panda.columns) - 1])]#対象行のデータを格納
        Store_panda = pd.DataFrame(sort_list)  # DataFrameに変換
        # index振って，DBに格納
        Store_panda = Store_panda.iloc[:,1:len(Store_panda.columns)-1]
        Store_panda = Store_panda.reset_index()
        Store_panda.to_sql(Uma_roop1[i][22:25]+'-'+Toku_roop[j][22:25] + "Toku_target", ENGINE,
                           if_exists='replace',index=False)  # postgreに作成データを出力，存在してたらreplace
        del sort_list, Store_panda

    cursor.close()  # データベースの操作を終了する
    conn.commit()  # 変更をデータベースに保存
    conn.close()  # データベースを閉じる
    del Toku_panda

process_time = time.time() - start
print(process_time)#  12.3hour

#--------------------------------------------------------------------------------------
# 特徴量について考察
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
# 特徴量データ
sql20 = 'SELECT * FROM public."tokutyo_moto" ORDER BY index ASC;'  # 教師データ
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
tokutyo_moto = pd.read_sql(sql20, conn)  # sql:実行したいsql，conn:対象のdb名
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
akisyu_indexnum = pd.read_sql(sql45, conn)  # sql:実行したいsql，conn:対象のdb名
achokyo_indexnum = pd.read_sql(sql46, conn)  # sql:実行したいsql，conn:対象のdb名a
abanu_indexnum = pd.read_sql(sql47, conn)  # sql:実行したいsql，conn:対象のdb名
syu_indexnum = pd.read_sql(sql48, conn)  # sql:実行したいsql，conn:対象のdb名

ENGINE = create_engine(CONNECT_STR)  # postgreは指定しなきゃいけない
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる
# endregion

# region tokutyou_generator TODO
import time
start = time.time()

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


# データの欠測，補間処理
def matome_index(matome, index):
    torima = pd.DataFrame((akisyu_box_tanharai3.index.values // 500) + 2011)
    torima = (torima.rename(columns={0: 'datayear'}))
    return pd.concat([matome, index, torima], axis=1)

# 初期設定
year_num = 11
basyo_num = 10
main_num = 50
# 統計データを作成する
moto_data = tokutyo_moto.copy()  # defaultはtrue copyにしないと参照渡しになって元データから変更になってしまう
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
# 時系列で並べ替え
moto_data['nara'] = moto_data['ID'] + moto_data['umaban']  # 並べ替え用
moto_data_1 = moto_data.sort_values('nara')  # indexがおかしいので，昇順で並べ替え　これで西暦月日順にデータが並び変わる
# index振りなおし
moto_data_1 = moto_data_1.drop('index', axis=1)
moto_data_2 = moto_data_1.reset_index(drop=True)  # 一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
moto_data_2 = moto_data_2.reset_index(drop=False)  # 一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。 なんかわからんけどこれが正解っぽい
# 表示
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
moto_2010_0 = moto_data_2[moto_data_2['year'] >= 2010]  # 2010年以降のデータだけにする。moto_data_2⇒moto_2010
moto_2010 = moto_2010_0.reset_index(drop=True)  # 一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
moto_2010 = moto_2010.drop(columns=['index'])  # いらん列削除で並べ替え完了
moto_2010 = moto_2010.reset_index(drop=False)  # 一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。 なんかわからんけどこれが正解っぽい
# 様々な条件でのindexを取得⇒ここは一つの条件でindex様々に取得して，その様々なindexのかつをしたほうがおしゃれかも ちょいむず
# TODO itertools.combinations これで変数の組み合わせわかる

# region Feature value
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
t122 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1150) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝 ★この条件はない
t123 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t124 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1300) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t125 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t126 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1500) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t127 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t128 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1700) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t129 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1800) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t130 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1900) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝 ★この条件はない
t131 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2000) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t132 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2100) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝 ★この条件は15回しかない
t133 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t134 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2300) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t135 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t136 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2500) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t137 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t138 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2800) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝 ★この条件は43回しかない
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
t160 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2800) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ ★この条件はない
t161 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3000) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t162 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3200) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t163 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3400) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ ★この条件はない
t164 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3600) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ ★この条件はない
t165 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1000) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t166 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1150) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝 ★この条件はない
t167 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t168 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1300) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝 ★この条件はない
t169 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t170 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1500) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t171 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t172 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1700) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t173 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1800) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t174 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1900) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝 ★この条件はない
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
t204 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2800) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ ★この条件はない
t205 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3000) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t206 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3200) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t207 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3400) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ ★この条件はない
t208 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3600) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ ★この条件はない
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
t_num=267
# endregion

# 条件のindexをlistに格納
jyo_list_pre = []
jyo_list_pre.extend(
    [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25,
     t26,t27, t28, t29, t30, t31, t32, t33, t34, t35, t36, t37, t38, t39, t40, t41, t42, t43, t44, t45, t46, t47, t48, t49,
     t50, t51, t52, t53, t54,t55, t56, t57, t58, t59, t60, t61, t62, t63, t64, t65, t66, t67, t68, t69, t70, t71, t72, t73, t74, t75, t76, t77,
     t78, t79, t80, t81, t82,t83, t84, t85, t86, t87, t88, t89, t90, t91, t92, t93, t94, t95, t96, t97, t98, t99, t100, t101, t102, t103, t104,
     t105, t106, t107, t108,t109, t110, t111, t112, t113, t114, t115, t116, t117, t118, t119, t120, t121, t122, t123, t124, t125, t126, t127,
     t128, t129, t130, t131,t132, t133, t134, t135, t136, t137, t138, t139, t140, t141, t142, t143, t144, t145, t146, t147, t148, t149, t150,
     t151, t152, t153, t154,t155, t156, t157, t158, t159, t160, t161, t162, t163, t164, t165, t166, t167, t168, t169, t170, t171, t172, t173,
     t174, t175, t176, t177,t178, t179, t180, t181, t182, t183, t184, t185, t186, t187, t188, t189, t190, t191, t192, t193, t194, t195, t196,
     t197, t198, t199, t200,t201, t202, t203, t204, t205, t206, t207, t208, t209, t210, t211, t212, t213, t214, t215, t216, t217, t218, t219,
     t220, t221, t222, t223,t224, t225, t226, t227, t228, t229, t230, t231, t232, t233, t234, t235, t236, t237, t238, t239, t240, t241, t242,
     t243, t244, t245, t246,t247, t248, t249, t250, t251, t252, t253, t254, t255, t256, t257, t258, t259, t260, t261, t262, t263, t264, t265,t266, t267])  # 全267条件

jyo_list = []
for i in range(len(jyo_list_pre)):
    t_check = jyo_list_pre[i]
    if len(t_check)>=10000: # 10000個以上データあれば格納
        jyo_list.append(t_check)

print([len(v) for v in jyo_list])

akisyu_box_tanharai = akisyu_box_tanharai.drop(['index'], axis=1)  # index列削除
akisyu_box_fukuharai = akisyu_box_fukuharai.drop(['index'], axis=1)  # index列削除
akisyu_box_syouritu = akisyu_box_syouritu.drop(['index'], axis=1)  # index列削除
akisyu_box_fukuritu = akisyu_box_fukuritu.drop(['index'], axis=1)  # index列削除
achokyo_box_tanharai = achokyo_box_tanharai.drop(['index'], axis=1)  # index列削除
achokyo_box_fukuharai = achokyo_box_fukuharai.drop(['index'], axis=1)  # index列削除
achokyo_box_syouritu = achokyo_box_syouritu.drop(['index'], axis=1)  # index列削除
achokyo_box_fukuritu = achokyo_box_fukuritu.drop(['index'], axis=1)  # index列削除
abanu_box_tanharai = abanu_box_tanharai.drop(['index'], axis=1)  # index列削除
abanu_box_fukuharai = abanu_box_fukuharai.drop(['index'], axis=1)  # index列削除
abanu_box_syouritu = abanu_box_syouritu.drop(['index'], axis=1)  # index列削除
abanu_box_fukuritu = abanu_box_fukuritu.drop(['index'], axis=1)  # index列削除
asyu_box_tanharai = asyu_box_tanharai.drop(['index'], axis=1)  # index列削除
asyu_box_fukuharai = asyu_box_fukuharai.drop(['index'], axis=1)  # index列削除
asyu_box_syouritu = asyu_box_syouritu.drop(['index'], axis=1)  # index列削除
asyu_box_fukuritu = asyu_box_fukuritu.drop(['index'], axis=1)  # index列削除
at_kisyu_sample = at_kisyu_sample.drop(['index'], axis=1)  # index列削除
at_chokyo_sample = at_chokyo_sample.drop(['index'], axis=1)  # index列削除
at_banu_sample = at_banu_sample.drop(['index'], axis=1)  # index列削除
at_syu_sample = at_syu_sample.drop(['index'], axis=1)  # index列削除
at_kisyu_main = at_kisyu_main.drop(['index'], axis=1)  # index列削除
at_chokyo_main = at_chokyo_main.drop(['index'], axis=1)  # index列削除
at_banu_main = at_banu_main.drop(['index'], axis=1)  # index列削除
at_syu_main = at_syu_main.drop(['index'], axis=1)  # index列削除
# サンプル数10以下をnanに変換
thr = 5
at_kisyu_sample2 = at_kisyu_sample.where(at_kisyu_sample > thr, np.nan)  # 10以下をnanにする
at_chokyo_sample2 = at_chokyo_sample.where(at_kisyu_sample > thr, np.nan)
at_banu_sample2 = at_banu_sample.where(at_kisyu_sample > thr, np.nan)
at_syu_sample2 = at_syu_sample.where(at_kisyu_sample > thr, np.nan)
# 数値データを1にする
at_kisyu_sample3 = at_kisyu_sample2.where(at_kisyu_sample < thr, 1)  # 10以上を1にする
at_chokyo_sample3 = at_chokyo_sample2.where(at_kisyu_sample < thr, 1)
at_banu_sample3 = at_banu_sample2.where(at_kisyu_sample < thr, 1)
at_syu_sample3 = at_syu_sample2.where(at_kisyu_sample < thr, 1)
# df_bool=sum((at_kisyu_sample4==5.0).sum())#足し算
# 特徴量データ×sampleデータして残すデータを決める
akisyu_box_tanharai2 = akisyu_box_tanharai * at_kisyu_sample3
akisyu_box_fukuharai2 = akisyu_box_fukuharai * at_kisyu_sample3
akisyu_box_syouritu2 = akisyu_box_syouritu * at_kisyu_sample3
akisyu_box_fukuritu2 = akisyu_box_fukuritu * at_kisyu_sample3
achokyo_box_tanharai2 = achokyo_box_tanharai * at_chokyo_sample3
achokyo_box_fukuharai2 = achokyo_box_fukuharai * at_chokyo_sample3
achokyo_box_syouritu2 = achokyo_box_syouritu * at_chokyo_sample3
achokyo_box_fukuritu2 = achokyo_box_fukuritu * at_chokyo_sample3
abanu_box_tanharai2 = abanu_box_tanharai * at_banu_sample3
abanu_box_fukuharai2 = abanu_box_fukuharai * at_banu_sample3
abanu_box_syouritu2 = abanu_box_syouritu * at_banu_sample3
abanu_box_fukuritu2 = abanu_box_fukuritu * at_banu_sample3
asyu_box_tanharai2 = asyu_box_tanharai * at_syu_sample3
asyu_box_fukuharai2 = asyu_box_fukuharai * at_syu_sample3
asyu_box_syouritu2 = asyu_box_syouritu * at_syu_sample3
asyu_box_fukuritu2 = asyu_box_fukuritu * at_syu_sample3
# 全ての行がnanの列番号を抽出。を残ったデータの平均で置き換え
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
# 全行NaNの列は削除する dropna(how='all', axis=1)
# メインを11年分並べる，縦に
# 騎手メイン
kn_10_0 = (pd.concat([(pd.DataFrame(at_kisyu_main.iloc[0, :]))] * 10)).rename(columns={0: 'jockey'})
kn_10_1 = pd.concat([(pd.DataFrame(at_kisyu_main.iloc[1, :]))] * 10).rename(columns={1: 'jockey'})
kn_10_2 = pd.concat([(pd.DataFrame(at_kisyu_main.iloc[2, :]))] * 10).rename(columns={2: 'jockey'})
kn_10_3 = pd.concat([(pd.DataFrame(at_kisyu_main.iloc[3, :]))] * 10).rename(columns={3: 'jockey'})
kn_10_4 = pd.concat([(pd.DataFrame(at_kisyu_main.iloc[4, :]))] * 10).rename(columns={4: 'jockey'})
kn_10_5 = pd.concat([(pd.DataFrame(at_kisyu_main.iloc[5, :]))] * 10).rename(columns={5: 'jockey'})
kn_10_6 = pd.concat([(pd.DataFrame(at_kisyu_main.iloc[6, :]))] * 10).rename(columns={6: 'jockey'})
kn_10_7 = pd.concat([(pd.DataFrame(at_kisyu_main.iloc[7, :]))] * 10).rename(columns={7: 'jockey'})
kn_10_8 = pd.concat([(pd.DataFrame(at_kisyu_main.iloc[8, :]))] * 10).rename(columns={8: 'jockey'})
kn_10_9 = pd.concat([(pd.DataFrame(at_kisyu_main.iloc[9, :]))] * 10).rename(columns={9: 'jockey'})
kn_10_10 = pd.concat([(pd.DataFrame(at_kisyu_main.iloc[10, :]))] * 10).rename(columns={10: 'jockey'})
kn_10_all = pd.concat(
    [kn_10_0, kn_10_1, kn_10_2, kn_10_3, kn_10_4, kn_10_5, kn_10_6, kn_10_7, kn_10_8, kn_10_9, kn_10_10])  # 11年分複製
kn_10_all = kn_10_all.reset_index(drop=True)
# 調教師メイン
cn_10_0 = (pd.concat([(pd.DataFrame(at_chokyo_main.iloc[0, :]))] * 10)).rename(columns={0: 'chokyo'})
cn_10_1 = pd.concat([(pd.DataFrame(at_chokyo_main.iloc[1, :]))] * 10).rename(columns={1: 'chokyo'})
cn_10_2 = pd.concat([(pd.DataFrame(at_chokyo_main.iloc[2, :]))] * 10).rename(columns={2: 'chokyo'})
cn_10_3 = pd.concat([(pd.DataFrame(at_chokyo_main.iloc[3, :]))] * 10).rename(columns={3: 'chokyo'})
cn_10_4 = pd.concat([(pd.DataFrame(at_chokyo_main.iloc[4, :]))] * 10).rename(columns={4: 'chokyo'})
cn_10_5 = pd.concat([(pd.DataFrame(at_chokyo_main.iloc[5, :]))] * 10).rename(columns={5: 'chokyo'})
cn_10_6 = pd.concat([(pd.DataFrame(at_chokyo_main.iloc[6, :]))] * 10).rename(columns={6: 'chokyo'})
cn_10_7 = pd.concat([(pd.DataFrame(at_chokyo_main.iloc[7, :]))] * 10).rename(columns={7: 'chokyo'})
cn_10_8 = pd.concat([(pd.DataFrame(at_chokyo_main.iloc[8, :]))] * 10).rename(columns={8: 'chokyo'})
cn_10_9 = pd.concat([(pd.DataFrame(at_chokyo_main.iloc[9, :]))] * 10).rename(columns={9: 'chokyo'})
cn_10_10 = pd.concat([(pd.DataFrame(at_chokyo_main.iloc[10, :]))] * 10).rename(columns={10: 'chokyo'})
cn_10_all = pd.concat(
    [cn_10_0, cn_10_1, cn_10_2, cn_10_3, cn_10_4, cn_10_5, cn_10_6, cn_10_7, cn_10_8, cn_10_9, cn_10_10])  # 11年分複製
cn_10_all = cn_10_all.reset_index(drop=True)
# 馬主メイン
bn_10_0 = (pd.concat([(pd.DataFrame(at_banu_main.iloc[0, :]))] * 10)).rename(columns={0: 'banushi'})
bn_10_1 = pd.concat([(pd.DataFrame(at_banu_main.iloc[1, :]))] * 10).rename(columns={1: 'banushi'})
bn_10_2 = pd.concat([(pd.DataFrame(at_banu_main.iloc[2, :]))] * 10).rename(columns={2: 'banushi'})
bn_10_3 = pd.concat([(pd.DataFrame(at_banu_main.iloc[3, :]))] * 10).rename(columns={3: 'banushi'})
bn_10_4 = pd.concat([(pd.DataFrame(at_banu_main.iloc[4, :]))] * 10).rename(columns={4: 'banushi'})
bn_10_5 = pd.concat([(pd.DataFrame(at_banu_main.iloc[5, :]))] * 10).rename(columns={5: 'banushi'})
bn_10_6 = pd.concat([(pd.DataFrame(at_banu_main.iloc[6, :]))] * 10).rename(columns={6: 'banushi'})
bn_10_7 = pd.concat([(pd.DataFrame(at_banu_main.iloc[7, :]))] * 10).rename(columns={7: 'banushi'})
bn_10_8 = pd.concat([(pd.DataFrame(at_banu_main.iloc[8, :]))] * 10).rename(columns={8: 'banushi'})
bn_10_9 = pd.concat([(pd.DataFrame(at_banu_main.iloc[9, :]))] * 10).rename(columns={9: 'banushi'})
bn_10_10 = pd.concat([(pd.DataFrame(at_banu_main.iloc[10, :]))] * 10).rename(columns={10: 'banushi'})
bn_10_all = pd.concat(
    [bn_10_0, bn_10_1, bn_10_2, bn_10_3, bn_10_4, bn_10_5, bn_10_6, bn_10_7, bn_10_8, bn_10_9, bn_10_10])  # 11年分複製
bn_10_all = bn_10_all.reset_index(drop=True)
# 種牡馬メイン
sbn_10_0 = (pd.concat([(pd.DataFrame(at_syu_main.iloc[0, :]))] * 10)).rename(columns={0: 'syuboba'})
sbn_10_1 = pd.concat([(pd.DataFrame(at_syu_main.iloc[1, :]))] * 10).rename(columns={1: 'syuboba'})
sbn_10_2 = pd.concat([(pd.DataFrame(at_syu_main.iloc[2, :]))] * 10).rename(columns={2: 'syuboba'})
sbn_10_3 = pd.concat([(pd.DataFrame(at_syu_main.iloc[3, :]))] * 10).rename(columns={3: 'syuboba'})
sbn_10_4 = pd.concat([(pd.DataFrame(at_syu_main.iloc[4, :]))] * 10).rename(columns={4: 'syuboba'})
sbn_10_5 = pd.concat([(pd.DataFrame(at_syu_main.iloc[5, :]))] * 10).rename(columns={5: 'syuboba'})
sbn_10_6 = pd.concat([(pd.DataFrame(at_syu_main.iloc[6, :]))] * 10).rename(columns={6: 'syuboba'})
sbn_10_7 = pd.concat([(pd.DataFrame(at_syu_main.iloc[7, :]))] * 10).rename(columns={7: 'syuboba'})
sbn_10_8 = pd.concat([(pd.DataFrame(at_syu_main.iloc[8, :]))] * 10).rename(columns={8: 'syuboba'})
sbn_10_9 = pd.concat([(pd.DataFrame(at_syu_main.iloc[9, :]))] * 10).rename(columns={9: 'syuboba'})
sbn_10_10 = pd.concat([(pd.DataFrame(at_syu_main.iloc[10, :]))] * 10).rename(columns={10: 'syuboba'})
sbn_10_all = pd.concat(
    [sbn_10_0, sbn_10_1, sbn_10_2, sbn_10_3, sbn_10_4, sbn_10_5, sbn_10_6, sbn_10_7, sbn_10_8, sbn_10_9,
     sbn_10_10])  # 11年分複製
sbn_10_all = sbn_10_all.reset_index(drop=True)
# 水平結合⇒これを元データとくっつける
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