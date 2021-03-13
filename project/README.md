Table of Content
1. Introduction
2. Requirement and Set-up
	a) Requirements
	b) Set-Up
3. User roles, models and views
	a) Users roles
	b) Models
	c) Views
4. Functionality
	a) Register
	b) Login, Log-out
	c) Admin View
	d) Patient Index
	e) Add a Patient, Delete a patient
	f) Patient Profiles
		i) Profile picture
		ii) Patient Information
		iii) Hospitalization Status and History
		iv) Daily Log
		v) Allergies
		vi) Vitals
5. Limitations and improvements
6. References
7. Conclusion


1.	Introduction
This website is submitted as a capstone project for the CS50W class taken via HarvardX. It is a simple patient management system for a hospital which allows nurses and staff to track of the health of patients by keep a record of things such as allergies, vital signs and daily logs. It is still far from being at a level of being usable in a professional setting but it serves as a demonstration of what is possible.
It was developed by using Django as a platform and for portability, uses a minimal number of imported modules/functionalities static templates files as possible.

2.	Requirement and Set-up
	a)	Requirements
	-	CS50: For submitting the project.
	-	Django: The platform.
	-	Pillow: To allow the use of images in models.
	b)	Set-Up
	The following additions to the Django setting file are required:
	-	AUTH_USER_MODEL = “$APPNAME.User”
	-	MEDIA_URL = '/media/'
	-	MEDIA_ROOT = BASE_DIR / 'media'

3.	User roles, models and views
	a)	Users roles
	-	Guest: As a guest, user can only view the main splash page on the index view. attempts to view any other page will redirect to a login page.
	-	Nurse/Regular User: Nurses/Regular users can view, edit/add/delete patient pages.
	-	Admin: Admin users have full authority. Including editing all models manually view the admin portal.
	b)	Models
	-	Users: Because patients and guests do not have the ability to view and edit pages, users are simply synonymous with nurses/regular users as described above.
	-	Patients: this model contains the basic information for all patients, including name. age, address, profile picture, etc.
	-	Logs: Contains the daily logs. Each log is linked to a nurse and a patient, so that they can be displayed on the correct patient page and the author + timestamp of the log is known.
	-	Hospitalizations: This model contains the check-in, check-out timestamps for each patient. This allows to know if a patient is currently hospitalized or has been hospitalized in the past and when.
	-	Allergies: Contain the allergies applicable to each patient, including the allergy cause, the effects, category and severity.
	-	Records: contains all the vital sign records for each patient for vital signs (heart Rate, respiratory rate, blood pressure, body temperature).
	c)	Views
	-	index view: Renders the static index.html “splash” page.
	-	login_view, logout_view, register views: These view provide the login, logout and register pages respectively. They were taken directly from earlier CS50W projects.
	-	patientindex view: This view provides the list of all patients registered in the system and sends it to the template patientindex.html to display the list of patients in paginated tables of 20 patients.
	-	Patient view: This is the most complex view of the project. It receives the patient id as an input and display the patient profile. It uses the patient ID to extract the patient model, the applicable allergies, logs and hospitalization statuses. The results are then shown in paginated tables on the profile.html template.
	-	addpatient, editpatient, deletepatient views: These views give a registered the ability to add a patient, and edit or delete an existing patient when the request is sent by POST. If the request is not via POST, the context 	parameters (including forms) are sent to the templates add.html, edit.html and delete html respectively.
	-	editpicture view: This view allows a registered user to edit or add a picture for a patient profile.
	-	checkinout view: This view allows a registered user to change the patient’s status from check-in to checked out of the hospital.
	-	addlog, editlog, deletelog views: These views give a registered the ability to add a daily log item for patient, and edit or delete an existing  log for a patient when the request is sent by POST. If the request is not via POST, the context parameters (including forms) are sent to the templates add.html, edit.html and delete html respectively.
	-	addallergy, editallergy, deleteallergy views: These views give a registered the ability to add an allergy for patient, and edit or delete an existing  allergy for a patient when the request is sent by POST. If the request is not via POST, the context parameters (including forms) are sent to the templates add.html, edit.html and delete html respectively.
	-	chart view: This view gets the patient id and vital sign id as an input, and then extracts the required data from the database. It then formats the data in the proper format required by Google Charts via a JSON format, so that 	the graphs can be viewed and update without refreshing the page. The data decimal data is encoded for JSON by using the DecimalEncoder class.

