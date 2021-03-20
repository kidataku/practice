# tokutyou_gen は①tokutyou_generator_moto_0，②tokutyou_generator_moto_1，③tokutyou_generator_2の3つから構成される。特徴量を作成する。
# ①tokutyou_generator_moto_0->特徴量作成のために，払い戻しなども含めた元データを作成するスクリプトWall time: 188min コードの最適化までOK
# ②tokutyou_generator->10000個くらいの特徴量をtarget-encodingで作成するスクリプト Wall time: 43171s->12時間　はじめ～元データへの追加前までで437分(7.29時間)

# region tokutyou_generator_moto_0
import time

start = time.time()


# 行番号を探す関数
def my_index(l, x, default=np.nan):
    if x in l:
        return l.index(x)  # 一致するデータがあるときはindexを返す
    else:
        return default  # ないときはNaNを返す


# 必要なデータの準備
# uma_raceから必要な馬の情報の取り出す
matome_data = n_uma_race.loc[:,
              ['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'umaban', 'bamei', 'chokyosiryakusyo',
               'banusiname', 'kisyuryakusyo', 'kakuteijyuni', 'odds']]
matome_data['ID'] = n_uma_race['year'] + n_uma_race['monthday'] + n_uma_race['jyocd'] + n_uma_race['kaiji'] + \
                    n_uma_race['nichiji'] + n_uma_race['racenum']  # レースIDの作成
# raceから必要なレースの情報の取り出す
matomerare_race = n_race.loc[:,
                  ['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'kyori', 'trackcd', 'sibababacd',
                   'dirtbabacd']]
matomerare_race['ID'] = n_race['year'] + n_race['monthday'] + n_race['jyocd'] + n_race['kaiji'] + n_race['nichiji'] + \
                        n_race['racenum']  # レースIDの作成
# n_haraiから必要な馬の情報の取り出す
n_harai_matome = n_harai.loc[:,
                 ['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'paytansyoumaban1', 'paytansyopay1',
                  'paytansyoumaban2', 'paytansyopay2', 'paytansyoumaban3', 'paytansyopay3', 'payfukusyoumaban1',
                  'payfukusyopay1',
                  'payfukusyoumaban2', 'payfukusyopay2', 'payfukusyoumaban3', 'payfukusyopay3', 'payfukusyoumaban4',
                  'payfukusyopay4', 'payfukusyoumaban5', 'payfukusyopay5', ]]
n_harai_matome['ID'] = n_harai['year'] + n_harai['monthday'] + n_harai['jyocd'] + n_harai['kaiji'] + n_harai[
    'nichiji'] + n_harai['racenum']  # レースIDの作成
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
# データはlistに入れて高速化
a_kyori, a_trackcd, a_sibababacd, a_dirtbabacd, a_father = [], [], [], [], []
# データはlistに入れて高速化
a_tanuma1, a_tanpay1, a_tanuma2, a_tanpay2, a_tanuma3, a_tanpay3 = [], [], [], [], [], []
a_uma1, a_pay1, a_uma2, a_pay2, a_uma3, a_pay3, a_uma4, a_pay4, a_uma5, a_pay5 = [], [], [], [], [], [], [], [], [], []
# for文でデータを抽出
for i in range(len(matome_data)):
    if i % 100000 == 0:
        print(i)
    idx = my_index(matomerare_race_list, matome_data_list[i])  # 行番号を取得
    idx_father = my_index(matomerare_bamei_list, matome_bamei_list[i])  # 行番号を取得
    idx1 = my_index(n_harai_matome_idlist, matome_data_list[i])  # 行番号を取得
    # レースID
    if np.isnan(idx):  # NaNならTrue can't find the index
        moji_str1a = moji_str1b = moji_str1c = moji_str1d = np.nan
    else:
        moji_str1a = kyori_list[idx]
        moji_str1b = trackcd_list[idx]
        moji_str1c = sibababacd_list[idx]
        moji_str1d = dirtbabacd_list[idx]
    # 父親の馬名
    if np.isnan(idx_father):  # NaNならTrue can't find the index
        moji_str1e = np.nan
    else:
        moji_str1e = fathername_list[idx_father]
    # 払い戻し
    if np.isnan(idx1):  # NaNならTrue can't find the index
        moji_str0a = moji_str0b = moji_str0c = moji_str0d = moji_str0e = moji_str0f = np.nan
        moji_stra = moji_strb = moji_strc = moji_strd = moji_stre = moji_strf = moji_strg = moji_strh = moji_stri = moji_strj = np.nan
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
          'father': a_father, 'tanuma1': a_tanuma1, 'tanpay1': a_tanpay1, 'tanuma2': a_tanuma2, 'tanpay2': a_tanpay2,
          'tanuma3': a_tanuma3, 'tanpay3': a_tanpay3,
          'fukuuma1': a_uma1, 'fukupay1': a_pay1, 'fukuuma2': a_uma2,
          'fukupay2': a_pay2, 'fukuuma3': a_uma3, 'fukupay3': a_pay3, 'fukuuma4': a_uma4, 'fukupay4': a_pay4,
          'fukuuma5': a_uma5, 'fukupay5': a_pay5},
    columns=['kyori', 'trackcd', 'sibababacd', 'dirtbabacd', 'father', 'tanuma1', 'tanpay1', 'tanuma2', 'tanpay2',
             'tanuma3', 'tanpay3', 'fukuuma1', 'fukupay1', 'fukuuma2', 'fukupay2', 'fukuuma3', 'fukupay3', 'fukuuma4',
             'fukupay4', 'fukuuma5', 'fukupay5'])
