
(function ($) {
    "use strict";
    jQuery(document).ready(function ($) {
        $(document).on('submit','#contact-form',function(e){
            
            e.preventDefault();
            var name = $('#name').val();
            var email = $('#email').val();
            var subject = $('#subject').val();
            var message = $('#message').val();
            
          

            if (!name) {
                 $('#name').removeClass('error');
                 $('#name').addClass('error').attr('placeholder','Name*');
             }else{
                 $('#name').removeClass('error');
             }
            if (!email) {
                 $('#email').removeClass('error');
                 $('#email').addClass('error').attr('placeholder','Email*')
             }else{
                 $('#email').removeClass('error');
             }
            if (!subject) {
                 $('#subject').removeClass('error');
                 $('#subject').addClass('error').attr('placeholder','Subject*')
             }else{
                 $('#subject').removeClass('error');
             }
            if (!message) {
                 $('#message').removeClass('error');
                 $('#message').addClass('error').attr('placeholder','Message*')
             }else{
                 $('#message').removeClass('error');
             }
             
            
            if ( name && email && subject && message ) {
             	$.ajax({
	                 type: "POST",
	                 url: 'contact.php',
	                 data:{
                         'name': name,
                         'email': email,
                         'subject': subject,
                         'message': message,
	                 },
	                 success:function(data){
                         $('#contact-form').children('.email-success').remove();
                         $('#contact-form').prepend('<span class="alert alert-success email-success">'+data+'</span>');
                         $('#name').val('');
                         $('#email').val('');
                         $('#subject').val('');
                         $('#message').val('');
                         $('.email-success').fadeOut(3000);
                         
	                 }
	             });
             }else{
                $('#contact-form').children('.email-success').remove();
                $('#contact-form').prepend('<span class="alert alert-danger email-success">somenthing is wrong</span>');
                $('.email-success').fadeOut(3000);
             }

            
            
        });
    })

}(jQuery));	
