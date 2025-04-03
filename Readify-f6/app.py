import sqlite3
import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import firebase_admin
from firebase_admin import credentials, auth, firestore
from flask import Flask, render_template, request, redirect, url_for, flash, session
import time

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"C:\Users\adity\Downloads\useracc-d7781-firebase-adminsdk-fbsvc-dab45e7f1b.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

DATABASE = 'bookstore.db'

# Initialize SQLite Database and create required tables if not exist
def init_db():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Create Books Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        price REAL,
        image TEXT
    )
    ''')

    # Create Cart Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_id INTEGER NOT NULL,
        FOREIGN KEY (book_id) REFERENCES books(id)
    )
    ''')

    # Create Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    ''')

    # Insert sample data into books table (prices converted to INR and additional categories)
    cursor.executemany('''
    INSERT INTO books (title, category, description, price, image) VALUES (?, ?, ?, ?, ?)
    ''', [
        ('Atomic Habits', 'Self-Help', 'A guide to building good habits and breaking bad ones', 1200, 'atmoic habits.jpg'),
        ('Bhagwat Geeta', 'Spirituality', 'Ancient Hindu text on spiritual wisdom', 1000, 'everyday gita.jpg'),
        ('Reminder of Him', 'Romance', 'A heartfelt story of love and memory', 1050, 'Reminder of him.jpg'),
        ('Think and Grow Rich', 'Self-Help', 'A book on the power of personal beliefs and the path to success', 850, 'think and grow rich.jpg'),
        ('Enlightenment: The Only Revolution', 'Spirituality', 'A deep dive into the concept of enlightenment', 1100, 'Enlightnment the only revolution.jpg'),
        ('The Power of Your Subconscious Mind', 'Self-Help', 'Understanding the power of the subconscious mind to shape your life', 1300, 'The power of your subconseious Mind.jpg'),
        ('A Good Girl\'s Guide to Murder', 'Mystery', 'A thrilling mystery novel', 900, 'A good girls guide to murder.jpg'),
        ('The Housemaid', 'Thriller', 'A gripping story of betrayal and suspense', 1000, 'the house maid.jpg'),
        ('The Art of Being Alone', 'Self-Help', 'A book on embracing solitude and personal growth', 950, 'the art of being alone.jpg'),
        ('The Monk Who Sold His Ferrari', 'Self-Help', 'A fable about fulfilling your dreams and reaching your destiny', 1050, 'the monk who sold hid ferrari.jpg'),
        ('Don\'t Believe Everything You Think', 'Psychology', 'A guide to questioning and changing harmful thought patterns', 850, 'dont believe everything you think.jpg'),
        ('The Art of War', 'Philosophy', 'Ancient Chinese military strategy and tactics', 700, 'the art of war.jpg'),
        ('The Silent Patient', 'Thriller', 'A psychological thriller about a woman who stopped speaking', 1100, 'the silent patient.jpg'),
        ('Three Thousand Stitches', 'Biography', 'The inspiring story of a social activist', 900, 'the thousand stitches.jpg'),
        ('The Complete Novels of Sherlock Holmes', 'Mystery', 'A collection of all Sherlock Holmes novels', 2200, 'Sherlock Homes.jpg'),
        ('The Mountain Is You', 'Self-Help', 'A book about overcoming self-sabotage', 1200, 'the mountain is you.jpg'),
        ('The Glorious Quran', 'Spirituality', 'The holy book of Islam', 1300, 'the glorious quran.jpg'),
        ('Holy Bible', 'Spirituality', 'The sacred scripture of Christianity', 1500, 'the holy bible.jpg'),
        ('The Subtle Art of Not Giving a F*ck', 'Self-Help', 'A book about embracing life\'s challenges with a new perspective', 1300, 'the subtitle the art of not giving f.jpg'),
        ('The Alchemist', 'Fiction', 'A philosophical novel about following your dreams', 1000, 'the alchimist.jpg'),
        ('Verity', 'Romance', 'A romantic thriller that keeps you guessing', 1050, 'Verity.jpg'),
        ('The Midnight Library', 'Fiction', 'A novel about exploring the infinite possibilities of life choices', 1100, 'the midnight library.jpg'),
        ('Deep Work', 'Self-Help', 'A book on focusing without distractions to achieve massive success', 1300, 'Deep work.jpg'),
        ('You Can', 'Self-Help', 'A motivational book about achieving your goals', 900, 'You can.jpg'),
        ('Sapiens: A Brief History of Humankind', 'Non-Fiction', 'A book about the history of the human species', 1500, 'Sapiens the brief history of humain kind.jpg'),
        ('Courage to Be Disliked', 'Philosophy', 'A guide to living a life free from the expectations of others', 1200, 'The courage to be disliked.jpg'),
        ('The 5 AM Club', 'Self-Help', 'A book on waking up early to transform your life', 1100, 'the 5am club.jpg'),
        ('Anxious People', 'Fiction', 'A comedy-drama about life and personal struggles', 950, 'Anxious people.jpg'),
        ('The 48 Laws of Power', 'Self-Help', 'A book about the principles of power and influence', 1300, '48-laws-of-power.jpg'),
        ('It Ends with Us', 'Romance', 'A story about love and resilience', 1050, 'It ends with us.jpg'),
        ('One Arranged Murder', 'Mystery', 'A thrilling mystery about an arranged marriage gone wrong', 1100, 'One arranged marrage murder.jpg'),
        ('Siddhartha', 'Fiction', 'A novel about the spiritual journey of self-discovery', 850, 'Siddhartha.jpg'),
        ('The Five Love Languages', 'Self-Help', 'A book about understanding how different people give and receive love', 1000, 'the five love languages.jpg'),
        ('The Blue Umbrella', 'Children', 'A charming story about a little girl and her blue umbrella', 600, 'the blue umbrella.jpg'),
        ('Start with Why', 'Business', 'A book on the importance of understanding the purpose behind your actions', 1100, 'start with why.jpg'),
        ('Think Like a Monk', 'Self-Help', 'A guide to leading a peaceful and purposeful life', 1200, 'Think like a monk.jpg'),
        ('Too Late', 'Thriller', 'A gripping crime novel about consequences', 1050, 'too late.jpg'),
        ('Corporate Chanakya', 'Business', 'A book on leadership and strategic thinking', 1200, 'corporate Chanakya.jpg'),
        ('The Diary of a CEO', 'Biography', 'A collection of reflections by a successful entrepreneur', 1500, 'the diary of a CEO.jpg'),
        ('Thinking, Fast and Slow', 'Psychology', 'A book about the two systems of thinking that drive our decisions', 1500, 'thinking fast and slow.jpg'),
        ('Do It Today', 'Self-Help', 'A guide to overcoming procrastination and taking action now', 850, 'DO it today.jpg'),
        ('The Diary of a Young Girl', 'Biography', 'The personal diary of Anne Frank', 650, 'the diary of young girl.jpg')
    ])

    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    search_query = request.args.get('search', '')
    category_filter = request.args.get('category', '')
    cart_count = 0
    username = ""

    if 'user_id' in session:
        user_id = session['user_id']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM cart WHERE user_id=?', (user_id,))
        cart_count = cursor.fetchone()[0]
        
        # Fetch the username of the logged-in user
        cursor.execute('SELECT username FROM users WHERE id=?', (user_id,))
        user = cursor.fetchone()
        if user:
            username = user[0]
        
        conn.close()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if search_query:
        cursor.execute('SELECT * FROM books WHERE title LIKE ?', ('%' + search_query + '%',))
    elif category_filter:
        cursor.execute('SELECT * FROM books WHERE category=?', (category_filter,))
    else:
        cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()

    return render_template('index.html', books=books, cart_count=cart_count, username=username)

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')  # Create an 'about_us.html' template