saigo = pd.concat([matome_data, merge], axis=1)  # 水平結合
# データをpostgreへ
cre_data_1 = saigo.reset_index()  # indexを与える
conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
cursor = conn.cursor()  # データベースを操作できるようにする
cre_data_1.to_sql("tokutyo_moto", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる
process_time = time.time() - start
print(process_time / 60)
# endregion

# region tokutyou_generator
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
moto_data_2 = moto_data_2.reset_index(
    drop=False)  # 一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。 なんかわからんけどこれが正解っぽい
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
moto_2010 = moto_data_2[moto_data_2['year'] >= 2010]  # 2010年以降のデータだけにする。moto_data_2⇒moto_2010
# umadataの抽出，2000年以降に産まれた馬だけを選択 not use
n_uma_pro['birthdate'] = pd.to_numeric(n_uma_pro["birthdate"], errors='coerce')
n_uma_pro = n_uma_pro[n_uma_pro['birthdate'] >= 20000001]  # 2000年からの馬を集計　10万頭くらい
# 様々な条件でのindexを取得⇒ここは一つの条件でindex様々に取得して，その様々なindexのかつをしたほうがおしゃれかも ちょいむず
# TODO itertools.combinations これで変数の組み合わせわかる

# region Feature value
t1 = list(moto_2010[((moto_2010['umaban'] < 9))].index)  # 馬番9より小さい　OK
t2 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400))].index)  # 馬番9より小さいかつ距離1400以下　OK
t3 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (
            moto_2010['kyori'] <= 2200))].index)  # 馬番9より小さいかつ距離1400~2200　OK
t4 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (
            moto_2010['kyori'] <= 3600))].index)  # 馬番9より小さいかつ距離2200~3600　OK
