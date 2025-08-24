# 単勝モデル　オリジナデータ
# ⓪ライブラリの準備
import pandas as pd
import numpy as np

# DBとのやり取りライブラリ
import psycopg2
from sqlalchemy import create_engine

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
sql7 = 'SELECT * FROM public."0Input_Data_Uma" ORDER BY index ASC;'  # 教師データ
sql8 = 'SELECT * FROM public."0Input_Data_Race" ORDER BY index ASC;'  # 教師データ
n_input_u = pd.read_sql(sql7, conn)  # umarace詳細すべて取り出す
n_input_r = pd.read_sql(sql8, conn)  # umarace詳細すべて取り出す

# DB閉じる
cursor.close()  # データベースの操作を終了する
conn.commit()  # 変更をデータベースに保存
conn.close()  # データベースを閉じる

# データ加工
n_in0 = pd.concat([n_input_u, n_input_r.loc[:,'0trackcd']], axis=1)  # 横方向の連結
del n_input_u,n_input_r
n_in0['raceID'] = n_in0['0year'] + n_in0['0monthday'] + n_in0['0jyocd'] + n_in0['0kaiji']+n_in0['0nichiji'] \
                  +n_in0['0racenum'] # ID
# 初期入力
year_list=[2013,2014,2015,2016,2017,2018,2019,2020]
month_list=[1,4,7,10]
babatra_list=[0,1] # 芝orダート

for year_v in range(len(year_list)):
    year=year_list[year_v]
    for month_v in range(len(month_list)):
        month = month_list[month_v]
        for babatra_v in range(len(babatra_list)):
            babatra = babatra_list[babatra_v] # 0：芝,1：ダート,芝10-22,ダート23-26

            # 処理開始
            if month==1:
                year_low=year-1
                year_high=year-1
                month_low=month
                month_high=12
            else:
                year_low=year-1
                year_high=year
                month_low=month
                month_high=month-1

            if babatra==0:
                babatra_low=10
                babatra_high=22
            else:
                babatra_low=23
                babatra_high=26
            # データフィルタリング
            n_in=n_in0.copy()
            n_in['0monthday']=n_in['0monthday'].str[0:2]
            n_in['0monthday'] = n_in['0year']+n_in['0monthday']
            n_in['0monthday'] = pd.to_numeric(n_in["0monthday"], errors='coerce')
            # 0をつける処理
            if month_low == 1 or month_low == 4 or month_low == 7:
                month_low='0'+str(month_low)
            if month_low == '04' or month_low == '07' or month_low == 10:
                month_high='0'+str(month_high)
            n_in = n_in[((int(str(year_low)+str(month_low)) <= n_in['0monthday'])
                         & (n_in['0monthday'] <= int(str(year_high)+str(month_high))))]
            n_in['0jyocd'] = pd.to_numeric(n_in["0jyocd"], errors='coerce')
            n_in = n_in[((1 <= n_in['0jyocd']) & (n_in['0jyocd'] <= 10))] # 中央
            n_in['0trackcd'] = pd.to_numeric(n_in["0trackcd"], errors='coerce')
            n_in = n_in[((babatra_low <= n_in['0trackcd']) & (n_in['0trackcd'] <= babatra_high))]
            n_in = n_in.reset_index(drop=True)  # index振りなおす
            n_in['0year']=n_in['0year'].astype(str)
            n_in['0jyocd']=n_in['0jyocd'].astype(str)
            n_in['0trackcd']=n_in['0trackcd'].astype(str)
            n_in=n_in.loc[:, ['raceID', '0kakuteijyuni', '0kettonum', '0kisyuryakusyo']]  # ベイズモデリングに必要なデータだけ取り出し
            n_in['0kakuteijyuni'] = n_in['0kakuteijyuni'].astype(int)
            df_new = n_in.rename(columns={'raceID': 'RaceID', '0kakuteijyuni': 'OoA', '0kettonum': 'horseID', '0kisyuryakusyo': 'jockeyID'})
            # 中止の馬は削除する，中止の場合の強さははかれないため
            df_new = df_new[df_new['OoA'] != 0]
            # 同着の馬は順位を1ずらし，順位を昇順にする,データ振りなおし
            df0 = pd.DataFrame(index=[], columns=['RaceID', 'OoA', 'horseID', 'jockeyID'])
            i = 0
            for raceID, sdf in df_new.groupby('RaceID'):
                if len(sdf) >= 5: # 5頭以上なら
                    i=i+1
                    sdf = sdf.sort_values('OoA') # 着順ソート
                    if any(sdf.duplicated(subset='OoA')): #重複あれば 20476行目重複
                        sdf.loc[:, 'OoA'] = np.arange(1, len(sdf) + 1)
                    sdf['RaceID'] = i
                    df0 = df0.append(sdf, ignore_index=True)
            # 血統番号を振りなおす→ここで血統番号と騎手IDの対応表作っておく
            df0_hozon=df0.loc[:,['horseID','jockeyID']]
            from sklearn import preprocessing
            le = preprocessing.LabelEncoder() # LabelEncoder()は，文字列や数値で表されたラベルを，0~(ラベル種類数-1)までの数値に変換してくれるもの
            le.fit(df0['horseID'])
            df0['horseID'] = le.transform(df0['horseID'])
            df0['horseID'] =df0['horseID'] +1
            le.fit(df0['jockeyID'])
            df0['jockeyID'] = le.transform(df0['jockeyID'])
            df0['jockeyID'] =df0['jockeyID'] +1

            #対応表保存
            df0_hozon = pd.concat([df0_hozon, df0.loc[:,['horseID','jockeyID']]], axis=1)  # 横方向の連結
            # indexを1はじまりにする
            df0.index = np.arange(1, len(df0)+1)

            # CSVで出力
            import os  # フォルダ作成用
            fold_name='stan'
            fold_name = 'moto'
            fold_name1 = 'hikaku'
            # 日にちでフォルダ作成
            new_path = 'data_forR\stan\{}'.format(fold_name)
            new_path1 = 'data_forR\stan\{}'.format(fold_name1)
            stanlabel = 'stan'+str(int(year))+'-'+str(int(month))+'-'+str(int(babatra))
            complabel = 'comp'+str(int(year))+'-'+str(int(month))+'-'+str(int(year_low))+'-'+str(int(month_low))+'-'\
                        +str(int(year_high))+'-'+str(int(month_high))+'-'+str(int(babatra))
            if not os.path.exists(new_path):  # ディレクトリがなかったら
                os.mkdir(new_path)  # 作成したいフォルダ名を作成
            if not os.path.exists(new_path1):  # ディレクトリがなかったら
                os.mkdir(new_path1)  # 作成したいフォルダ名を作成
            # csv出力
            csv_name_stan = new_path + '\{}.csv'.format(stanlabel)
            csv_name_comp = new_path1 + '\{}.csv'.format(complabel)
            df0.to_csv(csv_name_stan, encoding='utf-8', index=False)  # utf-8-sigボムあり，utf-8-なし
            df0_hozon.to_csv(csv_name_comp, encoding='utf-8', index=False)  # utf-8-sigボムあり，utf-8-なし

