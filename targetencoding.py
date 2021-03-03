# region targetencodingのデータを欠測処理して，使いやすい形にする 5s TODO
#targetencodingのデータを欠測処理して，使いやすい形にする
import time
start = time.time()
#水平結合 yearも
def matome_index(matome,index):
    torima=pd.DataFrame((akisyu_box_tanharai3.index.values//500)+2011)
    torima=(torima.rename(columns={0: 'datayear'}))
    return pd.concat([matome,index,torima],axis=1)

# region various condition
akisyu_box_tanharai1 = akisyu_box_tanharai.drop(['index'], axis=1)#index列削除
akisyu_box_fukuharai1 = akisyu_box_fukuharai.drop(['index'], axis=1)#index列削除
akisyu_box_syouritu1 = akisyu_box_syouritu.drop(['index'], axis=1)#index列削除
akisyu_box_fukuritu1 = akisyu_box_fukuritu.drop(['index'], axis=1)#index列削除
achokyo_box_tanharai1 = achokyo_box_tanharai.drop(['index'], axis=1)#index列削除
achokyo_box_fukuharai1 = achokyo_box_fukuharai.drop(['index'], axis=1)#index列削除
achokyo_box_syouritu1 = achokyo_box_syouritu.drop(['index'], axis=1)#index列削除
achokyo_box_fukuritu1 = achokyo_box_fukuritu.drop(['index'], axis=1)#index列削除
abanu_box_tanharai1 = abanu_box_tanharai.drop(['index'], axis=1)#index列削除
abanu_box_fukuharai1 = abanu_box_fukuharai.drop(['index'], axis=1)#index列削除
abanu_box_syouritu1 = abanu_box_syouritu.drop(['index'], axis=1)#index列削除
abanu_box_fukuritu1 = abanu_box_fukuritu.drop(['index'], axis=1)#index列削除
asyu_box_tanharai1 = asyu_box_tanharai.drop(['index'], axis=1)#index列削除
asyu_box_fukuharai1 = asyu_box_fukuharai.drop(['index'], axis=1)#index列削除
asyu_box_syouritu1 = asyu_box_syouritu.drop(['index'], axis=1)#index列削除
asyu_box_fukuritu1 = asyu_box_fukuritu.drop(['index'], axis=1)#index列削除
at_kisyu_sample1 = at_kisyu_sample.drop(['index'], axis=1)#index列削除
at_chokyo_sample1 = at_chokyo_sample.drop(['index'], axis=1)#index列削除
at_banu_sample1 = at_banu_sample.drop(['index'], axis=1)#index列削除
at_syu_sample1 = at_syu_sample.drop(['index'], axis=1)#index列削除
at_kisyu_main1 = at_kisyu_main.drop(['index'], axis=1)#index列削除
at_chokyo_main1 = at_chokyo_main.drop(['index'], axis=1)#index列削除
at_banu_main1 = at_banu_main.drop(['index'], axis=1)#index列削除
at_syu_main1 = at_syu_main.drop(['index'], axis=1)#index列削除
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
#水平結合⇒これを元データとくっつける
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
# endregion

#AI学習用データの作成，総まとめ編　TODO 20210223にやろう
#tokutyo_motoと特徴量を結合させる，↑を参照しながら水平にデータを結合していく　　16個DFある

#③どう結合させるのか賢いか？
df_indexmatch=tokutyo_moto.loc[:, ['index','kisyuryakusyo','chokyosiryakusyo','banusiname','father','year', 'jyocd','umaban','kyori','sibababacd','dirtbabacd','trackcd']]#元データ

def_motodata = pd.DataFrame(index=range(len(tokutyo_moto)), columns=range(len(asyu_box_tanharai4.columns)))  # 空データを作成
def add_featurevalue(moto_pandas,featurevalue_panda,basyo_panda):
    list(akisyu_indexnum.iloc[2,1])#セルデータの取り出し 文字になってる問題
    """
    場所データ参照して，元データの対応する1行に特徴量を追加する

    Parameters
    ----------
    moto_pandas: pandas
    NaNで作成した元データ
    featurevalue_panda: pandas
    大量の特徴量データ
    basyo_panda: pandas
    元データのどの行にデータを追加すればよいかが記載されている

    Returns
    -------
    kijyun_t_D: float
    基準タイム
    kyori_s_D: float
    距離指数
    """
    torima=pd.DataFrame((akisyu_box_tanharai3.index.values//500)+2011)
    torima=(torima.rename(columns={0: 'datayear'}))
    return pd.concat([matome,index,torima],axis=1)


#akisyu_indexnum,achokyo_indexnum,abanu_indexnum,asyu_indexnum　を見ればどの行にデータを入れればいいかわかる。


process_time = time.time() - start
print(process_time)
# endregion