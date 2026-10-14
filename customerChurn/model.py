import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
import math
import pickle
from imblearn.over_sampling import SMOTE
import xgboost as xgb
from sklearn.metrics import accuracy_score, classification_report 
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split 

csv = pd.read_csv('Bank Customer Churn Prediction.csv')
df = pd.DataFrame(csv)

df_new = df.drop('customer_id', axis=1)

def pretrain_cleaning():
    df['gender'] = df['gender'].replace({'Male': 1, 'Female': 0})
    df['country'] = df['country'].replace({'France': 1, 'Germany': 0, 'Spain': 2})
    global df_new
    df_new = df.drop('customer_id', axis=1)

def normalization():
    scaler = MinMaxScaler()
    columns = ['balance', 'estimated_salary']
    df_new[columns] = scaler.fit_transform(df_new[columns])
    return scaler 

class Preprocessing:
    def split_trainset(self):
        X = df_new.drop('churn', axis=1)
        y = df_new['churn']

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    def class_imbalance(self):
        smote = SMOTE(random_state=42)
        self.X_train_smote, self.y_train_smote = smote.fit_resample(self.X_train, self.y_train)

        self.X_train_smote['gender'] = self.X_train_smote['gender'].astype('int64')
        self.X_train_smote['country']= self.X_train_smote['country'].astype('int64')

        self.X_test['gender'] = self.X_test['gender'].astype('int64')
        self.X_test['country']= self.X_test['country'].astype('int64')

    def convert_to_matrix(self):
        self.xgb_train = xgb.DMatrix(self.X_train_smote, self.y_train_smote)
        self.xgb_test = xgb.DMatrix(self.X_test, self.y_test)

        return self.xgb_train, self.xgb_test, self.y_test

class ModelCreationAndTraining:
    def __init__(self):
        self.evals_result = {}
        self.n = 127

    def model_params(self):
        self.params = {
            'objective': 'binary:logistic', 
            'eval_metric': ['logloss', 'auc', 'rmse'],
            'max_depth': 5, 
            'learning_rate': 0.2, 
        }

    def model_train(self, xgb_train, xgb_test):
        model = xgb.train(
            params=self.params, 
            dtrain=xgb_train, 
            num_boost_round=self.n, 
            evals=[(xgb_train, 'train'), (xgb_test, 'test')], 
            evals_result=self.evals_result, 
            verbose_eval=True 
        )
        model.save_model('churn_model.xgb')
        return model, xgb_test


pretrain_cleaning()
scaler = normalization()
preprocess = Preprocessing()
preprocess.split_trainset()
preprocess.class_imbalance()
xgb_train, xgb_test, dummy4 = preprocess.convert_to_matrix()

model_create = ModelCreationAndTraining()
model_create.model_params()
model, xgb_test = model_create.model_train(xgb_train, xgb_test)

model = xgb.Booster()
model.load_model('churn_model.xgb')

df_new['churn_probability(%)'] = 0 

with open('preprocessor.pkl', 'wb') as f:
    pickle.dump({'scaler': scaler, 'feature_names': model.feature_names}, f)


def model_predict(data):
    transformed_data = np.asarray(data).reshape(1, -1)

    array = xgb.DMatrix(transformed_data, feature_names=model.feature_names)
    test_pred = model.predict(array)
    print('**************')
    print(test_pred)
    print('**************')

    return test_pred

def add_predictions_db():
    new_df = df_new
    pred_features = new_df[model.feature_names].astype('float64').astype('int64')
    all_rows_dmatrix = xgb.DMatrix(pred_features, feature_names=model.feature_names)
    new_df['churn_probability(%)'] = model.predict(all_rows_dmatrix)

    new_df['churn_probability(%)'] = new_df['churn_probability(%)']*100
    return new_df

def save_db_csv(df):
    df.to_csv('customer_churn_db.csv', index=False)

final_db = add_predictions_db()
save_db_csv(final_db)
# test_data = [500, 1, 1, 23, 4, 0.65500, 1, 0, 1, 0.25565]

# prediction = model_predict(test_data)
# print(f"{math.ceil(prediction[0]*100)}%")


