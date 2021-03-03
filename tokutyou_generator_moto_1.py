# region tokutyou_generator_moto_1:特徴量元データに単勝払い戻しと複勝払い戻しを列に追加するスクリプトWall time: 1min 28s　コードの最適化までたぶんOK
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
moto_data_2 = moto_data_1.reset_index(drop=True)#一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。
moto_data_2 = moto_data_2.reset_index(drop=False)  # 一番左のindexをindexに合わせて振りなおし。drop=trueにして新規にindex発行しないようにする。これでなおった。 なんかわからんけどこれが正解っぽい
# 表示
moto_data_2['year'] = moto_data_2['year'].astype(int)  # 確定順位をobjectからintに変換
# endregion