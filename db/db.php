<?php
$servername = "pinspire-lamp-vm";
$username = "root";
$password = "xqPsqsOgJJEgNl";
$database = "pinspire";

// Create connection
$conn = new mysqli($servername, $username, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
