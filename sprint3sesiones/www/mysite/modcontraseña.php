<?php
if (empty($_SESSION['user_id'])) {
    header("Location: login.html");
    exit();
}

$db = new mysqli('localhost', 'root', '1234', 'mysitedb');
if ($db->connect_error) {
    die("Error de conexión: " . $db->connect_error);
}

$current_password = $_POST['current_password'];
$new_password = $_POST['new_password'];
$confirm_password = $_POST['confirm_password'];
$user_id = $_SESSION['user_id'];

if ($new_password !== $confirm_password) {
    die("Las nuevas contraseñas no coinciden.");
}

$stmt = $db->prepare("SELECT contraseña FROM tUsuarios WHERE id = ?");
$stmt->bind_param("i", $user_id);
$stmt->execute();
$stmt->bind_result($hashed_password);
$stmt->fetch();
$stmt->close();

if (!password_verify($current_password, $hashed_password)) {
    die("La contraseña actual es incorrecta.");
}

$new_hashed_password = password_hash($new_password, PASSWORD_DEFAULT);
$stmt = $db->prepare("UPDATE tUsuarios SET contraseña = ? WHERE id = ?");
$stmt->bind_param("si", $new_hashed_password, $user_id);

if ($stmt->execute()) {
    echo "Contraseña actualizada con éxito.";
    echo "<a href='main.php'>Volver a la página principal</a>";
} else {
    echo "Error al actualizar la contraseña.";
}

$stmt->close();
$db->close();
?>