4.	Functionality
	a)	Register
	This allows anyone with access to the website to register an account as a nurse/regular user.
	b)	Login, Log-out
	A user can login and logout by clicking the link
	c)	Admin View
	The admin view provides an administrator with the ability to edit any data in any model shown in the section above.
	d)	Patient Index
	One a user is logged-in, this page can be accessed to see a list of patients registered in the database. When a patient is clicked, the user is taken to the patient’s profile page.
	e)	Add a Patient, Delete a patient
	A user can add a new patient, which includes patient information such as patient name, birth date, contact information, gender, bed location, insurance information and secondary contact information etc. A profile picture can also be 	uploaded.
	f)	Patient Profiles
		i) Profile picture
		The user profile can include a picture, which can be enlarged when it is clicked. A button above the picture allows a user to update or add a profile picture.
		ii)	Patient Information
		The profile information is displayed, which shows the patient name, birth date, contact information, gender, bed location, insurance information and secondary contact information etc. All these fields can be edited at a later date.
		iii) Hospitalization Status and History
		It is possible to check-in or a check-out a patient of the hospital. This way, a patient profile can be kept intact should a patient be released, in case he/she is re-admitted to the hospital at later date. A record of check-ins and check-outs should be displayed.
		iv)	Daily Log
		The page should display a daily log, written by a nurse, showing the log content, the author and a time/date; the logs are displayed from newest to latest. It should be possible for a user to add a new log, and to delete/edit previous logs.
		v) Allergies
		The page should display allergies for a patient, showing details about the allergy such as allergy type, reaction, severity. It should be possible for a user to add a new allergy, and to delete/edit existing allergies.
		vi)	Vitals
		The page shows a plot of the vitals (blood pressure, respiratory rate, body temperature, heart rate) over time for the patient. It is possible to add a point for the current time/data for the select vital sign. The charts use a JSON 		response so that the charts can be updated without having to refreshing the page. The charts are powered by Google Charts, this is so charts can be displayed without installing any other dependencies for Django.

5.	Limitations and improvements
-	It should not be possible for any person who visits the page to register and therefore, edit/delete/add patient information. In a real life scenario, this should not be possible
-	Patient index should sortable and searchable.
-	When a adding a patient, there should be a way to check of the patient already exists.
-	Bed location should be linked to the check-in button (not to the patient information as it is currently). Furthermore, check-in button should also include a “reason for hospitalization” field.
-	Daily logs should contain more necessary fields (such as toilet use, eating habits, etc.)
-	Times should displayed as per the user’s time zone, currently uses UTC
-	Chart data should be editable and the range should be adjustable as well.
-	Users should have a profile page/customized home page.
-	Field validation could be added for many fields.
-	Profile pictures should be compressed at upload. Also, a delete button should be added to the “edit/upload picture” page. (currently, picture can be deleted by submitting the form with no file uploaded).
-	Blood pressure charts should be overlayed.
-	Models should have better description/names in the admin panel

6.	References
https://www.djangoproject.com/  - General resource
https://www.w3.org/ - General resource
https://getbootstrap.com/docs/4.3/getting-started/introduction/  -  The entire layout was taken from bootstrap documentation examples.
https://stackoverflow.com/questions/44133562/django-add-placeholder-text-to-form-field - How to add placeholder text to a Django form.
https://stackoverflow.com/questions/1960516/python-json-serialize-a-decimal-object -	How to JSON serialize decimal object. Logic for this was taken from there.
https://developers.google.com/chart/interactive/docs/php_example - For chart implementation.
https://developers.google.com/chart/interactive/docs/gallery/linechart - For chart implementation.
https://simpsons.fandom.com/wiki/Snowball_I - Simpsons cat picture.
http://www.dummytextgenerator.com/ - Random text generator

7.	Conclusion
Thank you!
