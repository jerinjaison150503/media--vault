from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import FileUpload
from .forms import FileUploadForm

# User registration view
def reg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if username or email already exists
        if User.objects.filter(username=name).exists():
            messages.error(request, "Username already taken!")
            return redirect('/reg/')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return redirect('/reg/')

        # Create the user
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please log in.")
        return redirect('/log/')

    return render(request, 'user/reg.html')

# User login view
def log(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validate email and password input
        if not email or not password:
            messages.error(request, "Please provide both email and password.")
            return redirect('/log/')

        # Get the username from the email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('/log/')

        # Authenticate the user
        user = auth.authenticate(username=user.username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user_id'] = user.id  # Store user ID in session
            messages.success(request, "Logged in successfully!")
            return redirect('/home/')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('/log/')

    return render(request, 'user/log.html')

# Home page view
@login_required
def home(request):
    # Retrieve files uploaded by the logged-in user
    uploaded_files = FileUpload.objects.filter(user=request.user)
    return render(request, 'user/home.html', {'user': request.user, 'uploaded_files': uploaded_files})

# File upload view
@login_required
def uploadfile(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the uploaded file with the associated user
            file_upload = form.save(commit=False)
            file_upload.user = request.user  # Associate file with the logged-in user
            file_upload.save()  # Save the file
            messages.success(request, "File uploaded successfully!")  # Success message
            return redirect('/home/')  # Hardcoded redirect to home page
        else:
            messages.error(request, "Failed to upload file. Please check the form.")  # Error message
    else:
        form = FileUploadForm()  # Initialize the form for GET request

    return render(request, 'user/upload.html', {'form': form, 'user': request.user})

# User logout view
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)  # Log out the user
        request.session.flush()  # Clear session data
        messages.success(request, "You have been logged out.")
    
    return redirect('/log/')  # Hardcoded redirect