# --------------------------------------------------------------------------------
# pandas元データ
df5 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5])
df6 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6])
df7 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7])
df8 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8])
df9 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8, 9])
df10 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
df11 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
df12 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
df13 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
df14 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14])
df15 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
df16 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16])
df17 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17])
df18 = pd.DataFrame(index=[], columns=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18])

# レースを同じ頭数のレースごとにまとめる
for raceID, sdf in n_in.groupby('raceID'):
    sdf = sdf[sdf['0kakuteijyuni'] != 0]  # 着順0の行以外を抽出(競走中止を削除)
    sdf = sdf.sort_values('0kakuteijyuni')
    sdf = sdf.loc[:, ['0kettonum']] .T # ベイズモデリングに必要なデータだけ取り出し
    sh = sdf.shape #列番号リセット
    sdf.columns = range(1,sh[1]+1)
    if len(sdf.columns) == 5:
        df5 = df5.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 6:
        df6 = df6.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 7:
        df7 = df7.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 8:
        df8 = df8.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 9:
        df9 = df9.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 10:
        df10 = df10.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 11:
        df11 = df11.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 12:
        df12 = df12.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 13:
        df13 = df13.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 14:
        df14 = df14.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 15:
        df15 = df15.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 16:
        df16 = df16.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 17:
        df17 = df17.append(sdf, ignore_index=True)
    elif len(sdf.columns) == 18:
        df18 = df18.append(sdf, ignore_index=True)

