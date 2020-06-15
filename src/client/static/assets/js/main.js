!(function($) {
  "use strict";

  // Nav Menu
  $(document).on('click', '.nav-menu a, .mobile-nav a', function(e) {
      let hash = this.hash;
      let target = this.target;
      if (target.length) {

        if ($(this).parents('.nav-menu, .mobile-nav').length) {
          $('.nav-menu .active, .mobile-nav .active').removeClass('active');
          $(this).closest('li').addClass('active');
        }

        if (target == '#header') {
          $('#header').removeClass('header-top');
          return false;
        }

        if (!$('#header').hasClass('header-top')) {
          $('#header').addClass('header-top');
        }

        e.stopPropagation();
    }
  });

})(jQuery);