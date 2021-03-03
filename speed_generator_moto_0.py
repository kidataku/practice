# region speed_generator_moto_0:スピード指数作成のための元データを作成してDBに出力するスクリプト コードの最適化までたぶんOK
# ⓪騎手・調教師・血統・馬主・生産者ごとの勝率・複勝率・単勝回収率・回収率などの特徴量を作成
# uma_raceから必要な馬の情報の取り出す 元データ
matome_data = n_uma_race.loc[:,['year', 'monthday', 'jyocd', 'kaiji', 'nichiji', 'racenum', 'bamei', 'futan', 'time', 'kakuteijyuni']]
matome_data['ID'] = n_uma_race['year'] + n_uma_race['monthday'] + n_uma_race['jyocd'] + n_uma_race['kaiji'] +n_uma_race['nichiji'] + n_uma_race['racenum']  # レースIDを追加
# raceから必要なレースの情報の取り出す　追加データ
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
# 行番号を探す関数
def my_index(l, x, default=np.nan):
    if x in l:#Lにxがあれば
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