from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import CASCADE
from django.utils.timezone import now

from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.db.models import Sum
import uuid
import random
import string

from tinymce.models import HTMLField

# from invoice.serializers import base_url
# base_url = "http://" + "127.0.0.1:8000"

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class GroupHDR(models.Model):
    GroupID = models.CharField(help_text='код', max_length=150, unique=True)
    GroupName = models.CharField(help_text='Ner ', max_length=150)
    FeaturedGroup = models.BooleanField(default=True, help_text='Kacc.mn сайт дээр онцлох эсэх')
    HeaderGroup = models.BooleanField(default=True, help_text='Kacc.mn сайт дээр Header дээр харуулах')
    ShowMenuGroup = models.BooleanField(default=False, help_text='Kacc.mn сайт дээр Menu дээр харуулах')
    GroupImage = models.ImageField(upload_to='group', null=True, blank=True)

    def __str__(self):
        return self.GroupName
    class Meta:
        verbose_name=  "Барааны бүрэг Header"
        verbose_name_plural =  "WebSite - Барааны бүрэг Header"


class GroupDTL(models.Model):
    GroupHDRPk = models.ForeignKey(GroupHDR, on_delete=CASCADE)
    GroupDTLName = models.CharField(help_text='Ner ', max_length=150)

    def __str__(self):
        return self.GroupDTLName
    class Meta:
        verbose_name=  "Барааны бүрэг Detail"
        verbose_name_plural =  "WebSite - Барааны бүрэг Detail"


class Color(models.Model):
    item = models.ForeignKey('InfoProduct', related_name='color_variants', on_delete=models.CASCADE)
    item_code = models.CharField(max_length=50, unique=True)
    ColorName = models.CharField(max_length=50)
    qty = models.IntegerField(default=0)
    hex_value = models.CharField(max_length=7)  # Hex code for color representation (e.g., #FFFFFF)

    def __str__(self):
        return self.ColorName
    class Meta:
        verbose_name=  "Барааны өнгөний мэдээлэл"
        verbose_name_plural =  "WebSite - Барааны өнгөний мэдээлэл"


class ColorImage(models.Model):
    product = models.ForeignKey('InfoProduct', related_name='color_images', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='products/images/color_variants/', null=True, blank=True)

    def __str__(self):
        return f"Image for {self.product.TCItemNameMongol}"
    class Meta:
        verbose_name=  "Барааны зургууд"
        verbose_name_plural =  "WebSite - Барааны зургууд"


class HardwareCategory(models.Model):
    # item = models.ForeignKey('InfoProductNew', related_name='hardware_categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name=  "Үзүүлэлт төрөл"
        verbose_name_plural =  "WebSite - Үзүүлэлт төрөл"


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='brands/images/', null=True, blank=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name= "Брендүүд"
        verbose_name_plural = "WebSite - Брендүүд"


class HardwareSpecification(models.Model):
    item = models.ForeignKey('InfoProduct', related_name='hardware_specifications', on_delete=models.CASCADE)
    category = models.ForeignKey(HardwareCategory, on_delete=models.CASCADE, related_name='specifications') # ForeignKey to HardwareCategory
    name = models.CharField(max_length=255)  # e.g., I5-4th
    detail = models.CharField(max_length=50, blank=True, null=True)# e.g., "3rd", "4th", "12th"
    description = models.CharField(max_length=255, blank=True, null=True)  # Detailed description

    def __str__(self):
        return f"{self.name} ({self.category})"
    class Meta:
        verbose_name=  "Үзүүлэлт"
        verbose_name_plural =  "WebSite - Үзүүлэлт"


class PromotionalProduct(models.Model):
    main_product = models.ForeignKey(
        "InfoProduct",
        on_delete=models.CASCADE,
        related_name="promo_for"
    )
    promo_product = models.ForeignKey(
        "InfoProduct",
        on_delete=models.CASCADE,
        related_name="promoted_by"
    )
    quantity = models.PositiveIntegerField(default=1, help_text="Урамшууллын барааны тоо хэмжээ")


    def __str__(self):
        return f"{self.main_product.TCItemCode} -> {self.promo_product.TCItemCode} ({self.quantity})"

    class Meta:
        verbose_name=  "Урамшуулалын бараа"
        verbose_name_plural =  "WebSite - Урамшуулалын бараа"


