import { displayManagerInfo, Manager } from '../index.js';

function getManagerInfoAndDisplay() {
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

function getManager(): Promise<Manager> {
  return fetch('/tg-bot/manager/get-me', {
    method: 'GET'
  })
    .then((response) => {
      if (response.status !== 200) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .then((data: {"manager_info": Manager}) => {
      console.log('Data received:', data);
      return data["manager_info"]; // Return the data conforming to the Manager interface
    })
    .catch((error) => {
      console.error(
        'There has been a problem with your fetch operation:',
        error
      );
      throw error; // Rethrow the error
    });
}

export { getManager, getManagerInfoAndDisplay };
