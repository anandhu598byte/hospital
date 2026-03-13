from django.conf import settings
from django.contrib.messages import success
from django.shortcuts import render, redirect
from .forms import BookingForm
from .forms import BookingForm
from .models import Department, Doctor, Booking
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


# Create your views here.

def index(request):
    return render(request, 'index.html')
def about(request):
    return render(request, 'about.html')
def booking(request):

    if request.method == "POST":
        form=BookingForm(request.POST)
        if form.is_valid():

            data=form.cleaned_data
            request.session['booking_data'] = {
                'p_name': data['p_name'],
                'p_phone': data['p_phone'],
                'p_email': data['p_email'],
                'doc_name': data['doc_name'].id,
                'booking_date': str(data['booking_date']),
            }
            session=stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data':{
                            'currency':'INR',
                            'product_data':{
                                'name':'Doctor Appointment Fee',
                            },
                            'unit_amount':50000,
                        },
                        'quantity':1,
                    }
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/booking'),
            )
            return redirect(session.url)
        else:
            form=BookingForm()
        return render(request, 'booking.html',{'form':form})
    form=BookingForm()
    return render(request, 'booking.html',{'form':form})




def doctors(request):
    dict_docs={
        'doctors':Doctor.objects.all()
    }
    return render(request, 'doctors.html',dict_docs)
def contact(request):
    return render(request, 'contact.html')
def department(request):
    dict_dept={
        "dept":Department.objects.all()
    }
    return render(request, 'department.html',dict_dept)

def success(request):

    data = request.session.get('booking_data')

    if data:
        doctor = Doctor.objects.get(id=data['doc_name'])

        Booking.objects.create(
            p_name=data['p_name'],
            p_phone=data['p_phone'],
            p_email=data['p_email'],
            doc_name=doctor,
            booking_date=data['booking_date']
        )


        del request.session['booking_data']
    return render(request, 'confirmation.html')
