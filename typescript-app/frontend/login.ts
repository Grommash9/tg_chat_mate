document.addEventListener('DOMContentLoaded', function () {
  clearCookies();
  let login_button = document.getElementById(
    'login-button-object'
  ) as HTMLButtonElement;
  login_button.addEventListener('click', SignIn);

  let email_input = document.getElementById(
    'login-input-object'
  ) as HTMLInputElement;
  let password_input = document.getElementById(
    'password-input-object'
  ) as HTMLInputElement;

  email_input.addEventListener('keyup', function (event) {
    event.preventDefault();
    if (event.key === 'Enter') {
      SignIn();
    }
  });
  password_input.addEventListener('keyup', function (event) {
    event.preventDefault();
    if (event.key === 'Enter') {
      SignIn();
    }
  });
});

function SignIn() {
  let email_input = document.getElementById(
    'login-input-object'
  ) as HTMLInputElement;
  let password_input = document.getElementById(
    'password-input-object'
  ) as HTMLInputElement;
  let payload = {
    user_name: email_input.value,
    password: password_input.value
  };
  fetch(`/tg-bot/manager/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  }).then((response) => {
    if (response.status === 200) {
      return response.json().then((data) => {
        password_input.value = '';
        setCookie('AUTHToken', data['token'], 7);
        console.log('Success:', data);
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

function setCookie(name: string, value: string, daysToLive: number) {
  var cookieValue = encodeURIComponent(value);
  var cookie = name + '=' + cookieValue;

  if (typeof daysToLive === 'number') {
    cookie += '; max-age=' + daysToLive * 24 * 60 * 60;
    cookie += '; path=/';
  }

  document.cookie = cookie;
}

function clearCookies() {
  var cookies = document.cookie.split(';');

  for (var i = 0; i < cookies.length; i++) {
    var cookie = cookies[i];
    var eqPos = cookie.indexOf('=');
    var name = eqPos > -1 ? cookie.substring(0, eqPos) : cookie;
    document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
  }
}
