<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $firstname = $_POST["firstname"];
    $lastname = $_POST["lastname"];
    $password = $_POST["psw"];
    
    // Here you can perform further validation and processing of the form data
    // For example, you might want to insert the data into a database.
    
    // After processing, you can redirect the user to a thank you page or display a success message.
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Form Submission Result</title>
</head>
<body>
    <h1>Form Submission Result</h1>
    <?php if ($_SERVER["REQUEST_METHOD"] == "POST"): ?>
        <p>Thank you for signing up, <?php echo $firstname; ?>!</p>
    <?php else: ?>
        <p>No form submission has occurred.</p>
    <?php endif; ?>
</body>
</html>
