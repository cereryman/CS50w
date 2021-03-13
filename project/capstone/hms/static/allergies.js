document.addEventListener('DOMContentLoaded', function() {
  // Call the function to add an allergy
  show_add_allergy_form();
});

function show_add_allergy_form() {
	document.querySelector('#add-allergy').addEventListener('click', () => {
		form = document.getElementById("add-allergy-form");
		if (form.style.display == 'block') {
			form.style.display = 'none';
			document.querySelector('#add-allergy').className = "btn btn-primary btn-lg";
    		document.querySelector('#add-allergy').innerHTML = "+ Add Allergy";
		}
		else {
			form.style.display = 'block';
			document.querySelector('#add-allergy').className = "btn btn-danger btn-lg";
    		document.querySelector('#add-allergy').innerHTML = "Cancel";
		}
	});
}