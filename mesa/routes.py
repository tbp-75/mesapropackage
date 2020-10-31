
from flask import render_template, jsonify, request, flash, redirect, url_for
from mesa.forms import PredictionForm
import pandas as pd
import numpy as np
import json

from mesa import app
from mesa.models import dataconnector

# Initialize data connector to proucts.csv
products = dataconnector()

# ---ML Model specific imports
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, recall_score
from sklearn.preprocessing import StandardScaler
# ---

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/restapis")
def restapis():
    return render_template('restapis.html', title='REST APIs')

# API CALLS


@app.route("/api/Getproducts", methods=['POST'])
def getproducts():
    # Load data
    catalog = products.read_data()

    # Parse to json
    products_json = catalog.to_json(orient='records')
    parsed = json.loads(products_json)

    return jsonify({'products': parsed})


@app.route('/api/Addproducts', methods=['POST'])
def addproduct():
    # Input from api call
    new_product = {
        'name': request.json['name'],
        'price per gm': request.json['price per gm'],
        'quantity': request.json['quantity']
    }
    # Convert new product to DataFrame
    np = pd.DataFrame(new_product, index=[0])

    # Call append data connector function
    products.append_data(np)

    return jsonify({'message': 'Product added sucessfully', 'products': new_product})


@app.route('/api/Editproducts', methods=['POST'])
def editProduct():
    # Input from api call
    edit_product = {
        'name': request.json['name'],
        'price per gm': request.json['price per gm'],
        'quantity': request.json['quantity']
    }
    # Convert product to DataFrame
    ep = pd.DataFrame(edit_product, index=[0])

    # Call edit data connector function
    products.edit_data(ep)

    return jsonify({'message': 'Product updated successfully', 'products': edit_product})


@app.route('/api/Deleteproducts', methods=['POST'])
def deleteProduct():
    # Input from api call
    product_name_to_delete = {
        'name': request.json['name']
    }

    # Convert product to DataFrame
    dp = pd.DataFrame(product_name_to_delete, index=[0])

    # Call delete data connector function
    products.delete_data(dp)

    return jsonify({'message': 'Product removed successfully', 'products': product_name_to_delete})

# ======================= ML Diabetes Model===================================

@app.route("/ML/predictdiabetes", methods = ['GET','POST'])
def predictdiabetes():
    form = PredictionForm()
    
    # Verify if form contains any data
    data =  [x for x in form.data.values()][:8]
    notvalid = any(element is None for element in data)
        
    
    if notvalid == True:        
        return render_template('predictdiabetes.html',
                                title='ML Diabetes', form = form)
      
    else:
        # flash(data, 'success')

        # Open ML model and scaler
        model = pickle.load(open('mesa/ml_models/diabetes.pkl','rb'))
        scaler = pickle.load(open('mesa/ml_models/scaler.pkl','rb'))

        # Collect values from form
        # prediction_values = [x for x in form.data.values()][:8]  
        prediction_values = data      

        
        # Scaled values before sending to model        
        prediction_values_scaled = scaler.transform([prediction_values])
        
        # Make prediction
        prediction = model.predict_proba(prediction_values_scaled)[0,1]

        flash('The probability of suffering diabetes is: '+'{:.1%}'.format(prediction), 'success')

        return render_template('predictdiabetes.html',
                                title='ML Diabetes', form = form)