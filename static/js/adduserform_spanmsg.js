var add_form = document.getElementById('save_btn');
add_form.onclick = function () {
    //fields
    var first_name = document.getElementById("first_name");
    var last_name = document.getElementById("last_name");
    var username = document.getElementById("username");
    var email = document.getElementById("email");
    var role = document.getElementById("role");
    var password = document.getElementById("password");
    var repassword = document.getElementById("confirm_password");
    var male_gender = document.getElementById("male");
    var female_gender = document.getElementById("female");
    var fileInput = document.getElementById("fileInput");

    //span tags
    
    var u_user = document.getElementById("u_username");
    var u_firstn = document.getElementById("u_firstn");
    var u_lastn = document.getElementById("u_lastn");
    var u_mail = document.getElementById("u_mail");
    var u_role = document.getElementById("u_role");
    var u_pwd = document.getElementById("u_pwd");
    var u_con_pwd = document.getElementById("u_con_pwd");
    var u_gen = document.getElementById("u_gen");
    var u_file = document.getElementById("u_file");

    first_name.style.border = "none";
    last_name.style.border = "none";
    email.style.border = "none";
    username.style.border = "none";
    role.style.border ="none";
    password.style.border = "none";
    repassword.style.border = "none";
    username.style.border = "none";
    male_gender.style.border = "none";
    female_gender.style.border = "none";
    fileInput.style.border = "none";

    u_firstn.style.display = "none";
    u_lastn.style.display = "none";
    u_user.style.display = "none";
    u_user.style.display = "none";
    u_mail.style.display = "none";
    u_role.style.display = "none";
    u_pwd.style.display = "none";
    u_con_pwd.style.display = "none";
    // u_mob.style.display = "none";
    u_gen.style.display = "none";
    u_file.style.display = "none";

    // if (username.value == "" && first_name.value == "" && last_name.value == "" && email.value == "" && password.value == "" && repassword.value == "" && mobile.value == "" && gender.value == ""){
    //     main_form_span.innerHTML = "empty form";
    //     main_form_span.style.display = "block";
    //     return false;
    // }
    if (username.value === "") {
        u_user.innerHTML = "Enter username";
        username.style.border = "1px solid red";
        u_user.style.display = "block";
        return false;
    }
    else if (!username.value.match(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/)) {
        u_user.innerHTML = "Please enter valid username ";
        username.style.border = "1px solid red";
        u_user.style.display = "block";
        return false;
    }
    if (first_name.value == "") {
        u_firstn.innerHTML = "Enter first name";
        first_name.style.border = "1px solid red";
        u_firstn.style.display = "block";
        return false;
    }
  
    if (last_name.value == "") {
        u_lastn.innerHTML = "Enter Last name";
        last_name.style.border = "1px solid red";
        u_lastn.style.display = "block";
        return false;
    }

    if (email.value === "") {
        u_mail.innerHTML = "Empty email field";
        email.style.border = "1px solid red";
        u_mail.style.display = "block";
        return false;
    }
    else if (!email.value.match(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/)) {
        u_mail.innerHTML = "Please enter valid email";
        email.style.border = "1px solid red";
        u_mail.style.display = "block";
        return false;
    }
    if (role.value == "") {
        u_role.innerHTML = "Please select";
        role.style.border = "1px solid red";
        u_role.style.display = "block"; 
        return false;
    }

    if (password.value == "") {
        u_pwd.innerHTML = "Enter password";
        password.style.border = "1px solid red";
        u_pwd.style.display = "block";
        return false;
    }
    if (repassword.value == "") {
        u_con_pwd.innerHTML = "Enter confirm password";
        repassword.style.border = "1px solid red";
        u_con_pwd.style.display = "block";
        return false;
    }
    if (password.value != repassword.value) {
        u_con_pwd.innerHTML = "Password doesn't match Confirm Password";
        repassword.style.border = "1px solid red";
        u_con_pwd.style.display = "block";
        return false;
    }
     
    if (male_gender.checked == '' && female_gender.checked == '' ) {
        u_gen.innerHTML=" Please choose any one";
        male_gender.style.border = "1px solid red";
        female_gender.style.border = "1px solid red";
        u_gen.style.display = "block";
        return false;
    }
    if (fileInput.value == '') {
        u_file.innerHTML = "Choose file";
        fileInput.style.border = "1px solid red";
        u_file.style.display = "block";
        return false;
    }
     
   
  
    // if (mobile.value == "") {
    //     u_mob.innerHTML = "Enter mobile number";
    //     mobile.style.border ="1px solid red";
    //     u_mob.style.display = "block";
    //     return false;
    // }
    // if (gender.value === "") {
    //     u_gen.innerHTML = "Select a gender";
    //     u_gen.style.display = "block";
    //     return false;
    // }


   return true;

}

