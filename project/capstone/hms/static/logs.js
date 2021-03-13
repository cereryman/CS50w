document.addEventListener('DOMContentLoaded', function() {
  // Call the function to add an log
  show_add_log_form();
});

function show_add_log_form() {
	document.querySelector('#add-log').addEventListener('click', () => {
		form = document.getElementById("add-log-form");
		if (form.style.display == 'block') {
			form.style.display = 'none';
			document.querySelector('#add-log').className = "btn btn-primary btn-lg";
    		document.querySelector('#add-log').innerHTML = "+ Add Log";
		}
		else {
			form.style.display = 'block';
			document.querySelector('#add-log').className = "btn btn-danger btn-lg";
    		document.querySelector('#add-log').innerHTML = "Cancel";
		}
	});
}