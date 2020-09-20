from django.contrib.auth import get_user_model
from django.contrib.auth import forms as admin_forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

User = get_user_model()

from bootstrap_datepicker_plus import DatePickerInput
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django_countries.widgets import CountrySelectWidget

class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    phone = PhoneNumberField()
    error_message = admin_forms.UserCreationForm.error_messages.update(
        {
            "duplicate_username": _("This username has already been taken."),
            "invalid_phone_number":_("This phone number input is incorrect")
        }
    )

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ('name', 'email', 'phone', 'photo', 'doc', 'DOB', 'gender', 'ssn', 'address', 'zipcode', 'country')
        widgets = {
            'DOB': DatePickerInput(format='%Y-%m-%d'),
            'phone': PhoneNumberPrefixWidget(),
            'country': CountrySelectWidget(),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if not phone:
            raise ValidationError(self.error_message["invalid_phone_number"])

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])

class UserChangePin(forms.ModelForm):
    class Meta:
        model = User
        fields = ['pin']

