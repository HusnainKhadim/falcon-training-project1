from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from datetime import datetime, timezone
from .forms import SignupForm, LoginForm
from . models import *


def index(request):
    return render(request, 'index.html')

def signup(request):

    
    if request.method == 'POST':

        form = SignupForm(request.POST)

        if form.is_valid():
            
            PendingUsers.objects.create(username=form.data['username'], password=form.data['password1'])
            
            return redirect('signup')
        else:
            return redirect('signup')

    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form':form})
    

def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                
                return redirect('success_page')   
                   
    form = LoginForm()
    return render(request, 'login.html', {'form':form})
    
@login_required(login_url='/login/')  
def success_page(request):

    if request.method == 'POST':

        search_type = request.POST.get('optionSelect')
        search_keyword = request.POST.get('query')

        if search_type == 'id':
            books = Books.objects.filter(pk=search_keyword)

        elif search_type == 'name':
            books = Books.objects.filter(euipment_name=search_keyword)
            return render(request, 'success_page.html', {'books': books})
        else:
            books = Books.objects.filter(euipment_type=search_keyword)
            return render(request, 'success_page.html', {'books': books})
    
    else:
        books = Books.objects.all()
        return render(request, 'success_page.html', {'books': books, 'book_type':'all'})
    
@login_required
def users_reservations(request):

    user_id = request.user

    equipments = Books.objects.filter(requested_or_not=True, booked_or_not=False,requested_user_id=user_id)

    return render(request, 'users_reservations.html', {'booked_equipments':equipments})


@login_required
def cancel_request(request, id):

    book = Books.objects.get(pk=id, requested_user_id=request.user)
    book.requested_or_not = False
    book.save()

    equipments = Books.objects.filter(requested_or_not=True, booked_or_not=False,requested_user_id=request.user)

    return render(request, 'users_reservations.html', {'booked_equipments':equipments})


@login_required
def request_for_all(request, id):

    book = Books.objects.get(pk=id)

    if book.requested_or_not == True:
        return render(request, "cannot_request.html")

    book.requested_or_not = True
    book.requested_user_id=request.user
    book.availabilty=False
    book.save()
    
    books = Books.objects.all()

    return render(request, 'success_page.html', {'books':books, 'book_type': 'all'})

@login_required
def request_for_available(request, id):

    book = Books.objects.get(pk=id)

    if book.requested_or_not == True:
        return render(request, "cannot_request.html")

    book.requested_or_not = True
    book.requested_user_id=request.user
    book.availabilty=False
    book.save()
    
    books = Books.objects.filter(availabilty=True)

    return render(request, 'success_page.html', {'books':books, 'book_type': 'availability'})


@login_required
def request_for_Pc(request, id):

    book = Books.objects.get(pk=id)

    if book.requested_or_not == True:
        return render(request, "cannot_request.html")

    book.requested_or_not = True
    book.requested_user_id=request.user
    book.availabilty=False
    book.save()
    
    books = Books.objects.filter(euipment_type = 'Pc')

    return render(request, 'success_page.html', {'books':books, 'book_type': 'Pc'})


@login_required
def request_for_Electronics(request, id):

    book = Books.objects.get(pk=id)

    if book.requested_or_not == True:
        return render(request, "cannot_request.html")

    book.requested_or_not = True
    book.requested_user_id=request.user
    book.availabilty=False
    book.save()
    
    books = Books.objects.filter(euipment_type = 'Electronics')

    return render(request, 'success_page.html', {'books':books, 'book_type': 'Electronics'})


@login_required
def request_for_Book(request, id):

    book = Books.objects.get(pk=id)

    if book.requested_or_not == True:
        return render(request, "cannot_request.html")

    book.requested_or_not = True
    book.requested_user_id=request.user
    book.availabilty=False
    book.save()
    
    books = Books.objects.filter(euipment_type = 'Book')

    return render(request, 'success_page.html', {'books':books, 'book_type': 'Book'})


