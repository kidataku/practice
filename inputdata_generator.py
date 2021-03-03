# region inputdata_generator:inputdataを過去5走分作成してDBに出力するスクリプト　もともと②だったやつ スピード指数はここに格納　Wall time: 20h 18min 39s　もうめんどいからいいか
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
spped_from_db1 = spped_from_db
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