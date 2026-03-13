from django.contrib import admin
from .models import Department, Doctor, Booking

class DoctorInline(admin.TabularInline):
    model = Doctor
    extra = 0
    fields = ('doc_name','doc_spec','doc_image')
    readonly_fields = ('doc_name','doc_spec','doc_image')


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id','dep_name')
    list_display_links = ('dep_name',)
    inlines = [DoctorInline]


admin.site.register(Department, DepartmentAdmin)


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    fields = ('p_name','p_phone','p_email','booking_date','booked_on')
    readonly_fields = ('p_name','p_phone','p_email','booking_date','booked_on')


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('id','doc_name','dep_name')
    search_fields = ('doc_name',)
    list_display_links = ('doc_name',)
    inlines = [BookingInline]


admin.site.register(Doctor, DoctorAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id','p_name','p_phone','p_email','doc_name','booking_date','booked_on')
    search_fields = ('p_name','p_phone')
    list_filter = ('doc_name','booking_date')
    list_display_links = ('p_name',)


    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Admin and Reception see all bookings
        if request.user.is_superuser or request.user.groups.filter(name="Reception").exists():
            return qs

        # Doctor sees only their bookings
        doctor = Doctor.objects.filter(user=request.user).first()
        if doctor:
            return qs.filter(doc_name=doctor)

        return qs


admin.site.register(Booking, BookingAdmin)

