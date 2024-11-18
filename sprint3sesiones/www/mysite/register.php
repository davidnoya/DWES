<?php
$db = new mysqli('localhost', 'root', '1234', 'mysitedb');
if ($db->connect_error) {
    die("Error de conexión: " . $db->connect_error);
}

$email = $_POST['email'];
$password1 = $_POST['password1'];
$password2 = $_POST['password2'];

if (empty($email) || empty($password1) || empty($password2)) {
    die("Todos los campos son obligatorios.");
}

if ($password1 !== $password2) {
    die("Las contraseñas no coinciden.");
}

$stmt = $db->prepare("SELECT id FROM tUsuarios WHERE email = ?");
$stmt->bind_param("s", $email);
$stmt->execute();
$stmt->store_result();

if ($stmt->num_rows > 0) {
    die("El correo ya está registrado.");
}
$stmt->close();

$hashed_password = password_hash($password1, PASSWORD_DEFAULT);

$stmt = $db->prepare("INSERT INTO tUsuarios (email, contraseña) VALUES (?, ?)");
$stmt->bind_param("ss", $email, $hashed_password);

if ($stmt->execute()) {
    header("Location: main.php");
} else {
    die("Error al registrar el usuario.");
}

$stmt->close();
$db->close();
?>
