# 単勝モデル　オリジナデータ
# ⓪ライブラリの準備
import pandas as pd
import numpy as np

# データ可視化ライブラリ
import matplotlib.pyplot as plt
import seaborn as sns

# LightGBMライブラリ
import lightgbm as lgb

# カテゴリカル変数用
from sklearn import preprocessing

# 訓練データとモデル評価用データに分けるライブラリ
from sklearn.model_selection import train_test_split

# DBとのやり取りライブラリ
import psycopg2
from sqlalchemy import create_engine

# Category Encoders
import category_encoders as ce

# 結果を可視化
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# グラフの設定
from jupyterthemes import jtplot

jtplot.style(theme='monokai')  # 選んだテーマの名前

# pdの設定
pd.set_option('display.max_rows', 500)  # 行すべてみる
pd.set_option('display.max_columns', 500)  # 列すべてみる
# -------------------------------------------------------

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
sql7 = 'SELECT * FROM public."0Input_Data_Uma";'  # 教師データ
sql8 = 'SELECT * FROM public."0Input_Data_Race";'  # 教師データ
sql9 = 'SELECT * FROM public."1Input_Data_Uma";'  # 教師データ
sql10 = 'SELECT * FROM public."1Input_Data_Race";'  # 教師データ
sql11 = 'SELECT * FROM public."2Input_Data_Uma";'  # 教師データ
sql12 = 'SELECT * FROM public."2Input_Data_Race";'  # 教師データ
sql13 = 'SELECT * FROM public."3Input_Data_Uma";'  # 教師データ
sql14 = 'SELECT * FROM public."3Input_Data_Race";'  # 教師データ
sql15 = 'SELECT * FROM public."4Input_Data_Uma";'  # 教師データ
sql16 = 'SELECT * FROM public."4Input_Data_Race";'  # 教師データ
sql17 = 'SELECT * FROM public."5Input_Data_Uma";'  # 教師データ
sql18 = 'SELECT * FROM public."5Input_Data_Race";'  # 教師データ
roop = [sql7, sql8, sql9, sql10, sql11, sql12, sql13, sql14, sql15, sql16, sql17, sql18]  # ひとまとめ

# データをindex順に並べなおす　ここ時間かかるので何とかしたい
# データを12セット分(umaとraceで6個ずつ)格納する箱を準備
data_list = [[] for torima in range(len(roop))]  # n_uma_race用
for i in range(len(roop)):  # 12のsqlに対して
    n_input_u = pd.read_sql(roop[i], conn)  # umarace詳細すべて取り出す
    sss = n_input_u.sort_values('index')  # 昇順で並べ替え
    del sss['index']  # index列を削除
    data_list[i] = sss.reset_index()  # index振りなおして格納
    del n_input_u, sss

# DB閉じる
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる


# ③予測したいレースの条件(開催場所，馬場状態，距離)を指定。対象の行番号をlistで返す
def det_jyoken(data_list, basyo_min, basyo_max, trackcd_min, trackcd_max, kyori_min, kyori_max):
    # 開催場所、芝・ダ、距離についての条件もとに抽出するデータを決定する
    n_input_u = data_list[0]  # umarace詳細すべて取り出す ここでは対象データは存在
    n_input_r = data_list[1]  # race詳細すべて取り出す
    n_input_u = n_input_u.loc[:, ['0jyocd']]  # 開催場所だけ取り出す
    n_input_r = n_input_r.loc[:, ['0trackcd', '0kyori']]  # trackcd,kyoriだけ取り出す
    n_in = pd.concat([n_input_u, n_input_r], axis=1)  # 横方向の連結
    del n_input_u, n_input_r  # メモリ確保
    # 欠損値処理，型変換
    n_in["0jyocd"] = pd.to_numeric(n_in["0jyocd"], errors='coerce')  # 文字はnanで置換，それ以外はfloatへ
    n_in["0trackcd"] = n_in["0trackcd"].astype(float)  # 芝・ダなどについての条件
    n_in["0kyori"] = n_in["0kyori"].astype(float)  # 距離についての条件
    # 開催場所、芝・ダ、距離についての条件を入力する 中央の芝で1800～2400など
    get_index = n_in[(basyo_min <= n_in["0jyocd"]) & (n_in["0jyocd"] <= basyo_max) & (trackcd_min <= n_in["0trackcd"]) \
                     & (n_in["0trackcd"] <= trackcd_max) & (kyori_min <= n_in["0kyori"]) & (
                                 n_in["0kyori"] <= kyori_max)]  # 条件を入力
    # return list(get_index.index)#行番号抽出
    return list(get_index.index)  # 行番号抽出


