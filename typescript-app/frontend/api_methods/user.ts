function GetUser(user_id: number) {
  return fetch(`/tg-bot/user/` + user_id, {
    method: 'GET'
  })
    .then((response) => {
      if (response.status === 200) {
        return response.json().then((data) => {
          console.log('GET user data:', data);
          return data; // Return the data instead of just true
        });
      } else {
        return response.json().then((data) => {
          alert(`Error: ${data['result']}`);
          console.error('Error:', data['result']);
          return null; // Return null or an appropriate error object
        });
      }
    })
    .catch((error) => {
      console.error('There was an error during getting user:', error);
      return null; // Return null or an appropriate error object
    });
}

function UpdateUser(user_id: number, payload: object) {
  return fetch(`/tg-bot/user/` + user_id, {
    method: 'POST',
    body: JSON.stringify(payload),
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then((response) => {
      if (response.status === 200) {
        return response.json().then((data) => {
          console.log('Success user was modified', data);
          return true; // Resolve the promise with true
        });
      } else {
        return response.json().then((data) => {
          alert(`Error: ${data['result']}`);
          console.error('Error:', data['result']);
          return false; // Resolve the promise with false
        });
      }
    })
    .catch((error) => {
      console.error('There was an error modifying the user:', error);
      return false; // Resolve the promise with false
    });
}

export { UpdateUser, GetUser };
