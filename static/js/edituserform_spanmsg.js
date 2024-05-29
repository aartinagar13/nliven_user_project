var edit_form = document.getElementById('save_btn');
edit_form.onclick = function () {
		var first_name = document.getElementById("first_name");
		var last_name = document.getElementById("last_name");
		var email = document.getElementById("email");
		var password = document.getElementById("password");
		var repassword = document.getElementById("confirm_password");
		var fileInput = document.getElementById("fileInput");

		//span tags
		var u_firstn = document.getElementById("u_firstn");
		var u_lastn = document.getElementById("u_lastn");
		var u_mail = document.getElementById("u_mail");
		var u_pwd = document.getElementById("u_pwd");
		var u_con_pwd = document.getElementById("u_con_pwd");
		var u_file = document.getElementById("u_file");


		first_name.style.border ="none"; 
		last_name.style.border ="none";
		email.style.border ="none";
		password.style.border ="none";
		repassword.style.border ="none";
		fileInput.style.border = "none";

		u_firstn.style.display = "none";
		u_lastn.style.display = "none";
		u_mail.style.display = "none";
		u_pwd.style.display = "none";
		u_con_pwd.style.display = "none";
		u_file.style.display = "none";

		

		if (first_name.value == "") {
			u_firstn.innerHTML = "Enter first name";
			first_name.style.border = "1px solid red";
			u_firstn.style.display = "block";
			return false;
		}
		if (last_name.value == "") {
			u_lastn.innerHTML = "Enter Last name";
			last_name.style.border ="1px solid red";
			u_lastn.style.display = "block";
			return false;
		}
	

		if (email.value === "") {
			u_mail.innerHTML = "Empty email field";
			email.style.border ="1px solid red";
			u_mail.style.display = "block";
			return false;}
		else if( !email.value.match(/^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/)) {
			u_mail.innerHTML ="Please enter valid email";
			email.style.border ="1px solid red";
			u_mail.style.display = "block";
			return false;
		}
	
		if (password.value == "") {
			u_pwd.innerHTML = "Enter password";
			password.style.border ="1px solid red";
			u_pwd.style.display = "block";
			return false;
		}
		if (repassword.value == "") {
			u_con_pwd.innerHTML = "Enter confirm password";
			repassword.style.border ="1px solid red";
			u_con_pwd.style.display = "block";
			return false;
		}
		if (password.value != repassword.value) {
			u_con_pwd.innerHTML = "Password doesn't match Confirm Password";
			repassword.style.border = "1px solid red";
			u_con_pwd.style.display = "block";
			return false;
		}
		if (fileInput.value == '') {
			u_file.innerHTML = "Choose file";
			fileInput.style.border = "1px solid red";
			u_file.style.display = "block";
			return false;
		}
		 
		return true;
    }