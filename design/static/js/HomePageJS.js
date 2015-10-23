function accountAccess(accessType)
{
	var username = document.getElementById('usernameInput').value;
	var password = document.getElementById('passwordInput').value;
	var accessType = accessType + ""

	var query = 
	[{
		"accesstype" : accessType,
		"username": username,
		"password": password
	}];

	$.ajax({
		type: 'POST',
		url: "http://livecodedocs.csse.rose-hulman.edu:5000/login",
		data: JSON.stringify(query, null, '\t'),
		contentType: "application/json; charset=utf-8",
		dataType: "json"
	}); 
}

document.addEventListener('DOMContentLoaded', function () {
	document.getElementById('loginbutton').addEventListener("click", function () { accountAccess(0); });
	document.getElementById('signupbutton').addEventListener("click", function () {accountAccess(0); });
	document.getElementById('loginbutton').addEventListener("click", function () {window.location.href = "../templates/project.html"})
	document.getElementById('helpButton').addEventListener("click", function () {window.location.href = "../templates/Help.html"})
});
