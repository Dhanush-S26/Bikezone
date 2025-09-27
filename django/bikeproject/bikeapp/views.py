from django.shortcuts import render,redirect
from . models import BikeCollections,Booking,Testride
from django.contrib import messages
from django.utils import timezone
from datetime import datetime

# Create your views here.
def home(request):
    return render(request,'landing.html')
def bikes(request):
    bikess = BikeCollections.objects.all()
    return render(request,'bikes.html',{'bikess':bikess})

def profile(request):
    if request.user.is_authenticated:  
        user_name = request.user.username  

        # Get booking history
        bookings = Booking.objects.filter(username=user_name)
        # Attach price from BikeCollections
        booking_list = []
        for b in bookings:
            try:
                bike = BikeCollections.objects.get(name=b.prefered_bike)
                price = bike.price
            except BikeCollections.DoesNotExist:
                price = "N/A"
            booking_list.append({
                'username': b.username,
                'email': b.email,
                'phoneno': b.phoneno,
                'city': b.city,
                'prefered_bike': b.prefered_bike,
                'price': price,
            })

        # Get testride history
        testrides = Testride.objects.filter(username=user_name)
        testride_list = []
        for t in testrides:
            testride_list.append({
                'username': t.username,
                'email': t.email,
                'phoneno': t.phoneno,
                'city': t.city,
                'prefered_bike': t.prefered_bike,
                'price': 10000,
                'testride_datetime' : t.testride_datetime,
            })


        return render(request, 'profile.html', {
            'bookings': booking_list,
            'testrides': testride_list,
        })

    else:
        return render(request, 'profile.html', {
            'bookings': None,
            'testrides': None,
            'message': 'Please log in to see your history.'
        })
    
def bike1(request):
    return render(request,'bike1.html')
def bike2(request):
    return render(request,'bike2.html')
def bike3(request):
    return render(request,'bike3.html')
def bike4(request):
    return render(request,'bike4.html')
def bike5(request):
    return render(request,'bike5.html')
def bike6(request):
    return render(request,'bike6.html')
def bike7(request):
    return render(request,'bike7.html')
def bike8(request):
    return render(request,'bike8.html')
def bike9(request):
    return render(request,'bike9.html')
def bike10(request):
    return render(request,'bike10.html')
def bike11(request):
    return render(request,'bike11.html')
def bike12(request):
    return render(request,'bike12.html')
def bike13(request):
    return render(request,'bike13.html')
def bike14(request):
    return render(request,'bike14.html')
def bike15(request):
    return render(request,'bike15.html')
def bike16(request):
    return render(request,'bike16.html')
def bike17(request):
    return render(request,'bike17.html')
def bike18(request):
    return render(request,'bike18.html')
def bike19(request):
    return render(request,'bike19.html')
def bike20(request):
    return render(request,'bike20.html')
def contact(request):
    return render(request,'contact.html')
def book(request):
    if request.method == 'POST':
        if "booking" in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            phoneno = request.POST['phoneno']
            city = request.POST['city']
            prefered_bike = request.POST['prefered_bike']

            # Get bike price
            try:
                bike = BikeCollections.objects.get(name=prefered_bike)
                bike_price = bike.price
            except BikeCollections.DoesNotExist:
                bike_price = "N/A"  # fallback if bike not found
            
            booking, created = Booking.objects.get_or_create(
                phoneno = phoneno,
                defaults={
                    'username' : username,
                    'email' : email,
                    'city' : city,
                    'prefered_bike' : prefered_bike,
                }
            )
            if created:
                messages.success(request,f"Booking Successful! Your bike price is {bike_price}",extra_tags='bookmsg')
            else:
                messages.info(request, "You already booked with this number.",extra_tags='bookmsg')

        elif "check" in request.POST:
            phoneno = request.POST['phoneno']
            if Booking.objects.filter(phoneno=phoneno).exists():
                booking = Booking.objects.get(phoneno=phoneno)
                return render(request,'book.html',{'booking':booking})
    return render(request,'book.html')
def testride(request):
    if request.method == 'POST':
        if 'testride' in request.POST:
            username = request.POST['username']
            email = request.POST['email']
            phoneno = request.POST['phoneno']
            city = request.POST['city']
            prefered_bike = request.POST['prefered_bike']
            testride_datetime_str = request.POST['testride_datetime']

            # Convert string to datetime object first
            testride_datetime = datetime.strptime(testride_datetime_str, '%Y-%m-%dT%H:%M')
            
            # Make it timezone-aware
            testride_datetime = timezone.make_aware(testride_datetime)

            testride, created = Testride.objects.get_or_create(
                phoneno=phoneno,
                defaults={
                    'username': username,
                    'email': email,
                    'city': city,
                    'prefered_bike': prefered_bike,
                    'testride_datetime': testride_datetime,
                }
            )

            if created:
                messages.success(request, 'Booking testride successful! Your testride price 10000', extra_tags='ridemsg')
            else:
                messages.info(request, "You already booked testride with this number.", extra_tags='ridemsg')

        elif "checkride" in request.POST:
            phoneno = request.POST['phoneno']
            if Testride.objects.filter(phoneno=phoneno).exists():
                testride = Testride.objects.get(phoneno=phoneno)
                return render(request, 'testride.html', {'testride': testride})
            
    return render(request, 'testride.html')
    