class InfoProduct(models.Model):
    TCItemCode = models.CharField(help_text='Дотоод код-Санхүүгийн код', max_length=50, unique=True)
    TCItemGroupDTLPK = models.ManyToManyField(GroupDTL)
    TCIsView = models.BooleanField(default=False, help_text='Kacc.mn сайт дээр харуулах эсэх')
    # TCItemFactoryCode = models.CharField(max_length=50, null=True, blank=True)
    # TCHsCode = models.CharField(max_length=50, blank=True, null=True)
    TCItemNameMongol = models.CharField(max_length=100, blank=True)
    TCPrice = models.DecimalField(max_digits=50, decimal_places=20, blank=True)
    TCDiscountPrice = models.DecimalField(default=0, max_digits=50, decimal_places=20, blank=True)
    TCDiscountEndDate = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        help_text="Хөнгөлөлт дуусах хугацаа"
    )
    # TCItemNameEnglish = models.CharField(max_length=100, blank=True, null=True)
    # TCItemNameChina = models.CharField(max_length=100, blank=True, null=True)
    # TCItemPadaanName = models.CharField(max_length=100, blank=True, null=True)
    # TCFactoryWarrantyMonth = models.CharField(max_length=10, blank=True, null=True)
    # TCShopWarrantyMonth = models.CharField(max_length=10, blank=True, null=True)
    # TCAccessories = models.CharField(max_length=100, blank=True, null=True)
    TCInvoiceText = HTMLField(default="")
    TCOrderDetailText = HTMLField(default="")
    TCOneBoxQty = models.IntegerField(default=0, blank=True, null=True)
    # TCOneBoxWeight = models.IntegerField(default=0, blank=True, null=True)
    # TCOneBoxHeight = models.IntegerField(default=0, blank=True, null=True)
    # TCOneBoxLength = models.IntegerField(default=1, blank=True)
    # TCOneBoxNetWeightKg = models.DecimalField(max_digits=50, decimal_places=20, blank=True, null=True)
    # TCOneBoxGrossWeightKg = models.DecimalField(max_digits=50, decimal_places=20, blank=True, null=True)
    # TCOneBoxVolumeM3 = models.DecimalField(max_digits=50, decimal_places=20, blank=True, null=True)
    # TCOneTotalCBM = models.DecimalField(max_digits=50, decimal_places=20, blank=True, null=True)
    # TCImage1 = models.ImageField(upload_to='products', null=True, blank=True)
    # TCImage2 = models.ImageField(upload_to='products', null=True, blank=True)
    # TCImage3 = models.ImageField(upload_to='products', null=True, blank=True)
    # TCNote1 = models.TextField(null=True, blank=True)
    # TCUseInstructions = models.CharField(max_length=50, blank=True, null=True)
    TCVideoURL = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(default=now, editable=False)

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products', blank=True,
                              null=True)  # e.g., "Intel", "AMD"

    # Урамшууллын бараа
    promotional_products = models.ManyToManyField(
        "self",
        through="PromotionalProduct",
        symmetrical=False,
        related_name="main_promotions",
        blank=True,
        help_text="Урамшуулалд өгч болох бараанууд"
    )

    # Сэлбэгүүд
    spare_parts = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="used_by",
        blank=True,
        help_text="Сэлбэгийн жагсаалт"
    )

    class Meta:
        indexes = [
            models.Index(fields=['TCItemCode', 'TCItemNameMongol'])
        ]
        verbose_name = "Барааны мэдээлэл"
        verbose_name_plural = "Үндсэн - Барааны мэдээлэл"



    def save(self, *args, **kwargs):
        # If the object is new (no primary key), save it first to get the primary key
        if not self.pk:
            super(InfoProduct, self).save(*args, **kwargs)

        # After saving, aggregate the sum of qty from related colors
        self.TCOneBoxQty = self.color_variants.aggregate(total_qty=Sum('qty'))['total_qty'] or 0

        # Now save the instance again to store the updated TCOneBoxQty
        super(InfoProduct, self).save(*args, **kwargs)

    def recalculate_TCOneBoxQty(self):
        """Recalculate TCOneBoxQty based on the sum of qty in related Color instances."""
        self.TCOneBoxQty = self.color_variants.aggregate(total_qty=Sum('qty'))['total_qty'] or 0
        self.save(update_fields=['TCOneBoxQty'])

    def __str__(self):
        return self.TCItemNameMongol

    def get_color_variants(self):
        return [
            {
                "id": color.pk,
                "item_code": color.item_code,
                "ColorName": color.ColorName,
                "qty": color.qty,
                "hex_value": color.hex_value
            }
            for color in self.color_variants.all()  # Access related Color instances
        ]

    def get_hardware_specifications(self):
        return [
            {
                "id": spec.pk,
                "name": spec.name,
                "description": spec.description,
                "category": {
                    "id": spec.category.pk,
                    "name": spec.category.name,
                },
                "detail": spec.detail
            }
            for spec in self.hardware_specifications.all()  # Access related HardwareSpecification instances
        ]


