<?php
$db = new mysqli('172.16.0.2', 'root', '1234', 'mysitedb');
if ($db->connect_error) {
    die("Error de conexión: " . $db->connect_error);
}

$email = $_POST['email'];
$password = $_POST['password'];

$stmt = $db->prepare("SELECT id, contraseña FROM tUsuarios WHERE email = ?");
$stmt->bind_param("s", $email);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows === 0) {
    die("El correo no está registrado.");
}

$stmt->bind_result($user_id, $hashed_password);
$stmt->fetch();

if (password_verify($password, $hashed_password)) {
    $_SESSION['user_id'] = $user_id;
    header("Location: main.php");
    exit();
} else {
    die("Contraseña incorrecta.");
}

$stmt->close();
$db->close();
?>
