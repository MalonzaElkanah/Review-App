(function($) {
	$(".form-request").submit(function(event) {
       	event.preventDefault();
       	$.ajax({ 
       		data: $(this).serialize(),
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success: function(response) {
	            console.log(response);
	            if(response['success']) {
	            	alert(response['success']);
	            	if(response['redirect']){
	            		window.location.href = response['redirect'];
	            	}else{
		            	window.location.href = "../";
	            	}
	            }
	            if(response['error']) {
	            	alert(response['error']);
	            	$("#id_error-text").html("Error: "+response['error']+"");
	            }
        	},
	        error: function (request, status, error) {
	            console.log(request.responseText);
	        }
       	});
   	});

   	$(".link-request").click(function(event){
   		event.preventDefault();
   		$.ajax({
   			url: $(this).attr('href'),
   			success: function(response){
   				console.log(response);
	            if(response['success']) {
	            	alert(response['success']);
	            	if(response['redirect']){
	            		window.location.href = response['redirect'];
	            	}else{
		            	window.location.href = "../";
	            	}
	            }
	            if(response['error']) {
	            	alert(response['error']);
	            	$("#id_error-text").html("Error: "+response['error']+"");
	            }
   			},
	        error: function (request, status, error) {
	            console.log(request.responseText);
	        }
   		});
   	});

   	

})(jQuery);