function adduser() {
	
	event.preventDefault();
	var username = $('#username').val();
	var name = $('#name').val();
	var password = $('#password').val();
	var email = $('#email').val();
	var phone = $('#phone').val();
	var zipcode = $('#zipcode').val();
	var Url = 'http://127.0.0.1:5000/hcf/users/'.concat(username);

	$.ajax({
		type: 'POST',
		url: Url,
		cache: false,
		data: JSON.stringify({'name' : name, 'password': password, 'email_id':email,
			   'phone':phone, 'zipcode':zipcode, 'latitude':0, 'longitude':0}),
		dataType: 'json',
		contentType:"application/json; charset=utf-8",
  		crossDomain: true,
		success: function(data) {
			console.log(data);
			alert("Inside success");
		},
		error: function(xhr,err){
 		   alert("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
 		   alert("responseText: "+xhr.responseText);
		}
	});

	window.location.href = "index.html";

}