<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pins</title>
    <script>
        function fetchPins() {
            fetch('api.php')
                .then(response => response.json())
                .then(data => {
                    let output = "<h2>Recent Posts</h2><ul>";
                    data.forEach(post => {
                        output += `<li><strong>${post.FName} ${post.LName}:</strong> ${post.Title} - ${post.Description}</li>`;
                    });
                    output += "</ul>";
                    document.getElementById("posts").innerHTML = output;
                })
                .catch(error => console.error('Error fetching data:', error));
        }
    </script>
</head>
<body onload="fetchPosts()">
    <div id="posts">Loading...</div>
</body>
</html>