class ReqLog(models.Model):
    TCInvoiceNum = models.CharField(help_text='TCInvoiceNum', max_length=400, blank=True)
    TCReqMethod = models.CharField(help_text='TCReqMethod', max_length=400, blank=True)
    TCReqUrl = models.CharField(help_text='TCReqUrl', max_length=400, blank=True)
    TCReqBody = models.TextField(help_text='TCReqBody', blank=True)
    TCUser = models.CharField(help_text='TCUser', max_length=400, blank=True)
    TCCreatedDate = models.CharField(help_text='TCCreatedDate', max_length=50, blank=True)
    TCResponse = models.TextField(help_text='TCResponse', blank=True)

    def __str__(self):
        return self.TCInvoiceNum
    class Meta:
        verbose_name=  "API лог мэдээлэл"
        verbose_name_plural =  "Үндсэн - API лог мэдээлэл"


class Location(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name=  "Аймгийн мэдээлэл"
        verbose_name_plural =  "WebSite - Аймгийн мэдээлэл"


class SiteUsers(models.Model):
    USER_TYPE_CHOICES = [
        ('Admin', 'Админ'),
        ('Manager', 'Менежер'),
        ('User', 'Хэрэглэгч'),
    ]
    TCUserName = models.CharField(help_text='Нэр', max_length=150)
    TCEmail = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name='Email Address'
    )
    TCPhoneNumber = models.CharField(help_text='Утасны дугаар', max_length=150, blank=True)
    TCImage = models.ImageField(upload_to='users', null=True, blank=True)
    TCWhishLists = models.ManyToManyField(InfoProduct, blank=True)
    TCPassword = models.CharField(help_text='Нууц үг', max_length=150, blank=True)
    TCUserType = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='User',
        help_text='Хэрэглэгчийн төрөл'
    )

    def __str__(self):
        return self.TCUserName
    class Meta:
        verbose_name=  "WebSite Хэрэглэгчдын бүртгэл"
        verbose_name_plural =  "WebSite - WebSite Хэрэглэгчдын бүртгэл"


class UserAddress(models.Model):
    OPTION_1 = 'Гэр'
    OPTION_2 = 'Ажил'
    OPTION_3 = 'Бусад'

    ADRNAME = [
        (OPTION_1, 'Гэр'),
        (OPTION_2, 'Ажил'),
        (OPTION_3, 'Бусад'),
    ]

    TCUserPk = models.ForeignKey(SiteUsers,  on_delete=CASCADE)
    TCAddressName = models.CharField(max_length=100, choices=ADRNAME)
    TCCityLocation = models.ForeignKey(Location, on_delete=models.CASCADE)
    TCDetailAddress = models.TextField(help_text='Дэлгэрэнгүй Хаяг',  blank=True)
    TCGoogleMapUrl = models.CharField(help_text='TCGoogleMapUrl', max_length=350, blank=True)

    def __str__(self):
        return f"{self.TCUserPk.TCUserName} - {self.TCAddressName}"
    class Meta:
        verbose_name=  "WebSite Хэрэглэгчдын хаяг"
        verbose_name_plural =  "WebSite - WebSite Хэрэглэгчдын хаяг"


class OrderNum(models.Model):
    TCUserPk = models.ForeignKey(SiteUsers,  on_delete=CASCADE)
    order_number = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)
    class Meta:
        verbose_name=  "Захиалгын дугаар"
        verbose_name_plural =  "Үндсэн - Захиалгын дугаар"


class OrderedProduct(models.Model):
    order = models.ForeignKey('UserOrderHistory', on_delete=models.CASCADE)
    product = models.ForeignKey(InfoProduct, on_delete=models.CASCADE)
    selected_color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)  # Add this field
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ['order', 'product', 'selected_color']  # Adjust unique_together constraint

    def __str__(self):
        return f"{self.product} - {self.quantity} pcs"
    class Meta:
        verbose_name=  "Захиалсан бараа"
        verbose_name_plural =  "WebSite - Захиалсан бараа"


