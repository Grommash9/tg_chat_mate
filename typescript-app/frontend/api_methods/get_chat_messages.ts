import {displayChatHistory} from '../index.js';

function loadChatMessages(chat_id: number) {
    fetch('/tg-bot/get-messages/' + chat_id, {
      method: 'GET'
    })
      .then((response) => {
        if (response.status !== 200) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json(); // Parse JSON response
      })
      .then((data) => {
        console.log('Data received:', data);
        displayChatHistory(data); // Function to handle the display of data
      })
      .catch((error) => {
        console.error(
          'There has been a problem with your fetch operation:',
          error
        );
      });
  }

export default loadChatMessages;