$(document).ready(function() {
    $('#generateButton').click(function() {
        const inputText = $('#inputText').val();
        if (inputText.length > 500) {
            $('#responseText').text("Input text is too long");
            return;
        }

        $.ajax({
            url: "/generate",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({ text: inputText }),
            success: function(response) {
                $('#responseText').text(response.response);
            },
            error: function(error) {
                $('#responseText').text("An error occurred: " + error.responseJSON.error);
            }
        });
    });
});
