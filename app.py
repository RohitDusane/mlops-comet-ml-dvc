from flask import Flask, render_template, request, flash
from pipeline.prediction_pipeline import hybrid_recommendation

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing messages (optional, but recommended)

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = None

    if request.method == 'POST':
        try:
            # Get the user_id from the form
            user_id = int(request.form["userID"])
            
            # Call the hybrid recommendation function
            recommendations = hybrid_recommendation(user_id)
            
            # If no recommendations found, flash a message (optional)
            if not recommendations:
                flash('No recommendations found for this user.', 'warning')
        
        except ValueError:
            # Handle the case where user_id is not an integer
            flash('Please enter a valid user ID.', 'danger')
        except Exception as e:
            # Handle other errors and log them
            flash(f"An error occurred: {str(e)}", 'danger')

    return render_template('index.html', recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
