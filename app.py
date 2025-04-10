from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from model import predict_news  # Import the prediction function from model.py

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB setup (adjust the URI as needed)
client = MongoClient('mongodb://localhost:27017')
db = client['fake_news_detection']
users_collection = db['users']
news_collection = db['news']

# Routes
@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        
        # Check if user already exists
        if users_collection.find_one({'username': username}):
            return "Username already exists!"
        
        # Insert new user
        users_collection.insert_one({'username': username, 'password': password})
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check credentials
        user = users_collection.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            return redirect(url_for('main'))
        return "Invalid username or password!"
    
    return render_template('login.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    prediction = None
    if request.method == 'POST':
        news_text = request.form['news']
        prediction = predict_news(news_text)
        
        # Log the check in the database
        news_collection.insert_one({
            'username': session['username'],
            'news': news_text,
            'prediction': prediction
        })
    
    return render_template('main.html', prediction=prediction)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
