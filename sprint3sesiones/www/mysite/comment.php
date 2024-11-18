
<?php
$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('No se pudo conectar a la base de datos');
$libro_id = $_POST['juego_id'];
$comentario = $_POST['new_comment'];

$query = "INSERT INTO tComentarios (comentario, juego_id) VALUES ('$comentario', $libro_id)";
mysqli_query($db, $query) or die('Error al insertar el comentario');

echo "Comentario añadido.";
echo "<a href='/detail.php?id=$juego_id'>Volver</a>";
mysqli_close($db);
?>
