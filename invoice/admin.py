from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import *

# base_url = "https://" + "invoice.kacc.mn"
base_url = "http://" + "localhost:3030"
class GroupHDRAdmin(admin.ModelAdmin):
    model = GroupHDR
    list_display = ['GroupName', 'HeaderGroup', 'FeaturedGroup']
    search_fields = ['GroupName', 'HeaderGroup', 'FeaturedGroup']
    list_filter = ['HeaderGroup', 'FeaturedGroup']


admin.site.register(GroupHDR, GroupHDRAdmin)


class GroupDTLAdmin(admin.ModelAdmin):
    model = GroupDTL
    list_display = ['GroupHDRPk', 'id', 'GroupDTLName']
    search_fields = ['GroupHDRPk', 'id', 'GroupDTLName']


admin.site.register(GroupDTL, GroupDTLAdmin)



class ColorInline(admin.TabularInline):
    model = Color
    extra = 1  # Number of empty forms to display


class ReqLogAdmin(admin.ModelAdmin):
    model = ReqLog
    list_display = ['TCInvoiceNum', 'TCReqMethod', 'TCReqUrl', 'TCCreatedDate', 'TCResponse', 'TCUser']
    search_fields = ['TCInvoiceNum', 'TCReqMethod', 'TCReqUrl', 'TCCreatedDate', 'TCResponse', 'TCUser']


admin.site.register(ReqLog, ReqLogAdmin)


class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = ['name']
    search_fields = ['name']


admin.site.register(Location, LocationAdmin)


class SiteUsersAdmin(admin.ModelAdmin):
    model = SiteUsers
    list_display = ['TCUserName', 'TCEmail', 'TCPhoneNumber']
    search_fields = ['TCUserName', 'TCEmail', 'TCPhoneNumber']


admin.site.register(SiteUsers, SiteUsersAdmin)


class UserAddressAdmin(admin.ModelAdmin):
    model = UserAddress
    list_display = ['get_user_name', 'TCAddressName', 'TCCityLocation', 'TCDetailAddress', 'TCGoogleMapUrl']
    search_fields = ['TCUserPk__TCUserName', 'TCAddressName', 'TCCityLocation', 'TCDetailAddress', 'TCGoogleMapUrl']
    list_filter = ['TCUserPk__TCUserName', 'TCAddressName']
    def get_user_name(self, obj):
        return obj.TCUserPk.TCUserName

    get_user_name.short_description = 'User Name'


admin.site.register(UserAddress, UserAddressAdmin)


class UserOrderHistoryAdmin(admin.ModelAdmin):
    model = UserOrderHistory
    list_display = ('get_user_name', 'TCOrderNumber', 'get_address_name', 'TCTotalAmount', 'TCIsPayed', 'TCIsCompany', 'TCOrderedProducts', 'TCCreatedDate')
    list_filter = ('TCIsPayed', 'TCIsCompany', 'TCUserPk__TCUserName')
    search_fields = ('TCOrderNumber', 'TCUserPk__TCUserName', 'TCTotalAmount')
    readonly_fields = (
    'pk', 'TCUserPk', 'TCOrderNumber', 'TCAddress', 'TCOrderedProducts', 'TCCreatedDate', 'TCTotalAmount')

    def TCOrderedProducts(self, obj):
        return ", ".join([str(product.TCItemCode) for product in obj.TCOrderedProduct.all()])

    TCOrderedProducts.short_description = "Ordered Products"


    def get_user_name(self, obj):
        return obj.TCUserPk.TCUserName

    get_user_name.short_description = 'User Name'

    def get_address_name(self, obj):
        return obj.TCAddress.TCDetailAddress

    get_address_name.short_description = 'Detail Address Name'



admin.site.register(UserOrderHistory, UserOrderHistoryAdmin)


class PDFModelAdmin(admin.ModelAdmin):
    model = PDFModel
    list_display = ['pdf_file']


admin.site.register(PDFModel, PDFModelAdmin)


