# region tokutyou_generator_2:10000個くらいの特徴量をtarget-encodingで作成するスクリプト Wall time: 4h 58min 30s
# pandasのデータをfloat型にする　NaNもあるし，float型
# 競走中止とかは将来的に
import time
start = time.time()
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
# region various condition
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
t122 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1150) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t123 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t124 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1300) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t125 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t126 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1500) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t127 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t128 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1700) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t129 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1800) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t130 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 1900) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t131 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2000) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t132 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2100) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t133 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t134 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2300) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t135 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t136 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2500) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t137 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
t138 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2800) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以下かつ1000mかつ芝
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
t160 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 2800) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t161 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3000) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t162 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3200) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t163 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3400) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t164 = list(moto_2010[((moto_2010['umaban'] < 9) & (moto_2010['kyori'] == 3600) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以下かつ1000mかつダ
t165 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1000) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t166 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1150) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t167 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1200) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t168 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1300) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t169 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1400) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t170 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1500) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t171 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1600) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t172 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1700) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t173 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1800) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
t174 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 1900) & ((moto_2010['sibababacd'] > 0)))].index)  # 9以上かつ1000mかつ芝
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
t204 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 2800) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t205 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3000) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t206 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3200) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t207 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3400) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
t208 = list(moto_2010[((moto_2010['umaban'] >= 9) & (moto_2010['kyori'] == 3600) & ((moto_2010['sibababacd'] == 0)))].index)  # 9以上かつ1000mかつダ
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
# endregion
# 条件のindexをlistに格納
jyo_list = []
jyo_list.extend(
    [t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25,t26,
     t27, t28, t29, t30, t31, t32, t33, t34, t35, t36, t37, t38, t39, t40, t41, t42, t43, t44, t45, t46, t47, t48, t49,t50, t51, t52, t53, t54,
     t55, t56, t57, t58, t59, t60, t61, t62, t63, t64, t65, t66, t67, t68, t69, t70, t71, t72, t73, t74, t75, t76, t77,t78, t79, t80, t81, t82,
     t83, t84, t85, t86, t87, t88, t89, t90, t91, t92, t93, t94, t95, t96, t97, t98, t99, t100, t101, t102, t103, t104,t105, t106, t107, t108,
     t109, t110, t111, t112, t113, t114, t115, t116, t117, t118, t119, t120, t121, t122, t123, t124, t125, t126, t127,t128, t129, t130, t131,
     t132, t133, t134, t135, t136, t137, t138, t139, t140, t141, t142, t143, t144, t145, t146, t147, t148, t149, t150,t151, t152, t153, t154,
     t155, t156, t157, t158, t159, t160, t161, t162, t163, t164, t165, t166, t167, t168, t169, t170, t171, t172, t173,t174, t175, t176, t177,
     t178, t179, t180, t181, t182, t183, t184, t185, t186, t187, t188, t189, t190, t191, t192, t193, t194, t195, t196,t197, t198, t199, t200,
     t201, t202, t203, t204, t205, t206, t207, t208, t209, t210, t211, t212, t213, t214, t215, t216, t217, t218, t219,t220, t221, t222, t223,
     t224, t225, t226, t227, t228, t229, t230, t231, t232, t233, t234, t235, t236, t237, t238, t239, t240, t241, t242,t243, t244, t245, t246,
     t247, t248, t249, t250, t251, t252, t253, t254, t255, t256, t257, t258, t259, t260, t261, t262, t263, t264, t265,t266, t267])  # 全267条件
