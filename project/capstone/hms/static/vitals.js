document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  document.querySelector('#SYS_BP').addEventListener('click', () => load_chart('SYS_BP'));
  document.querySelector('#DIA_BP').addEventListener('click', () => load_chart('DIA_BP'));
  document.querySelector('#RR').addEventListener('click', () => load_chart('RR'));
  document.querySelector('#BT').addEventListener('click', () => load_chart('BT'));
  document.querySelector('#HR').addEventListener('click', () => load_chart('HR'));
  // Load chart
  load_chart();
  // Call the function to add a point
  add();
});

function load_chart(vital) {
  // default error message if JSON request comes in empty or data is incorrectly formatted.
  var error_msg = "No data!";
  // Initialize title variable
  var title;
  // Default chart to load vital is blank.
  vital = (typeof vital !== 'undefined') ?  vital : 'HR';
  // Set global variable VITAL
  VITAL = vital;
  // for each vital, deactivave the button if seledted
  for (i = 0; i < VITALS.length; i++) {
    if (VITALS[i] != vital) {
      document.querySelector(`#${VITALS[i]}`).removeAttribute("disabled");
    }
    else {
      document.querySelector(`#${VITALS[i]}`).setAttribute("disabled", true);
    }
  }
  // for each vital, deactivave the button if seleted and set the chart title.
  // Eventually, should be dynamically set and not hard-coded
  if (vital == "SYS_BP") {
    title = "Systolic Blood Pressure";
  } else if (vital == "DIA_BP") {
    title = "Diastolic Blood Pressure";
  } else if (vital == "RR") {
    title = "Respiratory Rate";
  } else if (vital == "BT") {
    title = "Body Temperature";
  } else {
    title = "Heart Rate";
  }
  // Fetch the JSON data and display the charts.
  // References:
  // https://developers.google.com/chart/interactive/docs/php_example
  // https://developers.google.com/chart/interactive/docs/gallery/linechart
  var jsonData = "";
  $.ajax({
	  url: `/chart/${PATIENT}/${vital}`,
	  success: function (data) {
		  jsonData = data;
		  google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);
      // Parse the data and draw the chart
      function drawChart() {
	      jsonData = jsonData.trim();
	      jsonData = jsonData.replace(/'/g, '"');
	      jsonData = jQuery.parseJSON(jsonData);
	      var data = google.visualization.arrayToDataTable(jsonData);
	      var options = {
		      title: title,
		      legend: { position: 'bottom' }
	      };
	      var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
        // Catch google chart errors and replace with default message.
	      google.visualization.events.addListener(chart, 'error', function (googleError) {
          google.visualization.errors.removeError(googleError.id);
          document.querySelector('#curve_chart').innerHTML = error_msg;
        });
	      chart.draw(data, options);
      }
	   },
	   error: function (xhr, type) {
      document.querySelector('#curve_chart').innerHTML = error_msg;
	   }
  });
}

function add() {
  // By default, hide the form
  document.querySelector('#add-form').style.display = 'none';
  // user is adding flag
  adding = false;
  // If VITAL is empty or invalid, escape.
  if(typeof VITAL == 'undefined' || !VITALS.includes(VITAL)) return;
  // Detect add/cancel link click
  document.querySelector('#add-vital').addEventListener('click', () => {
    // If the user is not adding, onclick, show the add view
    if (adding != true) {
      adding = true;
      // Change the link text to cancel, show the add form and disable buttons to change chart
      var i;
      for (i = 0; i < VITALS.length; i++) {
        document.querySelector(`#${VITALS[i]}`).setAttribute("disabled", true);
      }
      document.querySelector('#add-vital').className = "btn btn-danger btn-lg";
      document.querySelector('#add-vital').innerHTML = "Cancel";
      document.querySelector('#add-form').style.display = 'block';
      // Detect when the user click the submit button.
      document.querySelector('#add-form').onsubmit = () => {
        // obtain values from the form and send to the API
        fetch(`/add_vital/${PATIENT}/${VITAL}`, {
          method: 'POST',
          body: JSON.stringify({
            value: document.querySelector('#add-value').value
          }),
        })
        // Check if response is successful.
        .then(response => response.json())
        .then(result => {
          // If successful, show confirmation message. renable the buttons and hife the form
          if (result.message == "Value added successfully.") {
            alert(result.message);
            document.querySelector('#add-vital').className = "btn btn-primary btn-lg";
            document.querySelector('#add-vital').innerHTML = "+ Add Value";
            document.querySelector('#add-form').style.display = 'none';
            adding = false;
            // Reload of the page to show updated graph.
            load_chart(VITAL);
          }
          // Else, show error message
          else {
            alert(result.message);
          }
        });
        //Prevent the default submission of the form
        return false;
      };
    }
    else {
      // If the user is adding, onclick, "cancel" and return to the normal view
      document.querySelector('#add-vital').className = "btn btn-primary btn-lg";
      document.querySelector('#add-vital').innerHTML = "+ Add Value";
      document.querySelector('#add-form').style.display = 'none';
      load_chart(VITAL);
      adding = false;
    }
  });
}