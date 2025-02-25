<?php
include 'db/db.php';

$sql = "SELECT Users.Id, Users.FName, Users.LName, Pins.Title, Pins.Description 
        FROM Users 
        JOIN Pins ON Users.Id = Pins.UserId 
        LIMIT 10";

$result = $conn->query($sql);

$posts = array();
while ($row = $result->fetch_assoc()) {
    $posts[] = $row;
}

header('Content-Type: application/json');
echo json_encode($posts);

$conn->close();
?>
