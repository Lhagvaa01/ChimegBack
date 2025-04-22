from datetime import datetime

from django.utils.timezone import localtime

from .models import *
from rest_framework import serializers
from collections import OrderedDict
from django.contrib.auth.models import User
from django.conf import settings

# base_url = "https://" + settings.ALLOWED_HOSTS[1] + settings.MEDIA_URL
base_url = "https://" + "api.chimeg.mn"
# base_url = "http://" + "127.0.0.1:8000"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class GroupHDRSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupHDR
        fields = ['id', 'GroupID', 'GroupName', 'FeaturedGroup', 'HeaderGroup']


class GroupDTLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GroupDTL
        fields = ['id', 'GroupDTLName']


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'item_code', 'ColorName', 'qty', 'image', 'hex_value']
        read_only_fields = ['id']

    def get_image(self, obj):
        request = self.context.get('request')
        # Full URL for the image field
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None



class HardwareCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = HardwareCategory
        fields = ['id', 'name']  # Including 'id' for easier referencing


class HardwareSpecificationSerializer(serializers.ModelSerializer):
    # Nested category data in HardwareSpecification
    category = HardwareCategorySerializer()

    class Meta:
        model = HardwareSpecification
        fields = [
            'id',
            'name',
            'description',
            'category',
            'detail'
        ]


class BrandSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Brand
        fields = ['pk', 'name', 'image']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Remove the default `id` field if it exists
        if 'id' in representation:
            del representation['id']

        # Add full URL to image field using base URL
        if 'image' in representation and representation['image']:
            request = self.context.get('request')
            # base_url = request.build_absolute_uri('/') if request else settings.BASE_URL
            representation['image'] = f"{base_url.rstrip('/')}{representation['image']}"

        return representation


class InfoProductSerializer(serializers.ModelSerializer):
    color_variants = ColorSerializer(many=True, read_only=True)
    hardware_specifications = HardwareSpecificationSerializer(many=True, read_only=True)
    brand = BrandSerializer()

    class Meta:
        model = InfoProduct
        fields = [
            'TCItemNameMongol', 'TCPrice', 'TCDiscountPrice', 'TCItemNameEnglish',
            'TCItemNameChina', 'TCHsCode', 'TCInvoiceText', 'TCOrderDetailText',
            'TCFactoryWarrantyMonth', 'TCShopWarrantyMonth', 'TCAccessories',
            'TCOneBoxQty', 'TCNote1', 'created_at', 'hardware_specifications', 'brand'  # Correct field name here
        ]


    def create(self, validated_data):
        # Handling nested 'color_variants' creation
        color_variants_data = validated_data.pop('color_variants', [])
        hardware_specifications_data = validated_data.pop('hardware_specifications', [])

        product = InfoProduct.objects.create(**validated_data)

        # Create Color instances
        # for color_data in color_variants_data:
        #     Color.objects.create(item=product, **color_data)

        # Create HardwareSpecification instances if needed
        for spec_data in hardware_specifications_data:
            HardwareSpecification.objects.create(item=product, **spec_data)

        return product

    def update(self, instance, validated_data):
        color_variants_data = validated_data.pop('color_variants', [])
        hardware_specifications_data = validated_data.pop('hardware_specifications', [])

        # Update main fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update color variants
        for color_data in color_variants_data:
            color_variant = Color.objects.get(id=color_data['id'], item=instance)
            color_variant.qty = color_data.get('qty', color_variant.qty)  # Update qty
            color_variant.save()

        # Update hardware specifications
        for spec_data in hardware_specifications_data:
            spec_variant = HardwareSpecification.objects.get(id=spec_data['id'], item=instance)
            spec_variant.name = spec_data.get('name', spec_variant.name)
            spec_variant.description = spec_data.get('description', spec_variant.description)
            spec_variant.detail = spec_data.get('detail', spec_variant.detail)
            spec_variant.category_id = spec_data['category']['id']  # Assuming category is being updated
            spec_variant.save()

        return instance


class ReqLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReqLog
        fields = '__all__'

    def save(self, **kwargs):
        # Set TCCreatedDate to the current local date and time if not provided
        if not self.validated_data.get('TCCreatedDate'):
            self.validated_data['TCCreatedDate'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')

        return super().save(**kwargs)

    def to_representation(self, instance):
        # Use OrderedDict to control the order of fields in the JSON response
        ordered_representation = OrderedDict([
            ("pk", instance.pk),
            ("TCInvoiceNum", instance.TCInvoiceNum),
            ("TCReqMethod", instance.TCReqMethod),
            ("TCReqUrl", instance.TCReqUrl),
            ("TCReqBody", instance.TCReqBody),
            ("TCUser", instance.TCUser),
            ("TCCreatedDate", instance.TCCreatedDate),
            ("TCResponse", instance.TCResponse),
        ])

        return ordered_representation


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class SiteUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUsers
        fields = '__all__'

    def to_representation(self, instance):
        ordered_representation = {
            "id": instance.pk,
            "TCUserName": instance.TCUserName,
            "TCEmail": instance.TCEmail,
            "TCPhoneNumber": instance.TCPhoneNumber,
            "TCImage": f"{base_url}{instance.TCImage}" if instance.TCImage else None,
            "TCPassword": instance.TCPassword,
            "TCWhishLists": list(instance.TCWhishLists.values_list('pk', flat=True)),
            "TCUserType": instance.TCUserType,
        }

        return ordered_representation


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAddress
        fields = '__all__'


class OrderNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderNum
        fields = '__all__'


def generate_order_number():
    # Generate a unique identifier
    unique_id = uuid.uuid4().hex[:4]  # Using the first 8 characters of a UUID

    random_letter = random.choice(string.ascii_letters)

    # Combine the timestamp, unique ID, and random digits to form the order number
    order_number = f'{unique_id}{random_letter}'
    # UserOrderHistory.activate_orders()

    return order_number


class OrderedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedProduct
        fields = ['product', 'quantity', 'selected_color']


class UserOrderHistorySerializer(serializers.ModelSerializer):
    TCOrderedProduct = OrderedProductSerializer(many=True, source='orderedproduct_set', read_only=True)

    class Meta:
        model = UserOrderHistory
        fields = '__all__'

    def create(self, validated_data):
        # Set default values for the creation date if not provided
        validated_data.setdefault('TCCreatedDate', timezone.now().strftime('%Y-%m-%d %H:%M:%S'))

        # Retrieve ordered products data from the initial request data
        ordered_products_data = self.initial_data.get('TCOrderedProduct')

        # Create the main UserOrderHistory record
        user_order_history = UserOrderHistory.objects.create(**validated_data)

        # Loop through each ordered product data and create OrderedProduct entries
        for ordered_product_data in ordered_products_data:
            product_id = ordered_product_data.pop('product')  # item_code of the product
            quantity = ordered_product_data.get('quantity')

            try:
                # Retrieve the InfoProduct instance by matching the color's item_code
                color_instance = Color.objects.get(item_code=product_id)
                product_instance = color_instance.item  # Get the related InfoProduct
            except Color.DoesNotExist:
                raise serializers.ValidationError(f"Product with item code {product_id} does not exist.")

            # Check stock availability
            if color_instance.qty < quantity:
                raise serializers.ValidationError(
                    f"Not enough stock for product '{product_id}'. Available: {color_instance.qty}, requested: {quantity}")

            # Create the OrderedProduct and reduce the stock for the color variant
            OrderedProduct.objects.create(order=user_order_history, product=product_instance,
                                          selected_color=color_instance, quantity=quantity)
            color_instance.qty -= quantity
            color_instance.save()

        return user_order_history

    def to_representation(self, instance):
        # Customize the representation of the UserOrderHistory instance
        ordered_representation = {
            "pk": instance.pk,
            "TCUserPk": instance.TCUserPk.pk,
            "TCOrderNumber": instance.TCOrderNumber,
            "TCAddress": instance.TCAddress.pk,
            "TCTotalAmount": instance.TCTotalAmount,
            "TCIsPayed": instance.TCIsPayed,
            "TCIsCompany": instance.TCIsCompany,
            "TCCompanyRd": instance.TCCompanyRd,
            "TCCompanyName": instance.TCCompanyName,
            "TCOrderedProduct": [
                {
                    "productId": item.product.pk,
                    "productColor": item.selected_color.ColorName if item.selected_color else None,
                    "quantity": item.quantity,
                }
                for item in instance.orderedproduct_set.all()
            ],
            "TCCreatedDate": instance.TCCreatedDate,
        }
        return ordered_representation


class ProductDownloadsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductDownloads
        fields = '__all__'

    def to_representation(self, instance):
        # Use OrderedDict to control the order of fields in the JSON response
        ordered_representation = OrderedDict([
            ("pk", instance.pk),
            ("TCFileName", instance.TCFileName),
            ("TCProducts", list(instance.TCProducts.values_list('pk', flat=True))),
            ("TCFileUrl", f"{base_url}/media/{instance.TCFileUrl}" if instance.TCFileUrl else None)

        ])

        return ordered_representation


class SiteSliderSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSlider
        fields = '__all__'

    def to_representation(self, instance):
        ordered_representation = OrderedDict([
            ("pk", instance.pk),
            ("TCFileUrl", f"{base_url}/media/{instance.TCSliderImage}" if instance.TCSliderImage else None)

        ])

        return ordered_representation


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'type', 'account', 'journalid', 'amount',
            'posted_date', 'statement_date', 'description'

        ]


class InvoiceNumSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceNum
        fields = ['pk', 'invNum']


class PartnerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnerImage
        fields = ['image']


class PartnerSerializer(serializers.ModelSerializer):
    images = PartnerImageSerializer(many=True, read_only=True)

    class Meta:
        model = Partner
        fields = ['id', 'name', 'logo', 'description', 'website', 'created_at', 'images']


class ProgramInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramInfo
        fields = ['name', 'description', 'contact', 'website_url', 'image']
