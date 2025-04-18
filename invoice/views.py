import base64
import os
import re
from decimal import Decimal
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from decimal import Decimal
import threading
import requests
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import render

from .parsers import XMLParser
from .serializers import *
from datetime import datetime, timedelta

import json
from django.core.exceptions import ValidationError, ObjectDoesNotExist, MultipleObjectsReturned
from rest_framework.views import APIView
from rest_framework import authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db import connection
from django.db.models import F, Q
from django.core.cache import cache
from rest_framework.pagination import PageNumberPagination

import hashlib



def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def index(request):
    return HttpResponse("Hello world!!!")




class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class GroupHDRViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = GroupHDR.objects.all().order_by('-GroupID')
    serializer_class = GroupHDRSerializer
    # permission_classes = [permissions.IsAuthenticated]

class get_GroupHDR(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        queryset = GroupHDR.objects.all()
        # queryset = GroupHDR.objects.filter(FeaturedGroup=True)
        #allData
        selected_fields = []
        for query in queryset:
            group_dtl_data = GroupDTLSerializer(GroupDTL.objects.filter(GroupHDRPk=query.id), many=True).data
            group_dtl_dict = {str(item['id']): item['GroupDTLName'] for item in group_dtl_data}

            cat_img_url = query.GroupImage.url if query.GroupImage else None

            category_data = {
                'catId': query.id,
                'catName': query.GroupName,
                'catImg': f"{base_url}/media/{query.GroupImage}" if query.GroupImage else None,
                'isFeatured': query.FeaturedGroup,
                'isHeader': query.HeaderGroup,
                'isShowMenu': query.ShowMenuGroup,
                'catDtl': [group_dtl_dict],
            }

            selected_fields.append(category_data)
        return JsonResponse({"statusCode": "200", "dtl": selected_fields})


class InfoProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = InfoProduct.objects.all()
    serializer_class = InfoProductSerializer
    # permission_classes = [permissions.IsAuthenticated]


from django.core import serializers


class get_product_detail(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, id):
        product = get_object_or_404(InfoProduct, TCItemCode=id)
        # try:
        #     product = InfoProduct.objects.get(TCItemCode=id)
        # except:
        #     pass
        response = serializers.serialize('python', [product], ensure_ascii=False)
        return JsonResponse(response, safe=False)


class get_InvoiceNumberView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, userId, isNeh):
        current_date_suffix = timezone.now().strftime('%y-%m%d')
        last_invoice = ''
        last_date = ''
        print(isNeh)

        try:
            # Retrieve the latest invoice
            last_invoice = InvoiceNum.objects.latest('invNum')
            last_invoice_number = int(last_invoice.invNum)
        except InvoiceNum.DoesNotExist:
            # Handle the case where there is no previous invoice
            last_invoice_number = 0


        new_invoice_number = last_invoice_number + 1

        last_invoice_numeric = f"{new_invoice_number}" + userId


        last_invoice.invNum = new_invoice_number
        last_invoice.save()

        return Response({"statusCode": "200", "dtl": last_invoice_numeric}, status=200)


# @csrf_exempt
# @require_POST

def TCount(stock_locations):
    total_count_on_hand = 0

    for location in stock_locations:
        total_count_on_hand += location.get("count_on_hand", 0)

    return total_count_on_hand


class LocationListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return JsonResponse({"statusCode": "200", "dtl": serializer.data})


class SiteUserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = SiteUsers.objects.filter(pk=pk)
        serializer = SiteUsersSerializer(user, many=True)
        return JsonResponse({"statusCode": "200", "dtl": serializer.data})


class CreateUserView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SiteUsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"statusCode": "200", "dtl": serializer.data})
        return JsonResponse({'error': 'Invalid JSON data', "body": serializer.errors}, status=400)


class EditUserAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            user = SiteUsers.objects.get(pk=pk)
        except SiteUsers.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)


        serializer = SiteUsersSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"statusCode": "200", "dtl": serializer.data})
        return JsonResponse({'error': 'Invalid JSON data', "body": serializer.errors}, status=400)


class UserAddressListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = UserAddress.objects.filter(TCUserPk=pk)
        serializer = UserAddressSerializer(user, many=True)
        return JsonResponse({"statusCode": "200", "dtl": serializer.data})


class CreateUserAddressAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UserAddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"statusCode": "200", "dtl": serializer.data})
        return JsonResponse({'error': 'Invalid JSON data', "body": serializer.errors}, status=400)


class EditUserAddressAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            address = UserAddress.objects.get(pk=pk)
        except UserAddress.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        serializer = UserAddressSerializer(address, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"statusCode": "200", "dtl": serializer.data})
        return JsonResponse({'error': 'Invalid JSON data', "body": serializer.errors}, status=400)


class DeleteUserAddressAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            user_address = UserAddress.objects.get(pk=pk)
            user_address.delete()
            return JsonResponse({"statusCode": "200", "dtl": "Deleted"})
        except UserAddress.DoesNotExist:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)


class UserOrderHistoryListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if pk == 0:
            # pk==0 үед TCIsPayed=True бүх захиалгыг харуулна
            # user = UserOrderHistory.objects.filter(TCIsPayed=True)
            user = UserOrderHistory.objects.all()
        else:
            # Өөр pk үед TCUserPk=pk захиалгыг харуулна
            user = UserOrderHistory.objects.filter(TCUserPk=pk)

        serializer = UserOrderHistorySerializer(user, many=True)
        return JsonResponse({"statusCode": "200", "dtl": serializer.data})


class CreateUserOrderHistoryAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, *args, **kwargs):
        serializer = UserOrderHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"statusCode": "200", "dtl": serializer.data})
        return JsonResponse({'error': 'Invalid JSON data', "body": serializer.errors}, status=400)


class EditUserOrderHistoryAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, pk, *args, **kwargs):
        try:
            history = UserOrderHistory.objects.get(pk=pk)
        except UserOrderHistory.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        serializer = UserOrderHistorySerializer(history, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"statusCode": "200", "dtl": serializer.data})
        return JsonResponse({'error': 'Invalid JSON data', "body": serializer.errors}, status=400)


class SiteLoginUserAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        user = SiteUsers.objects.filter(TCEmail=email).first()
        if user:
            if user.TCPassword == password:  # Use Django's built-in check_password method
                serializer = SiteUsersSerializer(user)
                return JsonResponse({"statusCode": 200, "dtl": serializer.data})
            else:
                return JsonResponse({"statusCode": 200, "dtl": "Incorrect password"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return JsonResponse({"statusCode": 200, "dtl": "User not found"}, status=status.HTTP_404_NOT_FOUND)



class get_ProductDownloads(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, itemCode):
        # queryset = InfoProduct.objects.all()
        # queryset = ProductDownloads.objects.all()

        print(itemCode)
        if itemCode != 0:
            queryset = ProductDownloads.objects.filter(TCProducts=itemCode).distinct()
            print(list(queryset))
        else:
            queryset = ProductDownloads.objects.none()



        serializer = ProductDownloadsSerializer(queryset, many=True)

        # selected_fields = []




        return JsonResponse({"statusCode": "200", "drivers": serializer.data})


class SiteSliderListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = SiteSlider.objects.all()
        serializer = SiteSliderSerializer(data, many=True)
        return JsonResponse({"statusCode": "200", "dtl": serializer.data})


class DiscountProductsListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = InfoProduct.objects.filter(TCDiscountPrice__gt=0, TCIsView=True)
        promotional_products = InfoProduct.objects.filter(
            Q(promotional_products__isnull=False)
        ).distinct()

        # Хэрэглэгчдийн харах боломжтой эсэхээр шүүх (жишээ нэмэлт)
        visible_promotional_products = promotional_products.filter(TCIsView=True)

        # Үр дүнг хэвлэх
        # for product in visible_promotional_products:
        #     print(product.TCItemNameMongol)
        # serializer = InfoProductSerializer(queryset, many=True)

        # queryset = queryset + visible_promotional_products
        combined_queryset = queryset.union(visible_promotional_products)

        selected_fields = []
        for query in combined_queryset:
            itemPk = query.pk
            group_dtl_list = [
                {
                    'pk': group_dtl.pk,
                }
                for group_dtl in query.TCItemGroupDTLPK.all()
            ]
            # if itemCode != "0":
            related_objects = query.TCItemGroupDTLPK.all()
            if related_objects.exists():
                for obj in related_objects:
                    group_hdr_pk = obj.GroupHDRPk
                group_hdr_pk = group_hdr_pk.pk

            else:
                group_hdr_pk = 0
            # group_hdr = query.TCItemGroupDTLPK.GroupHDRPk if query.TCItemGroupDTLPK else None

            # Extracting pk values from the list of dictionaries
            pk_values = [item['pk'] for item in group_dtl_list]

            if itemPk != 0:
                querysetD = ProductDownloads.objects.filter(TCProducts=itemPk).distinct()
                print(list(querysetD))
            else:
                querysetD = ProductDownloads.objects.none()

            serializerD = ProductDownloadsSerializer(querysetD, many=True)

            # Fetch color images
            color_images = [
                f"{base_url}{color_image.image.url}" for color_image in query.color_images.all() if color_image.image
            ]

            if not color_images and query.TCImage1:  # Fallback to TCImage1
                color_images = [f"{base_url}/media/{query.TCImage1}"]

            # Fetch color variants and hardware specifications
            color_variants = query.get_color_variants()
            hardware_specifications = query.get_hardware_specifications()
            brand_data = BrandSerializer(query.brand).data if query.brand else None
            selected_fields.append({
                'pk': itemPk,
                'itemCode': query.TCItemCode,
                'catId': [group_hdr_pk, [item['pk'] for item in group_dtl_list]],
                'name': query.TCItemNameMongol,
                'price': int(query.TCPrice),
                'discountPrice': int(query.TCDiscountPrice),
                'imgs': color_images,  # Set list of color variant images
                'qty': int(query.TCOneBoxQty),
                'color_variants': color_variants,
                'hardware_specifications': hardware_specifications,
                'brand': brand_data,
                'created_at': query.created_at,
                'tabInfo': [
                    {'title': "Танилцуулга", 'content': query.TCInvoiceText},
                    {'title': "Үзүүлэлт", 'content': query.TCInvoiceText},
                    {'title': "Татах", 'content': serializerD.data},
                ]
            })

        return JsonResponse({"statusCode": "200", "dtl": selected_fields})

        # return Response({"statusCode": "200", "dtl": serializer.data})


def SaveLog(request, response, isNehZar):
    try:
        full_url = request.build_absolute_uri()

        if isNehZar == "TR":
            req_log_data = {
                'TCInvoiceNum': "PayBill Transaction",
                'TCUser': "Admin",
                'TCReqMethod': request.method,
                'TCReqUrl': full_url,
                'TCReqBody': str(response),
                'TCCreatedDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'TCResponse': "Transaction",
            }
        else:

            data = request.data
            if isNehZar == True:
                req_log_data = {
                    'TCInvoiceNum': data['hdr']['TCInvoiceNumber'],
                    'TCUser': data['hdr']['TCCreatedUser'],
                }
            else:
                req_log_data = {
                    'TCInvoiceNum': data['TCIncomingCall'],
                    'TCUser': data['TCUsers'],
                }
            req_log_data.update({
                'TCReqMethod': request.method,
                'TCReqUrl': full_url,
                'TCReqBody': str(data),
                'TCCreatedDate': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
                'TCResponse': str(response),
            })






        serializer = ReqLogSerializer(data=req_log_data)

        if serializer.is_valid():
            log_instance = serializer.save()
        else:
            # Log the error instead of printing
            print("Error saving log: %s", serializer.errors)



    except KeyError as e:
        # Log the specific key error
        print("KeyError: %s", str(e))

    except Exception as e:
        # Log any other unexpected exceptions
        print("Unexpected error: %s", str(e))


@csrf_exempt
def transaction_view(request):
    if request.method == 'POST':
        parser = XMLParser()
        try:
            raw_xml = request.body.decode('utf-8')
            SaveLog(request, raw_xml, "TR")
            data = parser.parse(request)
        except Exception as e:
            return HttpResponseBadRequest(f"Invalid XML data: {str(e)}")

        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            transaction = serializer.save()
            # Response-г түрүүлж буцаах
            response_serializer = TransactionSerializer(transaction)
            response = JsonResponse(response_serializer.data, status=200)

            email_thread = threading.Thread(target=send_transaction_email, args=(transaction,))
            email_thread.start()

            return response
        return JsonResponse(serializer.errors, status=400)
    else:
        return HttpResponseBadRequest("Only POST methods are allowed")


def send_transaction_email(transaction):
    """Мэйл илгээх тусгай функц"""
    subject = "Шинэ гүйлгээний мэдэгдэл"
    text_content = (
        f"Шинэ гүйлгээ амжилттай бүртгэгдлээ.\n\n"
        f"Гүйлгээний дугаар: {transaction.journalid}\n"
        f"Гүйлгээний төрөл: {transaction.type}\n"
        f"Данс: {transaction.account}\n"
        f"Дүн: {transaction.amount}₮\n"
        f"Огноо: {transaction.posted_date}\n"
        f"Тайлбар: {transaction.description}\n\n"
        f"Энэ мэйлд хариу бичих шаардлагагүй."
    )
    html_content = render_to_string('emails/transaction_notification.html', {
        'transaction': transaction  # Context өгөгдөл дамжуулна
    })

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,  # Текст хувилбар
        from_email=settings.EMAIL_HOST_USER,
        to=['info.kaccmn@yahoo.com'],
    )
    email.attach_alternative(html_content, "text/html")  # HTML хувилбар
    email.send()


def format_amount(amount):
    return "{:,.0f}₮".format(amount)
class CheckOrderView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        description = request.query_params.get('TCOrderNumber')
        amount = request.query_params.get('TCTotalAmount')

        if not description:
            return JsonResponse({'error': 'description parameter is required'}, status=400)
        amount = Decimal(amount)



        try:
            order_number_match = re.search(r'\b[A-Z]*-?(\d+[A-Z]*\d*)\b', description)
            if not order_number_match:
                return JsonResponse({'error': 'Valid order number not found'}, status=400)

            order_number = order_number_match.group(1)
            # user_order_history = ""
            if amount:
                print(order_number)
                print(amount)
                user_order_history = Transaction.objects.get(description__icontains=order_number, amount=amount)
            else:
                print(amount)
                user_order_history = Transaction.objects.get(amount=amount)

            # print(user_order_history)
            # return JsonResponse({"status": "success", "data": {"description": user_order_history.description,
            #                                                    "amount": str(user_order_history.amount)}}, status=200)

            if amount < 1000000:
                amount -= Decimal(11000)

            orders = UserOrderHistory.objects.filter(TCOrderNumber__icontains=order_number, TCTotalAmount=amount)
            if orders.exists():
                for order in orders:
                    order.TCIsPayed = True
                    order.save()
                    formatted_total_amount = format_amount(order.TCTotalAmount)

                    # Deduct stock for each ordered product
                    ordered_products = OrderedProduct.objects.filter(order=order)
                    for ordered_product in ordered_products:
                        color_instance = ordered_product.selected_color
                        if color_instance and color_instance.qty >= ordered_product.quantity:
                            color_instance.qty = F('qty') - ordered_product.quantity
                            color_instance.save()

                            product_instance = ordered_product.product
                            product_instance.recalculate_TCOneBoxQty()
                        else:
                            available_qty = color_instance.qty if color_instance else 0
                            return JsonResponse(
                                {
                                    "error": f"Insufficient stock for product {ordered_product.product.pk} - {color_instance.ColorName if color_instance else 'Unknown'}",
                                    "available_qty": available_qty,
                                    "requested_qty": ordered_product.quantity,
                                },
                                status=400
                            )


                response = JsonResponse({"statusCode": "200", "dtl": "Order Confirm"}, status=200)

                # Send email in a separate thread
                email_thread = threading.Thread(target=self.send_order_email, args=(orders,))
                email_thread.start()

                return response
            return JsonResponse({"statusCode": "200", "dtl": "Захиалга олдсонгүй"}, status=200)



        except Transaction.DoesNotExist:
            return JsonResponse({"statusCode": "200", "dtl": "Not Pay"}, status=200)
        except MultipleObjectsReturned:
            return JsonResponse({"error": "Multiple records found for the given description"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)


    def send_order_email(self, orders):
        for order in orders:
            total_amount = order.TCTotalAmount
            if total_amount < 1000000:
                total_amount += 11000

            formatted_total_amount = "{:,.0f}₮".format(total_amount)
            user_email = order.TCUserPk.TCEmail  # Assuming the user email is stored here
            # user_email = "zayalhagva6@gmail.com"
            subject = "Захиалга баталгаажсан"
            html_content = render_to_string('emails/order_confirmation.html', {
                'user_name': order.TCUserPk.TCUserName,
                'order_number': order.TCOrderNumber,
                'total_amount': formatted_total_amount,
            })

            text_content = f"""
            Таны захиалга баталгаажлаа!

            Захиалгын дугаар: {order.TCOrderNumber}
            Нийт дүн: {formatted_total_amount}₮
            """

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[user_email],
                cc=['info.kaccmn@yahoo.com'],  # CC to additional email
            )
            email.attach_alternative(html_content, "text/html")
            email.send()
            print(user_email)


def generate_md5_hash(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()


def convert_datetime_format(date_str):
    if not date_str:
        return None
    try:
        # Attempt to parse the date with space
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        # Convert to ISO format
        return date_obj.isoformat()
    except ValueError:
        return date_str

def process_flight_data(flight_data):
    date_fields = [
        'FlightDeptimePlanDate',
        'FlightArrtimePlanDate',
        'FlightDeptimeReadyDate',
        'FlightArrtimeReadyDate',
        'FlightDeptimeDate',
        'FlightArrtimeDate',
        'FlightIngateTime',
        'FlightOutgateTime'
    ]

    for field in date_fields:
        if field in flight_data:
            flight_data[field] = convert_datetime_format(flight_data[field])

    return flight_data


class InfoProductNewViewSet(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = InfoProduct.objects.all()
    serializer_class = InfoProductSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        info_product = self.get_object()
        serializer = self.get_serializer(info_product)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)

    def update(self, request, pk=None, *args, **kwargs):
        info_product = self.get_object()
        serializer = self.get_serializer(info_product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        info_product = self.get_object()
        self.perform_destroy(info_product)
        return Response(status=204)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    # Define the path to the log file
    log_file_path = os.path.join(os.path.dirname(__file__), 'log.txt')

    # Append the IP address to the log file
    with open(log_file_path, 'a') as log_file:
        log_file.write(f"Client IP Addressd: {ip}\n")

    # Optionally print or return a response
    print(f"Logged IP Address: {ip}")


class get_SiteProductNew(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, itemCode):
        # Cache key for storing the result
        cache_key = f"product_data_{itemCode}"

        # Check if data is in cache
        cached_data = cache.get(cache_key)

        if cached_data:
            # If data is in cache, return cached response
            return Response(cached_data)

        # If data is not in cache, fetch it from database
        queryset = InfoProduct.objects.filter(TCIsView=True).select_related('brand').prefetch_related(
            'TCItemGroupDTLPK', 'color_images')

        if itemCode != "0":
            queryset = queryset.filter(TCItemCode=itemCode)

        selected_fields = []

        for product in queryset:
            itemPk = product.pk

            # Get related group detail primary keys
            group_dtl_list = [{'pk': group_dtl.pk} for group_dtl in product.TCItemGroupDTLPK.all()]
            group_hdr_pk = product.TCItemGroupDTLPK.first().GroupHDRPk.pk if product.TCItemGroupDTLPK.exists() else 0

            # Filter downloads related to the current product
            querysetD = ProductDownloads.objects.filter(
                TCProducts=itemPk).distinct() if itemPk else ProductDownloads.objects.none()
            serializerD = ProductDownloadsSerializer(querysetD, many=True)

            # Fetch color images
            color_images = [
                f"{base_url}{color_image.image.url}" for color_image in product.color_images.all() if color_image.image
            ]

            if not color_images and product.TCImage1:  # Fallback to TCImage1
                color_images = [f"{base_url}/media/{product.TCImage1}"]

            # Fetch color variants and hardware specifications
            color_variants = product.get_color_variants()
            hardware_specifications = product.get_hardware_specifications()
            brand_data = BrandSerializer(product.brand).data if product.brand else None

            # Fetch promotional products and spare parts
            promotional_products = [
                {
                    "TCItemCode": item["promo_product__TCItemCode"],
                    "quantity": item["quantity"]
                }
                for item in
                PromotionalProduct.objects.filter(main_product=product).values("promo_product__TCItemCode", "quantity")
            ]
            spare_parts = list(product.spare_parts.values_list('TCItemCode', flat=True))

            selected_fields.append({
                'pk': itemPk,
                'itemCode': product.TCItemCode,
                'catId': [group_hdr_pk, [item['pk'] for item in group_dtl_list]],
                'name': product.TCItemNameMongol,
                'price': int(product.TCPrice),
                'discountPrice': int(product.TCDiscountPrice),
                'discountEndDate': localtime(
                    product.TCDiscountEndDate).isoformat() if product.TCDiscountEndDate else None,
                'imgs': color_images,  # Set list of color variant images
                'qty': int(product.TCOneBoxQty),
                'color_variants': color_variants,
                'hardware_specifications': hardware_specifications,
                'brand': brand_data,
                'promotionalProducts': promotional_products,
                'spareParts': spare_parts,
                'created_at': product.created_at,
                'tabInfo': [
                    {'title': "Танилцуулга", 'content': product.TCInvoiceText},
                    {'title': "Үзүүлэлт", 'content': product.TCInvoiceText},
                    {'title': "Татах", 'content': serializerD.data},
                ]
            })

        # Store the response in cache for 15 minutes
        cache.set(cache_key, {"statusCode": "200", "dtl": selected_fields}, timeout=60 * 5)

        return Response({"statusCode": "200", "dtl": selected_fields})

class BrandListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdvertisementView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            ad = Advertisement.objects.latest('created_at')  # Хамгийн сүүлд нэмэгдсэн сурталчилгааг авах
            ad_data = {
                "version": ad.version,
                "title": ad.title,
                "description": ad.description,
                "image": request.build_absolute_uri(ad.image.url),
                "link": ad.link,
            }
        except Advertisement.DoesNotExist:
            # Advertisement байхгүй үед тохирох хариу
            ad_data = {
                "error": "No advertisement available"
            }
        return JsonResponse(ad_data)


class PartnerListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        partners = Partner.objects.all()
        serializer = PartnerSerializer(partners, many=True, context={'request': request})
        return Response(serializer.data)


class ProgramInfoAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        programs = ProgramInfo.objects.all()
        serializer = ProgramInfoSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