t5 = list(moto_2010[((moto_2010['umaban'] < 9) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 馬番9より小さいかつ良馬場　OK
t6 = list(moto_2010[((moto_2010['umaban'] < 9) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 馬番9より小さいかつ重馬場　OK
t7 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ芝　OK
t8 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつダート　OK
t9 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 馬番9より小さいかつ1400以下かつ良馬場　OK
t10 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 馬番9より小さいかつ1400~2200かつ良馬場　OK？
t11 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 馬番9より小さいかつ2200~3600かつ良馬場　OK？
t12 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 馬番9より小さいかつ1400以下かつ重馬場　OK？
t13 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 馬番9より小さいかつ1400~2200かつ重馬場　OK？
t14 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 馬番9より小さいかつ2200~3600かつ重馬場　OK？
t15 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ1400以下かつ芝　OK？
t16 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ1400～2200かつ芝　OK？
t17 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ2200～3600かつ芝　OK？
t18 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつ1400以下かつダート　OK？
t19 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつ1400～2200かつダート　OK？
t20 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつ2200～3600かつダート　OK？
t21 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['sibababacd'] > 0) & (
            (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 馬番9より小さいかつ芝でコースが11か17(内回り　OK？
t22 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['sibababacd'] > 0) & (
            (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 馬番9より小さいかつ芝でコースが12か18(外回り　OK？
t23 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ良馬場かつ芝　OK？
t24 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] > 0)))].index)  # 馬番9より小さいかつ重馬場かつ芝　OK？
t25 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつ良馬場かつダート　OK？
t26 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] == 0)))].index)  # 馬番9より小さいかつ重馬場かつダート　OK？
t27 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
                      (moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下かつ1400以下良かつ芝　OK？
t28 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
                      (moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下14-22かつ良かつ芝？
t29 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
                      (moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下22-36かつ良かつ芝？
t30 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
                      (moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下かつ1400以下重かつ芝　OK？
t31 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下14-22かつ重かつ芝？
t32 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 馬番9以下22-36かつ重かつ芝？
t33 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
                      (moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下かつ1400以下良かつダ　OK？
t34 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
                      (moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下14-22かつ良かつダ？
t35 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
                      (moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下22-36かつ良かつダ？
t36 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
                      (moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下かつ1400以下重かつダ　OK？
t37 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
                      (moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下14-22かつ重かつダ？
t38 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
                      (moto_2010['sibababacd'] == 0)))].index)  # 馬番9以下24-36かつ重かつダ？
t39 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下1400以下　芝　内回り？
t40 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (
            moto_2010['trackcd'] == 17)))].index)  # 8以下14-22　芝　内回り？
t41 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (
            moto_2010['trackcd'] == 17)))].index)  # 8以下24-36　芝　内回り?
t42 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下1400以下　芝　外回り？
t43 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (
            moto_2010['trackcd'] == 18)))].index)  # 8以下14-22　芝　外回り？
t44 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (
            moto_2010['trackcd'] == 18)))].index)  # 8以下22-36　芝　外回り？
t45 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下　良　芝　内回り？
t46 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下　重　芝　外回り？
t47 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下　重　芝　外回り？
t48 = list(moto_2010[((moto_2010['umaban'] < 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下　重　芝　内回り？
t49 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下14良芝内
t50 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下1422良芝内)
t51 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下2232良芝内)
t52 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下1422良芝外
t53 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下1422良芝外
t54 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下2232良芝外
t55 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下14重芝内
t56 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下1422重芝内
t57 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 8以下32重芝内
t58 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下14重芝外
t59 = list(moto_2010[((moto_2010['umaban'] < 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下1422重芝外
t60 = list(moto_2010[((moto_2010['umaban'] < 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                  (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 8以下36重芝外
# 馬番関係
t61 = list(moto_2010[((moto_2010['umaban'] >= 9))].index)
t62 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400))].index)
t63 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200))].index)
t64 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600))].index)
t65 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)
t66 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)
t67 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] > 0)))].index)
t68 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] == 0)))].index)
t69 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)
t70 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)
t71 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)
t72 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)
t73 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)
t74 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)
t75 = list(
    moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)))].index)
t76 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] > 0)))].index)
t77 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] > 0)))].index)
t78 = list(
    moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] == 0)))].index)
