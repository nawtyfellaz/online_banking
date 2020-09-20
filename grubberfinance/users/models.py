from django.contrib.auth.models import AbstractUser
from django.db.models import (
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    EmailField,
    FileField,
    ForeignKey,
    ImageField,
    IntegerField,
    OneToOneField,
    Q,
    SlugField,
    CASCADE,
    SET_NULL,
    URLField
)
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator
)

from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from grubberfinance.utils.functions import *

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

def upload_doc_path(instance, filename):
    new_filename = random.randint(1,3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "document/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)

NAME_REGEX = '^[a-zA-Z ]*$'
ZIP_REGEX = '^(^[0-9]{6}(?:-[0-9]{4})?$|^$)'

SEX = (
    ('', 'Choose Gender'),
    ('Male', 'MALE'),
    ('Female', 'FEMALE'),
)

ACCOUNT = (
    ('', 'Select Account Type'),
    ('Certificate Deposit Account', 'Certificate Deposit Account'),
    ('Checking Account', 'Checking Account'),
    ('Savings Account', 'Savings Account'),
)


class User(AbstractUser):
    """Default user for grubberfinance."""

    #: First and last name do not cover name patterns around the globe
    name            = CharField(_("Firstname Surname"), blank=True, max_length=255)
    slug            = SlugField(unique=True, null=True, max_length=255) # hello world -> hello-world
    photo           = ImageField(_('User Display Photo/Logo'), upload_to=upload_image_path, null=True, blank=True) #, storage=MediaStorage()
    doc             = FileField(_('Drivers Licence, National Identity, Utility Bill'), upload_to=upload_doc_path, null=True, blank=True) #, storage=ProtectedStorage()
    email           = EmailField(_('email address'), unique=True)
    phone           = PhoneNumberField(_('Phone Number'), blank=True, unique=True, null=True)#, region="US", E164_only=True
    DOB             = DateField(_('Date of Birth'), max_length=8, blank=True, null=True)
    gender          = CharField(_('Gender'), max_length=7, blank=True, null=True, choices=SEX)
    account_type    = CharField(_('Account Type'), max_length=32, blank=True, null=True, choices=ACCOUNT)
    account_number  = CharField(_('Account Number'), max_length=12, unique=True, null=True, blank=True)
    routing_number  = CharField(_('Routing Number'), max_length=12, unique=True, null=True, blank=True)
    balance         = DecimalField(_('Account Balance'), default=0, max_digits=12, decimal_places=2, null=True, blank=True)
    pin             = CharField(_('Online Pin'), max_length=4, null=True, blank=True)
    address         = CharField(_('Residntial Address'), max_length=600, null=True, blank=True, unique=True)
    zipcode         = CharField(_('Zip Code'), max_length=10, null=True, blank=True, unique=True, validators=[RegexValidator(regex=ZIP_REGEX,message='Must be valid zipcode in formats 12345 or 12345-1234', code='invalid_zip_code')], help_text="Must be valid zipcode in formats 12345 or 12345-1234")
    ssn             = CharField(_('Social Security Number'), max_length=10, blank=True, null=True)
    country         = CountryField(default='US')
    terms           = BooleanField(default=False)
    transfer        = BooleanField(default=True)
    is_superuser    = BooleanField(default=False)
    is_staff        = BooleanField(default=False)
    is_active       = BooleanField(default=True)
    date_joined     = DateTimeField(default=timezone.now)
    updated         = DateTimeField(auto_now_add=True)
    terms           = BooleanField(default=False)

    @property
    def age(self):
        TODAY = datetime.date.today()
        if self.DOB:
            return u"%s" % relativedelta.relativedelta(TODAY, self.DOB).years
        else:
            return None

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
