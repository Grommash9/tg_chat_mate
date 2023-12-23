function FileUpload() {
    let attachment_input = document.getElementById(
      'file-input'
    ) as HTMLInputElement;
  
    attachment_input.click();
    attachment_input.addEventListener('change', function (event) {
      const input = event.target as HTMLInputElement;
      if (input && input.files && input.files.length > 0) {
        const file = input.files[0];
        console.log("file", file)
        if (file) {
          const reader = new FileReader();
          reader.onload = function (evt) {
            const fileReader = evt.target as FileReader;
              const binary = fileReader.result;
              let headers = {
                'X-Filename': file.name,
                'Content-Type': file.type
              };
  
              fetch('/tg-bot/file_upload', {
                method: 'POST',
                body: binary,
                headers: headers
              })
                .then((response) => response.json())
                .then((data) => {
                  if (
                    (data.error && data.error === 'file uploaded!') ||
                    data.error === 'file already exists!'
                  ) {
                    const fileList = document.getElementById(
                      'files-attachment-list'
                    );
                    if (fileList) {
                      fileList.innerHTML = '';
                    }
                    const listItem = document.createElement('li');
                    listItem.classList.add('file-attached');
                    listItem.id = data['file_id'];
                    const fileName = document.createElement('p');
                    fileName.classList.add('attached-file-name');
                    fileName.id = 'attached-file-name';
                    fileName.innerText = file.name;
                    listItem.appendChild(fileName);
                    const removeButton = document.createElement('button');
                    removeButton.classList.add('remove-attachment-button');
                    removeButton.innerText = 'Remove';
                    removeButton.onclick = function () {
                      listItem.remove();
                    };
  
                    listItem.appendChild(removeButton);
                    if (fileList) {
                      fileList.appendChild(listItem);
                    }
                    console.log('File uploaded id:', data['file_id']);
                  } else {
                    alert(`Error: ${data.error}`);
                    console.error('Failed to upload file:', data.error);
                  }
                })
                .catch((error) => {
                  console.error(
                    'There has been a problem with your fetch operation:',
                    error
                  );
                });
            }
            reader.readAsArrayBuffer(file);
          };
      }
    });
  }

export default FileUpload;