r7=len(df7)
r8=len(df8)
r9=len(df9)
r10=len(df10)
r11=len(df11)
r12=len(df12)
r13=len(df13)
r14=len(df14)
r15=len(df15)
r16=len(df16)
r17=len(df17)
r18=len(df18)
race_num = r7 + r8 + r9 + r10 + r11 + r12 + r13 + r14 + r15 + r16 + r17 + r18

# index振りなおせる
df7.index = np.arange(1, len(df7)+1)
df8.index = np.arange(1, len(df8)+1)
df9.index = np.arange(1, len(df9)+1)
df10.index = np.arange(1, len(df10)+1)
df11.index = np.arange(1, len(df11)+1)
df12.index = np.arange(1, len(df12)+1)
df13.index = np.arange(1, len(df13)+1)
df14.index = np.arange(1, len(df14)+1)
df15.index = np.arange(1, len(df15)+1)
df16.index = np.arange(1, len(df16)+1)
df17.index = np.arange(1, len(df17)+1)
df18.index = np.arange(1, len(df18)+1)

# R用にCSVで出力
import os  # フォルダ作成用
matome_df=[df7,df8,df9,df10,df11,df12,df13,df14,df15,df16,df17,df18]
input_kensakuDAY='test'
# 日にちでフォルダ作成
new_path = 'data_forR\{}'.format(input_kensakuDAY)

for i in range(len(matome_df)):
    Rdata=matome_df[i]
    kensakuID = str(i+7)

    if not os.path.exists(new_path):  # ディレクトリがなかったら
        os.mkdir(new_path)  # 作成したいフォルダ名を作成
    # csv出力
    hozonsaki = new_path + '\{}.csv'.format(kensakuID)
    Rdata.to_csv(hozonsaki, encoding='utf-8', index=False) # utf-8-sigボムあり，utf-8-なし




###############################################################################################
# 以下pystan用のコード，pystanはすこしお休みでRstanに託す
###############################################################################################

#TODO これすれば解決
LW = np.array(LW, dtype=np.int32)

# ここからstan用
# import
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pystan
import pandas as pd
from scipy.stats import mstats

# stan model
stan_model = '''
    data {
      int N;      // num of horses 
      int G;  // num of races
      int<lower=1, upper=N> LW7[G,7];  // order of arrival of each race 
    }

    parameters {
      ordered[7] performance7[G];
      vector[N] mu;
      real<lower=0> s_mu;
      vector<lower=0>[N] s_pf;
    }

    model {
      for (g in 1:G)
        for (i in 1:7)
          performance7[g,i] ~ normal(mu[LW7[g,i]], s_pf[LW7[g,i]]);

      mu ~ normal(0, s_mu);
      s_pf ~ gamma(10, 10);
    }
'''

# compile
sm = pystan.StanModel(model_code=stan_model)
# data(dictionary)
stan_data = {'N': n_in.shape[0], 'G': r7, 'LW7': df7}

# fitting
fit = sm.sampling(data=stan_data, iter=2000, warmup=500, chains=3, seed=1992)



'''
int N
⇒全馬の数(7~18頭での全て),推定したい馬すべてだから
int<lower=1, upper=N> LW7[G[7],7];  // order of arrival of each race 
⇒7頭用のレース配列
LWは「試合数(G)」×「試合当たりのプレイヤー数」の二次元配列
int G[18]
⇒この人は18レース分しか解析してない？ちがうか
与えるデータは14種類
7頭だて～18頭だてまで別の配列を準備する
'''

