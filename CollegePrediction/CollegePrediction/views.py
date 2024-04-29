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
        try:
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
                first_4_digits = str(predicted_class[0])[:4]

            # Filter College Information based on the first 4 digits of Course_Code
            matched_courses = college_info[college_info['Course_Code'].astype(str).str.startswith(first_4_digits)]['Course_Code'].tolist()

            # Look up College Names based on matched Course_Codes
            college_names = college_info.loc[college_info['Course_Code'].isin(matched_courses), 'College_Name'].tolist()

            # Extracting the first element of predicted_class
            predicted_course_code = str(predicted_class[0])

            # ************************* Colleges *****************************
            # Actual path to CSV file
            csv_file_path = os.path.join(settings.BASE_DIR, 'CollegePrediction', 'utils', 'Admission (1).csv')

            # Load your CSV data
            csv_data = pd.read_csv(csv_file_path)

            # Convert input data to float
            rank = float(request.POST.get('rank'))
            cet_score = float(request.POST.get('cetScore'))

            # Filter the CSV data based on the specified criteria
            filtered_data = csv_data[
                (csv_data['CET_Score'].between(cet_score - 3.0, cet_score + 3.0)) &
                (csv_data['Merit_No'].between(rank - 100, rank + 100))
            ]

            if filtered_data.empty:
                print('Filtered data is empty')  # No colleges found matching the criteria
                

            # Get the unique course codes from the filtered data
            unique_course_codes = filtered_data['Course_Code'].unique()

            # Convert unique_course_codes to a pandas DataFrame
            unique_course_codes_df = pd.DataFrame({'Course_Code': unique_course_codes.astype(str)})

            # Select the top 9 Course_Codes based on their frequency
            top_9_courses = unique_course_codes_df.head(9)['Course_Code'].tolist()

            print(top_9_courses)
            # Get the length of the top_9_courses list
            length_top_9_courses = len(top_9_courses)
            print("Length of top_9_courses:", length_top_9_courses)

            # Extract the first four digits of the top 9 course codes
            first_4_digits_list = [str(course)[:4] for course in top_9_courses]

            # List to store all first 4 digits strings
            all_first_4_digits_str = []

            # Handle the case where the first elements of predicted_class are integers
            for i in range(length_top_9_courses):  # Loop from 0 to 8
                if isinstance(first_4_digits_list[i], int):
                    first_4_digits_str = str(first_4_digits_list[i])[:4]
                else:
                    first_4_digits_str = str(first_4_digits_list[i])[:4]
                # Add first_4_digits_str to the list
                all_first_4_digits_str.append(first_4_digits_str)
                # Do something with first_4_digits_str
                print("First 4 digits for index", i, ":", first_4_digits_str)

            # Print all first 4 digits strings
            print("All first 4 digits strings:", all_first_4_digits_str)

            # Assuming 'static' is in your Django project directory
            file_path_upd = os.path.join(settings.BASE_DIR, 'CollegePrediction', 'utils', 'SPPUCollegeList.xlsx')

            # Load College Information from Excel
            college_info_upd = pd.read_excel(file_path_upd)

            # Filter College Information based on the first 4 digits of Course_Code
            matched_courses_upd = college_info_upd[college_info_upd['Course_Code'].astype(str).str.startswith(tuple(all_first_4_digits_str))]['Course_Code'].tolist()
            print(matched_courses_upd)

            # Look up College Names based on matched Course_Codes
            top_colleges = college_info_upd.loc[college_info['Course_Code'].isin(matched_courses_upd), 'College_Name'].tolist()
            
            context = list(zip(top_9_courses, top_colleges))
            
            # ------------------------ End College -----------------------------------------

            # Histogram
            # actual path to CSV file
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
            
            #************************* End Histogram ***************************
            
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^ Start Colleges Histogram ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            # Colleges Histogram
            # Actual path to CSV file
            csv_file_path_histo = os.path.join(settings.BASE_DIR, 'CollegePrediction', 'utils', 'Admission _Copy.csv')

            # Load CSV data
            admission_data = pd.read_csv(csv_file_path_histo)

            # Debugging: Print out the top 9 courses to verify their values
            print("Top 9 Courses:", top_9_courses)

            # Extract relevant information from input data
            selected_category = request.POST.get('category')
            selected_gender = request.POST.get('gender')

            # Plot histograms for the top 9 courses
            histogram_images_list = []

            try:
                for course_code in top_9_courses:
                    course_code = int(course_code)
                    filtered_admission_data = admission_data[
                        (admission_data['Course_Code'] == course_code) &  
                        (admission_data['Category'] == selected_category) &
                        (admission_data['Gender'] == selected_gender) 
                    ]

                    
                    # Check if any data is filtered
                    if filtered_admission_data.empty:
                        print(f"Filtered data is empty for Course Code: {course_code}")
                    else:
                        # Proceed with plotting histograms
                        # Group the filtered data by 'Year' and find the maximum CET_Score as the cutoff
                        grouped_data = filtered_admission_data.groupby('Year')['CET_Score'].max().reset_index(name='Cut_Off')
                        aspect_ratio = 1.25  # Adjust as needed
                        plot_width = 5  # Adjust width as needed
                        plot_height = plot_width / aspect_ratio

                        plt.figure(figsize=(plot_width, plot_height))
                        bars = plt.bar(grouped_data['Year'], grouped_data['Cut_Off'], color='#5a8fc4', edgecolor='#000000', width=0.6)

                        # Adding labels on top of each bar
                        for bar in bars:
                            yval = bar.get_height()
                            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.05, round(yval, 2), ha='center', va='bottom', color='black', fontweight='bold')

                        plt.xlabel('Year')
                        plt.ylabel('Cut Off CET Score')
                        plt.title(f'Course code {course_code} with Cut Off CET Scores for {selected_category}')
                        plt.grid(True)
                        plt.xticks(grouped_data['Year'])

                        # Save the plot to a BytesIO object
                        image_stream = io.BytesIO()
                        plt.savefig(image_stream, format='png')
                        image_stream.seek(0)

                        # Encode the image as base64
                        encoded_image_histo = base64.b64encode(image_stream.read()).decode('utf-8')
                        image_stream.close()

                        # Append the encoded image to the list
                        histogram_images_list.append(encoded_image_histo)

                        # Close the plot
                        plt.close('all')

            except Exception as e:
                print("Error occurred:", e)






   #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ End Colleges Histogram ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            
            delay_counter = 0 
            return render(request, 'result.html', {'predicted_course_code': predicted_course_code,
                                                    'matched_courses': matched_courses,
                                                    'college_names': college_names,
                                                    'top_9_courses':top_9_courses,
                                                    'context':context,
                                                    'delay_counter': delay_counter,
                                                    'top_colleges': top_colleges,
                                                    'histogram_images_list': histogram_images_list,
                                                    'histogram_image': encoded_image})
        except Exception as e:
            # Handle the exception (e.g., print the error, log it, or display a user-friendly message)
            print(f"Error: {str(e)}")
            return render(request, 'error.html', {'error_message': 'An error occurred while making predictions'})

    return render(request, 'input_form.html')


#-------------------------------------------------------------------------------------------------------

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
