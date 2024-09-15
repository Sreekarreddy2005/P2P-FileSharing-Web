const socket = io();
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('fileInput');
const chooseFileButton = document.getElementById('chooseFileButton');
const uploadButton = document.getElementById('uploadButton');
const fileLink = document.getElementById('fileLink');
const shareOptions = document.getElementById('shareOptions');
const copyLinkButton = document.getElementById('copyLinkButton');
const emailLinkButton = document.getElementById('emailLinkButton');
const whatsappLinkButton = document.getElementById('whatsappLinkButton');
const loginButton = document.getElementById('loginButton');
const logoutButton = document.getElementById('logoutButton');

// Function to display a confirmation message
function displayConfirmationMessage(message) {
    alert(message);
}

dropZone.addEventListener('click', () => {
    fileInput.click();
});

chooseFileButton.addEventListener('click', () => {
    fileInput.click();
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('hover');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('hover');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('hover');
    const files = e.dataTransfer.files;
    fileInput.files = files;
    displayConfirmationMessage('File has been chosen: ' + files[0].name);
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length > 0) {
        displayConfirmationMessage('File has been chosen: ' + fileInput.files[0].name);
    }
});

uploadButton.addEventListener('click', () => {
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        const fileUrl = data.file_url;
        const message = data.message;
        fileLink.innerHTML = `<a href="${fileUrl}" target="_blank">Download File</a>`;
        shareOptions.style.display = 'block';
        alert(message); // Display success message

        copyLinkButton.onclick = () => {
            navigator.clipboard.writeText(fileUrl).then(() => {
                alert('Link copied to clipboard!');
            });
        };

        emailLinkButton.onclick = () => {
            window.location.href = `mailto:?subject=File Sharing Link&body=Here is your file link: ${fileUrl}`;
        };

        whatsappLinkButton.onclick = () => {
            window.location.href = `https://wa.me/?text=Here is your file link: ${fileUrl}`;
        };
    })
    .catch(error => {
        console.error('Error:', error);
        alert('File upload failed. Please try again.'); // Display error message
    });
});

socket.on('message', (data) => {
    console.log(data);
});

document.addEventListener('DOMContentLoaded', function() {
    const loggedIn = document.cookie.split('; ').find(row => row.startsWith('loggedIn='));
    if (loggedIn && loggedIn.split('=')[1] === 'true') {
        loginButton.textContent = 'Logged In';
        loginButton.disabled = true;
        logoutButton.style.display = 'inline-block';
    } else {
        loginButton.textContent = 'Login';
        loginButton.disabled = false;
        logoutButton.style.display = 'none';
    }
});

logoutButton.addEventListener('click', () => {
    document.cookie = "loggedIn=false; path=/; expires=Thu, 01 Jan 1970 00:00:00 GMT";
    loginButton.textContent = 'Login';
    loginButton.disabled = false;
    logoutButton.style.display = 'none';
});