class UserOrderHistory(models.Model):
    TCUserPk = models.ForeignKey(SiteUsers, on_delete=models.CASCADE)
    TCOrderNumber = models.CharField(help_text='Order Number', max_length=10, blank=True)
    TCAddress = models.ForeignKey(UserAddress, on_delete=models.CASCADE)
    TCTotalAmount = models.DecimalField(max_digits=50, decimal_places=20, default=0, blank=True)
    TCIsPayed = models.BooleanField(default=False, help_text='Төлбөр төлөгдсөн эсэх')
    TCOrderedProduct = models.ManyToManyField(InfoProduct, through=OrderedProduct)
    TCCreatedDate = models.DateTimeField(default=now, editable=False)
    TCIsCompany = models.BooleanField(default=False, help_text='НӨАТ Компани дээр авах эсэх')
    TCCompanyRd = models.CharField(help_text='Компани регистер', max_length=11, blank=True, null=True)
    TCCompanyName = models.CharField(help_text='Компани нэр', max_length=100, blank=True, null=True)

    # def __str__(self):
    #     return self.TCOrderNumber
    class Meta:
        verbose_name=  "Захиалгын түүх"
        verbose_name_plural =  "WebSite - Захиалгын түүх"


class PDFModel(models.Model):
    pdf_file = models.FileField(upload_to='pdfs/')
    # Add any other fields you need

    def __str__(self):
        return self.pdf_file.name
    class Meta:
        verbose_name=  "PDFModel"
        verbose_name_plural =  "WebSite - PDFModel"


class ProductDownloads(models.Model):
    TCFileName = models.CharField(help_text='Нэр', max_length=150)
    TCProducts = models.ManyToManyField(InfoProduct, blank=True)
    TCFileUrl = models.FileField(upload_to='Downloads')

    def __str__(self):
        return self.TCFileName
    class Meta:
        verbose_name=  "Барааны татах материал"
        verbose_name_plural =  "WebSite - Барааны татах материал"


class SiteSlider(models.Model):
    TCSliderImage = models.ImageField(upload_to='Downloads', null=True, blank=True)

    def __str__(self):
        if self.TCSliderImage:
            return self.TCSliderImage.url
        else:
            return "No Image"

    class Meta:
        verbose_name = "WebSite Нүүр зураг"
        verbose_name_plural = "WebSite - WebSite Нүүр зураг"


class Transaction(models.Model):

    type = models.CharField(
        max_length=20,
        verbose_name="Гүйлгээний төрөл"
    )
    account = models.CharField(
        max_length=20,
        verbose_name="Гүйлгээ хийгдсэн дансны дугаар"
    )
    journalid = models.CharField(
        max_length=50,
        verbose_name="Банкин дахь гүйлгээний дугаар"
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        verbose_name="Мөнгөн дүн"
    )
    posted_date = models.CharField(
        max_length=50,
        verbose_name="Гүйлгээний огноо"
    )
    statement_date = models.CharField(
        max_length=50,
        verbose_name="Хуулганы огноо"
    )
    description = models.CharField(
        max_length=50,
        verbose_name="Гүйлгээний утга"
    )


    def __str__(self):
        return f"{self.type} - {self.account} - {self.amount}"
    class Meta:
        verbose_name = "PayBill Гүйлгээний мэдээлэл"
        verbose_name_plural = "WebSite - PayBill Гүйлгээний мэдээлэл"


class InvoiceNum(models.Model):
    invNum = models.CharField(default=100, max_length=100, unique=True)
    class Meta:
        verbose_name = "Нэхэмжлэл захиалгын дугаар"
        verbose_name_plural = "Нэхэмжлэл - Нэхэмжлэл захиалгын дугаар"


class Advertisement(models.Model):
    version = models.CharField(max_length=50, unique=True, verbose_name="Version")
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='advertisements/', verbose_name="Image")
    link = models.URLField(verbose_name="Redirect Link")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=['title'])  # BranchName талбарт индекс үүсгэх
        ]
        verbose_name = "Мэдэгдэл"
        verbose_name_plural = "WebSite - Мэдэгдэл"


class Partner(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to="partners/logos/", blank=True, null=True)
    description = models.TextField()
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Хамтран ажилласан хэрэглэгчид"
        verbose_name_plural = "WebSite - Хамтран ажилласан хэрэглэгчид"


class PartnerImage(models.Model):
    partner = models.ForeignKey(Partner, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="partners/")

    def __str__(self):
        return f"Image for {self.partner.name}"
    class Meta:
        verbose_name = "Хамтран ажилласан зураг"
        verbose_name_plural = "WebSite - Хамтран ажилласан зураг"


class ProgramInfo(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    contact = models.CharField(max_length=255)
    website_url = models.URLField()
    image = models.ImageField(upload_to='program_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Хамтрагч программ хангамж"
        verbose_name_plural = "WebSite - Хамтрагч программ хангамж"

