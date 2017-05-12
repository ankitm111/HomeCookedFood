
function load_contactus() {
    window.location.href="contactus.html";
}

function login() {
	event.preventDefault();
	$.ajax({
		type: 'GET',
		url: 'http://127.0.0.1:5000/hcf/token',
		cache: false,
  		beforeSend: function(xhr){
            xhr.setRequestHeader("Authorization",
                "Basic " + btoa( $('#uname1').val() + ":" + $('#pwd').val()));
        },
  		crossDomain: true,
		success: function(data) {
			console.log(data);
			alert("Inside success");
			localStorage.setItem("logintoken", data["token"]);
			window.location.href="homepage.html";
		},
		error: function(xhr,err){
 		   alert("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
 		   alert("responseText: "+xhr.responseText);
 		   showIndexPage();
		}
	});
}


function adduser() {
	
	event.preventDefault();
	var username = $('#uname2').val();
	var name = $('#name').val();
	var password = $('#password').val();
	var email = $('#email').val();
	var phone = $('#mobile').val();
	var zipcode = '95035';//$('#zipcode').val();
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
			window.location.href = "index.html";
		},
		error: function(xhr,err){
 		   alert("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
 		   alert("responseText: "+xhr.responseText);
		}
	});
}

function showIndexPage() {
	window.location.href = "index.html";
}

function addreview() {
	event.preventDefault();
	var currentUser = "";

}

////////////////////////////////////////////////////////////////////////
var next = 0;

function adddish() {
        event.preventDefault();
        var addto = document.getElementById("dishdiv");
        next = next + 1;

        var input_dn = document.createElement("input");
        input_dn.autocomplete = "off";
        input_dn.placeholder = "Dish name";
        input_dn.id = "field_dishname" + next;
        input_dn.type = "text";
        addto.appendChild(input_dn);

        var input_dq = document.createElement("input");
        input_dq.autocomplete = "off";
        input_dq.type="number";
        input_dq.min = 1;
        input_dq.placeholder = "Dish quantity";
        input_dq.id = "field_dishquantity" + next;
        addto.appendChild(input_dq);

        var rem_btn = document.createElement("button");
        rem_btn.class = "btn";
        rem_btn.id = "b_rem" + next;
        rem_btn.innerHTML = "-";
        rem_btn.onclick = remove;

        addto.appendChild(rem_btn);       

        $("#count").val(next);
}

function remove() {
    event.preventDefault();
    // TODO: make sure that we extract the number from the end, currently this approach does
    // not work if we reach the id # 10 as we only look at the last character.
    var fieldNum = this.id.charAt(this.id.length - 1);
    var fieldID_dishname = "#field_dishname" + fieldNum;
    var fieldID_dishquantity = "#field_dishquantity" + fieldNum;

    $(this).remove();
    $(fieldID_dishname).remove();
    $(fieldID_dishquantity).remove();
}


function addmeal() {

}