t79 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] == 0)))].index)
t80 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] == 0)))].index)
t81 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)) & (
(moto_2010['sibababacd'] > 0)))].index)
t82 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)) & (
(moto_2010['sibababacd'] > 0)))].index)
t83 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] > 0)))].index)
t84 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] > 0)))].index)
t85 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] == 0)))].index)
t86 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] == 0)))].index)
t87 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t88 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t89 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t90 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t91 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t92 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)
t93 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t94 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t95 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t96 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t97 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t98 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)
t99 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t100 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t101 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t102 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t103 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t104 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t105 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t106 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t107 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t108 = list(moto_2010[((moto_2010['umaban'] >= 9) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t109 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t110 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t111 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t112 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t113 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t114 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t115 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t116 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t117 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)
t118 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] <= 1400) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t119 = list(moto_2010[((moto_2010['umaban'] >= 9) & (1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
t120 = list(moto_2010[((moto_2010['umaban'] >= 9) & (2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)
# 馬番関係
t121 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1000) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t122 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1150) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t123 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1200) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t124 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1300) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t125 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1400) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t126 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1500) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t127 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1600) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t128 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1700) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t129 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1800) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t130 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1900) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t131 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2000) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t132 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2100) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t133 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2200) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t134 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2300) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t135 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2400) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t136 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2500) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t137 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2600) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t138 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2800) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t139 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3000) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t140 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3200) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t141 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3400) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t142 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3600) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t143 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1000) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t144 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1150) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t145 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1200) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t146 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1300) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t147 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1400) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t148 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1500) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t149 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1600) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t150 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1700) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t151 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1800) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t152 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1900) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t153 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2000) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t154 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2100) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t155 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2200) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t156 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2300) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t157 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2400) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t158 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2500) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t159 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2600) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t160 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2800) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t161 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3000) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t162 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3200) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t163 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3400) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t164 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3600) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t165 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1000) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t166 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1150) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t167 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1200) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t168 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1300) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t169 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1400) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t170 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1500) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t171 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1600) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t172 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1700) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t173 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1800) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t174 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1900) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t175 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2000) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t176 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2100) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t177 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2200) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t178 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2300) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t179 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2400) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t180 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2500) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t181 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2600) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t182 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2800) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t183 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3000) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t184 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3200) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t185 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3400) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t186 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3600) & (
(moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t187 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1000) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t188 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1150) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t189 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1200) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t190 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1300) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t191 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1400) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t192 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1500) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t193 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1600) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t194 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1700) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t195 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1800) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t196 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1900) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t197 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2000) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t198 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2100) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t199 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2200) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t200 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2300) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t201 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2400) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t202 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2500) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t203 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2600) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t204 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2800) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t205 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3000) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t206 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3200) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t207 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3400) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t208 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3600) & (
(moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
# 距離関係
t209 = list(moto_2010[((moto_2010['kyori'] <= 1400))].index)  # 1400以下
t210 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200))].index)  # 1422
t211 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600))].index)  # 2236
t212 = list(
    moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 14良
t213 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 1422良
t214 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 2236良
t215 = list(
    moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 14重
t216 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 1422重
t217 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 2236重
t218 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)))].index)  # 14芝
t219 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] > 0)))].index)  # 1422芝
t220 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] > 0)))].index)  # 2236芝
t221 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] == 0)))].index)  # 14ダ
t222 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] == 0)))].index)  # 1422ダ
t223 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] == 0)))].index)  # 2236ダ
t224 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] > 0)))].index)  # 14良芝
t225 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 1422良芝
t226 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 2236良芝
t227 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] > 0)))].index)  # 14重芝
t228 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 1422重芝
t229 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 2236重芝
t230 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] == 0)))].index)  # 14良ダ
t231 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 1422良ダ
t232 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 2236良ダ
t233 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] == 0)))].index)  # 14重ダ
t234 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 1422重ダ
t235 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 2236重ダ
t236 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 14芝内
t237 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 1422芝内
t238 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 2236芝内
t239 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 14芝外
t240 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 1422芝外
t241 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 2236芝外
t242 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 14良芝内
t243 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 1422良芝内
t244 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 2236良芝内
t245 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 14良芝外
t246 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 1422良芝外
t247 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 2236良芝外
t248 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 14重芝内
t249 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 1422重芝内
t250 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 2236重芝内
t251 = list(moto_2010[((moto_2010['kyori'] <= 1400) & ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & (
(moto_2010['sibababacd'] > 0)) & ((moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 14重芝外
t252 = list(moto_2010[((1400 < moto_2010['kyori']) & (moto_2010['kyori'] <= 2200) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 1422重芝内
t253 = list(moto_2010[((2200 < moto_2010['kyori']) & (moto_2010['kyori'] <= 3600) & (
(moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
                                   (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 2236重芝内
# 馬場状態良・重関係
t254 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)))].index)  # 良
t255 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)))].index)  # 重
t256 = list(moto_2010[(
            ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 良芝
t257 = list(moto_2010[(
            ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)))].index)  # 重芝
t258 = list(moto_2010[(
            ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 良ダ
t259 = list(moto_2010[(
            ((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] == 0)))].index)  # 重ダ
t260 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 良芝内
t261 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 重芝外
t262 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] == 1)) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 良芝外
t263 = list(moto_2010[(((moto_2010['sibababacd'] + moto_2010['dirtbabacd'] > 1)) & ((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 重芝内
# 芝/ダ関係
t264 = list(moto_2010[(((moto_2010['sibababacd'] > 0)))].index)  # 芝
t265 = list(moto_2010[(((moto_2010['sibababacd'] == 0)))].index)  # ダ
t266 = list(moto_2010[(((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 11) | (moto_2010['trackcd'] == 17)))].index)  # 内芝
t267 = list(moto_2010[(((moto_2010['sibababacd'] > 0)) & (
            (moto_2010['trackcd'] == 12) | (moto_2010['trackcd'] == 18)))].index)  # 外芝
# endregion

# 条件のindexをlistに格納
jyo_list = []
jyo_list.extend(
    [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25,
     t26,
     t27, t28, t29, t30, t31, t32, t33, t34, t35, t36, t37, t38, t39, t40, t41, t42, t43, t44, t45, t46, t47, t48, t49,
     t50, t51, t52, t53, t54,
     t55, t56, t57, t58, t59, t60, t61, t62, t63, t64, t65, t66, t67, t68, t69, t70, t71, t72, t73, t74, t75, t76, t77,
     t78, t79, t80, t81, t82,
     t83, t84, t85, t86, t87, t88, t89, t90, t91, t92, t93, t94, t95, t96, t97, t98, t99, t100, t101, t102, t103, t104,
     t105, t106, t107, t108,
     t109, t110, t111, t112, t113, t114, t115, t116, t117, t118, t119, t120, t121, t122, t123, t124, t125, t126, t127,
     t128, t129, t130, t131,
     t132, t133, t134, t135, t136, t137, t138, t139, t140, t141, t142, t143, t144, t145, t146, t147, t148, t149, t150,
     t151, t152, t153, t154,
     t155, t156, t157, t158, t159, t160, t161, t162, t163, t164, t165, t166, t167, t168, t169, t170, t171, t172, t173,
     t174, t175, t176, t177,
     t178, t179, t180, t181, t182, t183, t184, t185, t186, t187, t188, t189, t190, t191, t192, t193, t194, t195, t196,
     t197, t198, t199, t200,
     t201, t202, t203, t204, t205, t206, t207, t208, t209, t210, t211, t212, t213, t214, t215, t216, t217, t218, t219,
     t220, t221, t222, t223,
     t224, t225, t226, t227, t228, t229, t230, t231, t232, t233, t234, t235, t236, t237, t238, t239, t240, t241, t242,
     t243, t244, t245, t246,
     t247, t248, t249, t250, t251, t252, t253, t254, t255, t256, t257, t258, t259, t260, t261, t262, t263, t264, t265,
     t266, t267])  # 全267条件
# 払い戻しなどの集計用に必要な列（単勝/複勝払い戻し，確定順位）だけ抽出
np_moto_2010 = np.array(moto_data_2.loc[:, ['tan_harai', 'fuku_harai', 'kakuteijyuni']])

# 集計データを格納する用のlistを作成　二次元配列（リストのリスト）11年×10場×50メイン
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
# uma
# uma_box_tanharai=[[] for torima in range(100*len(uma_data))]#n_uma_race用 100000くらい
# uma_box_fukuharai=[[] for torima in range(100*len(uma_data))]#n_uma_race用
# uma_box_syouritu=[[] for torima in range(100*len(uma_data))]#n_uma_race用
# uma_box_fukuritu=[[] for torima in range(100*len(uma_data))]#n_uma_race用
# mainを追加するよう 11year
kisyu_main_11 = [[] for torima in range(year_num)]  # 騎手用　★
chokyo_main_11 = [[] for torima in range(year_num)]  # 調教師用　★
banu_main_11 = [[] for torima in range(year_num)]  # 馬主用　★
syu_main_11 = [[] for torima in range(year_num)]  # 種牡馬用　★
# count用
count = 0
count_uma = 0
count_main = 0
# nanのnp作成
mat = np.zeros([1, len(jyo_list)])
mat[:, :] = np.nan

# データ作成 11年×10場×50個（メイン）＝5500個
for i in range(year_num):  # 11年分
    # 年の範囲を指定する
    year_hani = 2011 + i  # 2011~2021でデータを作る　2011年までのデータは2012年に使う
    year_hani_low = year_hani - 3  # 2015なら2012
    year_hani_high = year_hani - 1  # 2015なら2014で2012-2014の3年間のデータを使用する
    print(year_hani)
    # 対象年以下を指定
    year_list = list(moto_2010[(
                (year_hani_low <= moto_2010['year']) & (moto_2010['year'] <= year_hani_high))].index)  # 特徴量作成のための元データ 2015年のデータなら2012年から2014年のデータを使用
    tokuapply_list = list(moto_2010[(moto_2010['year'] == year_hani)].index)  # 特徴量をapplyする行 ↑の例なら2015年とか
    # メイン取得用
    moto_main = moto_2010[((year_hani_low <= moto_2010['year']) & (moto_2010['year'] <= year_hani_high))]
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
        basyo_list = list(moto_2010[(moto_2010['jyocd'] == jyonum)].index)
        yearbasyo_list = list(set(year_list) & set(basyo_list))  # 年と場所に関する条件
        # uma_data=list(moto_main['bamei'].value_counts().to_dict().keys())#bamei　辞書にしてキーをlistで取得
        for j in range(main_num):  # 4つのメインに対して50個分データを作成
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
            # 特徴量作成用のindex
            kisyu_index1 = list(set(kisyu_list) & set(yearbasyo_list))#mainとyearとbasyoでindexを取得
            chokyo_index1 = list(set(chokyo_list) & set(yearbasyo_list))
            banu_list_index1 = list(set(banu_list) & set(yearbasyo_list))
            syu_index1 = list(set(syu_list) & set(yearbasyo_list))
            # list内包表記 特徴量作成用 mapの代わりになる　https://qiita.com/KTakahiro1729/items/c9cb757473de50652374
            syukei_kisyu = [set(kisyu_index1) & set(i_nakami) for i_nakami in jyo_list]  # main×267条件で1×267配列誕生
            syukei_chokyo = [set(chokyo_index1) & set(i_nakami) for i_nakami in jyo_list]
            syukei_banu = [set(banu_list_index1) & set(i_nakami) for i_nakami in jyo_list]
            syukei_syu = [set(syu_index1) & set(i_nakami) for i_nakami in jyo_list]
            # 特徴量を適応する行のindex
            kisyu_indexapp = list(set(kisyu_list) & set(tokuapply_list) & set(basyo_list))
            chokyo_indexapp = list(set(chokyo_list) & set(tokuapply_list) & set(basyo_list))
            banu_list_indexapp = list(set(banu_list) & set(tokuapply_list) & set(basyo_list))
            syu_indexapp = list(set(syu_list) & set(tokuapply_list) & set(basyo_list))
            # list内包表記 特徴量を適応する行 mapの代わりになる　https://qiita.com/KTakahiro1729/items/c9cb757473de50652374
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
at_kisyu_sample2 = at_kisyu_sample1.where(at_kisyu_sample1 > 5, np.nan)  # 5以下をnanにする
at_chokyo_sample2 = at_chokyo_sample1.where(at_kisyu_sample1 > 5, np.nan)
at_banu_sample2 = at_banu_sample1.where(at_kisyu_sample1 > 5, np.nan)
at_syu_sample2 = at_syu_sample1.where(at_kisyu_sample1 > 5, np.nan)
# 数値データを1にする
at_kisyu_sample3 = at_kisyu_sample2.where(at_kisyu_sample1 < 5, 1)  # 5以上を1にする
at_chokyo_sample3 = at_chokyo_sample2.where(at_kisyu_sample1 < 5, 1)
at_banu_sample3 = at_banu_sample2.where(at_kisyu_sample1 < 5, 1)
at_syu_sample3 = at_syu_sample2.where(at_kisyu_sample1 < 5, 1)
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
# それぞれの列においてNANを残ったデータの平均で置き換え
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
kn_10_all = pd.concat(
    [kn_10_0, kn_10_1, kn_10_2, kn_10_3, kn_10_4, kn_10_5, kn_10_6, kn_10_7, kn_10_8, kn_10_9, kn_10_10])  # 11年分複製
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
cn_10_all = pd.concat(
    [cn_10_0, cn_10_1, cn_10_2, cn_10_3, cn_10_4, cn_10_5, cn_10_6, cn_10_7, cn_10_8, cn_10_9, cn_10_10])  # 11年分複製
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
bn_10_all = pd.concat(
    [bn_10_0, bn_10_1, bn_10_2, bn_10_3, bn_10_4, bn_10_5, bn_10_6, bn_10_7, bn_10_8, bn_10_9, bn_10_10])  # 11年分複製
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

process_time = time.time() - start
print(process_time)#437分

# ③どう結合させるのか賢いか？　夜はここから spend 276min
import itertools

alldata = [akisyu_box_tanharai4, akisyu_box_fukuharai4, akisyu_box_syouritu4, akisyu_box_fukuritu4,
           achokyo_box_tanharai4, achokyo_box_fukuharai4, achokyo_box_syouritu4,achokyo_box_fukuritu4,
           abanu_box_tanharai4, abanu_box_fukuharai4, abanu_box_syouritu4, abanu_box_fukuritu4,
           asyu_box_tanharai4, asyu_box_fukuharai4, asyu_box_syouritu4, asyu_box_fukuritu4]# 4mainの勝率，回収率をまとめる

for z in range(len(alldata)):# 16個分
    print(z)
    torima_maindata = alldata[z].iloc[:, 0:267]  # 列取り出し
    # どのindex使うか
    if 0 <= z < 4:# 騎手
        ifdata = indexnum10
    elif 4 <= z < 8:# 調教
        ifdata = indexnum20
    elif 8 <= z < 12:# 馬主
        ifdata = indexnum30
    else:# 種牡馬
        ifdata = indexnum40

    torima_indexdata = ifdata.iloc[:, 1:268]  # 列取り出し
    def_motodata = pd.DataFrame(index=range(len(tokutyo_moto)),
    columns=range(len(torima_indexdata.columns)))  # 空データを作成 914907×267

    # indexdata 5500*267の全セルに対してfor文を回す itertoolsを使えばfor2つが1つで済む
    for i, j in itertools.product(range(len(torima_indexdata)), range(len(torima_indexdata.columns))):# 5500*267
        toridashi_data = torima_indexdata.iloc[i, j]  # 行データが格納されているlistを取り出し
        for k in range(len(toridashi_data)):#  list内のデータ数だけ実行
            def_motodata.iloc[toridashi_data[k], j] = torima_maindata.iloc[i, j]#TODO ここが時間かかる numpyにする？

    # index振って，DBに格納
    def_motodata = def_motodata.reset_index()
    conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
    cursor = conn.cursor()  # データベースを操作できるようにする
    def_motodata.to_sql(str(z) + "Tokutyo_data", ENGINE, if_exists='replace',
    index=False)  # postgreに作成データを出力，存在してたらreplace
    cursor.close()  # データベースの操作を終了する
    conn.commit()  # 変更をデータベースに保存
    conn.close()  # データベースを閉じる

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
indexnum10.to_sql("t_kisyu_indexnum", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
indexnum20.to_sql("t_chokyo_indexnum", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
indexnum30.to_sql("t_banu_indexnum", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
indexnum40.to_sql("t_syu_indexnum", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
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
