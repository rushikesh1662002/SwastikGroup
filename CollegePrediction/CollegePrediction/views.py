# views.py
from django.template import loader
from django.contrib.auth import get_user_model
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login,logout

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