# stan model
stan_model = '''
    data {
      int N;      // num of horses 
      int G[18];  // num of races
      int<lower=1, upper=N> LW7[G[7],7];  // order of arrival of each race 
      int<lower=1, upper=N> LW8[G[8],8];
      int<lower=1, upper=N> LW9[G[9],9];
      int<lower=1, upper=N> LW10[G[10],10];
      int<lower=1, upper=N> LW11[G[11],11];
      int<lower=1, upper=N> LW12[G[12],12];
      int<lower=1, upper=N> LW13[G[13],13];
      int<lower=1, upper=N> LW14[G[14],14];
      int<lower=1, upper=N> LW15[G[15],15];
      int<lower=1, upper=N> LW16[G[16],16];
      int<lower=1, upper=N> LW17[G[17],17];
      int<lower=1, upper=N> LW18[G[18],18];
    }
    
    parameters {
      ordered[7] performance7[G[7]];
      ordered[8] performance8[G[8]];
      ordered[9] performance9[G[9]];
      ordered[10] performance10[G[10]];
      ordered[11] performance11[G[11]];
      ordered[12] performance12[G[12]];
      ordered[13] performance13[G[13]];
      ordered[14] performance14[G[14]];
      ordered[15] performance15[G[15]];
      ordered[16] performance16[G[16]];
      ordered[17] performance17[G[17]];
      ordered[18] performance18[G[18]];
    
      vector[N] mu;
      real<lower=0> s_mu;
      vector<lower=0>[N] s_pf;
    }
    
    model {
      for (r in 2:18){
        for (g in 1:G[r]){
          for (i in 1:r){
            if (r==7)
              performance7[g,i] ~ normal(mu[LW7[g,i]], s_pf[LW7[g,i]]);
            else if (r==8)
              performance8[g,i] ~ normal(mu[LW8[g,i]], s_pf[LW8[g,i]]);
            else if (r==9)
              performance9[g,i] ~ normal(mu[LW9[g,i]], s_pf[LW9[g,i]]);
            else if (r==10)
              performance10[g,i] ~ normal(mu[LW10[g,i]], s_pf[LW10[g,i]]);
            else if (r==11)
              performance11[g,i] ~ normal(mu[LW11[g,i]], s_pf[LW11[g,i]]);
            else if (r==12)
              performance12[g,i] ~ normal(mu[LW12[g,i]], s_pf[LW12[g,i]]);
            else if (r==13)
              performance13[g,i] ~ normal(mu[LW13[g,i]], s_pf[LW13[g,i]]);
            else if (r==14)
              performance14[g,i] ~ normal(mu[LW14[g,i]], s_pf[LW14[g,i]]);
            else if (r==15)
              performance15[g,i] ~ normal(mu[LW15[g,i]], s_pf[LW15[g,i]]);
            else if (r==16)
              performance16[g,i] ~ normal(mu[LW16[g,i]], s_pf[LW16[g,i]]);
            else if (r==17)
              performance17[g,i] ~ normal(mu[LW17[g,i]], s_pf[LW17[g,i]]);
            else if (r==18)
              performance18[g,i] ~ normal(mu[LW18[g,i]], s_pf[LW18[g,i]]);
          }
        }
      }
    
      mu ~ normal(0, s_mu);
      s_pf ~ gamma(10, 10);
}
'''

# compile
sm = pystan.StanModel(model_code=stan_model)
# data(dictionary)
stan_data = {'N':n_in.shape[0], 'G[18]':race_num, 'LW7':df7, 'G[7]':r7, 'LW8':df8, 'G[8]':r8,'LW9':df9, 'G[9]':r9,'LW10':df10, 'G[10]':r10,
             'LW11':df11, 'G[11]':r11,'LW12':df12, 'G[12]':r12,'LW13':df13, 'G[13]':r13,'LW14':df14, 'G[14]':r14,'LW15':df15, 'G[15]':r15,
             'LW16':df16, 'G[16]':r16,'LW17':df17, 'G[17]':r17,'LW18':df18, 'G[18]':r18}

# fitting
fit = sm.sampling(data=stan_data, iter=2000, warmup=500, chains=3, seed=1992)

# TODO df7.rows = range(1, len(df7) + 1)

# import
import numpy as np
import matplotlib.pyplot as plt
import seaborn
import pystan
import pandas as pd
from scipy.stats import mstats

# make data
N = 200
K = 4

def get_data():
    a0 = 350.
    b0 = 20.
    s_a = 40.
    s_b = 5.
    s_Y = 30.

    a = np.random.normal(loc=a0, scale=s_a, size=(K,))
    b = np.random.normal(loc=b0, scale=s_b, size=(K,))

    KID = []
    X = []
    Y = []

    for n in range(N):
        kid = np.random.randint(0, K, 1)
        KID.append(int(kid))

        x = np.random.randint(22, 45, 1)
        X.append(x)

        Y.append(np.random.normal(loc=a[kid] + b[kid] * (x - 22), scale=s_Y))

    return (np.array(X).reshape(N, 1).astype(np.float32),
            np.array(Y).reshape(N, 1),
            np.array(KID).reshape(N, 1).astype(np.int32))

# data visualization
X_data, Y_data, KID_data = get_data()
plt.scatter(X_data, Y_data, c=KID_data, cmap='tab10')
plt.show()

# data frame
df = pd.DataFrame(np.hstack([X_data, Y_data, KID_data]), columns=['age', 'salary', 'KID'])

