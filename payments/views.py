from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .forms import CheckoutForm, CouponForm, PaymentForm
from django.core.exceptions import ObjectDoesNotExist
from items.models import Item
from orders.models import OrderItem, Order
from accounts.models import Address
import random
import string
import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages
from accounts.models import UserProfile
from .models import Payment
from django.http import Http404
from items.models import Label,AccessaryLabel   

# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY
stripeToken = settings.STRIPE_PUBLISHABLE_KEY


def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)


def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid


class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            context = {
                'form': form,
                'couponform': CouponForm(),
                'order': order,
                'DISPLAY_COUPON_FORM': False,
                'acc_labels': AccessaryLabel.objects.all(),
                'men_links' : Label.objects.filter(categories__name='Men'),
                'women_links' : Label.objects.filter(categories__name='Women'),
                'kids_links' : Label.objects.filter(categories__name='Kids'),
            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})

            billing_address_qs = Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update(
                    {'default_billing_address': billing_address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("payments:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('payments:checkout')
                else:
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')
                    shipping_address2 = form.cleaned_data.get(
                        'shipping_address2')
                    shipping_number = form.cleaned_data.get(
                        'shipping_number')
                    shipping_city = form.cleaned_data.get(
                        'shipping_city')
                    shipping_zip = form.cleaned_data.get('shipping_zip')

                    if is_valid_form([shipping_address1, shipping_number,shipping_city, shipping_zip]):
                        print('shipping-valid')

                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                            apartment_address=shipping_address2,
                            number=shipping_number,
                            city=shipping_city,
                            zip=shipping_zip,
                            address_type='S'
                        )
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()

                        set_default_shipping = form.cleaned_data.get(
                            'set_default_shipping')
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")

                use_default_billing = form.cleaned_data.get(
                    'use_default_billing')
                same_billing_address = form.cleaned_data.get(
                    'same_billing_address')

                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = 'B'
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    print("Using the defualt billing address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        address_type='B',
                        default=True
                    )
                    if address_qs.exists():
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default billing address available")
                        return redirect('payments:checkout')
                else:
                    print("User is entering a new billing address")
                    billing_address1 = form.cleaned_data.get(
                        'billing_address')
                    billing_address2 = form.cleaned_data.get(
                        'billing_address2')
                    billing_number = form.cleaned_data.get(
                        'billing_number')
                    billing_city = form.cleaned_data.get(
                        'billing_city')
                    billing_zip = form.cleaned_data.get('billing_zip')

                    if is_valid_form([billing_address1, billing_number,billing_city, billing_zip]):
                        print('billing-valid')
                        billing_address = Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            apartment_address=billing_address2,
                            city=billing_city,
                            number=billing_number,
                            zip=billing_zip,
                            address_type='B'
                        )
                        billing_address.save()

                        order.billing_address = billing_address
                        order.save()

                        set_default_billing = form.cleaned_data.get(
                            'set_default_billing')
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(
                            self.request, "Please fill in the required billing address fields")

                payment_option = form.cleaned_data.get('payment_option')

                if payment_option == 'O':
                    return redirect('payments:payment', payment_option='online')
                elif payment_option == 'C':
                    return redirect('payments:payment', payment_option='cod')
                else:
                    messages.warning(
                        self.request, "Invalid payment option selected")
                    return redirect('payments:checkout')
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("orders:order-summary")


class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        payment_option = kwargs['payment_option']
        if order.billing_address:
            if payment_option == 'online':
                context = {
                    'order': order,
                    'DISPLAY_COUPON_FORM': False,
                    'payment_option' : 'Online - JazzCash or EasyPaisa',
                    'acc_labels': AccessaryLabel.objects.all(),
                    'men_links' : Label.objects.filter(categories__name='Men'),
                    'women_links' : Label.objects.filter(categories__name='Women'),
                    'kids_links' : Label.objects.filter(categories__name='Kids'),
                        
                 }
                messages.warning(
                    self.request, "Waiting for order confirmation. Please read the note in online payment section.")

            elif payment_option == 'cod':
                context = {
                    'order': order,
                    'DISPLAY_COUPON_FORM': False,
                    'payment_option' : 'Cash on Delivery',
                     'acc_labels': AccessaryLabel.objects.all(),
                    'men_links' : Label.objects.filter(categories__name='Men'),
                    'women_links' : Label.objects.filter(categories__name='Women'),
                    'kids_links' : Label.objects.filter(categories__name='Kids'),
                }
            else:
                raise Http404("Payment method does not exist")
            
            return render(self.request, "payment.html", context)
        else:
            messages.warning(
                self.request, "You have not added a billing address")
            return redirect("payments:checkout")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        userprofile = UserProfile.objects.get(user=self.request.user)
        payment_option = kwargs['payment_option']


        amount = int(order.get_total() * 100)

        try:

            # create the payment
            payment = Payment()
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.option = str(payment_option)
            payment.order = order
            payment.save()

            # assign the payment to the order

            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            ref_code = create_ref_code()
            order.ordered = True
            order.ref_code = ref_code
            order.save()

            messages.success(self.request, "Your order was successful! Your order code is {}. Please note it down for your surety.".format(ref_code),)

            return redirect("/")

            

        except Exception as e:
            # send an email to ourselves
            messages.warning(
                self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")

        return redirect("/payment/cod/")


class AddCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(
                    user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Successfully added coupon")
                return redirect("payments:checkout")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("payments:checkout")
