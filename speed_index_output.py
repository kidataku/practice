# region speed_index_output:対象日のレースの馬のスピード指数を出力するスクリプト コードの最適化までたぶんOK
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