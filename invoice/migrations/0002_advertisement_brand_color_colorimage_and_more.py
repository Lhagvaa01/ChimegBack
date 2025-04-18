# Generated by Django 5.0.4 on 2025-04-18 07:52

import django.db.models.deletion
import django.utils.timezone
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.CharField(max_length=50, unique=True, verbose_name='Version')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.TextField(verbose_name='Description')),
                ('image', models.ImageField(upload_to='advertisements/', verbose_name='Image')),
                ('link', models.URLField(verbose_name='Redirect Link')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
            ],
            options={
                'verbose_name': 'Мэдэгдэл',
                'verbose_name_plural': 'WebSite - Мэдэгдэл',
            },
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='brands/images/')),
            ],
            options={
                'verbose_name': 'Брендүүд',
                'verbose_name_plural': 'WebSite - Брендүүд',
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_code', models.CharField(max_length=50, unique=True)),
                ('ColorName', models.CharField(max_length=50)),
                ('qty', models.IntegerField(default=0)),
                ('hex_value', models.CharField(max_length=7)),
            ],
            options={
                'verbose_name': 'Барааны өнгөний мэдээлэл',
                'verbose_name_plural': 'WebSite - Барааны өнгөний мэдээлэл',
            },
        ),
        migrations.CreateModel(
            name='ColorImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='products/images/color_variants/')),
            ],
            options={
                'verbose_name': 'Барааны зургууд',
                'verbose_name_plural': 'WebSite - Барааны зургууд',
            },
        ),
        migrations.CreateModel(
            name='HardwareCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Үзүүлэлт төрөл',
                'verbose_name_plural': 'WebSite - Үзүүлэлт төрөл',
            },
        ),
        migrations.CreateModel(
            name='HardwareSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('detail', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'verbose_name': 'Үзүүлэлт',
                'verbose_name_plural': 'WebSite - Үзүүлэлт',
            },
        ),
        migrations.CreateModel(
            name='InvoiceNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invNum', models.CharField(default=100, max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Нэхэмжлэл захиалгын дугаар',
                'verbose_name_plural': 'Нэхэмжлэл - Нэхэмжлэл захиалгын дугаар',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Аймгийн мэдээлэл',
                'verbose_name_plural': 'WebSite - Аймгийн мэдээлэл',
            },
        ),
        migrations.CreateModel(
            name='OrderedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
            ],
            options={
                'verbose_name': 'Захиалсан бараа',
                'verbose_name_plural': 'WebSite - Захиалсан бараа',
            },
        ),
        migrations.CreateModel(
            name='OrderNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Захиалгын дугаар',
                'verbose_name_plural': 'Үндсэн - Захиалгын дугаар',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ImageField(blank=True, null=True, upload_to='partners/logos/')),
                ('description', models.TextField()),
                ('website', models.URLField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Хамтран ажилласан хэрэглэгчид',
                'verbose_name_plural': 'WebSite - Хамтран ажилласан хэрэглэгчид',
            },
        ),
        migrations.CreateModel(
            name='PartnerImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='partners/')),
            ],
            options={
                'verbose_name': 'Хамтран ажилласан зураг',
                'verbose_name_plural': 'WebSite - Хамтран ажилласан зураг',
            },
        ),
        migrations.CreateModel(
            name='PDFModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='pdfs/')),
            ],
            options={
                'verbose_name': 'PDFModel',
                'verbose_name_plural': 'WebSite - PDFModel',
            },
        ),
        migrations.CreateModel(
            name='ProductDownloads',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TCFileName', models.CharField(help_text='Нэр', max_length=150)),
                ('TCFileUrl', models.FileField(upload_to='Downloads')),
            ],
            options={
                'verbose_name': 'Барааны татах материал',
                'verbose_name_plural': 'WebSite - Барааны татах материал',
            },
        ),
        migrations.CreateModel(
            name='ProgramInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('contact', models.CharField(max_length=255)),
                ('website_url', models.URLField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='program_images/')),
            ],
            options={
                'verbose_name': 'Хамтрагч программ хангамж',
                'verbose_name_plural': 'WebSite - Хамтрагч программ хангамж',
            },
        ),
        migrations.CreateModel(
            name='PromotionalProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, help_text='Урамшууллын барааны тоо хэмжээ')),
            ],
            options={
                'verbose_name': 'Урамшуулалын бараа',
                'verbose_name_plural': 'WebSite - Урамшуулалын бараа',
            },
        ),
        migrations.CreateModel(
            name='SiteSlider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TCSliderImage', models.ImageField(blank=True, null=True, upload_to='Downloads')),
            ],
            options={
                'verbose_name': 'WebSite Нүүр зураг',
                'verbose_name_plural': 'WebSite - WebSite Нүүр зураг',
            },
        ),
        migrations.CreateModel(
            name='SiteUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TCUserName', models.CharField(help_text='Нэр', max_length=150)),
                ('TCEmail', models.EmailField(max_length=100, unique=True, verbose_name='Email Address')),
                ('TCPhoneNumber', models.CharField(blank=True, help_text='Утасны дугаар', max_length=150)),
                ('TCImage', models.ImageField(blank=True, null=True, upload_to='users')),
                ('TCPassword', models.CharField(blank=True, help_text='Нууц үг', max_length=150)),
                ('TCUserType', models.CharField(choices=[('Admin', 'Админ'), ('Manager', 'Менежер'), ('User', 'Хэрэглэгч')], default='User', help_text='Хэрэглэгчийн төрөл', max_length=10)),
            ],
            options={
                'verbose_name': 'WebSite Хэрэглэгчдын бүртгэл',
                'verbose_name_plural': 'WebSite - WebSite Хэрэглэгчдын бүртгэл',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=20, verbose_name='Гүйлгээний төрөл')),
                ('account', models.CharField(max_length=20, verbose_name='Гүйлгээ хийгдсэн дансны дугаар')),
                ('journalid', models.CharField(max_length=50, verbose_name='Банкин дахь гүйлгээний дугаар')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Мөнгөн дүн')),
                ('posted_date', models.CharField(max_length=50, verbose_name='Гүйлгээний огноо')),
                ('statement_date', models.CharField(max_length=50, verbose_name='Хуулганы огноо')),
                ('description', models.CharField(max_length=50, verbose_name='Гүйлгээний утга')),
            ],
            options={
                'verbose_name': 'PayBill Гүйлгээний мэдээлэл',
                'verbose_name_plural': 'WebSite - PayBill Гүйлгээний мэдээлэл',
            },
        ),
        migrations.CreateModel(
            name='UserAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TCAddressName', models.CharField(choices=[('Гэр', 'Гэр'), ('Ажил', 'Ажил'), ('Бусад', 'Бусад')], max_length=100)),
                ('TCDetailAddress', models.TextField(blank=True, help_text='Дэлгэрэнгүй Хаяг')),
                ('TCGoogleMapUrl', models.CharField(blank=True, help_text='TCGoogleMapUrl', max_length=350)),
            ],
            options={
                'verbose_name': 'WebSite Хэрэглэгчдын хаяг',
                'verbose_name_plural': 'WebSite - WebSite Хэрэглэгчдын хаяг',
            },
        ),
        migrations.CreateModel(
            name='UserOrderHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TCOrderNumber', models.CharField(blank=True, help_text='Order Number', max_length=10)),
                ('TCTotalAmount', models.DecimalField(blank=True, decimal_places=20, default=0, max_digits=50)),
                ('TCIsPayed', models.BooleanField(default=False, help_text='Төлбөр төлөгдсөн эсэх')),
                ('TCCreatedDate', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('TCIsCompany', models.BooleanField(default=False, help_text='НӨАТ Компани дээр авах эсэх')),
                ('TCCompanyRd', models.CharField(blank=True, help_text='Компани регистер', max_length=11, null=True)),
                ('TCCompanyName', models.CharField(blank=True, help_text='Компани нэр', max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Захиалгын түүх',
                'verbose_name_plural': 'WebSite - Захиалгын түүх',
            },
        ),
        migrations.RemoveField(
            model_name='callregdtl',
            name='TCCallReasonTypePk',
        ),
        migrations.RemoveField(
            model_name='callregdtl',
            name='TCCallTypeNamePk',
        ),
        migrations.RemoveField(
            model_name='zarlagahdr',
            name='TCInfoBranchPk',
        ),
        migrations.RemoveField(
            model_name='nehemjlelhdr',
            name='TCInfoBranchPk',
        ),
        migrations.RemoveField(
            model_name='zarlagahdr',
            name='TCInfoEmployeePk',
        ),
        migrations.RemoveField(
            model_name='nehemjlelhdr',
            name='TCInfoEmployeePk',
        ),
        migrations.RemoveField(
            model_name='zarlagahdr',
            name='TCInfoPaymentTypePk',
        ),
        migrations.RemoveField(
            model_name='nehemjlelhdr',
            name='TCInfoPaymentTypePk',
        ),
        migrations.RemoveField(
            model_name='zarlagahdr',
            name='TCInfoCustomersPk',
        ),
        migrations.RemoveField(
            model_name='nehemjlelhdr',
            name='TCInfoCustomersPk',
        ),
        migrations.RemoveField(
            model_name='zarlagahdr',
            name='TCInvoiceSettingsPk',
        ),
        migrations.RemoveField(
            model_name='nehemjlelhdr',
            name='TCInvoiceSettingsPk',
        ),
        migrations.RemoveField(
            model_name='nehemjleldtl',
            name='TCNehemjlelNewHdrPk',
        ),
        migrations.RemoveField(
            model_name='nehemjleldtl',
            name='TCProductPk',
        ),
        migrations.DeleteModel(
            name='SystemMenu',
        ),
        migrations.DeleteModel(
            name='SystemMenuDtl',
        ),
        migrations.DeleteModel(
            name='SystemNames',
        ),
        migrations.DeleteModel(
            name='Users',
        ),
        migrations.RemoveField(
            model_name='zarlagadtl',
            name='TCProductPk',
        ),
        migrations.RemoveField(
            model_name='zarlagadtl',
            name='TCZarlagaHdrPk',
        ),
        migrations.AlterModelOptions(
            name='groupdtl',
            options={'verbose_name': 'Барааны бүрэг Detail', 'verbose_name_plural': 'WebSite - Барааны бүрэг Detail'},
        ),
        migrations.AlterModelOptions(
            name='grouphdr',
            options={'verbose_name': 'Барааны бүрэг Header', 'verbose_name_plural': 'WebSite - Барааны бүрэг Header'},
        ),
        migrations.AlterModelOptions(
            name='infoproduct',
            options={'verbose_name': 'Барааны мэдээлэл', 'verbose_name_plural': 'Үндсэн - Барааны мэдээлэл'},
        ),
        migrations.AlterModelOptions(
            name='reqlog',
            options={'verbose_name': 'API лог мэдээлэл', 'verbose_name_plural': 'Үндсэн - API лог мэдээлэл'},
        ),
        migrations.RenameField(
            model_name='infoproduct',
            old_name='TCItemGrossWeight',
            new_name='TCOneBoxGrossWeightKg',
        ),
        migrations.RenameField(
            model_name='infoproduct',
            old_name='TCItemNetWeight',
            new_name='TCOneBoxNetWeightKg',
        ),
        migrations.RemoveField(
            model_name='infoproduct',
            name='TCOneBoxlength',
        ),
        migrations.AddField(
            model_name='grouphdr',
            name='FeaturedGroup',
            field=models.BooleanField(default=True, help_text='Kacc.mn сайт дээр онцлох эсэх'),
        ),
        migrations.AddField(
            model_name='grouphdr',
            name='GroupImage',
            field=models.ImageField(blank=True, null=True, upload_to='group'),
        ),
        migrations.AddField(
            model_name='grouphdr',
            name='HeaderGroup',
            field=models.BooleanField(default=True, help_text='Kacc.mn сайт дээр Header дээр харуулах'),
        ),
        migrations.AddField(
            model_name='grouphdr',
            name='ShowMenuGroup',
            field=models.BooleanField(default=False, help_text='Kacc.mn сайт дээр Menu дээр харуулах'),
        ),
        migrations.AddField(
            model_name='infoproduct',
            name='TCDiscountEndDate',
            field=models.DateTimeField(blank=True, default=None, help_text='Хөнгөлөлт дуусах хугацаа', null=True),
        ),
        migrations.AddField(
            model_name='infoproduct',
            name='TCDiscountPrice',
            field=models.DecimalField(blank=True, decimal_places=20, default=0, max_digits=50),
        ),
        migrations.AddField(
            model_name='infoproduct',
            name='TCItemGroupDTLPK',
            field=models.ManyToManyField(to='invoice.groupdtl'),
        ),
        migrations.AddField(
            model_name='infoproduct',
            name='TCOneBoxVolumeM3',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=50, null=True),
        ),
        migrations.AddField(
            model_name='infoproduct',
            name='spare_parts',
            field=models.ManyToManyField(blank=True, help_text='Сэлбэгийн жагсаалт', related_name='used_by', to='invoice.infoproduct'),
        ),
        migrations.AlterField(
            model_name='infoproduct',
            name='TCInvoiceText',
            field=tinymce.models.HTMLField(default=''),
        ),
        migrations.AlterField(
            model_name='infoproduct',
            name='TCIsView',
            field=models.BooleanField(default=False, help_text='Kacc.mn сайт дээр харуулах эсэх'),
        ),
        migrations.AlterField(
            model_name='infoproduct',
            name='TCItemCode',
            field=models.CharField(help_text='Дотоод код-Санхүүгийн код', max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='infoproduct',
            name='TCOneBoxHeight',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='infoproduct',
            name='TCOneBoxWeight',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='infoproduct',
            name='TCOrderDetailText',
            field=tinymce.models.HTMLField(default=''),
        ),
        migrations.AddIndex(
            model_name='advertisement',
            index=models.Index(fields=['title'], name='invoice_adv_title_230f22_idx'),
        ),
        migrations.AddField(
            model_name='infoproduct',
            name='brand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='products', to='invoice.brand'),
        ),
        migrations.AddField(
            model_name='color',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='color_variants', to='invoice.infoproduct'),
        ),
        migrations.AddField(
            model_name='colorimage',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='color_images', to='invoice.infoproduct'),
        ),
        migrations.AddField(
            model_name='hardwarespecification',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='invoice.hardwarecategory'),
        ),
        migrations.AddField(
            model_name='hardwarespecification',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hardware_specifications', to='invoice.infoproduct'),
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.infoproduct'),
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='selected_color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.color'),
        ),
        migrations.AddField(
            model_name='partnerimage',
            name='partner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='invoice.partner'),
        ),
        migrations.AddField(
            model_name='productdownloads',
            name='TCProducts',
            field=models.ManyToManyField(blank=True, to='invoice.infoproduct'),
        ),
        migrations.AddField(
            model_name='promotionalproduct',
            name='main_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promo_for', to='invoice.infoproduct'),
        ),
        migrations.AddField(
            model_name='promotionalproduct',
            name='promo_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='promoted_by', to='invoice.infoproduct'),
        ),
        migrations.AddField(
            model_name='infoproduct',
            name='promotional_products',
            field=models.ManyToManyField(blank=True, help_text='Урамшуулалд өгч болох бараанууд', related_name='main_promotions', through='invoice.PromotionalProduct', to='invoice.infoproduct'),
        ),
        migrations.AddIndex(
            model_name='infoproduct',
            index=models.Index(fields=['TCItemCode', 'TCItemNameMongol'], name='invoice_inf_TCItemC_644b34_idx'),
        ),
        migrations.AddField(
            model_name='siteusers',
            name='TCWhishLists',
            field=models.ManyToManyField(blank=True, to='invoice.infoproduct'),
        ),
        migrations.AddField(
            model_name='ordernum',
            name='TCUserPk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.siteusers'),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='TCCityLocation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.location'),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='TCUserPk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.siteusers'),
        ),
        migrations.AddField(
            model_name='userorderhistory',
            name='TCAddress',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.useraddress'),
        ),
        migrations.AddField(
            model_name='userorderhistory',
            name='TCOrderedProduct',
            field=models.ManyToManyField(through='invoice.OrderedProduct', to='invoice.infoproduct'),
        ),
        migrations.AddField(
            model_name='userorderhistory',
            name='TCUserPk',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.siteusers'),
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='invoice.userorderhistory'),
        ),
        migrations.DeleteModel(
            name='CallReasonType',
        ),
        migrations.DeleteModel(
            name='CallRegDtl',
        ),
        migrations.DeleteModel(
            name='CallType',
        ),
        migrations.DeleteModel(
            name='InfoBranch',
        ),
        migrations.DeleteModel(
            name='InfoEmployee',
        ),
        migrations.DeleteModel(
            name='InfoPaymentType',
        ),
        migrations.DeleteModel(
            name='InfoShopCustomers',
        ),
        migrations.DeleteModel(
            name='InvoiceSettings',
        ),
        migrations.DeleteModel(
            name='NehemjlelHdr',
        ),
        migrations.DeleteModel(
            name='NehemjlelDtl',
        ),
        migrations.DeleteModel(
            name='ZarlagaDtl',
        ),
        migrations.DeleteModel(
            name='ZarlagaHdr',
        ),
        migrations.AddField(
            model_name='infoproduct',
            name='TCOneBoxLength',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
