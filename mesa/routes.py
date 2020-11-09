
from flask import render_template, jsonify, request, flash, redirect, url_for
from mesa.forms import PredictionForm, ProductsForm
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

# ============= PRODUCT CATALOG======================================
# WEB INTERFACE
@app.route("/Products/Catalog", methods=['GET','POST'])
def getproductcatalog():
    catalog = pd.DataFrame(products.read_data())
    form = ProductsForm()
 
    return render_template('productcatalog.html'
                            , tables=[catalog.to_html( header = True, index= False)]
                            , form = form)


@app.route("/Products/add", methods=['GET','POST'])
def addproduct_web():
    form = ProductsForm()

    # Verify if form contains any data
    new_product =  [x for x in form.data.values()][:3]
    notvalid = any(element is None for element in new_product)
    
    if notvalid:        
        
        return render_template('addproduct.html', title = "Add new product", form = form)
      
    else:
                               
        new_product_df = pd.DataFrame(new_product)

        products.append_data(new_product_df.T)
        
        flash(f'{new_product[0]}  added successfully','success')        
        return redirect(url_for('getproductcatalog'))                           
        
 
@app.route("/Products/delete", methods=['GET','POST'])
def deleteproduct_web():
    form = ProductsForm()

    delete_product =  [x for x in form.data.values()][:3]
    notvalid = delete_product[0] is None

    if notvalid:
        
        return render_template('deleteproduct.html', title = "Delete Products", form = form)

    else:
        q = delete_product[0]
        nprod = pd.DataFrame({'name': [q]})
        products.delete_data(nprod)

        flash(f'{delete_product[0]} removed successfully','success')

        return redirect(url_for('getproductcatalog'))

@app.route("/Products/search", methods=['GET','POST'])
def searchproduct_web():
    form = ProductsForm()

    # Verify if form contains any data
    search_product =  [x for x in form.data.values()][:3]
    notvalid = search_product[0] is None

    if notvalid:        
        
        return render_template('getproduct.html', title = "Search product", form = form)
      
    else:
        # q = search_product[0]
        # eprod = pd.DataFrame({'name': [q]})
        # new_product_df = pd.DataFrame(search_product)
        q = products.get_record(search_product[0])
        
        # flash(q)
        # flash(f'{search_product[0]}  selected successfully','success')        
        # return render_template('editproduct.html', title = "OK product", form = form, record = q)
        return redirect(url_for('editproduct_web', record = q))

@app.route("/edit/<record>", methods=['GET','POST'])
def editproduct_web(record):
    form = ProductsForm()

    search_product =  [x for x in form.data.values()][:3]
    notvalid = search_product[0] is None
    
    if notvalid:
        return render_template('editproduct.html', title = 'Edit product', form = form, record = record)
    else:
        sp = pd.DataFrame(search_product, index= ['name','price per gm','quantity'])
       
        products.edit_data(sp.T)
        
        flash(f'Updated Successfuly {search_product[0]}, Price: {search_product[1]}, Quantity: {search_product[2]}', 'success')

        return redirect(url_for('getproductcatalog'))
        # return render_template('editproduct.html', title = 'Edit product', form = form, record = record)

        

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