(function() {
	'use strict';

	var tinyslider = function() {
		var el = document.querySelectorAll('.testimonial-slider');

		if (el.length > 0) {
			var slider = tns({
				container: '.testimonial-slider',
				items: 1,
				axis: "horizontal",
				controlsContainer: "#testimonial-nav",
				swipeAngle: false,
				speed: 700,
				nav: true,
				controls: true,
				autoplay: true,
				autoplayHoverPause: true,
				autoplayTimeout: 3500,
				autoplayButtonOutput: false
			});
		}
	};
	tinyslider();

	


	var sitePlusMinus = function() {

		var value,
    		quantity = document.getElementsByClassName('quantity-container');

		function createBindings(quantityContainer) {
	      var quantityAmount = quantityContainer.getElementsByClassName('quantity-amount')[0];
	      var increase = quantityContainer.getElementsByClassName('increase')[0];
	      var decrease = quantityContainer.getElementsByClassName('decrease')[0];
	      increase.addEventListener('click', function (e) { increaseValue(e, quantityAmount); });
	      decrease.addEventListener('click', function (e) { decreaseValue(e, quantityAmount); });
	    }

	    function init() {
	        for (var i = 0; i < quantity.length; i++ ) {
						createBindings(quantity[i]);
	        }
	    };

	    function increaseValue(event, quantityAmount) {
	        value = parseInt(quantityAmount.value, 10);

	        console.log(quantityAmount, quantityAmount.value);

	        value = isNaN(value) ? 0 : value;
	        value++;
	        quantityAmount.value = value;
	    }

	    function decreaseValue(event, quantityAmount) {
	        value = parseInt(quantityAmount.value, 10);

	        value = isNaN(value) ? 0 : value;
	        if (value > 0) value--;

	        quantityAmount.value = value;
	    }
	    
	    init();
		
	};
	sitePlusMinus();


})()





function updateItemStock(button) {

	var itemId = $(button).data('item-id');
	var quantityInput = button.parentNode.parentNode.querySelector('.quantity-amount');
	var currentQty = parseInt(quantityInput.value);
	

	if ( button.classList.contains('increase')) {
	  currentQty += 1;
	} else if ( button.classList.contains('decrease') && currentQty > 0) {
	  currentQty-= 1;
	}
	
	quantityInput.value = currentQty;
  
	// Your other logic here (e.g., send an AJAX request to update the database)
	console.log('Item ID:', itemId, 'New Quantity:', currentQty);

	$.ajax({
        url: '/update_item_stock',  // Replace with your actual route
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            id: itemId,
            new_stock: currentQty
        }),
        success: function(response) {
            console.log('Item stock updated successfully:', response);
			updateCartTotals();
			// updateCartItemTotal();
        },
        error: function(error) {
            console.error('Error updating item stock:', error);
        }
    });
	if ( currentQty == 0 ) {
		removeFromCart(button)
	}
  }

function addToCart(event, button) {

	event.preventDefault();
	// const itemId = $(button).data('item-id');
	const itemName = $(button).data('item-name');
	const itemPrice = $(button).data('item-price');
	const itemImage = $(button).data('item-image');

	// Send an AJAX request to add the item to the cart
	$.ajax({
	   url: '/add_to_cart',  // Replace with the actual route on your server
	   method: 'POST',
	   contentType: 'application/json',
	   data: JSON.stringify({
		  name: itemName,
		  price: itemPrice,
		  image: itemImage // You can customize the quantity if needed
	   }),
	   success: function(response) {
		  // Handle the response from the server if needed
		  console.log('Item added to cart:', response);
		  updateCartTotals();
	   },
	   error: function(error) {
		  // Handle errors if the request fails
		  console.error('Error adding item to cart:', error);
	   }
	});

 }
 
 function removeFromCart(button) {
	// Extract item information from the data attribute
	const itemId = $(button).data('item-id');
	// Send an AJAX request to remove the item from the cart
	$.ajax({
	   url: '/remove_from_cart',  // Replace with the actual route on your server
	   method: 'POST',
	   contentType: 'application/json',
	   data: JSON.stringify({
		  id: itemId,
	   }),
	   success: function(response) {
		  console.log('Item removed from cart:', response);
		  $(button).closest('.cart_item').remove();
		  updateCartTotals();
	   },
	   error: function(error) {
		  // Handle errors if the request fails
		  console.error('Error removing item from cart:', error);
	   }
	});
 }
 
 function updateCartTotals() {
    // Make an AJAX request to get the updated cart totals
	var priceElements = document.querySelectorAll('.price')

	priceElements.forEach(function (element) {
		$.ajax({
			url: '/get_cart_totals',  // Replace with the actual route on your server
			method: 'GET',
			success: function(response) {
				// Update the HTML elements displaying cart totals
				element.textContent = '£' + response.subtotal;
				element.textContent = '£' + response.total;
			},
			error: function(error) {
				console.error('Error getting cart totals:', error);
			}
		});
	});
}	

 
// function updateCartItemTotal() {
//     // Make an AJAX request to get the updated cart totals
// 	var priceElement = document.querySelector('.itemTotal')
// 	var itemStock = priceElement.getAttribute('item-stock');
// 	var itemPrice = priceElement.getAttribute('item-price');
// 	var totalPrice = priceElement.textContent;
// 	console.log(totalPrice)
// 	console.log(itemPrice)
// 	console.log(itemStock)
// 	$.ajax({
// 		url: '/get_itemCart_totals',  // Replace with the actual route on your server
// 		method: 'GET',
// 		contentType: 'application/json',
// 		data: JSON.stringify({
// 		qty: itemStock,
// 		price: itemPrice
// 		}),
// 		success: function(response) {
// 			// Update the HTML elements displaying cart totals
// 			element.textContent = '£' + response.item_total;
// 		},
// 		error: function(error) {
// 			console.error('Error getting cart totals:', error);
// 		}
// 	});

// }