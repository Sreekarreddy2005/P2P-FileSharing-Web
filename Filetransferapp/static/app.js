const socket = io();
const dropZone = document.getElementById('drop-zone');
const fileInput = document.getElementById('fileInput');
const uploadButton = document.getElementById('uploadButton');
const fileLink = document.getElementById('fileLink');
const shareOptions = document.getElementById('shareOptions');
const copyLinkButton = document.getElementById('copyLinkButton');
const emailLinkButton = document.getElementById('emailLinkButton');
const whatsappLinkButton = document.getElementById('whatsappLinkButton');

dropZone.addEventListener('click', () => {
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
        const fileUrl = data.file_url;
        fileLink.innerHTML = `<a href="${fileUrl}" target="_blank">Download File</a>`;
        shareOptions.style.display = 'block';

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
    .catch(error => console.error('Error:', error));
});

socket.on('message', (data) => {
    console.log(data);
});