# det_jyoken(data_list,1,10,10,22,1400,2000)#行番号をlistで出力する
# l_index=det_jyoken(data_list,1,10,10,22,1400,2000)#対象のレース条件についての行番号をlistで出力する　中央芝
l_index = det_jyoken(data_list, 1, 10, 23, 26, 1400, 2000)  # 対象のレース条件についての行番号をlistで出力する　中央ダート


# 1~10で予測対象を中央競馬と指定,10,22とかは芝orダートなど,1400～2200とかは距離

# ④訓練用データのダウンサンプリング(false値の数が多いので数をtrue値を同じにする)を行いさらに抽出データを減らす
# まずは目的変数の取り出しと着順なしのデータを削除
# ※着順なしのデータを削除して回収率の評価に悪影響を与えてるかも。例えば競走中止や競争除外なども含まれているかもしれない
# 除外馬についてのデータ前処理をもう少し気を付けなければならないはず
def downsample(data_list):
    tar_data = data_list[0]  # データを取り出す
    tar_data = tar_data['0kakuteijyuni']  # 目的変数である着順を取得
    tar_data = tar_data.loc[l_index]  # 対象のレース条件についての行だけ取得
    tar_data = tar_data.astype(float)  # str⇒floatに変換
    return tar_data[tar_data != 0.0]  # 着順あるものだけ取得


tar_data = downsample(data_list)

# データを訓練用データとモデル評価用データに分割 9：1
# train:test_size に分ける　random_stateを設定し，分割するデータを固定する
train_set, test_set = train_test_split(tar_data, test_size=0.1, shuffle=False)  # shuffle=Falseで時系列情報残す
test_ind = list(test_set.index)  # testの行番号抽出


# 訓練用データのダウンサンプリング(ここで目的変数を1着かどうかにするか，3着以内かどうかにするかを決定している)
def downsample_test(train_set, mokuteki):
    train_set[train_set <= mokuteki] = 1  # 0/1のラベル振り
    train_set[train_set > mokuteki] = 0  # 0/1のラベル振り
    # len((train_set[train_set  == 1])),len((train_set[train_set  == 0]))#要素の比わかる
    train_set_0 = train_set[train_set == 0]  # 0だけ抽出
    train_set_1 = train_set[train_set == 1]  # 1だけ抽出
    sortnum = (train_set_0.sample(n=len(train_set_1), random_state=0))  # 一応乱数シード固定 imbalanced-learnのほうがいいのか？
    return sorted(list(sortnum.index) + list(train_set_1.index))  # ダウンサンプリング完了し、学習データの行番号を取得
    # len((sortnum)),len((train_set_1)),len((test_ind))#要素の比わかる


train_ind = downsample_test(train_set, 1)  # 目的変数の値を決定

# ⑤ダウンサンプリング後の本当に必要なデータだけを12セット分*2抽出,条件を全体のデータに適用する
train_list = [[] for torima in range(len(roop))]  # n_uma_race用
test_list = [[] for torima in range(len(roop))]  # n_uma_race用


def get_needed(data_list, train_ind, test_ind):
    n_input_u = data_list[i]  # umarace詳細すべて取り出す
    n_input_u_train = n_input_u.loc[train_ind]  # 対象の行だけ取得
    n_input_u_test = n_input_u.loc[test_ind]  # 対象の行だけ取得
    train_list[i] = n_input_u_train
    test_list[i] = n_input_u_test
    del n_input_u, n_input_u_train, n_input_u_test


for i in range(len(roop)):  # データ24セットに対してtrain_index/test_indexに基づいたデータを抽出する。このデータに基づいて学習/評価を行う
    get_needed(data_list, train_ind, test_ind)

print([len(v) for v in train_list])  # リストの中の要素数を確認
print([len(v) for v in test_list])  # リストの中の要素数を確認
# list_list[2]#取り出しかたはこれ
del data_list

# ⑥データの前処理　AIが学習できるように型変換するなど
new_train_list = [[] for torima in range(len(roop))]  # データ処理後のlist
new_test_list = [[] for torima in range(len(roop))]  # データ処理後のlist

