function myfunc(){
	var usr = document.getElementById('x').value;
	var pass = document.getElementById('y').value;
	window.alert('Inside Function');
	window.alert(JSON.stringify({"username":usr,"password":pass}));
	fetch('api/user/login',{
		method: 'POST',
		headers: {
			'Accept':'application/json',
			'Content-Type':'application/json'					
		}
		body: JSON.stringify({"username":usr,"password":pass})
	}).then(function(response){
		window.alert(response);
	});
}