from flask import Flask, request, render_template, redirect, url_for, jsonify, session
from database import db, Login, Health, Requirements
import os
import subprocess
from datetime import datetime
import re
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = '##your custom code##'

# Initialize the database
db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/nurse')
def nurse():
    return render_template('nurse.html')


@app.route('/submit-requirements', methods=['POST'])
def submit_requirements():
    data = request.json
    username = data.get('username')
    user = Login.query.filter_by(username=username).first()
    user_id = user.user_id
    print(user_id)
    trans_fats = data.get('trans_fats')
    print(trans_fats)
    dietary_cholesterol = data.get('dietary_cholesterol')
    print(dietary_cholesterol)
    high_cholesterol_foods = data.get('high_cholesterol_foods')
    print(high_cholesterol_foods)
    carbohydrates = data.get('carbohydrates')
    print(carbohydrates)
    added_sugars = data.get('added_sugars')
    saturated_fats = data.get('saturated_fats')
    unsaturated_fats = data.get('unsaturated_fats')
    whole_grains = data.get('whole_grains')
    lean_proteins = data.get('lean_proteins')
    fiber = data.get('fiber')
    sodium = data.get('sodium')
    phosphorus = data.get('phosphorus')
    potassium = data.get('potassium')
    protein = data.get('protein')
    alcohol = data.get('alcohol')
    fructose = data.get('fructose')

    # Retrieve user_id from session

    # Query health_data_id based on user_id
    health_data = Health.query.filter_by(user_id=user_id).first()
    if health_data:
        user_id = health_data.health_data_id
        print(user_id)
        print('hi')
        # Insert data into Requirements table
        requirements = Requirements(
            health_data_id=user_id,
            trans_fats=trans_fats,
            dietary_cholesterol=dietary_cholesterol,
            high_cholesterol_foods=high_cholesterol_foods,
            carbohydrates=carbohydrates,
            added_sugars=added_sugars,
            saturated_fats=saturated_fats,
            unsaturated_fats=unsaturated_fats,
            whole_grains=whole_grains,
            lean_proteins=lean_proteins,
            fiber=fiber,
            sodium=sodium,
            phosphorus=phosphorus,
            potassium=potassium,
            protein=protein,
            alcohol=alcohol,
            fructose=fructose
        )

        db.session.add(requirements)
        db.session.commit()

        return jsonify({'message': 'Nutrient values submitted successfully!'})
    else:
        return jsonify({'message': 'Health data not found for this user.'})


@app.route('/health/<username>')
def get_health_data(username):
    user = Login.query.filter_by(username=username).first()

    if user:
        user_id = user.user_id
        print(user_id)
        #session['user_id'] = user_id
        # Query health data based on user_id
        health_data = Health.query.filter_by(user_id=user_id).first()
        if health_data:
            alert_text = f"Health Information for User ID {user_id}:\n"
            alert_text += f"High Cholesterol: {health_data.high_cholesterol}\n"
            alert_text += f"Diabetes 1: {health_data.diabetes_1}\n"
            alert_text += f"Diabetes 2: {health_data.diabetes_2}\n"
            alert_text += f"Cardiovascular Disease: {health_data.cardiovascular_disease}\n"
            alert_text += f"Kidney Disease: {health_data.kidney_disease}\n"
            alert_text += f"Hypertension: {health_data.hypertension}\n"
            alert_text += f"Obesity: {health_data.obesity}\n"
            alert_text += f"PCOS: {health_data.pcos}\n"
            alert_text += f"GERD: {health_data.gerd}\n"
            alert_text += f"Gout: {health_data.gout}\n"
            alert_text += f"Weight: {health_data.weight}\n"
            alert_text += f"Height: {health_data.height}\n"
            return alert_text
        else:
            return 'No health data found for this user.'
    else:
        return 'Username not found.'


@app.route('/question')
def question():
    user_id = request.args.get('user_id')
    print(user_id)
    return render_template('question.html', user_id=user_id)


@app.route('/why')
def why():
    return render_template('why.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/tryAI')
