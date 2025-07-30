from django.shortcuts import render, HttpResponse

# Create your views here.
def home(request):
    user_text = ""
    first_line = ""

    if request.method == "POST":
        user_text = request.POST.get("userText", "")

        uploaded_file = request.FILES.get("fileUpload")
        if uploaded_file:
            # Read the first line of the uploaded file (decode from bytes)
            first_line = uploaded_file.readline().decode('utf-8').strip()

    return render(request, "home.html", {
        "user_text": user_text,
        "first_line": first_line
    })