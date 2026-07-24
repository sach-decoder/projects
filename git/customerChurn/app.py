import pickle
import xgboost as xgb
import pandas as pd
import numpy as np
import math 
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS 

MODEL_PATH = 'churn_model.xgb'
PREPROCESSOR_PATH = 'preprocessor.pkl'

with open(PREPROCESSOR_PATH, 'rb') as f:
    prep = pickle.load(f)
    print("Preprocessor keys:", prep.keys())  # See what's actually in it
    print("Preprocessor contents:", prep)

scaler = prep['scaler']
feature_names = prep['feature_names']
print(feature_names)

model = xgb.Booster()
model.load_model(MODEL_PATH)

def predict_row(data):

    df = pd.DataFrame([data], columns=feature_names)
    df[['balance', 'estimated_salary']] = scaler.transform(df[['balance', 'estimated_salary']])

    array = xgb.DMatrix(df, feature_names=feature_names)
    return model.predict(array)


class Database:

    def db_connect(self):
        DB_NAME="postgres"
        DB_USER="postgres"
        DB_PASS="hello@123"
        DB_HOST="localhost"
        DB_PORT="5432"

        try:
            self.conn = psycopg2.connect(
                database=DB_NAME, 
                user=DB_USER, 
                password=DB_PASS, 
                host=DB_HOST, 
                port=DB_PORT)
            
            print('Database connection succesful')
        except Exception as e :
            print(e)

    def add_enteries_db(self, data):
        cur = self.conn.cursor()
        try:
            print("Inserting data:", data)
            print("Data length:", len(data))
            cur.execute("""
                        INSERT INTO public.customer_churn 
                        (credit_score, country, gender, age, tenure, balance, products_number, credit_card, active_member, estimated_salary, churn, churn_probability)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
                        """, tuple(data))
            self.conn.commit()
            print("Rows affected:", cur.rowcount)
            print("Insert successful!")
            cur.close()
            self.conn.close()

        except Exception as e:
            print("DB INSERT ERROR:", e)
            print("Error type:", type(e))
            raise

# sample = [500, 1, 1, 23, 4, 0.65500, 1, 0, 1, 0.25565, 0.6335] 
database = Database()
# database.db_connect()
# database.add_enteries_db()

# print(predict_row(sample))

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def prediction():
    data = request.get_json()
    print("Received data:", data)
    print("Feature names:", feature_names)

    model_input = data[:len(feature_names)]
    print("Model input:", model_input)
    print("Model input length:", len(model_input))

    extra = data[len(feature_names):]

    try:
        final_value = predict_row(model_input)
        prediction_value = float(final_value.item())

        db_array = list(model_input)
        if len(extra) >= 1:
            db_array.append(extra[0])   # churn label
        db_array.append(prediction_value)  # churn_probability(%)

        database.db_connect()
        database.add_enteries_db(db_array)
        return jsonify({'prediction': prediction_value})

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500