@login_required
def search_by_typing(request):
    option = request.POST.get("optionSelect")
    query = request.POST.get("query")

    if option == 'type':

        if query  == 'Book' or query == 'book':

            books = Books.objects.filter(euipment_type='Book')
            return render(request, 'success_page.html', {'books': books , 'book_type': 'Book'})
        elif query == 'Pc' or query == 'pc':

            books = Books.objects.filter(euipment_type='Pc')
            return render(request, 'success_page.html', {'books': books , 'book_type': 'Pc'})
        elif query == 'Electronics' or query == 'electronics':

            books = Books.objects.filter(euipment_type='Electronics')
            return render(request, 'success_page.html', {'books': books , 'book_type': 'Electronics'})
    
    elif option == 'id':

        books = Books.objects.get(pk=query)
        return render(request, 'success_page.html', {'books': books , 'book_type': 'all'})
    
    else:

        books = Books.objects.filter(euipment_name = query)
        return render(request, 'success_page.html', {'books': books , 'book_type': 'all'})




@login_required
def historical_bookings(request):

    historical_equipmetns = HistoricalBookings.objects.filter(user=request.user)
    return render(request, 'historical.html',{'historical':historical_equipmetns})

@login_required
def request_again(request, id):
    
    his_book = HistoricalBookings.objects.get(pk=id)

    booked_equipments = BookedEquipments.objects.filter(equipment_id__requested_user_id=request.user)


    for e in booked_equipments:

        if str(e) == str(his_book):
            
            return render(request, 'error_message.html')
        
    book = Books.objects.get(euipment_name=his_book.booked_equipment.euipment_name)

    
    book.requested_or_not = True
    book.booked_or_not = False
    book.requested_user_id=request.user
    book.availabilty=False
    book.save()


    books = HistoricalBookings.objects.filter(user=request.user)

    return render(request, 'historical.html', {'historical':books})


@login_required
def filter_equipments(request, keyword):
    
    if keyword  == 'Book':

        books = Books.objects.filter(euipment_type='Book')
        return render(request, 'success_page.html', {'books': books , 'book_type': 'Book'})
    elif keyword == 'Pc':
        books = Books.objects.filter(euipment_type='Pc')
        return render(request, 'success_page.html', {'books': books , 'book_type': 'Pc'})
    elif keyword == 'Electronics':
        books = Books.objects.filter(euipment_type='Electronics')
        return render(request, 'success_page.html', {'books': books , 'book_type': 'Electronics'})
    
    elif keyword == 'all':

        books = Books.objects.all()
        return render(request, 'success_page.html', {'books': books , 'book_type': 'all'})
    
    elif keyword == 'availability':

        books = Books.objects.filter(availabilty = True)

        return render(request, 'success_page.html', {'books': books , 'book_type': 'availability'})
    
    else:

        books = Books.objects.filter(requested_or_not = False, booked_or_not=False)
        return render(request, 'success_page.html', {'books': books})

@login_required
def admin_panel(request):

    if request.user.is_superuser:

        if request.method == 'POST':
            selected_option = request.POST.get('optionSelect')

            
            if selected_option == 'Inventory Status':
                items = Books.objects.all()
                item_count = Books.objects.all().count()
                return render(request, 'item_count.html', {'items':items, 'item_count': item_count})
            
            else:
                overdued_items = []
                count = 0
                books = BookedEquipments.objects.all()
                for book in books:

                    now = datetime.now(timezone.utc)

                    expiray_date = now - book.equipment_time

                    expiray_date_in_days = expiray_date.days

                    if expiray_date_in_days > book.equipment_id.return_days:
                        overdued_items.append(book)
                        count = count+1

                
                return render(request, 'overdued_items.html', {'items': overdued_items, 'count':count})

        else:
            return render(request, 'admin_panel.html' )
    else:
        return render(request, 'Not_admin.html')
    

def send_daily_email():

    books = BookedEquipments.objects.all()

    for book in books:

        now = datetime.now(timezone.utc)

        expiray_date = now - book.equipment_time

        expiray_date_in_days = expiray_date.days

        if expiray_date_in_days > book.equipment_id.return_days:

            print('Email should send')


            send_mail(
                'Daue Date Passed',
                'Your equipment has exceeded the due date kindly return it as soon as possible or re-new it!',
                'haxnat07@gmail.com',
                ['f2020266265@umt.edu.pk'],
                fail_silently=False,
                )



@login_required(login_url='/login/')  
def user_logout(request):
    logout(request)
    return redirect('home')
    
