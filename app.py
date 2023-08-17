# Flask
from flask import Flask, render_template, request
# Data manipulation
import pandas as pd
# Matrices manipulation
import numpy as np
# Script logging
import logging
# ML model
import joblib
# JSON manipulation
import json
# Utilities
import sys
import os

# Current directory
#current_dir = os.path.dirname(__file__)
current_dir = os.path.dirname('C:/Users/PERFECTO/PROJET_7_avec_FLASK_Api/')

#'C:/Users/User/'
#PROJET_7_avec_FLASK_Api


# Flask app
app = Flask(__name__, static_folder = 'static', template_folder = 'template')

# Logging
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

# Function
def ValuePredictor(data = pd.DataFrame):
	# Model name
	model_name = 'bin/model_7.pkl'
	# Directory where the model is stored
	model_dir = os.path.join(current_dir, model_name)
	# Load the model
	loaded_model = joblib.load(open(model_dir, 'rb'))
	# Predict the data
	result = loaded_model.predict(data)
	return result[0]

# Home page
@app.route('/')
def home():
	return render_template('index.html')

# Prediction page
@app.route('/prediction', methods = ['POST'])
def predict():
	if request.method == 'POST':
		# Get the data from form
		name = request.form['name']
		genre = request.form['genre']
		education = request.form['education']
		nombre_enfants = request.form['nombre_enfants']
		nombre_famille_membre = request.form['nombre_famille_membre']
		statut_marital = request.form['statut_marital']
		situation_logement = request.form['situation_logement']
		situation_crédit = request.form['situation_crédit']
		possession_maison = request.form['possession_maison']
		possession_voiture = request.form['possession_voiture']
		montant_total_crédits = request.form['montant_total_crédits']
		revenu_total = request.form['revenu_total']
		échéances_impayées = request.form['échéances_impayées']
		origine_revenu = request.form['origine_revenu']
		type_crédit = request.form['type_crédit']

		# Load template of JSON file containing columns name
		# Schema name
		schema_name = 'data/columns_set.json'
		# Directory where the schema is stored
		schema_dir = os.path.join(current_dir, schema_name)
		with open(schema_dir, 'r') as f:
			cols =  json.loads(f.read())
		schema_cols = cols['data_columns']

		
		

		# Parse the numerical columns
		schema_cols['CNT_CHILDREN'] = nombre_enfants
		schema_cols['CNT_FAM_MEMBERS'] = nombre_famille_membre
		schema_cols['NAME_FAMILY_STATUS'] = statut_marital
		schema_cols['NAME_HOUSING_TYPE'] = situation_logement
		schema_cols['CODE_GENDER'] = genre
		schema_cols['CREDIT_ACTIVE'] = situation_crédit
		schema_cols['NAME_EDUCATION_TYPE'] = education
		schema_cols['FLAG_OWN_REALTY'] = possession_maison
		schema_cols['FLAG_OWN_CAR'] = possession_voiture
		schema_cols['AMT_CREDIT_SUM'] = montant_total_crédits
		schema_cols['AMT_INCOME_TOTAL'] = revenu_total
		schema_cols['CNT_INSTALMENT_FUTURE'] = échéances_impayées
		schema_cols['NAME_INCOME_TYPE'] = origine_revenu
		schema_cols['NAME_CONTRACT_TYPE'] = type_crédit

		# Convert the JSON into data frame
		df = pd.DataFrame(
				data = {k: [v] for k, v in schema_cols.items()},
				dtype = float
			)

		# Create a prediction
		print(df.dtypes)
		result = ValuePredictor(data = df)

		# Determine the output
		if int(result) == 1:
			prediction = 'Cher Mr/Mrs/Ms {name}, votre demande de crédit est approuvée!'.format(name = name)
		else:
			prediction = 'Désolé Mr/Mrs/Ms {name}, votre demande de crédit est rejetée!'.format(name = name)

		# Return the prediction
		return render_template('prediction.html', prediction = prediction)
	
	# Something error
	else:
		# Return error
		return render_template('error.html', prediction = prediction)

if __name__ == '__main__':
    app.run(debug = True)