# umaに対する処理
# 必要なデータだけ抽出　馬体重処理も
numli = [0, 2, 4, 6, 8, 10]
for v in range(len(numli)):  # umaに対する処理(trainとtestに対して)
    tar_data = train_list[numli[v]].copy()  # データを取り出す
    test_data = test_list[numli[v]].copy()  # データを取り出す
    retuname = tar_data.columns  # 列名取得
    tar_data[retuname[20]] = (tar_data[retuname[19]] + (tar_data[retuname[20]]))  # 馬体重結合してデータ置き換え
    test_data[retuname[20]] = (test_data[retuname[19]] + (test_data[retuname[20]]))  # 馬体重結合してデータ置き換え
    tar_data = tar_data.drop(tar_data.columns[[0, 1, 2, 4, 5, 6, 9, 10, 19, 21, 24, 31, 33, 34]],
                             axis=1)  # axis=0は行，axis=1は列で削除
    test_data = test_data.drop(test_data.columns[[0, 1, 2, 4, 5, 6, 9, 10, 19, 21, 24, 31, 33, 34]],
                               axis=1)  # axis=0は行，axis=1は列で削除

    num_list = [1, 2, 4, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]  # 数字データ
    cate_list = [0, 3, 5, 6, 7, 9]  # カテゴリカルデータ
    retuname = tar_data.columns  # 列名取得
    for i in range(len(num_list)):  # 数字列に対する処理
        check = tar_data[retuname[num_list[i]]]
        tar_data[retuname[num_list[i]]] = pd.to_numeric(check, errors='coerce')  # 文字はnanで置換，プラスマイナスも数字になる　数字はintへ
        check_test = test_data[retuname[num_list[i]]]
        test_data[retuname[num_list[i]]] = pd.to_numeric(check_test, errors='coerce')  # 文字はnanで置換，プラスマイナスも数字になる　数字はintへ
    for i in range(len(cate_list)):  # カテゴリ列に対する処理
        check = tar_data[retuname[cate_list[i]]]
        check_test = test_data[retuname[cate_list[i]]]
        if i == 3 or i == 4 or i == 5:  # 数字に変換するやつ 調教師、馬主、騎手　全データに対して適用したほうがよいかも
            # Encodeしたい列をリストで指定。もちろん複数指定可能。
            list_cols = retuname[cate_list[i]]
            # 序数をカテゴリに付与して変換
            ce_oe = ce.OrdinalEncoder(cols=list_cols, handle_unknown='impute')
            df_session_ce_ordinal = ce_oe.fit_transform(check)
            tar_data[retuname[cate_list[i]]] = df_session_ce_ordinal.astype('category')  # 完了
            # 序数をカテゴリに付与して変換
            ce_oe = ce.OrdinalEncoder(cols=list_cols, handle_unknown='impute')
            df_session_ce_ordinal = ce_oe.fit_transform(check_test)
            test_data[retuname[cate_list[i]]] = df_session_ce_ordinal.astype('category')  # 完了
        else:
            torima = pd.to_numeric(check, errors='coerce')  # 文字はnanで置換，プラスマイナスも数字になる　数字はintへ
            tar_data[retuname[cate_list[i]]] = torima.astype('category')  # カテゴリカル変数に変換
            torima = pd.to_numeric(check_test, errors='coerce')  # 文字はnanで置換，プラスマイナスも数字になる　数字はintへ
            test_data[retuname[cate_list[i]]] = torima.astype('category')  # カテゴリカル変数に変換
    new_train_list[numli[v]] = tar_data
    new_test_list[numli[v]] = test_data

# raceに対する処理
# 必要なデータだけ抽出　馬体重処理も
numli = [1, 3, 5, 7, 9, 11]
for v in range(len(numli)):  ##raceに対する処理(trainとtestに対して)
    tar_data = train_list[numli[v]].copy()  # データを取り出す
    test_data = test_list[numli[v]].copy()  # データを取り出す
    tar_data = tar_data.iloc[:, [1, 2, 3, 4, 5, 25]]  # axis=0は行，axis=1は列で削除
    test_data = test_data.iloc[:, [1, 2, 3, 4, 5, 25]]  # axis=0は行，axis=1は列で削除
    retuname = tar_data.columns  # 列名取得
    for i in range(len(tar_data.columns)):
        check = tar_data[retuname[i]]
        check_test = test_data[retuname[i]]
        if i == 2:
            tar_data[retuname[i]] = pd.to_numeric(check, errors='coerce')  # 文字はnanで置換，プラスマイナスも数字になる　数字はintへ
            test_data[retuname[i]] = pd.to_numeric(check_test, errors='coerce')  # 文字はnanで置換，プラスマイナスも数字になる　数字はintへ
        else:
            torima = pd.to_numeric(check, errors='coerce')  # 文字はnanで置換，プラスマイナスも数字になる　数字はintへ
            tar_data[retuname[i]] = torima.astype('category')  # カテゴリカル変数に変換
            torima = pd.to_numeric(check_test, errors='coerce')  # 文字はnanで置換，プラスマイナスも数字になる　数字はintへ
            test_data[retuname[i]] = torima.astype('category')  # カテゴリカル変数に変換
    new_train_list[numli[v]] = tar_data
    new_test_list[numli[v]] = test_data
