var mainform = document.getElementById('l_form');
//alert(mainform);
mainform.onsubmit = function()
{ 
    var username = document.getElementById("email");
    //alert(username);
    var password = document.getElementById("exampleInputPassword1");
    var username_s = document.getElementById("u_user");
    var password_s = document.getElementById("u_pwd");
    username_s.style.display ="none";
    //alert(username_s);
    password_s.style.display ="none";
    username_s.style.border ="none";
    password_s.style.border ="none";
    
    if (username.value == "" && password.value == "") {
        username_s.innerHTML = "empty username";
        username.style.border ="1px solid red";
        username_s.style.display ="block";
        //alert(username_s);
        password_s.innerHTML = "empty password";
        password.style.border ="1px solid red";
        password_s.style.display ="block";
        return false;
    }
    if (username.value == "") {
        username_s.style.display ="block";
        username_s.innerHTML = "empty username";
        username.style.border ="1px solid red";
        return false;
    }
    else if( !username.value.match(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/)) {
        username_s.innerHTML ="please enter valid username";
        username.style.border ="1px solid red";
        username_s.style.display = "block";
        return false;
      
    }
    if (password.value == "") {
        password_s.style.display ="block";
        password_s.innerHTML = "empty password";
        password.style.border ="1px solid red";
        return false;
    }
   
        //if (username.value.match == "^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$" && password.value.match == "^ /0-9/g") {
        //    return false;
        //}
        //if (username.value.match== "^[a-z]+[\._]?[a-z 0-9]+[@]\w+[.]\w{2,3}$") {
        //   username_s.innerHTML = "must be in this mailto:format'abc@domain.xyz";
        //    return false;
        //}
        //if (password.value.match == "^ /0-9/g") {
        //   password_s.innerHTML = "must contain 6 digits";
        //    return false;
        // }
        //if (username.value != "" && password.value != "") {
          //  return false;
       // }
}
