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
    
    def fit(self, X, y, callbacks=None):  # 添加callbacks参数
        self.model.fit(X, y, epochs=200, batch_size=32, validation_data=(X_test_scaled[:, :, np.newaxis], y_test_onehot), callbacks=callbacks)  # 将callbacks参数传递给fit方法
    
    def predict(self, X):
        return self.model.predict(X)
    
    def score(self, X, y):
        _, accuracy = self.model.evaluate(X, y)
        return accuracy
        
