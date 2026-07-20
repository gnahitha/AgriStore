let products = [
{
    id: 1,
    name: "Rice",
    price: 50,
    stock: 100
},
{
    id: 2,
    name: "Wheat",
    price: 40,
    stock: 80
},
{
    id: 3,
    name: "Corn",
    price: 35,
    stock: 60
},
{
    id: 4,
    name: "Seeds",
    price: 120,
    stock: 40
},
{
    id: 5,
    name: "Fertilizer",
    price: 500,
    stock: 25
},
{
    id: 6,
    name: "Pesticide",
    price: 350,
    stock: 15
}
];

localStorage.setItem(
    "products",
    JSON.stringify(products)
);
function addToCart(productName, price) {

    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    let item = cart.find(p => p.product === productName);

    if(item){
        item.quantity += 1;
    }else{
        cart.push({
            product: productName,
            price: price,
            quantity: 1
        });
    }

    localStorage.setItem("cart", JSON.stringify(cart));

    alert(productName + " added to cart!");
}
function searchProducts(){

    let input =
    document.getElementById("searchBox")
    .value.toLowerCase();

    let products =
    document.getElementsByClassName("product");

    for(let i=0;i<products.length;i++){

        let text =
        products[i].innerText.toLowerCase();

        if(text.includes(input)){
            products[i].style.display = "";
        }else{
            products[i].style.display = "none";
        }
    }
}
function clearCart(){
    localStorage.clear();
    location.reload();
}
function increaseQuantity(productName){

    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    cart.forEach(item => {
        if(item.product === productName){
            item.quantity++;
        }
    });

    localStorage.setItem("cart", JSON.stringify(cart));

    location.reload();
}
function decreaseQuantity(productName){

    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    cart.forEach(item => {
        if(item.product === productName){

            if(item.quantity > 1){
                item.quantity--;
            }
        }
    });

    localStorage.setItem("cart", JSON.stringify(cart));

    location.reload();
}
function filterCategory(category){

    let products =
    document.getElementsByClassName("product");

    for(let i=0;i<products.length;i++){

        if(category === "all"){
            products[i].style.display = "";
        }
        else if(products[i].dataset.category === category){
            products[i].style.display = "";
        }
        else{
            products[i].style.display = "none";
        }
    }
}
function updateCartCount(){

    let cart =
    JSON.parse(localStorage.getItem("cart")) || [];

    let count = 0;

    cart.forEach(item => {
        count += item.quantity;
    });

    let cartCount =
    document.getElementById("cartCount");

    if(cartCount){
        cartCount.innerText = count;
    }
}

updateCartCount();
function showUser(){

    let user = localStorage.getItem("currentUser");

    if(user){

        document.getElementById("welcomeUser").innerHTML =
        "Welcome, " + user;

        document.getElementById("loginLink").style.display = "none";

        document.getElementById("registerLink").style.display = "none";

        document.getElementById("logoutBtn").style.display = "inline";
    }
}

showUser();

showUser();
function logout(){

    localStorage.removeItem(
        "currentUser"
    );

    location.reload();
}
function addReview(product){

    let reviewText =
    document.getElementById(
        product.toLowerCase() + "Review"
    ).value;

    let rating =
    document.getElementById(
        product.toLowerCase() + "Rating"
    ).value;

    let reviews =
    JSON.parse(localStorage.getItem("reviews"))
    || {};

    if(!reviews[product]){
        reviews[product] = [];
    }

    reviews[product].push({
        rating: rating,
        text: reviewText
    });

    localStorage.setItem(
        "reviews",
        JSON.stringify(reviews)
    );

    loadReviews(product);
}
function loadReviews(product){

    let reviews =
    JSON.parse(localStorage.getItem("reviews"))
    || {};

    let output = "";

    if(reviews[product]){

        reviews[product].forEach(review => {

            output += `
            <p>
            ${review.rating}
            ${review.text}
            </p>
            `;
        });
    }

    document.getElementById(
        product + "Reviews"
    ).innerHTML = output;
}
loadReviews("Rice");
const banners = [

"/static/images/banner1.jpg",

"/static/images/banner2.jpg",

"/static/images/banner3.jpg"

];

let currentBanner = 0;

setInterval(function(){

    currentBanner++;

    if(currentBanner >= banners.length){

        currentBanner = 0;

    }

    let img = document.getElementById("banner");

    if(img){

        img.src = banners[currentBanner];

    }

},3000);