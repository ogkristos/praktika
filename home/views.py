from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate ,logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from .models import Addmoney_info,UserProfile
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.db.models import Sum
from django.http import JsonResponse
import datetime
from django.utils import timezone
from django.db import transaction

def home(request):
    if request.session.has_key('is_logged'):
        return redirect('/index')
    return render(request,'home/login.html')

def index(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        addmoney_info = Addmoney_info.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(addmoney_info , 4)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {
           'page_obj' : page_obj
        }
        return render(request,'home/index.html',context)
    return redirect('home')

def register(request):
    return render(request,'home/register.html')

def password(request):
    return render(request,'home/password.html')

def charts(request):
    return render(request,'home/charts.html')

def search(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        fromdate = request.GET['fromdate']
        todate = request.GET['todate']
        addmoney = Addmoney_info.objects.filter(user=user, Date__range=[fromdate,todate]).order_by('-Date')
        return render(request,'home/tables.html',{'addmoney':addmoney})
    return redirect('home')

def tables(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        addmoney = Addmoney_info.objects.filter(user=user).order_by('-Date')
        return render(request,'home/tables.html',{'addmoney':addmoney})
    return redirect('home')

def addmoney(request):
    return render(request,'home/addmoney.html')

def profile(request):
    if request.session.has_key('is_logged'):
        try:
            user_id = request.session["user_id"]
            user = User.objects.get(id=user_id)
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Получаем все транзакции пользователя
            addmoney_info = Addmoney_info.objects.filter(user=user)
            
            # Инициализируем суммы
            sum_expense = 0
            sum_income = 0
            
            # Вычисляем суммы расходов и доходов
            for item in addmoney_info:
                if item.add_money == 'Expense':
                    sum_expense += item.quantity if item.quantity is not None else 0
                elif item.add_money == 'Income':
                    sum_income += item.quantity if item.quantity is not None else 0
            
            # Обновляем профиль пользователя
            profile.Savings = sum_income - sum_expense
            profile.income = sum_income
            profile.save()
            
            return render(request, 'home/profile.html', {'user': user, 'profile': profile})
        except Exception as e:
            messages.error(request, f"Error loading profile: {str(e)}")
            return redirect('/home')
    return redirect('/home')

def profile_edit(request,id):
    if request.session.has_key('is_logged'):
        add = User.objects.get(id=id)
        return render(request,'home/profile_edit.html',{'add':add})
    return redirect("/home")

def profile_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            try:
                user = User.objects.get(id=id)
                profile, created = UserProfile.objects.get_or_create(user=user)
                
                user.first_name = request.POST["fname"]
                user.last_name = request.POST["lname"]
                user.email = request.POST["email"]
                
                profile.Savings = request.POST["Savings"]
                profile.income = request.POST["income"]
                profile.profession = request.POST["profession"]
                
                user.save()
                profile.save()
                
                messages.success(request, "Profile updated successfully!")
                return redirect("/profile")
            except Exception as e:
                messages.error(request, f"Error updating profile: {str(e)}")
                return redirect("/profile")
    return redirect("/home")

def handleSignup(request):
    if request.method == 'POST':
        try:
            uname = request.POST["uname"]
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            email = request.POST["email"]
            profession = request.POST['profession']
            Savings = request.POST['Savings']
            income = request.POST['income']
            pass1 = request.POST["pass1"]
            pass2 = request.POST["pass2"]

            if User.objects.filter(username=uname).exists():
                messages.error(request," Username already taken, Try something else!!!")
                return redirect("/register")

            if len(uname) > 15:
                messages.error(request," Username must be max 15 characters")
                return redirect("/register")

            if not uname.isalnum():
                messages.error(request," Username should only contain letters and numbers")
                return redirect("/register")

            if pass1 != pass2:
                messages.error(request," Passwords do not match")
                return redirect("/register")

            user = User.objects.create_user(uname, email, pass1)
            user.first_name = fname
            user.last_name = lname
            user.save()

            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.profession = profession
            profile.Savings = Savings
            profile.income = income
            profile.save()

            messages.success(request," Your account has been successfully created")
            return redirect("/")
            
        except Exception as e:
            messages.error(request, f"Error during signup: {str(e)}")
            return redirect("/register")
    
    return HttpResponse('404 - NOT FOUND')

def handlelogin(request):
    if request.method =='POST':
        loginuname = request.POST["loginuname"]
        loginpassword1=request.POST["loginpassword1"]
        user = authenticate(username=loginuname, password=loginpassword1)
        if user is not None:
            dj_login(request, user)
            request.session['is_logged'] = True
            user = request.user.id 
            request.session["user_id"] = user
            messages.success(request, " Successfully logged in")
            return redirect('/index')
        else:
            messages.error(request," Invalid Credentials, Please try again")  
            return redirect("/")  
    return HttpResponse('404-not found')

def handleLogout(request):
        del request.session['is_logged']
        del request.session["user_id"] 
        logout(request)
        messages.success(request, " Successfully logged out")
        return redirect('home')

def addmoney_submission(request):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            addmoney_info1 = Addmoney_info.objects.filter(user=user1).order_by('-Date')
            add_money = request.POST["add_money"]
            quantity = request.POST["quantity"]
            Date = request.POST["Date"]
            Category = request.POST["Category"]
            add = Addmoney_info(user = user1,add_money=add_money,quantity=quantity,Date = Date,Category= Category)
            add.save()
            paginator = Paginator(addmoney_info1, 4)
            page_number = request.GET.get('page')
            page_obj = Paginator.get_page(paginator,page_number)
            context = {
                'page_obj' : page_obj
                }
            return render(request,'home/index.html',context)
    return redirect('/index')

def addmoney_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            add = Addmoney_info.objects.get(id=id)
            add.add_money = request.POST["add_money"]
            add.quantity = request.POST["quantity"]
            add.Date = request.POST["Date"]
            add.Category = request.POST["Category"]
            add.save()
            return redirect("/index")
    return redirect("/home")        

def expense_edit(request,id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info.objects.get(id=id)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        return render(request,'home/expense_edit.html',{'addmoney_info':addmoney_info})
    return redirect("/home")  

def expense_delete(request,id):
    if request.session.has_key('is_logged'):
        addmoney_info = Addmoney_info.objects.get(id=id)
        addmoney_info.delete()
        return redirect("/index")
    return redirect("/home")  

def stats(request):
    if request.session.has_key('is_logged'):
        todays_date = datetime.date.today()
        one_month_ago = todays_date - datetime.timedelta(days=30)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        addmoney_info = Addmoney_info.objects.filter(
            user=user1,
            Date__gte=one_month_ago,
            Date__lte=todays_date
        )
        
        # Initialize sums
        sum_expense = 0
        sum_income = 0
        
        # Calculate sums safely
        for item in addmoney_info:
            if item.add_money == 'Expense':
                sum_expense += item.quantity if item.quantity is not None else 0
            elif item.add_money == 'Income':
                sum_income += item.quantity if item.quantity is not None else 0

        # Get user profile safely
        try:
            user_profile = user1.userprofile
            savings = user_profile.Savings if user_profile.Savings is not None else 0
        except UserProfile.DoesNotExist:
            savings = 0

        # Calculate remaining amount
        remaining_amount = savings + sum_income - sum_expense
        negative_amount = 0

        if remaining_amount < 0:
            messages.warning(request, 'Your expenses exceeded your savings')
            negative_amount = abs(remaining_amount)
            remaining_amount = 0

        # Get category-wise expenses
        expense_category_totals = (
            addmoney_info.filter(add_money='Expense')
            .values('Category')
            .annotate(total_amount=Sum('quantity'))
            .order_by('-total_amount')
        )

        # Convert to list and handle None values
        categories = []
        amounts = []
        for item in expense_category_totals:
            categories.append(item['Category'])
            amounts.append(float(item['total_amount'] or 0))

        context = {
            'addmoney_info': {
                'sum': sum_expense,
                'x': remaining_amount,
                'y': negative_amount
            },
            'expense_category_totals': expense_category_totals,
            'categories': categories,
            'amounts': amounts,
            'sum_expense': sum_expense,
            'sum_income': sum_income,
            'remaining_amount': remaining_amount,
            'negative_amount': negative_amount,
            'user': user1
        }
        
        return render(request, 'home/stats.html', context)
    return redirect('home')

def expense_month(request):
    todays_date = datetime.date.today()
    one_month_ago = todays_date-datetime.timedelta(days=30)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_month_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.Category    
    Category_list = list(set(map(get_Category,addmoney)))

    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity += item.quantity if item.quantity is not None else 0
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y] = get_expense_category_amount(y,"Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def weekly(request):
    if request.session.has_key('is_logged'):
        todays_date = datetime.date.today()
        one_week_ago = todays_date - datetime.timedelta(days=7)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        addmoney_info = Addmoney_info.objects.filter(
            user=user1,
            Date__gte=one_week_ago,
            Date__lte=todays_date
        )
        
        # Initialize sums
        sum_expense = 0
        sum_income = 0
        
        # Calculate sums safely
        for item in addmoney_info:
            if item.add_money == 'Expense':
                sum_expense += item.quantity if item.quantity is not None else 0
            elif item.add_money == 'Income':
                sum_income += item.quantity if item.quantity is not None else 0

        # Get user profile safely
        try:
            user_profile = user1.userprofile
            savings = user_profile.Savings if user_profile.Savings is not None else 0
        except UserProfile.DoesNotExist:
            savings = 0

        # Calculate remaining amount
        remaining_amount = savings + sum_income - sum_expense
        negative_amount = 0

        if remaining_amount < 0:
            messages.warning(request, 'Your expenses exceeded your savings')
            negative_amount = abs(remaining_amount)
            remaining_amount = 0

        # Get category-wise expenses
        expense_category_totals = (
            addmoney_info.filter(add_money='Expense')
            .values('Category')
            .annotate(total_amount=Sum('quantity'))
            .order_by('-total_amount')
        )

        # Convert to list and handle None values
        categories = []
        amounts = []
        for item in expense_category_totals:
            categories.append(item['Category'])
            amounts.append(float(item['total_amount'] or 0))

        context = {
            'addmoney_info': {
                'sum': sum_expense,
                'x': remaining_amount,
                'y': negative_amount
            },
            'expense_category_totals': expense_category_totals,
            'categories': categories,
            'amounts': amounts,
            'sum_expense': sum_expense,
            'sum_income': sum_income,
            'remaining_amount': remaining_amount,
            'negative_amount': negative_amount,
            'user': user1
        }
        
        return render(request, 'home/weekly.html', context)
    return redirect('home')


def expense_week(request):
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=7)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.Category
    Category_list = list(set(map(get_Category,addmoney)))

    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity += item.quantity if item.quantity is not None else 0
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y] = get_expense_category_amount(y,"Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def info_year(request):
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=30*12)
    user_id = request.session["user_id"]
    user1 = User.objects.get(id=user_id)
    addmoney = Addmoney_info.objects.filter(user = user1,Date__gte=one_week_ago,Date__lte=todays_date)
    finalrep ={}

    def get_Category(addmoney_info):
        return addmoney_info.Category
    Category_list = list(set(map(get_Category,addmoney)))

    def get_expense_category_amount(Category,add_money):
        quantity = 0 
        filtered_by_category = addmoney.filter(Category = Category,add_money="Expense") 
        for item in filtered_by_category:
            quantity += item.quantity if item.quantity is not None else 0
        return quantity

    for x in addmoney:
        for y in Category_list:
            finalrep[y] = get_expense_category_amount(y,"Expense")

    return JsonResponse({'expense_category_data': finalrep}, safe=False)

def info(request):
    return render(request,'home/info.html')

def check(request):
    return render(request, 'home/check.html')