# stan model
stan_model = """
  data {
    int N;
    real X[N];
    real Y[N];
    int N_s;
    real X_s[N_s];
  }
  parameters {
    real a;
    real b;
    real<lower=0> sigma; 
  }
  model{
    for (n in 1:N){
      Y[n] ~ normal(a + b * (X[n] - 22), sigma);
    }
  }
  generated quantities {
    real Y_s[N_s];
    for (n in 1:N_s){
      Y_s[n] = normal_rng(a + b * (X_s[n] - 22), sigma);
    }
  }
"""
# compile
sm = pystan.StanModel(model_code=stan_model)
# data(dictionary)
X_s = np.arange(22, 60, 1) # 年齢を1歳ずつ加算している配列
N_s = X_s.shape[0] # 配列の大きさ
stan_data = {"N":df.shape[0], "X":df["age"], "Y":df["salary"], "N_s":N_s, "X_s":X_s}
# fitting
fit = sm.sampling(data=stan_data, iter=2000, warmup=500, chains=3, seed=1992)
# analysis
ms_a = fit.extract("a")["a"]
plt.hist(ms_a)
# bayse 95%
Y_p = fit.extract("Y_s")["Y_s"]
low_y, high_y = mstats.mquantiles(Y_p, [0.025, 0.975], axis=0)

plt.scatter(df["age"], df["salary"])
plt.fill_between(X_s, low_y, high_y, alpha=0.3, color="gray")
a_ = 319.61
b_ = 15.56
x_ = np.arange(22, 60, 1)
y_ = a_ + b_ * (x_ - 22)
plt.plot(x_, y_, c='r')



#####
cols = [
    'tourney_id', # Id of Tournament
    'tourney_name', # Name of the Tournament
    'surface', # Surface of the Court (Hard, Clay, Grass)
    'draw_size', # Number of people in the tournament
    'tourney_level', # Level of the tournament (A=ATP Tour, D=Davis Cup, G=Grand Slam, M=Masters)
    'tourney_date', # Start date of tournament
    'match_num', # Match number
    'winner_id', # Id of winner
    'winner_seed', # Seed of winner
    'winner_entry', # How the winner entered the tournament
    'winner_name', # Name of winner
    'winner_hand', # Dominant hand of winner (L=Left, R=Right, U=Unknown?)
    'winner_ht', # Height in cm of winner
    'winner_ioc', # Country of winner
    'winner_age', # Age of winner
    'winner_rank', # Rank of winner
    'winner_rank_points', # Rank points of winner
    'loser_id',
    'loser_seed',
    'loser_entry',
    'loser_name',
    'loser_hand',
    'loser_ht',
    'loser_ioc',
    'loser_age',
    'loser_rank',
    'loser_rank_points',
    'score', # Score
    'best_of', # Best of X number of sets
    'round', # Round
    'minutes', # Match length in minutes
    'w_ace', # Number of aces for winner
    'w_df', # Number of double faults for winner
    'w_svpt', # Number of service points played by winner
    'w_1stIn', # Number of first serves in for winner
    'w_1stWon', # Number of first serve points won for winner
    'w_2ndWon', # Number of second serve points won for winner
    'w_SvGms', # Number of service games played by winner
    'w_bpSaved', # Number of break points saved by winner
    'w_bpFaced', # Number of break points faced by winner
    'l_ace',
    'l_df',
    'l_svpt',
    'l_1stIn',
    'l_1stWon',
    'l_2ndWon',
    'l_SvGms',
    'l_bpSaved',
    'l_bpFaced'
]
df_matches = pd.concat([
    pd.read_csv('./atp_matches_2000.csv', usecols=cols),
    pd.read_csv('./atp_matches_2001.csv', usecols=cols),
    pd.read_csv('./atp_matches_2002.csv', usecols=cols),
    pd.read_csv('./atp_matches_2003.csv', usecols=cols),
    pd.read_csv('./atp_matches_2004.csv', usecols=cols),
    pd.read_csv('./atp_matches_2005.csv', usecols=cols),
    pd.read_csv('./atp_matches_2006.csv', usecols=cols),
    pd.read_csv('./atp_matches_2007.csv', usecols=cols),
    pd.read_csv('./atp_matches_2008.csv', usecols=cols),
    pd.read_csv('./atp_matches_2009.csv', usecols=cols),
    pd.read_csv('./atp_matches_2010.csv', usecols=cols),
    pd.read_csv('./atp_matches_2011.csv', usecols=cols),
    pd.read_csv('./atp_matches_2012.csv', usecols=cols),
    pd.read_csv('./atp_matches_2013.csv', usecols=cols),
    pd.read_csv('./atp_matches_2014.csv', usecols=cols),
    pd.read_csv('./atp_matches_2015.csv', usecols=cols),
    pd.read_csv('./atp_matches_2016.csv', usecols=cols),
    pd.read_csv('./atp_matches_2017.csv', usecols=cols),
])


