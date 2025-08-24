#乱数のシードを固定
import random
import numpy as np

random.seed(1234)
np.random.seed(1234)

#使用するパッケージ（ライブラリと関数）を定義
#scipy 平均0，分散1に正規化（標準化）関数
import scipy.stats

#標準正規分布の生成用
from numpy.random import randn

#グラフ描画用
import matplotlib.pyplot as plt