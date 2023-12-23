import {displayDialogList} from '../index.js';

function getChatListFromApi() {
    fetch('/tg-bot/chat-list', {
      method: 'GET'
    })
      .then((response) => {
        if (response.status !== 200) {
          throw new Error('Network response was not ok ' + response.statusText);
        }
        return response.json();
      })
      .then((data) => {
        console.log('Data received:', data);
        displayDialogList(data);
      })
      .catch((error) => {
        console.error(
          'There has been a problem with your fetch operation:',
          error
        );
      });
  }

export default getChatListFromApi;