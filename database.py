from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Login(db.Model):
    __tablename__ = 'login'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


class Health(db.Model):
    __tablename__ = 'health'
    health_data_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    high_cholesterol = db.Column(db.Enum('Yes', 'No'), nullable=False)
    diabetes_1 = db.Column(db.Enum('Yes', 'No'), nullable=False)
    diabetes_2 = db.Column(db.Enum('Yes', 'No'), nullable=False)
    cardiovascular_disease = db.Column(db.Enum('Yes', 'No'), nullable=False)
    kidney_disease = db.Column(db.Enum('Yes', 'No'), nullable=False)
    hypertension = db.Column(db.Enum('Yes', 'No'), nullable=False)
    obesity = db.Column(db.Enum('Yes', 'No'), nullable=False)
    pcos = db.Column(db.Enum('Yes', 'No'), nullable=False)
    gerd = db.Column(db.Enum('Yes', 'No'), nullable=False)
    gout = db.Column(db.Enum('Yes', 'No'), nullable=False)
    weight = db.Column(db.DECIMAL(5, 2), nullable=False)
    height = db.Column(db.DECIMAL(5, 2), nullable=False)


class Requirements(db.Model):
    __tablename__ = 'requirements'
    requirement_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    health_data_id = db.Column(db.Integer, nullable=False)
    carbohydrates = db.Column(db.DECIMAL(5, 2))
    added_sugars = db.Column(db.DECIMAL(5, 2))
    saturated_fats = db.Column(db.DECIMAL(5, 2))
    trans_fats = db.Column(db.DECIMAL(5, 2))
    dietary_cholesterol = db.Column(db.DECIMAL(5, 2))
    high_cholesterol_foods = db.Column(db.DECIMAL(5, 2))
    unsaturated_fats = db.Column(db.DECIMAL(5, 2))
    whole_grains = db.Column(db.DECIMAL(5, 2))
    lean_proteins = db.Column(db.DECIMAL(5, 2))
    fiber = db.Column(db.DECIMAL(5, 2))
    sodium = db.Column(db.DECIMAL(6, 2))
    phosphorus = db.Column(db.DECIMAL(5, 2))
    potassium = db.Column(db.DECIMAL(6, 2))
    protein = db.Column(db.DECIMAL(5, 2))
    alcohol = db.Column(db.DECIMAL(5, 2))
    fructose = db.Column(db.DECIMAL(5, 2))


class NutrientsIntake(db.Model):
    __tablename__ = 'nutrients_intake'
    intake_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    health_data_id = db.Column(db.Integer, nullable=False)
    requirement_id = db.Column(db.Integer, nullable=False)
    intake_date = db.Column(db.Date)
    carbohydrates = db.Column(db.DECIMAL(5, 2))
    added_sugars = db.Column(db.DECIMAL(5, 2))
    saturated_fats = db.Column(db.DECIMAL(5, 2))
    trans_fats = db.Column(db.DECIMAL(5, 2))
    dietary_cholesterol = db.Column(db.DECIMAL(5, 2))
    high_cholesterol_foods = db.Column(db.DECIMAL(5, 2))
    unsaturated_fats = db.Column(db.DECIMAL(5, 2))
    whole_grains = db.Column(db.DECIMAL(5, 2))
    lean_proteins = db.Column(db.DECIMAL(5, 2))
    fiber = db.Column(db.DECIMAL(5, 2))
    sodium = db.Column(db.DECIMAL(6, 2))
    phosphorus = db.Column(db.DECIMAL(5, 2))
    potassium = db.Column(db.DECIMAL(6, 2))
    protein = db.Column(db.DECIMAL(5, 2))
    alcohol = db.Column(db.DECIMAL(5, 2))
    fructose = db.Column(db.DECIMAL(5, 2))
    dish = db.Column(db.String(20))