class ProductDownloadsAdmin(admin.ModelAdmin):
    list_display = ('TCFileName', 'get_TCProducts_details', 'TCFileUrl')
    search_fields = ('TCFileName', 'TCProducts__TCItemCode')
    list_filter = ('TCProducts',)
    filter_horizontal = ('TCProducts',)

    def get_TCProducts_details(self, obj):
        return ", ".join([f"{product.TCItemCode} - {product.TCItemNameMongol}" for product in obj.TCProducts.all()])

    get_TCProducts_details.short_description = 'Product Details'


admin.site.register(ProductDownloads, ProductDownloadsAdmin)


class SiteSliderAdmin(admin.ModelAdmin):
    list_display = ('id', 'TCSliderImage')
    search_fields = ('TCSliderImage',)


admin.site.register(SiteSlider, SiteSliderAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'description', 'type', 'account', 'journalid', 'amount',
        'posted_date', 'statement_date'
    )
    search_fields = ('type', 'account', 'journalid', 'description')
    list_filter = ('type', 'posted_date', 'statement_date')
    ordering = ('-posted_date',)

admin.site.register(Transaction, TransactionAdmin)


class InvoiceNumAdmin(admin.ModelAdmin):
    list_display = ('pk', 'invNum')


admin.site.register(InvoiceNum, InvoiceNumAdmin)


class HardwareCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Brand, BrandAdmin)


class PartnerImageInline(admin.TabularInline):
    model = PartnerImage
    extra = 1


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'created_at', 'logo_preview')
    search_fields = ('name', 'description')
    inlines = [PartnerImageInline]

    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="width: 50px; height: auto;" />',
                base_url + obj.logo.url
            )
        return "No Logo"

    logo_preview.allow_tags = True
    logo_preview.short_description = "Logo"


admin.site.register(Partner, PartnerAdmin)


class ColorImageInline(admin.TabularInline):
    model = ColorImage
    extra = 1  # Adjust as needed


class ColorInline(admin.TabularInline):
    model = Color
    extra = 1
    fields = ('ColorName', 'item_code', 'qty', 'hex_value')  # Exclude 'image' from here


class HardwareSpecificationInline(admin.TabularInline):
    model = HardwareSpecification
    extra = 1
    # Optional: Customize fields to display in the inline form
    fields = ('category', 'name',  'detail', 'description')  # Adjust as needed


class PromotionalProductInline(admin.TabularInline):
    model = PromotionalProduct
    fk_name = 'main_product'
    extra = 1


class SparePartInline(admin.TabularInline):
    model = InfoProduct.spare_parts.through
    fk_name = "from_infoproduct"  # Үндсэн барааны гадаад түлхүүрийг заана
    extra = 1
    verbose_name = "Сэлбэг"
    verbose_name_plural = "Сэлбэгүүд"
    list_filter = ['InfoProduct__TCItemNameMongol', 'InfoProduct__TCItemCode']


class InfoProductAdmin(admin.ModelAdmin):
    list_display = (
        'TCItemNameMongol',
        'TCPrice',
        'TCIsView',
        'created_at'
    )
    search_fields = ('TCItemCode', 'TCItemNameMongol', 'TCItemNameEnglish', 'TCItemNameChina')
    list_filter = ('TCIsView',)
    inlines = [ColorInline, ColorImageInline, HardwareSpecificationInline, PromotionalProductInline, SparePartInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('color_variants', 'hardware_specifications')

admin.site.register(InfoProduct, InfoProductAdmin)


admin.site.register(HardwareCategory, HardwareCategoryAdmin)

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'created_at', 'updated_at')
    search_fields = ('title', 'version')
    list_filter = ('created_at',)
admin.site.register(Advertisement, AdvertisementAdmin)


class ProgramInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'website_url')
    search_fields = ('name', 'description')
admin.site.register(ProgramInfo, ProgramInfoAdmin)

class MetalRateAdmin(admin.ModelAdmin):
    list_display = ('metal', 'rate', 'updated_at')
    search_fields = ('metal', 'rate')
admin.site.register(MetalRate, MetalRateAdmin)
