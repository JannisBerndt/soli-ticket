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
if (localStorage.getItem('cookieSeen') != 'shown') {
    $('.cookie-banner').delay(2000).fadeIn();
    localStorage.setItem('cookieSeen','shown')
  };
  $('.close-banner').click(function() {
    $('.cookie-banner').fadeOut();
  })
}
