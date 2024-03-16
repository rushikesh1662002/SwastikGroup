<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

require 'static/CollegePrediction/assets/php/src/Exception.php';
require 'static/CollegePrediction/assets/php/src/PHPMailer.php';
require 'static/CollegePrediction/assets/php/src/SMTP.php';

$receiving_email_address = 'rp919321@gmail.com';

// Sender information
$name = $_POST['name'];
$email = $_POST['email'];
$subject = $_POST['subject'];
$message = $_POST['message'];

// Email headers
$headers  = "From: $name <$email>\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "MIME-Version: 1.0\r\n";
$headers .= "Content-Type: multipart/alternative; boundary='b1_rYkK3mYMaouR8CNbl6iNr0wCQqT6psvQpPoqCiJ7XU'\r\n";

echo 'Before sending email';
try {
    $phpmailer = new PHPMailer(true);

    // SMTP Configuration
    $phpmailer->isSMTP();
    $phpmailer->Host = 'smtp.gmail.com';
    $phpmailer->SMTPAuth = true;
    $phpmailer->Username = 'rp919321@gmail.com';
    $phpmailer->Password = 'lype huca tznu fsiw'; // Replace with your Gmail password
    $phpmailer->SMTPSecure = 'tls';
    $phpmailer->Port = 587;
    $phpmailer->AltBody = 'Test';

    // Email content
    $phpmailer->setFrom($email, $name);
    $phpmailer->addAddress($receiving_email_address);
    $phpmailer->Subject = $subject;
    $phpmailer->Body = $message;

    // Send email
    $phpmailer->send();
    echo 'Email sent successfully';
    echo 'Success';
} catch (Exception $e) {
    echo 'Error: Unable to send email. ', $phpmailer->ErrorInfo;
}
?>