print([len(v) for v in new_train_list])  # リストの中の要素数を確認
print([len(v) for v in new_test_list])  # リストの中の要素数を確認
del train_list


# ⑦説明変数と目的変数に分割 ここから12×2のデータを1×4にまとめる
# 訓練データを説明変数データ(X_train)と目的変数データ(y_train)に分割
def Train_Split(mokuteki):
    X_train = pd.concat([new_train_list[0], new_train_list[1], new_train_list[2], new_train_list[3], new_train_list[4], \
                         new_train_list[5], new_train_list[6], new_train_list[7], new_train_list[8], \
                         new_train_list[9], new_train_list[10], new_train_list[11]], axis=1).copy()  # 横方向の結合
    X_train = X_train.drop(
        ['0bataijyu', '0zogensa', '0kakuteijyuni', '0time', '0jyuni1c', '0jyuni2c', '0jyuni3c', '0jyuni4c',
         '0harontimel3', \
         '0timediff', '0kyakusitukubun'], axis=1)
    y_train = new_train_list[0]['0kakuteijyuni'].copy()
    y_train[y_train <= mokuteki] = 1  # 0/1のラベル振り
    y_train[y_train > mokuteki] = 0  # 0/1のラベル振り
    return X_train, y_train


# 訓練データを説明変数データ(X_train)と目的変数データ(y_train)に分割
X_train = Train_Split(1)[0]
y_train = Train_Split(1)[1]


# モデル評価用データを説明変数データ(X_test)と目的変数データ(y_testに分割
def Test_Split(mokuteki):
    X_test = pd.concat([new_test_list[0], new_test_list[1], new_test_list[2], new_test_list[3], new_test_list[4], \
                        new_test_list[5], new_test_list[6], new_test_list[7], new_test_list[8], \
                        new_test_list[9], new_test_list[10], new_test_list[11]], axis=1).copy()  # 横方向の結合
    X_test = X_test.drop(
        ['0bataijyu', '0zogensa', '0kakuteijyuni', '0time', '0jyuni1c', '0jyuni2c', '0jyuni3c', '0jyuni4c',
         '0harontimel3', \
         '0timediff', '0kyakusitukubun'], axis=1)
    y_test = new_test_list[0]['0kakuteijyuni'].copy()
    y_test[y_test <= mokuteki] = 1  # 0/1のラベル振り
    y_test[y_test > mokuteki] = 0  # 0/1のラベル振り
    return X_test, y_test


# モデル評価用データを説明変数データ(X_test)と目的変数データ(y_testに分割
X_test = Test_Split(1)[0]
y_test = Test_Split(1)[1]

# ⑧LightGBMのモデル構築
# LightGBM用のデータセットにすることで、高速で計算を行えるようになる
lgb_train = lgb.Dataset(X_train, y_train)  # train
lgb_eval = lgb.Dataset(X_test, y_test)  # 評価

# ここからもう少し理解を深める
# ハイパーパラメータを設定
params = {'metric': 'rmse', 'max_depth': 9}  # 評価基準:rmse，決定木の最大の深さ:9

# 学習を開始
gbm = lgb.train(params, lgb_train, valid_sets=lgb_eval, num_boost_round=10000, early_stopping_rounds=100,
                verbose_eval=50)
# ハイパーパラメータを設定,訓練データはlgb_trainだと指定,valid_sets=(lgb_train, lgb_eval),#lgb_trainとlgb_evalの結果を表示,lgb_trainとlgb_evalの結果を表示
# 学習を10000サイクル繰り返す,学習を10000サイクル繰り返す,100サイクル分くらいは観察し、過学習しているようならベストなサイクル数で学習を終了,学習過程を50サイクルずつ表示

# モデル評価用の説明変数(X_test)をLGBMに入れて結果を出力(predicted)
predicted = gbm.predict(X_test)

# 可視化の関数にぶち込めるように、モデル評価用データの予測値と正答値を加工して一つのデータフレームにする
pred_df = pd.concat([y_test.reset_index(drop=True), pd.Series(predicted)], axis=1)
pred_df.columns = ['true', 'pred']  # ラベル名を決定

