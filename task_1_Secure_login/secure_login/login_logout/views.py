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


@login_required
def manage_requests(request, id, accept_cancel):

    pending_user = PendingUsers.objects.get(id=id)

    if accept_cancel == 'accept':

        user = User.objects.create_user(username=pending_user.username, password=pending_user.password)
        user.is_active
        user.save()

        pending_user.delete()
    
    if accept_cancel == 'cancel':
        
        pending_user.delete()

    users = PendingUsers.objects.all()

    count = PendingUsers.objects.all().count()

    if count > 0 :
        return render(request, 'users_requests.html',{'pending_users': users} )
    else:
        return redirect('signup')


    


def user_login(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            # import pdb;pdb.set_trace()
            if user:
                login(request, user)
                
                return render(request, 'success_page.html')   
                   
    form = LoginForm()
    return render(request, 'login.html', {'form':form})
    
@login_required    
def success_page(request):

    if request.method == 'POST':

        import pdb;pdb.set_trace()

        # import pdb;pdb.set_trace()

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
        books = Books.objects.filter(availabilty=True)
        return render(request, 'success_page.html', {'books': books})
    
    return render(request, 'success_page.html', {'books': books})

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
def request_for_book(request, id):

    book = Books.objects.get(pk=id)

    book.requested_or_not = True
    book.requested_user_id=request.user
    book.availabilty=False
    book.save()
    
    books = Books.objects.filter(availabilty=True)

    return render(request, 'success_page.html', {'books':books})


@login_required
def historical_bookings(request):

    historical_equipmetns = HistoricalBookings.objects.filter(user=request.user)
    return render(request, 'historical.html',{'historical':historical_equipmetns})

@login_required
def request_again(request, id):
    
    his_book = HistoricalBookings.objects.get(pk=id)

    booked_equipments = BookedEquipments.objects.filter(equipment_id__requested_user_id=request.user)


    for e in booked_equipments:
        # import pdb;pdb.set_trace()
        if str(e) == str(his_book):
            
            return render(request, 'error_message.html')
        
    book = Books.objects.get(euipment_name=his_book.booked_equipment.euipment_name)

    
    book.requested_or_not = True
    book.booked_or_not = False
    book.requested_user_id=request.user
    book.availabilty=False
    book.save()


    books = HistoricalBookings.objects.filter(user=request.user)
    # import pdb;pdb.set_trace()

    return render(request, 'historical.html', {'historical':books})


@login_required
def filter_equipments(request, keyword):
    
    if keyword in ['Book', 'Electronics', 'Pc']:

        books = Books.objects.filter(euipment_type=keyword)
        
        return render(request, 'success_page.html', {'books': books})
    
    elif keyword == 'availability':

        books = Books.objects.filter(availabilty = True)

        return render(request, 'success_page.html', {'books': books})
    
    else:

        books = Books.objects.filter(requested_or_not = False, booked_or_not=False)
        return render(request, 'success_page.html', {'books': books})

@login_required
def admin_panel(request):

    if request.user.is_superuser:

        if request.method == 'POST':
            selected_option = request.POST.get('optionSelect')
            
            if selected_option == 'inventory status':
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

    
    

def user_logout(request):
    logout(request)
    return redirect('home')
    
