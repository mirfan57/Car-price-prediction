from flask import Flask, render_template, request
#import jsonify
#import requests
import pickle
import numpy as np
import sklearn
#from sklearn.preprocessing import StandardScaler


app = Flask(__name__)

model = pickle.load(open('car_prediction_RFmodel.pkl', 'rb'))

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

#scaler = StandardScaler()

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        total_years = int(request.form['total_years'])
        km_driven = float(request.form['km_driven'])
        engine = int(request.form['engine'])
        mileage = float(request.form['mileage'])
        max_power = float(request.form['max_power'])
        torque = float(request.form['torque'])
        seats = float(request.form['seats'])
        fuel_type = request.form['fuel_type']
        if fuel_type == 'Petrol':
            fuel_LPG = 0
            fuel_Diesel = 0
            fuel_Petrol = 1
        elif fuel_type == 'LPG':
            fuel_LPG = 1
            fuel_Diesel = 0
            fuel_Petrol = 0
        elif fuel_type == 'Diesel':
            fuel_LPG = 0
            fuel_Diesel = 1
            fuel_Petrol = 0
        else:
            fuel_LPG = 0
            fuel_Diesel = 0
            fuel_Petrol = 0
        total_years = 2022 - total_years

        seller_type = request.form['seller_type']
        if seller_type == 'Individual':
            seller_type_Individual = 1
            seller_type_Trustmark_Dealer = 0
        elif seller_type == 'Trustmark Dealer':
            seller_type_Individual = 0
            seller_type_Trustmark_Dealer = 1
        else:
            seller_type_Individual = 0
            seller_type_Trustmark_Dealer = 0

        transmission_type = request.form['transmission_type']
        if transmission_type == 'Manual':
            transmission_Manual = 1
        else:
            transmission_Manual = 0

        owner = request.form['owner']
        if owner == 'Second Owner':
            owner_Second_Owner = 1
            owner_Test_Drive_Car = 0
            owner_Third_Owner = 0
            owner_Fourth_and_Above_Owner = 0
        elif owner == 'Third Owner':
            owner_Second_Owner = 0
            owner_Test_Drive_Car = 0
            owner_Third_Owner = 1
            owner_Fourth_and_Above_Owner = 0
        elif owner == 'Test Drive Car':
            owner_Second_Owner = 0
            owner_Test_Drive_Car = 1
            owner_Third_Owner = 0
            owner_Fourth_and_Above_Owner = 0
        elif owner == 'Fourth & Above Owner':
            owner_Second_Owner = 0
            owner_Test_Drive_Car = 0
            owner_Third_Owner = 0
            owner_Fourth_and_Above_Owner = 1
        else:
            owner_Second_Owner = 0
            owner_Test_Drive_Car = 0
            owner_Third_Owner = 0
            owner_Fourth_and_Above_Owner = 0

        prediction = model.predict([[km_driven, mileage, engine, max_power, torque, seats, total_years, fuel_Diesel, fuel_LPG,
                                     fuel_Petrol, seller_type_Individual, seller_type_Trustmark_Dealer, transmission_Manual, 
                                     owner_Fourth_and_Above_Owner, owner_Second_Owner, owner_Test_Drive_Car, owner_Third_Owner]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index.html', prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html', prediction_text="You Can Sell The Car at Rs {}".format(output))

    else:
        return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True, port=8002)
