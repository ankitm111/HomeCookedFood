
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
			localStorage.setItem("logintoken", data["token"]);

			$('#myModal').modal('toggle');

			var loginButton = document.getElementById("login_logout");
			loginButton.innerHTML='Logout';
			loginButton.onclick = logout;

			var namelabel = document.getElementById("namelabel");
			namelabel.classList.remove("collapse");
			namelabel.innerHTML = "Hello ".concat(data["name"]);

		},
		error: function(xhr,err) {
 		   alert("Failure");
 		   showIndexPage();
		}
	});
}

function logout() {

	localStorage.setItem("logintoken", '');
	var loginButton = document.getElementById("login_logout");
	loginButton.innerHTML = "Login / Sign Up";
	loginButton.onclick = null;

	var namelabel = document.getElementById("namelabel");
	namelabel.classList.add("collapse"); // hide it
	namelabel.innerHTML = "";

	showIndexPage();
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
var nextDish = 0;

function adddish() {
        event.preventDefault();
        var dishdiv = document.getElementById("dishdiv");
        nextDish = nextDish + 1;

        var div = document.createElement("div");
        div.id = "field_dishdiv" + nextDish;
        div.class = "div";

        var input_dn = document.createElement("input");
        input_dn.autocomplete = "off";
        input_dn.class = "input";
        input_dn.placeholder = "Dish name";
        input_dn.id = "field_dishname" + nextDish;
        input_dn.type = "text";
        div.appendChild(input_dn);

        var input_dq = document.createElement("input");
        input_dq.autocomplete = "off";
        input_dq.class = "input";
        input_dq.type="number";
        input_dq.min = 1;
        input_dq.placeholder = "Dish quantity";
        input_dq.id = "field_dishquantity" + nextDish;
        div.appendChild(input_dq);

        var rem_btn = document.createElement("button");
        rem_btn.class = "btn btn-default";
        rem_btn.id = "b_rem" + nextDish;
        rem_btn.innerHTML = "-";
        rem_btn.onclick = removeDish;
        div.appendChild(rem_btn); 

        dishdiv.appendChild(div);

        $("#count").val(nextDish);
}

function removeDish() {
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

////////////////////////////////////////////////////////////////////////

var nextTag=0;

function addtag() {
        event.preventDefault();
        var addto = document.getElementById("tagsdiv");
        nextTag = nextTag + 1;

        var input_dn = document.createElement("input");
        input_dn.autocomplete = "off";
        input_dn.class = "input";
        input_dn.placeholder = "Tag name";
        input_dn.id = "field_tagname" + nextTag;
        input_dn.type = "text";
        addto.appendChild(input_dn);

        var rem_btn = document.createElement("button");
        rem_btn.class = "btn btn-default";
        rem_btn.id = "b_remtag" + nextTag;
        rem_btn.innerHTML = "-";
        rem_btn.onclick = removeTag;

        addto.appendChild(rem_btn);       

        $("#count").val(nextTag);
}

function removeTag() {
    event.preventDefault();
    // TODO: make sure that we extract the number from the end, currently this approach does
    // not work if we reach the id # 10 as we only look at the last character.
    var fieldNum = this.id.charAt(this.id.length - 1);
    var fieldID_tagname = "#field_tagname" + fieldNum;

    $(this).remove();
    $(fieldID_tagname).remove();
}

///////////////////////////////////////////////////////////////////////////////

function addmeal() {
	event.preventDefault();

	var mealname = $('#mealname').val();
	var maxmeals = $('#maxmeals').val();
	var mealprice = $('#mealprice').val();
	var mealitems = [];

	var dishes = document.getElementById('dishdiv').children;
	for (var i = 0; i < dishes.length; i++) {
		if (dishes[i].class == "div") {
			var dish = dishes[i].children;
			var dish_item = []
			for (var j = 0; j < dish.length; j++) {
				if (dish[j].class == "input") {
					dish_item.push(dish[j].value);
				}
			}
			mealitems.push(dish_item);
		}
	}

	var tagnames = [];
	var tags = document.getElementById("tagsdiv").children;
	for (var i = 0; i < tags.length; i++) {
		if (tags[i].class == "input") {
			tagnames.push(tags[i].value);
		}
	}

	// Convert mealitems array to dict
	meal_items = {};
	for (var i = 0; i < mealitems.length; i++) {
		d = mealitems[i];
		meal_items[d[0]] = d[1];
	}

	var Url = 'http://127.0.0.1:5000/hcf/users/provider/meals/'.concat(mealname);

	$.ajax({
		type: 'POST',
		url: Url,
		cache: false,
		xhrFields: { withCredentials:true },
		beforeSend: function(xhr){
            xhr.setRequestHeader("Authorization", "Basic " + btoa(localStorage.getItem("logintoken") + ":unused"));
        },
		data: JSON.stringify({'price' : mealprice, 'max_count': maxmeals, 'meal_items': meal_items, 'tagnames': tagnames}),
		contentType:"application/json; charset=utf-8",
  		crossDomain: true,
		success: function(data) {
			showIndexPage();
		},
		error: function(xhr,err){
 		   alert("readyState: " + xhr.readyState + "\nstatus: " + xhr.status);
 		   alert("responseText: "+xhr.responseText);
		}
	});

}