def tryAI():
    user_id = request.args.get('user_id')
    return render_template('tryAI.html', user_id=user_id)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/trainer')
def trainer():
    return render_template('trainer.html')


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')


from flask import render_template
from database import NutrientsIntake


@app.route('/dashboard')
def dashboard():
    # Get the user_id from the query parameters
    user_id = request.args.get('user_id')
    health_data = Health.query.filter_by(user_id=user_id).first()
    if health_data:
        health_data_id = health_data.health_data_id
    else:
        return jsonify({'error': 'Health data not found for the user.'}), 404
    if user_id:
        # Query the nutrients intake data for the user's health_data_id
        nutrients_data = NutrientsIntake.query.filter_by(health_data_id=health_data_id).all()

        return render_template('dashboard.html', nutrients_data=nutrients_data, user_id=user_id)
    else:
        # Redirect to login if user_id is not provided
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Create a new login object
        new_login = Login(username=username, email=email, password=password)

        # Add the new login to the database session
        db.session.add(new_login)

        # Commit the session to save the changes to the database
        db.session.commit()

        user = Login.query.filter_by(username=username).first()
        # Redirect the user to the question route after signing up
        return render_template('question.html', user_id=user.user_id)
    return render_template('signup.html')


@app.route('/authenticate', methods=['POST'])
def authenticate():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user with the given username and password
        user = Login.query.filter_by(username=username, password=password).first()

        if user:
            # If user exists, redirect to dashboard with user_id as a query parameter
            return redirect(url_for('dashboard', user_id=user.user_id))
        else:
            # If user doesn't exist or password is incorrect, redirect to login page
            return redirect(url_for('login'))


@app.route('/submit_questionnaire', methods=['POST'])
def submit_questionnaire():
    user_id = request.args.get('user_id')
    print('hi')
    print(user_id)
    if request.method == 'POST':
        # Retrieve form data
        gender = request.form.get('gender')
        height = request.form.get('height')
        weight = request.form.get('weight')
        condition1 = request.form.getlist('condition1')
        condition2 = request.form.getlist('condition2')
        condition3 = request.form.getlist('condition3')
        condition4 = request.form.getlist('condition4')
        condition5 = request.form.getlist('condition5')
        condition6 = request.form.getlist('condition6')
        condition7 = request.form.getlist('condition7')
        condition8 = request.form.getlist('condition8')
        condition9 = request.form.getlist('condition9')
        condition10 = request.form.getlist('condition10')# Change to 'condition' to match HTML
        user_id = request.args.get('user_id')
        print('hi')
        print(user_id)
        # Create a new Health object
        new_health_record = Health(
            user_id=user_id,  # Replace with actual user ID
            high_cholesterol='Yes' if 'High Cholesterol (Hyperlipidemia)' in condition1 else 'No',
            diabetes_1='Yes' if 'Diabetes Mellitus Type 1' in condition2 else 'No',
            diabetes_2='Yes' if 'Diabetes Mellitus Type 2' in condition3 else 'No',
            cardiovascular_disease='Yes' if 'Cardiovascular Disease' in condition4 else 'No',
            kidney_disease='Yes' if 'Kidney Disease' in condition5 else 'No',
            hypertension='Yes' if 'Hypertension' in condition6 else 'No',
            obesity='Yes' if 'Obesity' in condition7 else 'No',
            pcos='Yes' if 'Polycystic Ovary Syndrome (PCOS)' in condition8 else 'No',
            gerd='Yes' if 'Gastroesophageal Reflux Disease (GERD)' in condition9 else 'No',
            gout='Yes' if 'Gout' in condition10 else 'No',
            weight=float(weight) if weight else None,
            height=float(height) if height else None
        )

        # Add the new Health record to the database session
        db.session.add(new_health_record)

        # Commit the session to save the changes to the database
        db.session.commit()

        # Redirect the user to the dashboard
        return redirect(url_for('login'))

    # Handle GET requests or other cases where the method is not POST
    return redirect(url_for('question'))


