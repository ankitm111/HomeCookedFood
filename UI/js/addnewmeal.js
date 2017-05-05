var next = 1;

$(document).ready(function(){
   /* $(".add-more").click(function(e){
        e.preventDefault();
        var addto = document.getElementById("field");
        var addRemove = "#field";
        next = next + 1;

        addto.appendChild(document.createElement("br"));

        var input_dn = document.createElement("input");
        input_dn.autocomplete = "off";
        input_dn.placeholder = "Dish name";
        input_dn.id = "field_dishname" + next;
        input_dn.type = "text";
        addto.appendChild(input_dn);

        var input_dq = document.createElement("input");
        input_dq.autocomplete = "off";
        input_dq.placeholder = "Dish quantity";
        input_dq.id = "field_dishquantity" + next;
        input_dq.type = "number";
        addto.appendChild(input_dq);

        var add_btn = document.createElement("button");
        add_btn.class = "btn";
        add_btn.id = "b_add" + next;
        add_btn.innerHTML = "+";
        add_btn.onclick = "add()";

        addto.appendChild(add_btn);

        var rem_btn = document.createElement("button");
        rem_btn.class = "btn";
        rem_btn.id = "b_rem" + next;
        rem_btn.innerHTML = "-";
        rem_btn.onclick = "remove()";

        addto.appendChild(rem_btn);
        
        $("#field_dishname" + next).attr('data-source',$(addto).attr('data-source'));
        $("#field_dishquantity" + next).attr('data-source',$(addto).attr('data-source'));

        $("#count").val(next);  
        
    });*/

    
});


function add() {
        //e.preventDefault();
        var addto = document.getElementById("field");
        next = next + 1;

        //addto.appendChild(document.createElement("br"));

        var input_dn = document.createElement("input");
        input_dn.autocomplete = "off";
        input_dn.placeholder = "Dish name";
        input_dn.id = "field_dishname" + next;
        input_dn.type = "text";
        addto.appendChild(input_dn);

        var input_dq = document.createElement("input");
        input_dq.autocomplete = "off";
        input_dq.placeholder = "Dish quantity";
        input_dq.id = "field_dishquantity" + next;
        input_dq.type = "number";
        addto.appendChild(input_dq);

        var add_btn = document.createElement("button");
        add_btn.class = "btn";
        add_btn.id = "b_add" + next;
        add_btn.innerHTML = "+";
        add_btn.onclick = "add()";

        addto.appendChild(add_btn);

        var rem_btn = document.createElement("button");
        rem_btn.class = "btn";
        rem_btn.id = "b_rem" + next;
        rem_btn.innerHTML = "-";
        rem_btn.onclick = "remove()";

        addto.appendChild(rem_btn);
        
        //$("#field_dishname" + next).attr('data-source',$(addto).attr('data-source'));
        //$("#field_dishquantity" + next).attr('data-source',$(addto).attr('data-source'));

        $("#count").val(next);  
        
}


function remove() {
    //e.preventDefault();
    var fieldNum = this.id.charAt(this.id.length-1);
    var fieldID_dishname = "#field_dishname" + fieldNum;
    var fieldID_dishquantity = "#field_dishquantity" + fieldNum;

    $(this).remove();
    $(fieldID_dishname).remove();
    $(fieldID_dishquantity).remove();
}

function add_new_dish() {



}
