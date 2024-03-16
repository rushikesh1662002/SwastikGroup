from django.shortcuts import render
from django.core.mail import send_mail
from .forms import ContactForm
from django.template import loader
from django.contrib.auth import get_user_model
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .utils.ml_operations import predict
from django.views.decorators.http import require_POST
from django.conf import settings
from pycaret.classification import load_model
from pycaret.classification import predict_model
import os
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import io
import mpld3
import matplotlib
matplotlib.use('Agg')



# Assuming 'static' is in your Django project directory
file_path = os.path.join(settings.BASE_DIR, 'CollegePrediction', 'utils', 'SPPUCollegeList2.xlsx')

# Load College Information from Excel
college_info = pd.read_excel(file_path)


@require_POST
def prediction_view(request):
    # Initialize LabelEncoder
    label_encoder = LabelEncoder()

    if request.method == 'POST':
        # Get user input data from the form
        input_data = {
            'Year': 2023,
            'Gender': request.POST.get('gender'),
            'Category': request.POST.get('category'),
            'Merit_No': float(request.POST.get('rank')),
            'Seat_Types': request.POST.get('seattype'),
            'Round': request.POST.get('round'),
            'CET_Score': float(request.POST.get('cetScore')),
            'Chance_Of_Admit': 1
            # Add 'Year' if it's a categorical variable
            # Add more features as needed
        }

        # Convert the input data to a DataFrame
        input_df = pd.DataFrame([input_data])

        # Convert categorical variables using LabelEncoder
        categorical_columns = ['Category', 'Gender', 'Round', 'Seat_Types', 'Year']
        for col in categorical_columns:
            input_df[col] = label_encoder.fit_transform(input_df[col])

        print("Input DataFrame:")
        print(input_df)

        # Load the PyCaret model from the 'models' folder
        model_path = os.path.join(settings.BASE_DIR, 'CollegePrediction', 'models', 'multiclass')
  
        try:
            # Make predictions using the loaded model
            model = load_model(model_path)
            print("Model Loaded Successfully")

            result = predict_model(model, input_df)
            print("Predictions Successful")

            # Extracting the predicted class and Course Code where 'Chance_Of_Admit' is 1
            predicted_class = result['prediction_label'].tolist()
            print("Predicted Class:", predicted_class)

            # Ensure predicted_class is a list
            if not isinstance(predicted_class, list):
                predicted_class = [predicted_class]

            # Handle the case where the first element of predicted_class is an integer
            if isinstance(predicted_class[0], int):
                first_4_digits = str(predicted_class[0])[:4]
            else:
                first_4_digits = str(predicted_class[0][:4])

            # Filter College Information based on the first 4 digits of Course_Code
            matched_courses = college_info[college_info['Course_Code'].astype(str).str.startswith(first_4_digits)]['Course_Code'].tolist()

            # Look up College Names based on matched Course_Codes
            college_names = college_info.loc[college_info['Course_Code'].isin(matched_courses), 'College_Name'].tolist()

            # Extracting the first element of predicted_class
            predicted_course_code = str(predicted_class[0])
            
            # Histogram
            # Replace this with the actual path to your CSV file
            csv_file_path = os.path.join(settings.BASE_DIR, 'CollegePrediction', 'utils', 'Admission (1).csv')

            # Load your CSV data
            csv_data = pd.read_csv(csv_file_path)

            # Extract relevant information from input data
            current_category = input_data['Category']
            current_gender = input_data['Gender']

            # Filter the CSV data based on the predicted_class, current_category, current_gender, current_seat_type, and Chance_Of_Admit
            filtered_data = csv_data[
                (csv_data['Course_Code'] == predicted_class[0]) &
                (csv_data['Category'] == current_category) &
                (csv_data['Gender'] == current_gender) 
            ]


            # Group the filtered data by 'Year' and find the maximum CET_Score as the cutoff
            grouped_data = filtered_data.groupby('Year')['CET_Score'].max().reset_index(name='Cut_Off')
            aspect_ratio = 1.25  # Adjust as needed
            width_in_inches = 5  # Adjust width as needed
            height_in_inches = width_in_inches / aspect_ratio

            plt.figure(figsize=(width_in_inches, height_in_inches))
            bars = plt.bar(grouped_data['Year'], grouped_data['Cut_Off'], color='#5a8fc4', edgecolor='#000000', width=0.6)

            # Adding labels on top of each bar
            for bar in bars:
                yval = bar.get_height()
                plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom', color='black', fontweight='bold')

            plt.xlabel('Year')
            plt.ylabel('Cut Off CET Score')
            plt.title(f'Course code {predicted_class[0]} with Cut Off CET Scores for {current_category}')
            plt.grid(True)
            plt.xticks(grouped_data['Year'])

            # Save the plot to a BytesIO object
            image_stream = io.BytesIO()
            plt.savefig(image_stream, format='png')
            image_stream.seek(0)

            # Encode the image as base64
            encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
            image_stream.close()
            plt.close('all')

            # Render the result.html page with the histogram image
            return render(request, 'result.html', {'predicted_course_code': predicted_course_code, 'matched_courses': matched_courses, 'college_names': college_names, 'histogram_image': encoded_image})
        except Exception as e:
            # Handle the exception (e.g., print the error, log it, or display a user-friendly message)
            print(f"Error: {str(e)}")
            return render(request, 'error.html', {'error_message': 'An error occurred while making predictions'})

    return render(request, 'input_form.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send email
            recipient_email = 'rushikesh1662002@gmail.com'  
            send_mail(
                'Subject: {}'.format(subject),
                'From: {} ({})\n\n{}'.format(name, email, message),
                email,
                [recipient_email],
                fail_silently=False,
            )
            success_message = 'Your message was sent successfully.'
            print('Your message was sent successfully.')
            return render(request, 'index.html', {'form': ContactForm(), 'success_message': success_message})
 

    else:
        form = ContactForm()

    return render(request, 'index.html', {'form': form})


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'index.html', {'user': request.user})

def login_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pass1 = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=uname, password=pass1)

        if user is not None:
            # Login the user
            login(request, user)
            return redirect('home')  # Redirect to the home page or any other desired page
        else:
            # Authentication failed, show an error message or handle it accordingly
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})

    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')

        if pass1 != pass2:
            return HttpResponse("Passwords do not match")

        # Use get_user_model() to get the User model
        User = get_user_model()

        # Check if a user with the given username already exists
        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username is already taken. Choose a different one.")

        # Create a new user instance
        my_user = User.objects.create_user(username=uname, email=email, password=pass1)
        my_user.phone = phone
        my_user.save()
        return redirect('login')

    return render(request, 'signup.html')
def custom_logout(request):
    logout(request)
    return redirect('login')
