document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // Detect when the user click the sends button.
  document.querySelector("#compose-form").onsubmit = () => {
    // obtain values from the form and send to the API
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: document.querySelector('#compose-recipients').value,
        subject: document.querySelector('#compose-subject').value,
        body: document.querySelector('#compose-body').value
      }),
    })
    // Check if response is successful. (Note that I would prefer to use a status code for checking the status, but views.py only outputs a message.)
    .then(response => response.json())
    .then(result => {
      // debug console.log(result);
      // If successful, show confirmation message and load the sent mailbox.
      if (result.message == "Email sent successfully.") {
        alert(result.message);
        load_mailbox("sent");
      }
      // Else, show error message
      else {
        alert(result.error);
      }
    });
    // Prevent the default submission of the form
    return false;
  }
}

function load_mailbox(mailbox) {

  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Request emails
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Process mail items
    emails.forEach(email => {
      // Check read status
      if (email.read) {
        is_read = "read"
      }
      else {
        is_read = "unread"
      }
      // If the mail is sent box, the displayed name should be the recipient (this is different from the requirement, but is as per most mail clients)
      if (mailbox == "sent") {
        displayname = email.recipients
      }
      else {
        displayname = email.sender
      }
      // For each mail item, create new email listing
      const element = document.createElement('div');
      element.className = `row mailitem ${is_read}`; //read status has a CSS class.
      element.innerHTML = `<div class="column recipient left" id=>
                            ${displayname}
                          </div>
                          <div class="column middle">
                            <a href="#" id="${email.id}">${email.subject}</a>
                          </div>
                          <div class="column right">
                           ${email.timestamp}
                          </div>`;
      // Add email listing to DOM
      document.querySelector('#emails-view').append(element);
      // If mail item is clicked, display the email. In seperate function due to the complexity of the code.
      element.addEventListener('click', () => view_mail_item(email.id, mailbox));
    });
  });
}

function view_mail_item(id, mailbox) {

  // Mark the mail item as read
  fetch(`/emails/${id}`, {
    method: 'PUT',
    body: JSON.stringify({
      read: true,
    }),
  });
  // Clear the emails-view part of the DOM
  document.querySelector('#emails-view').innerHTML = "";
  // Fetch the mail item's data
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    // Print email
    // debug console.log(email);
    const element = document.createElement('div');
    element.innerHTML = `<div class="card" style="width: 20rem;">
                          <div class="card-body">
                            <h6 class="card-subtitle mb-2 text-muted"><b>From:</b> ${email.sender}</h6>
                            <h6 class="card-subtitle mb-2 text-muted"><b>To:</b> ${email.recipients}</h6>
                            <h6 class="card-subtitle mb-2 text-muted"><b>Subject:</b> ${email.subject}</h6>
                            <h6 class="card-subtitle mb-2 text-muted"><b>Timestamp:</b> ${email.timestamp}</h6>
                            <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
                          </div>
                        </div>
                        <p>${email.body}</p>`;
    // Add email item to DOM
    document.querySelector('#emails-view').append(element);
    // Add the archive button
    const archivebutton = document.createElement('div');
    // If mailbox is sent, disable the archive button.
    if (mailbox != "sent") {
      // If the mail item is already arhived, change the text on the button to "archived"
      if (email.archived == false) {
      archivebutton.innerHTML = `<button class="btn btn-secondary" id="archive">Archive</button>`;
      }
      else {
      archivebutton.innerHTML = `<button class="btn btn-secondary" id="archive">Archived</button>`;
      }
    }
    else {
      archivebutton.innerHTML = `<button class="btn btn-secondary" disabled id="archive">Archive</button>`;
    }
    document.querySelector('#emails-view').append(archivebutton);
    // On archive button is clicked, change the archive status in DB
    document.querySelector('#archive').addEventListener('click', () => {
      fetch(`/emails/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email.archived,
        }),
      });
      // Load the inbox
      load_mailbox("inbox");
      // Quick bug fix: Need force a reload, because sometimes the inbox does not update on the first load.
      location.reload(true);
    });
    // Check if the reply button is clicked
    document.querySelector('#reply').addEventListener('click', () => {
      displayname = email.sender
      // If mailbox is "sent", the recipient should be the original recipient, not the sender (which is the current user). (this is different from the requirement, but is as per most mail clients)
      if (mailbox == "sent") {
        replyto = email.recipients
      }
      else {
        replyto = email.sender
      }
      // Load the compose page and prefill the fields.
      compose_email();
      // Check if subjet already includes "Re:"
      var patt = new RegExp("Re:");
      if (!patt.test(email.subject)) {
        subject = `Re: ${email.subject}`;
      }
      else {
        subject = email.subject;
      }
      timedate = email.timestamp;
      body = email.body;
      document.querySelector("#compose-recipients").value = replyto;
      document.querySelector("#compose-subject").value = subject;
      document.querySelector("#compose-body").value = `\n\n\n-----------------------------\nOn ${timedate}, ${displayname} wrote: \n${body}`;
    });
  });
}