@app.route('/add_to_cart/<int:book_id>')
def add_to_cart(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO cart (user_id, book_id) VALUES (?, ?)', (user_id, book_id))
    conn.commit()
    conn.close()
    return redirect(url_for('home'))

@app.route('/book/<int:book_id>')
def book_details(book_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if book:
        cart_count = 0
        if 'user_id' in session:
            user_id = session['user_id']
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM cart WHERE user_id=?', (user_id,))
            cart_count = cursor.fetchone()[0]
            conn.close()
        
        return render_template('book_details.html', book=book, cart_count=cart_count)
    else:
        return "Book not found."

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']  # Storing as plain text (not secure)

        try:
            # Create user in Firebase Authentication
            user = auth.create_user(
                email=email,
                password=password,
                display_name=username
            )
            
            # Store user data in Firestore (including password)
            db.collection('users').document(user.uid).set({
                'username': username,
                'email': email,
                'password': password  # Plain text password
            })

            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '')
        password = request.form.get('password', '')

        try:
            # Authenticate with Firebase
            user = auth.get_user_by_email(email)

            # Fetch user details from Firestore
            user_doc = db.collection('users').document(user.uid).get()
            
            if user_doc.exists:
                user_data = user_doc.to_dict()

                if user_data.get('password') == password:  # Plain text password check
                    session['user_id'] = user.uid
                    session['email'] = email
                    flash('Login successful!', 'success')
                    return redirect(url_for('home'))
                else:
                    flash('Invalid password!', 'danger')
            else:
                flash('User not found!', 'danger')

        except Exception as e:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html')



@app.route('/cart')
def cart():
    cart_items = []
    if 'user_id' in session:
        user_id = session['user_id']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
        SELECT books.title, books.category, books.price
        FROM cart
        JOIN books ON cart.book_id = books.id
        WHERE cart.user_id=?
        ''', (user_id,))
        cart_items = cursor.fetchall()
        conn.close()
    
    return render_template('cart.html', books_in_cart=cart_items)

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    if request.method == 'POST':
        session['address'] = request.form.get('address')
        session['payment_method'] = request.form.get('payment_method')
        return redirect(url_for('confirm_purchase'))
    return render_template('purchase.html')

@app.route('/confirm_purchase', methods=['GET', 'POST'])
def confirm_purchase():
    payment_method = session.get('payment_method', 'Pay on Delivery')
    
    if request.method == 'POST':
        if payment_method == "PhonePe":
            # Simulate successful payment (Replace with actual PhonePe API)
            time.sleep(2)
            session['payment_status'] = 'Success'
        return redirect(url_for('thankyou'))
    
    return render_template('confirm_purchase.html', payment_method=payment_method)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect if not logged in

    user_id = session['user_id']
    user_doc = db.collection('users').document(user_id).get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        return render_template('profile.html', user=user_data)
    else:
        return "User not found", 404



@app.route('/verify_user', methods=['POST'])
def verify_user():
    email = request.form['email']
    try:
        user = auth.get_user_by_email(email)
        if user:
            session['verified_user'] = email
            return jsonify({'verified': True})
    except:
        return jsonify({'verified': False})

@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        return jsonify({'success': False, 'message': 'User not logged in'}), 401

    user_id = session['user_id']
    update_type = request.form.get('update_type')

    try:
        user_ref = db.collection('users').document(user_id)

        if update_type == 'phone':
            phone = request.form.get('phone')
            if phone:
                user_ref.update({'phone': phone})
                return jsonify({'success': True, 'message': 'Phone updated successfully'})

        elif update_type == 'address':
            address = request.form.get('address')
            if address:
                user_ref.update({'address': address})
                return jsonify({'success': True, 'message': 'Address updated successfully'})

        elif update_type == 'password':
            new_password = request.form.get('new_password')

            if new_password:
                # DEBUG: Print new password to check if it's received
                print(f"Updating password to: {new_password}")

                # Update password in Firestore users collection
                user_ref.update({'password': new_password})

                return jsonify({'success': True, 'message': 'Password updated successfully.'})

        return jsonify({'success': False, 'message': 'Invalid update request'}), 400

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 400

@app.route('/addresses')
def addresses():
    return render_template('addresses.html')

@app.route('/order_history')
def order_history():
    return render_template('order_history.html')

@app.route('/subscriptions')
def subscriptions():
    return render_template('subscriptions.html')

@app.route('/terms_conditions')
def terms_conditions():
    return render_template('terms_conditions.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/subscribe/<plan_name>')
def subscribe(plan_name):
    # Define subscription plans
    subscriptions = {
        'basic': {'name': 'Basic Plan', 'description': 'Access to 10 books per month', 'price': 299},
        'standard': {'name': 'Standard Plan', 'description': 'Access to 20 books per month + 10% discount on purchases', 'price': 499},
        'premium': {'name': 'Premium Plan', 'description': 'Unlimited book access + 20% discount on purchases', 'price': 799}
    }
    
    if plan_name not in subscriptions:
        return "Invalid Subscription Plan", 404

    # Fetch selected plan details
    selected_plan = subscriptions[plan_name]

    return render_template('subscription_purchase.html',
                           subscription_name=selected_plan['name'],
                           subscription_description=selected_plan['description'],
                           subscription_price=selected_plan['price'])


@app.route('/confirm_subscription_purchase', methods=['POST'])
def confirm_subscription_purchase():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    subscription_name = request.form.get('subscription_name')
    subscription_price = request.form.get('subscription_price')
    payment_method = request.form.get('payment_method')

    if not subscription_name or not subscription_price or not payment_method:
        return "Invalid Data", 400

    session['subscription_name'] = subscription_name
    session['subscription_price'] = subscription_price
    session['payment_method'] = payment_method

    return redirect(url_for('thankyou_subscription'))


@app.route('/thankyou_subscription')
def thankyou_subscription():
    return render_template('thankyou_subscription.html', 
                           subscription_name=session.get('subscription_name'), 
                           payment_method=session.get('payment_method'))

@app.route('/phonepe_payment')
def phonepe_payment():
    return "PhonePe Payment Page (To be implemented)"

@app.route('/Add_Bank')
def Add_Bank():
    return "Cash on Delivery Payment Page (To be implemented)"


if __name__ == '__main__':
    app.run(debug=True)