df_matches = df_matches.dropna(subset=['tourney_date'])
df_matches['year'] = df_matches['tourney_date'].apply(lambda x: int(str(x)[0:4]))
display(df_matches.head())
print(len(df_matches))

arr_target_player = np.array([
    'Roger Federer',
    'Rafael Nadal',
    'Novak Djokovic',
    'Andy Murray',
    'Stanislas Wawrinka',
    'Juan Martin Del Potro',
    'Milos Raonic',
    'Kei Nishikori',
    'Gael Monfils',
    'Tomas Berdych',
    'Jo Wilfried Tsonga',
    'David Ferrer',
    'Richard Gasquet',
    'Marin Cilic',
    'Grigor Dimitrov',
    'Dominic Thiem',
    'Nick Kyrgios',
    'Alexander Zverev'
])

df_tmp = df_matches[
    (df_matches['year'] >= 2015) &
    (df_matches['winner_name'].isin(arr_target_player)) &
    (df_matches['loser_name'].isin(arr_target_player))
]

arr_cnt = []
arr_rate = []
for player in arr_target_player:
    cnt_win = len(df_tmp[df_tmp['winner_name'] == player])
    cnt_lose = len(df_tmp[df_tmp['loser_name'] == player])
    arr_cnt.append(cnt_win+cnt_lose)
    arr_rate.append(cnt_win/(cnt_win+cnt_lose))

fig, axs = plt.subplots(ncols=2, figsize=(15, 5))

axs[0].bar(x=arr_target_player, height=arr_cnt, color='b', alpha=0.5)
axs[0].set(xlabel='player', ylabel='cnt')
for tick in axs[0].get_xticklabels():
    tick.set_rotation(75)

axs[1].bar(x=arr_target_player, height=arr_rate, color='r', alpha=0.5)
axs[1].set(xlabel='player', ylabel='rate')
for tick in axs[1].get_xticklabels():
    tick.set_rotation(75)

plt.show()

dic_target_player = {}
for player in arr_target_player:
    if player not in dic_target_player:
        dic_target_player[player] = len(dic_target_player)+1

LW = []
for player_a in arr_target_player:
    for player_b in arr_target_player:
        df_tmp = df_matches[
            (df_matches['year'] >= 2015) &
            (df_matches['winner_name'] == player_a) &
            (df_matches['loser_name'] == player_b)
        ]

        for _ in range(len(df_tmp)):
            LW.append([dic_target_player[player_b], dic_target_player[player_a]])

        df_tmp = df_matches[
            (df_matches['year'] >= 2015) &
            (df_matches['winner_name'] == player_b) &
            (df_matches['loser_name'] == player_a)
        ]

        for _ in range(len(df_tmp)):
            LW.append([dic_target_player[player_a], dic_target_player[player_b]])

LW = np.array(LW, dtype=np.int32)

model = """
    data {
        int N;
        int G;
        int<lower=1, upper=N> LW[G, 2];
    }
    parameters {
        ordered[2] performance[G];
        vector<lower=0>[N] mu;
        real<lower=0> s_mu;
        vector<lower=0>[N] s_pf;
    }
    model {
        for (g in 1:G)
            for (i in 1:2)
                performance[g, i] ~ normal(mu[LW[g, i]], s_pf[LW[g, i]]);
        mu ~ normal(0, s_mu);
        s_pf ~ gamma(10, 10);
    }
"""

fit1 = pystan.stan(model_code=model, data={'N': len(dic_target_player), 'G': len(LW), 'LW': LW}, iter=1000, chains=4, n_jobs=1)

# compile
sm = pystan.StanModel(model_code=model)
# data(dictionary)
data={'N': len(dic_target_player), 'G': len(LW), 'LW': LW}
# fitting
fit = sm.sampling(data=data, iter=1000, chains=4)