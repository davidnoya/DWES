<?php
$db = new mysqli('172.16.0.2', 'root', '1234', 'mysitedb');
if ($db->connect_error) {
    die("Error de conexión: " . $db->connect_error);
}

$juego_id = $_POST['juego_id'];
$comentario = $_POST['new_comment'];

$user_id = 'NULL';
if (!empty($_SESSION['user_id'])) {
    $user_id_a_insertar = $_SESSION['user_id'];
}

if (empty($comentario) || empty($juego_id)) {
    die("El comentario y el juego correspondiente son obligatorios.");
}

$stmt = $db->prepare("INSERT INTO tComentarios (comentario, juego_id, usuario_id) VALUES (?, ?, ?)");
$stmt->bind_param("ssi", $comentario, $juego_id, $user_id);

if ($stmt->execute()) {
    echo "<p>Comentario añadido con éxito.</p>";
    echo "<a href='/detail.php?juego_id=" . $juego_id . "'>Volver</a>";
} else {
    echo "<p>Error al añadir el comentario.</p>";
}

$stmt->close();
$db->close();
?>
