import { displayManagerInfo } from '../index.js';

function getManagerInfo() {
  fetch('/tg-bot/manager/get-me', {
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
      displayManagerInfo(data['manager_info']);
    })
    .catch((error) => {
      console.error(
        'There has been a problem with your fetch operation:',
        error
      );
    });
}

export default getManagerInfo;
