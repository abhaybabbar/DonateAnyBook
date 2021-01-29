from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from users.models import Order
# Create your views here.
def home(request):
    all_users= get_user_model().objects.all().count()
    books_donated = Order.objects.all().filter(status='True').count()
    books_pickup = Order.objects.all().filter(status='False').count()
    context = {'allusers': all_users, 'books_donated': books_donated, 'books_pickup': books_pickup}
    return render(request, 'main/home.html', context)

@login_required(login_url='login')
def donate(request):
    return render(request, 'main/forms.html')


def team(request):
    return render(request, 'main/team.html')    

def machine_learning(file_name):
    from google.cloud import vision
    from google.cloud.vision_v1 import types
    import pandas as pd
    import isbnlib
    import os, io
    os.chdir("C:\\Users\\91951\\Downloads")
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"turing-flow-301114-f4e6aa3e31d0.json."

    client = vision.ImageAnnotatorClient()
    my_list=[]
    
    for i in file_name:
        file_name = i
        image_path ="C:\\Users\\91951\\Downloads\\"+i

        with io.open(image_path, 'rb') as image_file:
            content = image_file.read()
        image = types.Image(content=content)


        """
        # or we can pass the image url
        image = vision.types.Image()
        image.source.image_uri = 'https://edu.pngfacts.com/uploads/1/1/3/2/11320972/grade-10-english_orig.png'
        """

        # annotate Image Response
        response = client.text_detection(image=image)  # returns TextAnnotation
        df = pd.DataFrame(columns=['locale', 'description'])

        texts = response.text_annotations
        for text in texts:
            df = df.append(
                dict(
                    locale=text.locale,
                    description=text.description
                ),
                ignore_index=True
            )

        string=df['description'][0]
        num=isbnlib.get_isbnlike(text=string, level='normal')
        string2=str(num)
        isbn=isbnlib.canonical(string2)
        info=isbnlib.meta(isbn)
        title = info.get('Title')
        author = info.get('Authors')

        my_list.append([title, author])

    return my_list

@login_required(login_url='login')
def result(request):
    files = request.POST.getlist('files')
    address = request.POST.get('Address')
    city = request.POST.get('City')
    state = request.POST.get('State')
    pincode = request.POST.get('PinCode')
    name = request.POST.get('name')
    email = request.POST.get('Email')
    number = request.POST.get('number')
    
    currentuser = request.user
    error = ""
    try:
        books = machine_learning(files)
    except:
        error = "There was a problem in detecting some books."
    for book in books:
        try:
            order = Order()
            order.username = currentuser
            order.address = address
            order.city = city
            order.state = state
            order.pincode = pincode
            order.name = name
            order.email = email
            order.number = number
            order.book_title = book[0]
            order.book_author = book[1]
            order.save()
        except:
            error = "There was a problem in detecting some books."      
    context = {
        'orders':books, 
        'thankyou': 'Thankyou For Donating the Following Books!!', 
        'error': error
        }
    return render(request, 'main/result.html', context)