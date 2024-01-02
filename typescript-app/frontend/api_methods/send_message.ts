function SendMessage(target_api_method: string, payload: object) {
  return fetch(`/tg-bot/` + target_api_method, {
    method: 'POST',
    body: JSON.stringify(payload),
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then((response) => {
      if (response.status === 200) {
        return response.json().then((data) => {
          console.log('Success message was sent', data);
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
      console.error('There was an error sending the message:', error);
      return false; // Resolve the promise with false
    });
}

export default SendMessage;
