/*!
    * Start Bootstrap - Creative v6.0.4 (https://startbootstrap.com/theme/creative)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-creative/blob/master/LICENSE)
    */
    (function($) {
  "use strict"; // Start of use strict

  // Smooth scrolling using jQuery easing
  $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
    if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
      var target = $(this.hash);
      target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
      if (target.length) {
        $('html, body').animate({
          scrollTop: (target.offset().top - 72)
        }, 1000, "easeInOutExpo");
        return false;
      }
    }
  });

  // Closes responsive menu when a scroll trigger link is clicked
  $('.js-scroll-trigger').click(function() {
    $('.navbar-collapse').collapse('hide');
  });

  // Activate scrollspy to add active class to navbar items on scroll
  $('body').scrollspy({
    target: '#mainNav',
    offset: 75
  });

  // Collapse Navbar
  var navbarCollapse = function() {
    if ($("#mainNav").offset().top > 100) {
      $("#mainNav").addClass("navbar-scrolled");
    } else {
      $("#mainNav").removeClass("navbar-scrolled");
    }
  };
  // Collapse now if page is not at top
  navbarCollapse();
  // Collapse the navbar when page is scrolled
  $(window).scroll(navbarCollapse);

  // Magnific popup calls
  $('#portfolio').magnificPopup({
    delegate: 'a',
    type: 'image',
    tLoading: 'Loading image #%curr%...',
    mainClass: 'mfp-img-mobile',
    gallery: {
      enabled: true,
      navigateByImgClick: true,
      preload: [0, 1]
    },
    image: {
      tError: '<a href="%url%">The image #%curr%</a> could not be loaded.'
    }
  });

})(jQuery); // End of use strict

$(()=> {
    console.log( "ready!" );
});


// We set the AJAX function that will save a bookmark and update its status
$('.save_button').click(function(event) {
    let suggestionID = $(this).attr('id');
    let productID = $('.result').attr('id');
    let userID = $('#user_id').val();
    const csrftoken = $('[name=csrfmiddlewaretoken]').val();
    $.ajax({
      url: "http://127.0.0.1:8000/bookmark/add/",
      type: 'POST',
      headers: {"X-CSRFToken": csrftoken},
      data: {
        'replacing_id': suggestionID,
        'replaced_id': productID,
        'user_id': userID,
      },
      dataType: 'json',
      cache: true,
      success: function(data) {
        if (data.status) {
          // alert('Favori sauvegardé');
          $(`#suggestion_${suggestionID}`).load(` #suggestion_${suggestionID} > *`);
        }
      }
    });
});


// // We set the AJAX function that will display results when taping in the search form
// $('.form-control').change(function(event) {
//   event.preventDefault();
//   let input = $(this).val();
//   console.log(input);
//   if (input.length > 1) {
//     $.ajax({
//       url: "http://127.0.0.1:8000/list/",
//       type: "GET",
//       data: {
//         'recherche': input
//       },
//       dataType: 'json',
//       success: function(data) {
//         for (let result in data.products) {
//           console.log(data.products[result]);
//           $("#results-list").append("<li><a href=\"{% url 'results' result.id %}\">" + data.products[result] + "</a></li>");
//         }
//       }
//     });
//   };
// });
