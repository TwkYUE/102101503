import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, TimeSeriesSplit
from sklearn.preprocessing import LabelEncoder, StandardScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Bidirectional
from keras.utils import to_categorical
from keras.optimizers import Adam
from hmmlearn import hmm
from sklearn.base import BaseEstimator
from keras.callbacks import ModelCheckpoint  # 导入ModelCheckpoint
# 读取特征数据和标签数据
features = np.load('feature.npy')
labels = np.load('label.npy')

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

print(X_train.shape)
print(X_test.shape)

# 使用HMM模型对观测序列进行训练，并得到隐藏状态序列
hmm_model = hmm.GaussianHMM(n_components=1)
hmm_model.fit(X_train)
hidden_states_train = hmm_model.predict(X_train)
hidden_states_test = hmm_model.predict(X_test)

# 将隐藏状态序列作为输入特征，与原始特征数据进行合并
X_train_combined = np.concatenate((X_train, hidden_states_train.reshape(-1, 1)), axis=1)
X_test_combined = np.concatenate((X_test, hidden_states_test.reshape(-1, 1)), axis=1)

# 对标签进行编码
label_encoder = LabelEncoder()
y_train_encoded = label_encoder.fit_transform(y_train)
y_test_encoded = label_encoder.transform(y_test)
num_classes = len(label_encoder.classes_)

# 预处理
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train_combined)
X_test_scaled = scaler.transform(X_test_combined)

# 将标签转换为one-hot编码
y_train_onehot = to_categorical(y_train_encoded, num_classes)
y_test_onehot = to_categorical(y_test_encoded, num_classes)


# 创建一个ModelCheckpoint回调函数，用于保存模型权重
checkpoint = ModelCheckpoint('model_weights_epoch_{epoch:02d}.h5',  # 保存每个训练批次结束后的模型权重
                             save_best_only=False,  # 保存每个训练批次的权重
                             save_weights_only=True,  # 只保存权重而不保存整个模型
                             period=4)  # 每隔一个epoch保存一次

# 定义一个继承自BaseEstimator的模型类
class MyModel(BaseEstimator):
    def __init__(self, hidden_units=1024):
        self.hidden_units = hidden_units
        self.model = self.create_model(hidden_units=self.hidden_units)
    
    def create_model(self, hidden_units):
        model = Sequential()
        model.add(Bidirectional(LSTM(hidden_units, return_sequences=True), input_shape=(X_train_scaled.shape[1], 1)))
        model.add(Bidirectional(LSTM(hidden_units)))
        model.add(Dense(num_classes, activation='softmax'))
        optimizer = Adam(learning_rate=0.0001)
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        return model
    
    def fit(self, X, y):
        self.model.fit(X, y, epochs=100, batch_size=32, validation_data=(X_test_scaled[:, :, np.newaxis], y_test_onehot))
    
    def predict(self, X):
        return self.model.predict(X)
    
    def score(self, X, y):
        _, accuracy = self.model.evaluate(X, y)
        return accuracy

# 创建时间序列交叉验证
tscv = TimeSeriesSplit(n_splits=5)

# 创建网格搜索对象
model = MyModel()
param_grid = {'hidden_units': [1024, 2048]}
grid = GridSearchCV(estimator=model, param_grid=param_grid, cv=tscv)

# 执行网格搜索
grid_result = grid.fit(X_train_scaled[:, :, np.newaxis], y_train_onehot)

# 输出最佳结果和参数组合
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))

# 使用最佳参数训练模型
best_params = grid_result.best_params_
model = MyModel(hidden_units=best_params['hidden_units'])
model.fit(X_train_scaled[:, :, np.newaxis], y_train_onehot)

# 在测试集上评估模型
accuracy = model.score(X_test_scaled[:, :, np.newaxis], y_test_onehot)
print('Test accuracy:', accuracy)
