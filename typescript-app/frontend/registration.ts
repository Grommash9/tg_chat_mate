document.addEventListener('DOMContentLoaded', function () {
  let create_manager_button = document.getElementById(
    'create-manager-account-button'
  ) as HTMLButtonElement;
  create_manager_button.addEventListener('click', CreateManager);

  let email_input = document.getElementById(
    'login-input-object'
  ) as HTMLInputElement;
  let password_input = document.getElementById(
    'password-input-object'
  ) as HTMLInputElement;
  let full_name_input = document.getElementById(
    'full-name-input-object'
  ) as HTMLInputElement;

  full_name_input.addEventListener('keyup', function (event) {
    event.preventDefault();
    if (event.key === 'Enter') {
      CreateManager();
    }
  });

  email_input.addEventListener('keyup', function (event) {
    event.preventDefault();
    if (event.key === 'Enter') {
      CreateManager();
    }
  });
  password_input.addEventListener('keyup', function (event) {
    event.preventDefault();
    if (event.key === 'Enter') {
      CreateManager();
    }
  });
});

function CreateManager() {
  let email_input = document.getElementById(
    'login-input-object'
  ) as HTMLInputElement;
  let password_input = document.getElementById(
    'password-input-object'
  ) as HTMLInputElement;
  let full_name_input = document.getElementById(
    'full-name-input-object'
  ) as HTMLInputElement;
  let payload = {
    user_name: email_input.value,
    password: password_input.value,
    full_name: full_name_input.value
  };
  fetch(`/tg-bot/registration`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  }).then((response) => {
    if (response.status === 200) {
      return response.json().then((data) => {
        password_input.value = '';
        alert('Account was created, please wait for activation');
        window.location.replace('/');
      });
    } else {
      return response.json().then((data) => {
        password_input.value = '';
        alert(`Error: ${data['error']}`);
        console.error('Error:', data['error']);
      });
    }
  });
}