# 払い戻しなどの集計用に必要な列（単勝/複勝払い戻し，確定順位）だけ抽出
np_moto_2010 = np.array(moto_data_2.loc[:, ['tan_harai', 'fuku_harai', 'kakuteijyuni']])
# 集計データを格納する用のlistを作成　二次元配列（リストのリスト）11年×10場×50メイン
kisyu_box_tanharai = [[] for torima in range(5500)]  # n_uma_race用
kisyu_box_fukuharai = [[] for torima in range(5500)]  # n_uma_race用
kisyu_box_syouritu = [[] for torima in range(5500)]  # n_uma_race用
kisyu_box_fukuritu = [[] for torima in range(5500)]  # n_uma_race用
chokyo_box_tanharai = [[] for torima in range(5500)]  # n_uma_race用
chokyo_box_fukuharai = [[] for torima in range(5500)]  # n_uma_race用
chokyo_box_syouritu = [[] for torima in range(5500)]  # n_uma_race用
chokyo_box_fukuritu = [[] for torima in range(5500)]  # n_uma_race用
banu_box_tanharai = [[] for torima in range(5500)]  # n_uma_race用
banu_box_fukuharai = [[] for torima in range(5500)]  # n_uma_race用
banu_box_syouritu = [[] for torima in range(5500)]  # n_uma_race用
banu_box_fukuritu = [[] for torima in range(5500)]  # n_uma_race用
syu_box_tanharai = [[] for torima in range(5500)]  # n_uma_race用
syu_box_fukuharai = [[] for torima in range(5500)]  # n_uma_race用
syu_box_syouritu = [[] for torima in range(5500)]  # n_uma_race用
syu_box_fukuritu = [[] for torima in range(5500)]  # n_uma_race用
# index番号把握用
kisyu_index = [[] for torima in range(5500)]  # 騎手用　★
chokyo_index = [[] for torima in range(5500)]  # 調教師用　★
banu_index = [[] for torima in range(5500)]  # 馬主用　★
syu_index = [[] for torima in range(5500)]  # 種牡馬用　★
# サンプル数確認用
kisyu_sample = [[] for torima in range(5500)]  # 騎手用　★
chokyo_sample = [[] for torima in range(5500)]  # 調教師用　★
banu_sample = [[] for torima in range(5500)]  # 馬主用　★
syu_sample = [[] for torima in range(5500)]  # 種牡馬用　★
# uma
# uma_box_tanharai=[[] for torima in range(100*len(uma_data))]#n_uma_race用 100000くらい
# uma_box_fukuharai=[[] for torima in range(100*len(uma_data))]#n_uma_race用
# uma_box_syouritu=[[] for torima in range(100*len(uma_data))]#n_uma_race用
# uma_box_fukuritu=[[] for torima in range(100*len(uma_data))]#n_uma_race用
# mainを追加するよう 11year
kisyu_main_11 = [[] for torima in range(11)]  # 騎手用　★
chokyo_main_11 = [[] for torima in range(11)]  # 調教師用　★
banu_main_11 = [[] for torima in range(11)]  # 馬主用　★
syu_main_11 = [[] for torima in range(11)]  # 種牡馬用　★
# count用
count = 0
count_uma = 0
count_main = 0
# nanのnp作成
mat = np.zeros([1, len(jyo_list)])
mat[:, :] = np.nan
# データ作成 11年×10場×50個（メイン）＝5500個
for i in range(11):  # 11年分
    year_hani = 2011 + i  # 2011~2021でデータを作る　2011年までのデータは2012年に使う
    year_hani_low=year_hani-3#2015なら2012
    year_hani_high=year_hani-1#2015なら2014で3年間のデータ
    print(year_hani)
    # 対象年以下を指定
    year_list = list(moto_2010[((year_hani_low <= moto_2010['year']) & (moto_2010['year']<= year_hani_high))].index)#特徴量作成のための元データ
    tokuapply_list = list(moto_2010[(((moto_2010['year'] == year_hani)))].index)#特徴量をapplyする行
    # メイン取得用
    moto_main = moto_2010[((year_hani_low <= moto_2010['year']) & (moto_2010['year']<= year_hani_high))]
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
        for j in range(50):  # 4つのメインに対して50個分データを作成
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
            kisyu_index1 = list(set(kisyu_list) & set(yearbasyo_list))
            chokyo_index1 = list(set(chokyo_list) & set(yearbasyo_list))
            banu_list_index1 = list(set(banu_list) & set(yearbasyo_list))
            syu_index1 = list(set(syu_list) & set(yearbasyo_list))
            # list内包表記 特徴量作成用 mapの代わりになる　https://qiita.com/KTakahiro1729/items/c9cb757473de50652374
            syukei_kisyu = [set(kisyu_index1) & set(i_nakami) for i_nakami in jyo_list]  # 大list=list×267，それぞれのlistの中にindexが格納されている
            syukei_chokyo = [set(chokyo_index1) & set(i_nakami) for i_nakami in jyo_list]
            syukei_banu = [set(banu_list_index1) & set(i_nakami) for i_nakami in jyo_list]
            syukei_syu = [set(syu_index1) & set(i_nakami) for i_nakami in jyo_list]
            # 特徴量を適応する行のindex
            kisyu_indexapp = list(set(kisyu_list) & set(tokuapply_list) & set(basyo_list))
            chokyo_indexapp = list(set(chokyo_list) & set(tokuapply_list) & set(basyo_list))
            banu_list_indexapp = list(set(banu_list) & set(tokuapply_list) & set(basyo_list))
            syu_indexapp = list(set(syu_list) & set(tokuapply_list) & set(basyo_list))
            # list内包表記 特徴量を適応する行 mapの代わりになる　https://qiita.com/KTakahiro1729/items/c9cb757473de50652374
            syukei_kisyuapp = [set(kisyu_indexapp) & set(i_nakami) for i_nakami in jyo_list]  # 大list=list×267，それぞれのlistの中にindexが格納されている
            syukei_chokyoapp = [set(chokyo_indexapp) & set(i_nakami) for i_nakami in jyo_list]
            syukei_banuapp = [set(banu_list_indexapp) & set(i_nakami) for i_nakami in jyo_list]
            syukei_syuapp = [set(syu_indexapp) & set(i_nakami) for i_nakami in jyo_list]
            # 格納
            # 特徴量を適応する行のindexを格納
            kisyu_index[count] = syukei_kisyuapp
            chokyo_index[count] = syukei_chokyoapp
            banu_index[count] = syukei_banuapp
            syu_index[count] = syukei_syuapp
            # 特徴量作成用
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
            # データないものは成績悪めのデータで置き換え？
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
#型変換 setはpandasにできない
henkan_list1 = []
henkan_list2 = []
henkan_list3 = []
henkan_list4 = []
for i in range(len(kisyu_index)):
    henkan_list1.append([list(kisyu_index[i][j]) for j in range(len(kisyu_index[i]))])
for i in range(len(chokyo_index)):
    henkan_list2.append([list(chokyo_index[i][j]) for j in range(len(chokyo_index[i]))])
for i in range(len(banu_index)):
    henkan_list3.append([list(banu_index[i][j]) for j in range(len(banu_index[i]))])
for i in range(len(syu_index)):
    henkan_list4.append([list(syu_index[i][j]) for j in range(len(syu_index[i]))])
# index
indexnum1 = pd.DataFrame(henkan_list1)
indexnum2 = pd.DataFrame(henkan_list2)
indexnum3 = pd.DataFrame(henkan_list3)
indexnum4 = pd.DataFrame(henkan_list4)
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

process_time = time.time() - start
print(process_time)
# endregion