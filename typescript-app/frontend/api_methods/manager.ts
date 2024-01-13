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

function getAllManagers(): Promise<Manager[]> {
  return fetch('/tg-bot/manager', {
    method: 'GET'
  })
    .then((response) => {
      if (response.status !== 200) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .then((data: { managers: Manager[] }) => {
      console.log('Data received:', data);
      return data['managers']; // Return the data conforming to the Manager interface
    })
    .catch((error) => {
      console.error(
        'There has been a problem with your fetch operation:',
        error
      );
      throw error; // Rethrow the error
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
    .then((data: { manager_info: Manager }) => {
      console.log('Data received:', data);
      return data['manager_info']; // Return the data conforming to the Manager interface
    })
    .catch((error) => {
      console.error(
        'There has been a problem with your fetch operation:',
        error
      );
      throw error; // Rethrow the error
    });
}

function deleteManager(username: string) {
  const payload = { username: username };
  return fetch(`/tg-bot/manager`, {
    method: 'DELETE',
    body: JSON.stringify(payload),
    headers: {
      'Content-Type': 'application/json'
    }
  })
  .then((response) => {
    if (response.status === 204) { // Check for 204 status code
      console.log('Success: manager was deleted!');
      return true; // Resolve the promise with true
    } else {
      console.error('Error: manager was not deleted. Status code:', response.status);
      return false; // Resolve the promise with false
    }
  })
  .catch((error) => {
    console.error('There was an error in manager deleting:', error);
    return false; // Resolve the promise with false
  });
}


export { getManager, getManagerInfoAndDisplay, getAllManagers, deleteManager };
