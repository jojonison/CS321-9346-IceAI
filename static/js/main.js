document.addEventListener('DOMContentLoaded', function() {
    // Initialization
    document.querySelector('.image-section').style.display = 'none';
    document.querySelector('.loader').style.display = 'none';
    document.querySelector('#result').style.display = 'none';

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                var imagePreview = document.getElementById('imagePreview');
                imagePreview.style.backgroundImage = 'url(' + e.target.result + ')';
                imagePreview.style.display = 'none';
                imagePreview.style.display = 'block';
            }
            reader.readAsDataURL(input.files[0]);
        }
    }
    document.getElementById('imageUpload').addEventListener('change', function() {
        var imageSection = document.querySelector('.image-section');
        imageSection.style.display = 'block';
        document.getElementById('btn-predict').style.display = 'block';
        document.getElementById('result').textContent = '';
        document.getElementById('result').style.display = 'none';
        readURL(this);
    });

    // Predict
    document.getElementById('btn-predict').addEventListener('click', function() {
        var fileInput = document.getElementById('imageUpload');
        if (fileInput.files.length > 0) {
            var formData = new FormData();
            formData.append('file', fileInput.files[0]);

            // Show loading animation
            this.style.display = 'none';
            document.querySelector('.loader').style.display = 'block';

            // Make prediction by calling API /predict
            var xhr = new XMLHttpRequest();
            xhr.open('POST', '/predict', true);
            xhr.onload = function() {
                if (xhr.status == 200) {
                    // Get and display the result
                    document.querySelector('.loader').style.display = 'none';
                    var resultElement = document.getElementById('result');
                    resultElement.textContent = 'Result: ' + xhr.responseText;
                    resultElement.style.display = 'block';
                    console.log('Success!');
                } else {
                    console.error('Request failed with status:', xhr.status);
                }
            };
            xhr.send(formData);
        } else {
            console.error('No file selected for prediction.');
        }
    });
});
