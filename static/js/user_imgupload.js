

    function displayChosenFile() {
        // Get the file input element
        var fileInput = document.getElementById('fileInput');
        // Get the selected file
        var chosenFile = fileInput.files[0];
        // Display the file name
        var chosenFileDisplay = document.getElementById('chosenFile');
        // Display the image
        var previewImage = document.getElementById('previewImage');

        // Check if the chosen file is an image
        if (chosenFile && chosenFile.type.startsWith('image/')) {
            var reader = new FileReader();

            // Set up the reader onload event
            reader.onload = function (e) {
                // Set the source of the image element to the read data URL
                previewImage.src = e.target.result;
            };

            // Read the file as a data URL
            reader.readAsDataURL(chosenFile);
        } else {
            // If the chosen file is not an image, clear the image element
            previewImage.src = '';
        }
    }
