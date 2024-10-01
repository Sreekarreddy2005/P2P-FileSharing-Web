document.addEventListener('DOMContentLoaded', function() {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('fileInput');
    const chooseFileButton = document.getElementById('chooseFileButton');
    const uploadButton = document.getElementById('uploadButton');
    const fileLink = document.getElementById('fileLink');
    const fileNames = document.getElementById('fileNames');
    const uploadStatus = document.getElementById('uploadStatus');
    const shareOptions = document.getElementById('shareOptions');
    const copyLinkButton = document.getElementById('copyLinkButton');
    const emailLinkButton = document.getElementById('emailLinkButton');
    const whatsappLinkButton = document.getElementById('whatsappLinkButton');

    // Handle click on drop zone to open file selector
    dropZone.addEventListener('click', function(e) {
        fileInput.click();
    });

    // File selection through the choose file button
    chooseFileButton.addEventListener('click', function () {
        fileInput.click();
    });

    // Handle file selection
    fileInput.addEventListener('change', function () {
        displayFileNames();
    });

    // Display the names of selected files
    function displayFileNames() {
        const files = fileInput.files;
        fileNames.innerHTML = '';
        if (files.length > 0) {
            for (let i = 0; i < files.length; i++) {
                fileNames.innerHTML += `<p>${files[i].name}</p>`;
            }
            uploadStatus.innerHTML = '<p>Files ready to be uploaded.</p>';
        }
    }

    // Handle the file upload process
    uploadButton.addEventListener('click', function () {
        const files = fileInput.files;
        if (files.length === 0) {
            uploadStatus.innerHTML = '<p style="color: red;">No files selected for upload. Please choose a file first.</p>';
            return;
        }

        const formData = new FormData();
        for (let i = 0; i < files.length; i++) {
            formData.append('file', files[i]);
        }

        uploadStatus.innerHTML = '<p>Uploading files...</p>';
        uploadFiles(formData);
    });

    // Function to upload files to the server
    function uploadFiles(formData) {
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.file_urls) {
                const urls = data.file_urls;
                fileLink.innerHTML = 'Files uploaded successfully! <br>' + 
                    urls.map(url => `<a href="${url}" target="_blank">${url}</a>`).join('<br>');
                uploadStatus.innerHTML = '<p style="color: green;">Upload successful!</p>';
                shareOptions.style.display = 'block';
            } else {
                throw new Error(data.error || 'An unknown error occurred during file upload.');
            }
        })
        .catch(error => {
            uploadStatus.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
    }

    // Copy link to clipboard functionality
    copyLinkButton.addEventListener('click', function () {
        const links = fileLink.querySelectorAll('a');
        const textToCopy = Array.from(links).map(link => link.href).join('\n');
        navigator.clipboard.writeText(textToCopy)
            .then(() => {
                uploadStatus.innerHTML = '<p style="color: green;">Link(s) copied to clipboard.</p>';
            })
            .catch(err => {
                uploadStatus.innerHTML = `<p style="color: red;">Failed to copy link: ${err.message}</p>`;
            });
    });

    // Share via email functionality
    emailLinkButton.addEventListener('click', function () {
        const links = fileLink.querySelectorAll('a');
        const textToShare = Array.from(links).map(link => link.href).join('\n');
        const mailtoLink = `mailto:?subject=Files from ZipZap&body=${encodeURIComponent(textToShare)}`;
        window.location.href = mailtoLink;
    });

    // Share via WhatsApp functionality
    whatsappLinkButton.addEventListener('click', function () {
        const links = fileLink.querySelectorAll('a');
        const textToShare = Array.from(links).map(link => link.href).join('\n');
        const whatsappLink = `https://wa.me/?text=${encodeURIComponent(textToShare)}`;
        window.open(whatsappLink, '_blank');
    });

    // Drag and drop functionality
    dropZone.addEventListener('dragover', (event) => {
        event.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', (event) => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (event) => {
        event.preventDefault();
        dropZone.classList.remove('dragover');

        fileInput.files = event.dataTransfer.files;
        const files = fileInput.files;
        fileNames.innerHTML = '';
        for (const file of files) {
            const listItem = document.createElement('li');
            listItem.textContent = file.name;
            fileNames.appendChild(listItem);
        }
    });
});