## ここまでは問題なさそう

# ⑨馬券購入，結果を可視化
# 検証用データセットの作成
# testデータをレース単位に分割⇒予測値をトータル1になるように正規化⇒期待値ある馬を一頭購入で収支をグラフ化
# テストデータのもともとのindexを取得する
check_data_list = [[] for torima in range(round(len(test_list[0])))]  # testデータをレース単位に区分したものを格納するlist


def create_test_data(test_list, pred_df):
    test_race = test_list[0].copy()  # テストの対象の行をコピー　indexは事前に設置済み
    test_race_id = pd.DataFrame(
        test_race['0year'] + test_race['0jyocd'] + test_race['0kaiji'] + test_race['0nichiji'] + test_race[
            '0racenum'])  # レースID作成
    kuttuki = test_list[0].loc[:,
              ['0year', '0monthday', '0kakuteijyuni', '0ninki', '0odds']]  # axis=0は行，axis=1は列で削除　順位とオッズ抽出
    test_race_id = pd.concat([test_race_id, kuttuki], axis=1)  # test用のデータの開催日、順位とオッズを同じデータフレームへ
    alldata = pd.concat([test_race_id.reset_index(drop=True), pred_df], axis=1)
    alldata.rename(columns={0: 'raceID'}, inplace=True)
    return alldata
    del test_list


alldata = create_test_data(test_list, pred_df)

# レースを同じレースごとにまとめる
mem = 0
for raceID, sdf in alldata.groupby('raceID'):
    sdf['pred_seiki'] = (sdf['pred'] / sdf['pred'].sum())  # 正規化した勝率を列に追加
    sdf['kitaiti'] = (sdf['pred'] / sdf['pred'].sum()) * ((sdf['0odds'].astype(float)) / 10)  # 期待値を列に追加
    sdf['0ninki'] = sdf['0ninki'].astype(int)
    check_data_list[mem] = sdf  # 分割したデータをlistに保存
    mem += 1

# レース単位で馬券を購入
okane_list_pred = []  # お財布_予測値
okane_list_ninki = []  # お財布_人気通り
okane_list_kitaiti = []  # お財布_高期待値
okane_pred = 100000  # 初期お金_予測値
okane_ninki = 100000  # 初期お金_人気通り
okane_kitaiti = 100000  # 初期お金_高期待値
for i in range(len(check_data_list)):
    if len(check_data_list[i]) > 0:  # データあるとき
        onerace = check_data_list[i]  # レースのコピー
        # 当たりはずれ処理 予測値
        if int(onerace.loc[(onerace['pred'].idxmax()), ['0kakuteijyuni']]) == 1:  # 予測値最大の馬の着順を取得
            okane_pred = okane_pred + int(
                (onerace.loc[(onerace['pred'].idxmax()), ['0odds']].astype(float)) / 10 * 1000) - 1000
        else:
            okane_pred = okane_pred - 1000
        # 当たりはずれ処理 人気通り
        if int(onerace.loc[(onerace['0ninki'].idxmin()), ['0kakuteijyuni']]) == 1:  # 予測値最大の馬の着順を取得
            okane_ninki = okane_ninki + int(
                onerace.loc[(onerace['0ninki'].idxmin()), ['0odds']].astype(float) / 10 * 1000) - 1000
        else:
            okane_ninki = okane_ninki - 1000
            # 当たりはずれ処理 高期待値
        if int(onerace.loc[(onerace['kitaiti'].idxmax()), ['0kakuteijyuni']]) == 1:  # 予測値最大の馬の着順を取得
            okane_kitaiti = okane_kitaiti + int(
                onerace.loc[(onerace['kitaiti'].idxmax()), ['0odds']].astype(float) / 10 * 1000) - 1000
        else:
            okane_kitaiti = okane_kitaiti - 1000

        okane_list_pred.append(okane_pred)
        okane_list_ninki.append(okane_ninki)
        okane_list_kitaiti.append(okane_kitaiti)

# データ生成
x = np.arange(len(okane_list_ninki))
y = np.array(okane_list_pred)
y1 = np.array(okane_list_ninki)
y2 = np.array(okane_list_kitaiti)
# プロット
plt.plot(x, y, label="okane_list_pred")
plt.plot(x, y1, label="okane_list_ninki")
plt.plot(x, y2, label="okane_list_kitaiti")
plt.xlabel("race")
plt.ylabel("money")
# 凡例の表示
plt.legend()
# プロット表示(設定の反映)
plt.show()