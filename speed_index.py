# speed_indexは①speed_generator_moto_0，②speed_generator_1，③speed_index_outputの3つから構成される。スピード指数を作成するスクリプト。
# ①speed_generator_moto_0->スピード指数作成のための元データを作成してDBに出力するスクリプト コードの最適化までたぶんOK 20分くらい？
# ②speed_generator_1->スピード指数を作成するコード コードの最適化までたぶんOK Wall time: 20分
# ③speed_index_output->対象日のレースの馬のスピード指数を出力するスクリプト コードの最適化までたぶんOK　5分くらい？

# region speed_generator_moto_0

# 行番号を探す関数を定義
def my_index(l, x, default=np.nan):
    if x in l:#Lにxがあれば
        return l.index(x)  # 一致するデータがあるときはindexを返す
    else:
        return default  # ないときはNaNを返す
# uma_raceから必要な馬の情報の取り出す 元データ
matome_data = n_uma_race.loc[:,['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'bamei', 'futan', 'time', 'kakuteijyuni']]
matome_data['ID'] = n_uma_race['year'] + n_uma_race['monthday'] + n_uma_race['jyocd'] + n_uma_race['kaiji'] +n_uma_race['nichiji'] + n_uma_race['racenum']  # レースIDを追加
# raceから必要なレースの情報の取り出す　追加データ(くっつけられる方)
matomerare_race = n_race.loc[:,['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'gradecd', 'syubetucd', 'jyokencd1','jyokencd2', 'jyokencd3', 'jyokencd4',
'jyokencd5', 'kyori', 'trackcd', 'tenkocd', 'sibababacd', 'dirtbabacd', 'kigocd']]
matomerare_race['ID'] = n_race['year'] + n_race['monthday'] + n_race['jyocd'] + n_race['kaiji'] + n_race['nichiji'] +n_race['racenum']  # レースIDを追加
# レースIDをlistにして検索しやすいようにする
matome_data_list = list(matome_data['ID'])  # レースIDをlistで取得
matomerare_race_list = list(matomerare_race['ID'])  # レースIDをlistで取得
# 準備 データ作成に必要なものだけlist化
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
# データ格納用のlistをそれぞれ作成
a_gradecd, a_syubetu, a_jyokencd1, a_jyokencd2, a_jyokencd3, a_jyokencd4, a_jyokencd5, a_kyori, a_trackcd, a_tenkocd, a_sibababacd, a_dirtbabacd, a_kigocd = [], [], [], [], [], [], [], [], [], [], [], [], []
# for文でデータを抽出
for i in range(len(matome_data)):
    if i % 100000 == 0:
        print(i)
    idx = my_index(matomerare_race_list, matome_data_list[i])  # 行番号を取得 matome_data_listの対象のIDが，matomerare_race_listで何行目にあるか調べその行番号を取得
    # レースID
    if np.isnan(idx):  # NaNならTrue データなければnanに
        moji_str0a =moji_str1a =moji_str1b =moji_str1c =moji_str1d =moji_str1e =moji_str1f =moji_str1g =moji_str1h =moji_str1i =moji_str1j =moji_str1k =moji_str1l = np.nan
    else:#データあれば取り出し
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
saigo = pd.concat([matome_data, merge], axis=1)#データを水平結合
# データpostgreへ
cre_data_1 = saigo.reset_index()  # indexを与える
conn = psycopg2.connect(" user=" + USER + " dbname=" + DB_NAME + " password=" + PASSWORD)  # データベースを開く
cursor = conn.cursor()  # データベースを操作できるようにする
cre_data_1.to_sql("a_time", ENGINE, if_exists='replace', index=False)  # postgreに作成データを出力，存在してたらreplace
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる
# endregion

# region speed_generator_1
import datetime
import time
start = time.time()

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
    syukei_D = df_moto_D[(df_moto_D['kyori'] == kyori_D) & (df_moto_D['jyocd'] == basyo_j_D) & (hajime_D <= df_moto_D['year']) & (df_moto_D['year'] < year_D)]#データ抽出
    kijyun_t_D = round(np.nanmean(syukei_D['sectime']), 1)  # 基準タイムを計算
    kyori_s_D = round(1 / (10 * np.nanmean(syukei_D['sectime'])) * 1000, 2)  # 距離指数を算出　×10することで妥当になる　距離指数＝1/基準タイム　ここ妥当かなぞ
    return kijyun_t_D, kyori_s_D

# 斤量を585⇒58.5みたいに直す
def futan_henkan(x):
    return float(x[0:2] + '.' + x[2])

# 走破時計を4桁の数字⇒秒になおす
def henkan(x):
    if x[0] == '0':
        return float(x[1:3] + '.' + x[3])
    else:
        return 60 * int(x[0]) + float(x[1:3] + '.' + x[3])

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
speed_data['futan_siyou'] = speed_data['futan'].apply(futan_henkan)
speed_data['sectime'] = speed_data['time'].apply(henkan)
speed_data['sectime'] = speed_data['sectime'].replace(0, np.nan)  # 走破時計0をNaNに置き換え
speed_data['year'] = pd.to_numeric(speed_data["year"], errors='coerce')  # numericに型変換しつつ欠測があったらnanで埋める
speed_data['kyori'] = pd.to_numeric(speed_data["kyori"], errors='coerce')  # numericに型変換しつつ欠測があったらnanで埋める 169161
speed_data['jyocd'] = pd.to_numeric(speed_data["jyocd"], errors='coerce')  # numericに型変換しつつ欠測があったらnanで埋め
speed_data = speed_data[speed_data['year'] >= 2010]  # 抽出　2010年～のデータ、バグデータの取り除き　892060 ⇒825827
# ①基準タイムと距離指数の算出
# 上記を算出するために元データとして天気：晴/曇り，馬場：良/稍，着順1～3着，条件：1～3勝クラス天気晴れのみのデータを抽出　825827⇒43429（36426 良だけだと）
speed_data_hare = speed_data[((speed_data['tenkocd'] == '1') | (speed_data['tenkocd'] == '2'))& ((speed_data['sibababacd'] == '1') | (speed_data['dirtbabacd'] == '1') | (
speed_data['sibababacd'] == '2') | (speed_data['dirtbabacd'] == '2'))& ((speed_data['kakuteijyuni'] == '01') | (speed_data['kakuteijyuni'] == '02') | (speed_data['kakuteijyuni'] == '03'))
& ((speed_data['jyokencd5'] == '005') | (speed_data['jyokencd5'] == '010') | (speed_data['jyokencd5'] == '016'))]
# 基準タイムと距離指数を格納する箱を作成　11年分を各年ごとに算出 芝72個、ダート56個
today = datetime.date.today()
year_range=today.year-2010#何年分作成したいか
kijyun_siba = [[] for torima in range(year_range)]  # 基準タイム用　芝
kijyun_dirt = [[] for torima in range(year_range)]  # 基準タイム用　ダート
kyori_siba = [[] for torima in range(year_range)]  # 距離指数用　芝
kyori_dirt = [[] for torima in range(year_range)]  # 距離指数用　ダート
count = 0  # 年度をカウントする用

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
            get=cal_index(df_siba, speed_data_hare, k, j, hajime, year)
            df_siba.iloc[k, j - 1]=get[0]
            df_siba_kyori.iloc[k, j - 1] =get[1]
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
                    spped_data_kakunou += [round(speed_index, 1)]  # スピード指数を格納　あとでまとめて追加する
                    index_kakunou += [pd_index]  # indexを格納　あとでまとめて追加する
            else:
                pass
                # ilocは列名の指定できないけど行番号の指定が取り出したものの何番目の行という考えかｔら。，locは指定できるけど行番号の指定がそいつがもともと持っている行番号になる。

# ③スピード指数格納　時間すごいかかる 1時間くらい ⇒短縮に成功
data = pd.DataFrame(index=range(len(a_time)))#くっつけるために0～すべてのデータ元データを作成
tempo=pd.DataFrame(spped_data_kakunou)
tempo_new = tempo.rename(columns={0: 'speed_idx'})
df_tempo=pd.concat([pd.DataFrame(index_kakunou), tempo_new], axis=1)
df_tempo_1 = df_tempo.set_index(0)
spped_append=pd.concat([data, df_tempo_1], axis=1)

a_time1=pd.concat([a_time, spped_append], axis=1)#くっつけ

process_time = time.time() - start
print(process_time/60)
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

# region speed_index_output
# speed_index_output:対象日のレースの馬のスピード指数を出力するスクリプト
import os  # フォルダ作成用

# データ準備
spped_from_db1 = spped_from_db
# レースIDと日にちをpandasに追加
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
# endregion