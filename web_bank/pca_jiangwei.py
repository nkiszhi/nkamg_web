"""
将多维数据降维至3，并输出每一种算法的  safe and dangerous csv文件
"""

import pandas as pd
from sklearn.decomposition import PCA

# 将多个特征降维到3维，并输出为csv文件
def PCA_pro(normal, abnormal, algorithm_name):
    # 归一化（已经完成）降维，对正常数据的处理
    pca = PCA(n_components=3)  # 保留n个主成分
    pca_normal = pd.DataFrame(pca.fit_transform(normal.iloc[:, 1:]), columns=['0', '1', '2'], index=normal.index)  # 去掉标签列
    pca_normal['label'] = 0
    pca_normal = pca_normal.reset_index()
    pca_normal.to_csv('./data/' + algorithm_name + '_normal.csv', index=None)

    # 对异常数据的处理
    pca = PCA(n_components=3)  # 保留n个主成分
    pca_abnormal = pd.DataFrame(pca.fit_transform(abnormal.iloc[:, 1:]), columns=['0', '1', '2'],
                              index=abnormal.index)  # 去掉标签列
    pca_abnormal['label'] = 0
    pca_abnormal = pca_abnormal.reset_index()
    pca_abnormal.to_csv('./data/' + algorithm_name + '_abnormal.csv', index=None)


# 读入csv文件，根据预测标签，将1695个数据划分为normal和abnormal
def split_data(df, df_feature, algorithm_name):

    label_name = algorithm_name + '_pred'  # KNN_pred
    new_df = pd.merge(pd.DataFrame(df[label_name]), df_feature, how='outer', left_index=True, right_index=True)
    normal_df = new_df.loc[new_df[label_name] == 0]
    abnormal_df = new_df.loc[new_df[label_name] == 1]
    PCA_pro(normal_df, abnormal_df, algorithm_name)


if __name__ == '__main__':
    df = pd.read_csv('./data/pyod_detection_results.csv')
    df = df.set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    df_feature = pd.read_csv('./data/normalized_feature_1695.csv').set_index(['MERCHANT_ACCT_ID', 'BATCH_TIME'])
    print(type(df_feature.index[0]))
    split_data(df, df_feature, 'KNN')
    split_data(df, df_feature, 'PCA')
    split_data(df, df_feature, 'VAE')
    split_data(df, df_feature, 'LOF')
    split_data(df, df_feature, 'IForest')
    split_data(df, df_feature, 'AutoEncoder')
    split_data(df, df_feature, 'FeatureBagging')
    split_data(df, df_feature, 'ABOD')
    split_data(df, df_feature, 'HBOS')
    split_data(df, df_feature, 'CBLOF')
    split_data(df, df_feature, 'LODA')
    split_data(df, df_feature, 'MCD')






