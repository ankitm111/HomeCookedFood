function login() {
	event.preventDefault();
	$.ajax({
		type: 'GET',
		url: 'http://127.0.0.1:5000/hcf/token',
		cache: false,
  		beforeSend: function(xhr){
            xhr.setRequestHeader("Authorization",
                //"Basic " + encodeBase64(username + ":" + password));
                "Basic " + btoa( $('#uname').val() + ":" + $('#pwd').val()));
        },
  		crossDomain: true,
		success: function(data) {
			console.log(data);
			alert("Inside success");
			localStorage.setItem("logintoken", data["token"]);
			alert(localStorage.getItem("logintoken"));
		},
		error: function(xhr,err){
 		   alert("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
 		   alert("responseText: "+xhr.responseText);
		}
	});
}


function signup() {
	window.location.href="signup.html";
}