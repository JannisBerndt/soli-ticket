var to_top_button = null;

function copyLink() {
    /* Get the text field */
    var copyText = document.getElementById("link");

    /* Select the text field */
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/

    /* Copy the text inside the text field */
    document.execCommand("copy");

    /* Alert the copied text */
    // alert("Copied the text: " + copyText.value);
}

function calcSum() {
    var amounts = document.getElementsByClassName('amount-field');
    var prices = document.getElementsByClassName('price');
    var sum = 0.00;
    for (var i = 0; i < amounts.length; i++) {
        var price = parseFloat(prices[i].innerHTML.replace(',', "."));
        var amount = parseInt(amounts[i].value);
        if(Number.isNaN(amount)) {
            amount = 0;
        }
        console.log(i);
        console.log(amount + ' mal ' + price);
        sum += amount * price;
    }
    console.log(sum.toFixed(2));
    document.getElementById('sum').innerHTML = sum.toFixed(2).replace('.', ",");
}

window.onload = function() {
    this.to_top_button = document.getElementById('to-top-button');
    this.to_top_button.onclick = function() {window.scrollTo({top: 0, behavior: "smooth",})};

    if (localStorage.getItem('cookieAccepted') != 1) {
        document.getElementById('cookie-banner').style.display = "flex";
    };
    $('.close-banner').click(function() {
        localStorage.setItem('cookieAccepted', 1)
        $('.cookie-banner').fadeOut();
    })

    window.onscroll = function() {
        setToTopButtonVisibility(this.to_top_button);
    }
}

function setToTopButtonVisibility(button) {
    if(document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        button.style.display = "inline-block";
    } else {
        button.style.display = "none";
    }
}