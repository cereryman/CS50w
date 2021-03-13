document.addEventListener('DOMContentLoaded', function() {
  // First, hide all the edit forms.
  var editforms = document.querySelectorAll('.edit-form');
      i = 0;
      l = editforms.length;
  for (i; i < l; i++) {
      editforms[i].style.display = 'none';
  }
  // Execute the like and edit functions.
  like();
  edit();
});

function like() {
  // Detect like click
  document.querySelectorAll('.like').forEach(post => {
    post.addEventListener('click', () => {
      // Change the like status for user and write to DB
      fetch(`/like/${post.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          like: !post.like,
        }),
      });
      // Calculated and # of likes and detect if user already liked by checking color.
      const like_count = parseInt(document.getElementById(`count-like-${post.id}`).innerText);
      // If the heart is red, user liked it.
      if (post.style.color == "red") {
        liked = true;
      }
      else {
        liked = false;
      }
      // If the user already like, decrease like count, other side increase by one. Change color accordinly.
      if (liked) {
        document.getElementById(`count-like-${post.id}`).innerText = like_count - 1;
        post.setAttribute('style', 'color: black');
      }
      else {
        document.getElementById(`count-like-${post.id}`).innerText = like_count + 1;
        post.setAttribute('style', 'color: red');
      }
    });
  });
}

function edit() {
  document.querySelectorAll('.edit').forEach(post => {
    // user is editing flag
    editing = false;
    // Detect edit/cancel link click
    post.addEventListener('click', () => {
      // If the user is not editing, onclick, show the edit view
      if (editing != true) {
        editing = true;
        // Change the link text to cancel, hide the post, show the edit form
        document.getElementById(`${post.id}`).getElementsByTagName('a')[0].innerHTML = "Cancel"
        document.getElementById(`post-body-${post.id}`).style.display = 'none';
        body = document.getElementById(`post-body-${post.id}`).innerText
        document.getElementById(`edit-form-${post.id}`).style.display = 'block';
        document.getElementById(`edit-form-body-${post.id}`).value = `${body}`;
        // Detect when the user click the save button.
        document.querySelector(`#edit-submit-${post.id}`).onsubmit = () => {
          // obtain values from the form and send to the API
          fetch(`/edit/${post.id}`, {
            method: 'POST',
            body: JSON.stringify({
              body: document.getElementById(`edit-form-body-${post.id}`).value
            }),
          })
          // Check if response is successful. #TODO: change to checking the status code
          .then(response => response.json())
          .then(result => {
            // If successful, show confirmation message.
            if (result.message == "Post edited successfully.") {
              alert(result.message);
              document.getElementById(`post-body-${post.id}`).style.display = 'block';
              document.getElementById(`edit-form-${post.id}`).style.display = 'none';
              editing = false;
              // Quick bug fix: Need force a reload of the page to show updated post.
              location.reload(true);
            }
            // Else, show error message
            else {
              alert(result.message);
            }
          });
          //Prevent the default submission of the form
          return false;
        }
      }
      else {
        // If the user is editing, onclick, "cancel" and return to the normal view
        document.getElementById(`${post.id}`).getElementsByTagName('a')[0].innerHTML = "Edit"
        document.getElementById(`post-body-${post.id}`).style.display = 'block';
        document.getElementById(`edit-form-${post.id}`).style.display = 'none';
        editing = false;
      }
    });
  });
}