# region tokutyou_generator_moto_0:特徴量作成のために，払い戻しなども含めた元データを作成するスクリプトWall time: 3h 13min 38s コードの最適化までたぶんOK
# ⓪騎手・調教師・血統・馬主・生産者ごとの勝率・複勝率・単勝回収率・回収率などの特徴量を作成

# 行番号を探す関数
def my_index(l, x, default=np.nan):
    if x in l:
        return l.index(x)  # 一致するデータがあるときはindexを返す
    else:
        return default  # ないときはNaNを返す

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
# データはlistに入れて高速化
a_kyori,a_trackcd,a_sibababacd,a_dirtbabacd,a_father = [],[],[],[],[]
# データはlistに入れて高速化
a_tanuma1,a_tanpay1,a_tanuma2,a_tanpay2,a_tanuma3,a_tanpay3 = [],[],[],[],[],[]
a_uma1,a_pay1,a_uma2,a_pay2,a_uma3,a_pay3,a_uma4,a_pay4,a_uma5,a_pay5 = [],[],[],[],[],[],[],[],[],[]
# for文でデータを抽出
for i in range(len(matome_data)):
    if i % 100000 == 0:
        print(i)
    idx = my_index(matomerare_race_list, matome_data_list[i])  # 行番号を取得
    idx_father = my_index(matomerare_bamei_list, matome_bamei_list[i])  # 行番号を取得
    idx1 = my_index(n_harai_matome_idlist, matome_data_list[i])  # 行番号を取得
    # レースID
    if np.isnan(idx):  # NaNならTrue
        moji_str1a =moji_str1b =moji_str1c =moji_str1d = np.nan
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
        moji_str0a =moji_str0b =moji_str0c=moji_str0d =moji_str0e =moji_str0f = np.nan
        moji_stra =moji_strb =moji_strc =moji_strd =moji_stre =moji_strf =moji_strg =moji_strh =moji_stri =moji_strj = np.nan
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
          'father': a_father, 'tanuma1': a_tanuma1,'tanpay1': a_tanpay1, 'tanuma2': a_tanuma2, 'tanpay2': a_tanpay2, 'tanuma3': a_tanuma3, 'tanpay3': a_tanpay3,
          'fukuuma1': a_uma1, 'fukupay1': a_pay1, 'fukuuma2': a_uma2,
          'fukupay2': a_pay2, 'fukuuma3': a_uma3, 'fukupay3': a_pay3, 'fukuuma4': a_uma4, 'fukupay4': a_pay4,
          'fukuuma5': a_uma5, 'fukupay5': a_pay5},
    columns=['kyori', 'trackcd', 'sibababacd', 'dirtbabacd', 'father', 'tanuma1', 'tanpay1', 'tanuma2', 'tanpay2',
             'tanuma3', 'tanpay3', 'fukuuma1', 'fukupay1', 'fukuuma2','fukupay2', 'fukuuma3', 'fukupay3', 'fukuuma4', 'fukupay4', 'fukuuma5', 'fukupay5'])
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