@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        image = request.files['image']
        image_path = os.path.join('assets/Unknown', image.filename)
        image.save(image_path)

        # Execute imageClassifierTest.py and capture its output
        output = subprocess.check_output(['python', 'imageClassifierTest.py'])
        output_str = output.decode('utf-8').strip()  # Convert bytes to string


        # Determine the predicted class from the output
        predicted_class = None
        if "Predicted Class:" in output_str:
            predicted_class_match = re.search(r'Predicted Class:\s*([^,]+)', output_str)
            predicted_class = predicted_class_match.group(1).strip()
        # Based on the predicted class, construct data for NutrientsIntake table
        nutrients_data = {}
        if predicted_class == "Pav-Bhaji":
            # Define data for Class1
            nutrients_data = {
                'carbohydrates': 40,
                'added_sugars': 5,
                'saturated_fats': 15,
                'trans_fats': 0,
                'dietary_cholesterol': 20,
                'high_cholesterol_foods': 5,
                'unsaturated_fats': 10,
                'whole_grains': 5,
                'lean_proteins': 10,
                'fiber': 8,
                'sodium': 80,
                'phosphorus': 15,
                'potassium': 40,
                'protein': 8,
                'alcohol': 0,
                'fructose': 3,
                'dish': 'Pav-Bhaji'
            }

        elif predicted_class == "Biryani":
            # Define data for Class2
            nutrients_data = {
                'carbohydrates': 60,
                'added_sugars': 3,
                'saturated_fats': 20,
                'trans_fats': 0,
                'dietary_cholesterol': 30,
                'high_cholesterol_foods': 10,
                'unsaturated_fats': 15,
                'whole_grains': 10,
                'lean_proteins': 20,
                'fiber': 5,
                'sodium': 70,
                'phosphorus': 25,
                'potassium': 50,
                'protein': 15,
                'alcohol': 0,
                'fructose': 2,
                'dish': 'Biryani'
            }

        elif predicted_class == "Chole-Bhature":
            # Define data for Chole Bhature
            nutrients_data = {
                'carbohydrates': 70,
                'added_sugars': 5,
                'saturated_fats': 25,
                'trans_fats': 0,
                'dietary_cholesterol': 35,
                'high_cholesterol_foods': 15,
                'unsaturated_fats': 20,
                'whole_grains': 5,
                'lean_proteins': 15,
                'fiber': 7,
                'sodium': 160,
                'phosphorus': 30,
                'potassium': 50,
                'protein': 10,
                'alcohol': 0,
                'fructose': 3,
                'dish': 'Chole-Bhature'
            }

        elif predicted_class == "Dabeli":
            # Define data for Dabeli
            nutrients_data = {
                'carbohydrates': 50,
                'added_sugars': 8,
                'saturated_fats': 15,
                'trans_fats': 0,
                'dietary_cholesterol': 25,
                'high_cholesterol_foods': 5,
                'unsaturated_fats': 10,
                'whole_grains': 5,
                'lean_proteins': 10,
                'fiber': 6,
                'sodium': 60,
                'phosphorus': 20,
                'potassium': 70,
                'protein': 8,
                'alcohol': 0,
                'fructose': 4,
                'dish': 'Dabeli'
            }

        elif predicted_class == "Dal":
            # Define data for Dal
            nutrients_data = {
                'carbohydrates': 30,
                'added_sugars': 2,
                'saturated_fats': 5,
                'trans_fats': 0,
                'dietary_cholesterol': 0,
                'high_cholesterol_foods': 0,
                'unsaturated_fats': 5,
                'whole_grains': 10,
                'lean_proteins': 25,
                'fiber': 8,
                'sodium': 50,
                'phosphorus': 40,
                'potassium': 30,
                'protein': 15,
                'alcohol': 0,
                'fructose': 1,
                'dish': 'Dal'
            }

        elif predicted_class == "Dhokla":
            # Define data for Dhokla
            nutrients_data = {
                'carbohydrates': 35,
                'added_sugars': 5,
                'saturated_fats': 2,
                'trans_fats': 0,
                'dietary_cholesterol': 0,
                'high_cholesterol_foods': 0,
                'unsaturated_fats': 3,
                'whole_grains': 15,
                'lean_proteins': 5,
                'fiber': 4,
                'sodium': 110,
                'phosphorus': 20,
                'potassium': 50,
                'protein': 6,
                'alcohol': 0,
                'fructose': 2,
                'dish': 'Dhokla'
            }

        elif predicted_class == "Masala-Dosa":
            # Define data for Masala Dosa
            nutrients_data = {
                'carbohydrates': 40,
                'added_sugars': 2,
                'saturated_fats': 3,
                'trans_fats': 0,
                'dietary_cholesterol': 0,
                'high_cholesterol_foods': 0,
                'unsaturated_fats': 4,
                'whole_grains': 20,
                'lean_proteins': 5,
                'fiber': 6,
                'sodium': 100,
                'phosphorus': 25,
                'potassium': 150,
                'protein': 8,
                'alcohol': 0,
                'fructose': 1,
                'dish': 'Masala-Dosa'
            }

        elif predicted_class == "Jalebi":
            # Define data for Jalebi
            nutrients_data = {
                'carbohydrates': 50,
                'added_sugars': 30,
                'saturated_fats': 10,
                'trans_fats': 0,
                'dietary_cholesterol': 0,
                'high_cholesterol_foods': 0,
                'unsaturated_fats': 5,
                'whole_grains': 0,
                'lean_proteins': 2,
                'fiber': 1,
                'sodium': 50,
                'phosphorus': 10,
                'potassium': 100,
                'protein': 2,
                'alcohol': 0,
                'fructose': 20,
                'dish': 'Jalebi'
            }

        elif predicted_class == "Kathi-Roll":
            # Define data for Kathi Roll
            nutrients_data = {
                'carbohydrates': 35,
                'added_sugars': 2,
                'saturated_fats': 8,
                'trans_fats': 0,
                'dietary_cholesterol': 20,
                'high_cholesterol_foods': 5,
                'unsaturated_fats': 10,
                'whole_grains': 10,
                'lean_proteins': 15,
                'fiber': 4,
                'sodium': 50,
                'phosphorus': 20,
                'potassium': 130,
                'protein': 12,
                'alcohol': 0,
                'fructose': 1,
                'dish': 'Kathi-Roll'
            }

        elif predicted_class == "Kofta":
            # Define data for Kofta
            nutrients_data = {
                'carbohydrates': 15,
                'added_sugars': 2,
                'saturated_fats': 10,
                'trans_fats': 0,
                'dietary_cholesterol': 30,
                'high_cholesterol_foods': 10,
                'unsaturated_fats': 5,
                'whole_grains': 5,
                'lean_proteins': 25,
                'fiber': 3,
                'sodium': 80,
                'phosphorus': 20,
                'potassium': 100,
                'protein': 20,
                'alcohol': 0,
                'fructose': 1,
                'dish': 'Kofta'
            }

        elif predicted_class == "Naan":
            # Define data for Naan
            nutrients_data = {
                'carbohydrates': 30,
                'added_sugars': 2,
                'saturated_fats': 5,
                'trans_fats': 0,
                'dietary_cholesterol': 0,
                'high_cholesterol_foods': 0,
                'unsaturated_fats': 3,
                'whole_grains': 5,
                'lean_proteins': 5,
                'fiber': 2,
                'sodium': 70,
                'phosphorus': 15,
                'potassium': 100,
                'protein': 5,
                'alcohol': 0,
                'fructose': 1,
                'dish': 'Naan'
            }

        elif predicted_class == "Pakora":
            # Define data for Pakora
            nutrients_data = {
                'carbohydrates': 25,
                'added_sugars': 2,
                'saturated_fats': 5,
                'trans_fats': 0,
                'dietary_cholesterol': 10,
                'high_cholesterol_foods': 5,
                'unsaturated_fats': 5,
                'whole_grains': 5,
                'lean_proteins': 10,
                'fiber': 3,
                'sodium': 80,
                'phosphorus': 15,
                'potassium': 100,
                'protein': 8,
                'alcohol': 0,
                'fructose': 1,
                'dish': 'Pakora'
            }

        elif predicted_class == "Paneer-Tikka":
            # Define data for Paneer Tikka
            nutrients_data = {
                'carbohydrates': 10,
                'added_sugars': 2,
                'saturated_fats': 5,
                'trans_fats': 0,
                'dietary_cholesterol': 15,
                'high_cholesterol_foods': 5,
                'unsaturated_fats': 3,
                'whole_grains': 0,
                'lean_proteins': 20,
                'fiber': 1,
                'sodium': 40,
                'phosphorus': 20,
                'potassium': 60,
                'protein': 15,
                'alcohol': 0,
                'fructose': 1,
                'dish': 'Paneer-Tikka'
            }

        elif predicted_class == "Pizza":
            # Define data for Pizza
            nutrients_data = {
                'carbohydrates': 40,
                'added_sugars': 5,
                'saturated_fats': 15,
                'trans_fats': 0,
                'dietary_cholesterol': 20,
                'high_cholesterol_foods': 10,
                'unsaturated_fats': 10,
                'whole_grains': 5,
                'lean_proteins': 10,
                'fiber': 4,
                'sodium': 70,
                'phosphorus': 30,
                'potassium': 70,
                'protein': 12,
                'alcohol': 0,
                'fructose': 2,
                'dish': 'Pizza'
            }

        elif predicted_class == "Samosa":
            # Define data for Samosa
            nutrients_data = {
                'carbohydrates': 30,
                'added_sugars': 2,
                'saturated_fats': 8,
                'trans_fats': 0,
                'dietary_cholesterol': 0,
                'high_cholesterol_foods': 0,
                'unsaturated_fats': 5,
                'whole_grains': 5,
                'lean_proteins': 5,
                'fiber': 3,
                'sodium': 60,
                'phosphorus': 20,
                'potassium': 50,
                'protein': 5,
                'alcohol': 0,
                'fructose': 1,
                'dish': 'Samosa'
            }

        elif predicted_class == "Momos":
            # Define data for Momos
            nutrients_data = {
                'carbohydrates': 25,
                'added_sugars': 2,
                'saturated_fats': 5,
                'trans_fats': 0,
                'dietary_cholesterol': 10,
                'high_cholesterol_foods': 5,
                'unsaturated_fats': 5,
                'whole_grains': 5,
                'lean_proteins': 10,
                'fiber': 3,
                'sodium': 80,
                'phosphorus': 15,
                'potassium': 100,
                'protein': 8,
                'alcohol': 0,
                'fructose': 1,
                'dish': 'Momos'
            }

        elif predicted_class == "Kulfi":
            # Define data for Kulfi
            nutrients_data = {
                'carbohydrates': 30,
                'added_sugars': 15,
                'saturated_fats': 10,
                'trans_fats': 0,
                'dietary_cholesterol': 30,
                'high_cholesterol_foods': 10,
                'unsaturated_fats': 5,
                'whole_grains': 0,
                'lean_proteins': 5,
                'fiber': 1,
                'sodium': 100,
                'phosphorus': 10,
                'potassium': 110,
                'protein': 5,
                'alcohol': 0,
                'fructose': 10,
                'dish': 'Kulfi'
            }

        elif predicted_class == "Idli":
            # Define data for Idli
            nutrients_data = {
                'carbohydrates': 25,
                'added_sugars': 1,
                'saturated_fats': 1,
                'trans_fats': 0,
                'dietary_cholesterol': 0,
                'high_cholesterol_foods': 0,
                'unsaturated_fats': 1,
                'whole_grains': 20,
                'lean_proteins': 5,
                'fiber': 3,
                'sodium': 60,
                'phosphorus': 15,
                'potassium': 100,
                'protein': 3,
                'alcohol': 0,
                'fructose': 1,
                'dish': 'Idli'
            }

        elif predicted_class == "Chai":
            # Define data for Chai
            nutrients_data = {
                'carbohydrates': 5,
                'added_sugars': 3,
                'saturated_fats': 1,
                'trans_fats': 0,
                'dietary_cholesterol': 0,
                'high_cholesterol_foods': 0,
                'unsaturated_fats': 1,
                'whole_grains': 0,
                'lean_proteins': 1,
                'fiber': 0,
                'sodium': 50,
                'phosphorus': 5,
                'potassium': 50,
                'protein': 1,
                'alcohol': 0,
                'fructose': 1,
                'dish': "Chai",
            }

        elif predicted_class == "Burger":
            # Define data for Burger
            nutrients_data = {
                'carbohydrates': 30,
                'added_sugars': 5,
                'saturated_fats': 10,
                'trans_fats': 1,
                'dietary_cholesterol': 30,
                'high_cholesterol_foods': 20,
                'unsaturated_fats': 10,
                'whole_grains': 5,
                'lean_proteins': 15,
                'fiber': 3,
                'sodium': 110,
                'phosphorus': 20,
                'potassium': 100,
                'protein': 15,
                'alcohol': 0,
                'fructose': 2,
                'dish': "Burger",
            }
        # Add more elif blocks for other classes as needed

        user_id = request.args.get('user_id')

        # Insert data into NutrientsIntake table
        # Fetching health_data_id from Health table using user_id
        health_data = Health.query.filter_by(user_id=user_id).first()
        if health_data:
            health_data_id = health_data.health_data_id
        else:
            return jsonify({'error': 'Health data not found for the user.'}), 404
        #health_data_id = health_data.health_data_id
        print(health_data_id)

        user_id = request.args.get('user_id')  # Assuming user_id is passed in the request parameters

        # Pull all records under the particular user_id for the current date
        current_date = datetime.now().date()
        intake_records = NutrientsIntake.query.filter_by(health_data_id=health_data_id, intake_date=current_date).all()

        # Initialize total nutrients sum
        total_nutrients_sum = {column: 0 for column in NutrientsIntake.__table__.columns.keys()[
                                                       3:-1] if column != 'intake_date'}  # Exclude 'intake_date' column

        # Calculate total nutrients sum
        for intake_record in intake_records:
            for column in total_nutrients_sum:
                value = getattr(intake_record, column)
                try:
                    numerical_value = float(value)
                    total_nutrients_sum[column] += numerical_value
                except (ValueError, TypeError):
                    print(
                        f"Skipping addition for column '{column}' with value '{value}' because it's not a numerical type.")

        # Get requirements for the user from the 'requirements' table
        user_requirements = Requirements.query.filter_by(health_data_id=health_data_id).first()


        # Filter out non-relevant columns (excluding 'health_data_id' from Requirements table)
        relevant_columns = [column for column in total_nutrients_sum.keys() if column != 'health_data_id']

        # Check if the sum of each nutrient is less than the value in records pulled from 'requirements' table
        requirements_met = True
        for column in relevant_columns:
            value = total_nutrients_sum[column]
            if value >= getattr(user_requirements, column):
                requirements_met = False
                break

        # Extract predicted class from the output string using regular expression
        predicted_class_match = re.search(r'Predicted Class:\s*([^,]+)', output_str)
        predicted_class = predicted_class_match.group(1) if predicted_class_match else 'Class not found'

        # Print result based on requirements
        if requirements_met:
            result = "Hurray! You can eat this"
            # Updating nutrients_intake table
            new_nutrients_intake = NutrientsIntake(
                health_data_id=health_data_id,
                requirement_id=user_requirements.requirement_id,
                intake_date=current_date,
                **nutrients_data
            )
            db.session.add(new_nutrients_intake)
            db.session.commit()
        else:
            result = "Oh no! Seems like you should not eat this"

        response_data = {
            'output': output_str,
            'predicted_class': predicted_class,
            'total_nutrients_sum': total_nutrients_sum,
            'requirements_met': requirements_met,
            'result': result
        }

        return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
