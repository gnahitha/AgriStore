from datetime import date
from .models import ChatUsage
from django.http import JsonResponse
import traceback
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .models import Product, Review, Cart, Order, OrderItem
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from django.db.models import Avg
from django.db.models import Avg
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")
def product_list(request):

    products = Product.objects.all()

    for product in products:

        reviews = Review.objects.filter(product=product)

        product.review_count = reviews.count()

        average = reviews.aggregate(Avg("rating"))["rating__avg"]

        if average:
            product.average_rating = round(average, 1)
        else:
            product.average_rating = 0

    cart_count = Cart.objects.count()

    wishlist_ids = []

    if request.user.is_authenticated:

        wishlist_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list(
            "product_id",
            flat=True
        )

    return render(
        request,
        "index.html",
        {
            "products": products,
            "cart_count": cart_count,
            "wishlist_ids": wishlist_ids,
        }
    )
def login_page(request):

    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect("/")

        else:

            messages.error(
                request,
                "Invalid Username or Password"
            )

    return render(request, "login.html")
def logout_page(request):

    logout(request)

    return redirect("/")

def register_page(request):

    if request.method == "POST":

        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")

        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")

        else:
            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(request, "Registration Successful.")

            return redirect("/login/")

    return render(request, "register.html")
def cart_page(request):

    cart_items = Cart.objects.all()

    total = 0

    for item in cart_items:
        item.subtotal = item.product.price * item.quantity
        total += item.subtotal

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total": total
        }
    )

from django.shortcuts import redirect
@login_required(login_url='/login/')

def checkout_page(request):

    cart_items = Cart.objects.all()

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":

        customer_name = request.POST.get("customer_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            customer_name=customer_name,
            phone=phone,
            address=address,
            total_amount=total
        )

        for item in cart_items:

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart_items.delete()

        return redirect("/order-success/")

    return render(
        request,
        "checkout.html",
        {
            "cart_items": cart_items,
            "total": total
        }
    )
@login_required(login_url='/login/')
def order_history(request):

    orders = Order.objects.prefetch_related(
    "orderitem_set"
     ).order_by("-created_at")
    return render(
        request,
        "order-history.html",
        {
            "orders": orders
        }
    )

def orders_page(request):
    return render(request, "orders.html")

def product_details(request):
    product_name = request.GET.get("product")

    product = Product.objects.get(name=product_name)
    reviews = Review.objects.filter(product=product)

    product.review_count = reviews.count()

    average = reviews.aggregate(Avg("rating"))["rating__avg"]

    if average:
     product.average_rating = round(average, 1)
    else:
     product.average_rating = 0

    if request.method == "POST":
        name = request.POST.get("name")
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            product=product,
            name=name,
            rating=rating,
            comment=comment
        )

    

    return render(
        request,
        "product-details.html",
        {
            "product": product,
            "reviews": reviews
        }
    )

from django.shortcuts import redirect
@login_required(login_url='/login/')
def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id)

    cart_item = Cart.objects.filter(product=product).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(
            product=product,
            quantity=1
        )

    return redirect("/")

def order_success(request):
    return render(request, "order-success.html")
from django.shortcuts import redirect

def increase_quantity(request, cart_id):

    item = Cart.objects.get(id=cart_id)

    item.quantity += 1

    item.save()

    return redirect("/cart/")


def decrease_quantity(request, cart_id):

    item = Cart.objects.get(id=cart_id)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("/cart/")


def clear_cart(request):

    Cart.objects.all().delete()

    return redirect("/cart/")
def remove_from_cart(request, cart_id):

    item = Cart.objects.get(id=cart_id)

    item.delete()

    return redirect("/cart/")
from django.contrib.auth.decorators import login_required

@login_required
def wishlist_page(request):

    wishlist_items = Wishlist.objects.filter(user=request.user)

    return render(
        request,
        "wishlist.html",
        {"wishlist_items": wishlist_items}
    )
from django.shortcuts import redirect

@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    wishlist = Wishlist.objects.filter(
        user=request.user,
        product=product
    )

    if wishlist.exists():

        wishlist.delete()

    else:

        Wishlist.objects.create(
            user=request.user,
            product=product
        )

    return redirect("/wishlist/")
@login_required(login_url='/login/')
def buy_again(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart_item = Cart.objects.filter(
        product=product
    ).first()

    if cart_item:

        cart_item.quantity += 1

        cart_item.save()

    else:

        Cart.objects.create(
            product=product,
            quantity=1
        )

    return redirect("/cart/")
@login_required(login_url="/login/")
def cancel_order(request, order_id):

    order = get_object_or_404(Order, id=order_id)

    if order.status in ["Placed", "Packed"]:

        order.is_cancelled = True
        order.status = "Cancelled"

        order.save()

    return redirect("/order-history/")
def chatbot_page(request):

    return render(
        request,
        "chatbot.html"
    )
def chatbot_response(request):

    if request.method != "POST":
        return JsonResponse({
            "reply": "Invalid Request."
        })

    message = request.POST.get("message", "").strip()

    if not message:
        return JsonResponse({
            "reply": "Please enter a question."
        })

    today = date.today()

    usage, created = ChatUsage.objects.get_or_create(
        user=request.user,
        date=today
    )

    if usage.count >= 45:

        return JsonResponse({
            "reply": """
🚫 <b>Daily AI Limit Reached</b><br><br>

You have used all <b>45 AI questions</b> today.<br><br>

Please come back tomorrow.
"""
        })

    try:

        prompt = f"""
You are AgriStore AI Assistant.

You are an expert agricultural scientist.

Rules:

- Answer ONLY agriculture questions.
- Never write long paragraphs.
- Use simple English.
- Maximum 120 words.
- Give answers in points.

Format:

🌱 Problem
- Point 1
- Point 2

✅ Solution
- Step 1
- Step 2
- Step 3
- Step 4

💡 Tips
- Tip 1
- Tip 2
- Tip 3

⚠️ Precautions
- Precaution 1
- Precaution 2

Question:
{message}
"""

        response = model.generate_content(prompt)

        print("========== GEMINI RESPONSE ==========")
        print(response)
        print("=====================================")

        answer = response.text.strip()

        if answer:

            usage.count += 1
            usage.save()

        answer = answer.replace("•", "<br>•")
        answer = answer.replace("🌱", "<br>🌱")
        answer = answer.replace("✅", "<br><br>✅")
        answer = answer.replace("💡", "<br><br>💡")
        answer = answer.replace("⚠️", "<br><br>⚠️")

    except Exception:

        traceback.print_exc()

        answer = """
⚠️ <b>Unable to get AI response.</b><br><br>

Possible reasons:<br>
• Slow Internet<br>
• Gemini server is busy<br>
• API quota exceeded<br>
• Temporary server issue<br><br>

Please try again after a few seconds.
"""

    remaining = 45 - usage.count

    return JsonResponse({

        "reply":
            answer +
            f"<br><br><hr><small>🤖 AI Questions Remaining Today: <b>{remaining}/45</b></small>"

    })