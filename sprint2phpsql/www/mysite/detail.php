<?php
$db = mysqli_connect('localhost', 'root', '1234', 'mysitedb') or die('No se pudo conectar a la base de datos');
if (!isset($_GET['id'])) {
    die('No se ha especificado un ID');
}
$id = $_GET['id'];
$query = "SELECT * FROM tJuegos WHERE id = $id";
$result = mysqli_query($db, $query) or die('Error en la consulta');
$book = mysqli_fetch_array($result);

echo "<h1>".$book['nombre']."</h1>";
echo "<h2>Temática: ".$book['tematica']."</h2>";
echo "<h2>Fecha de publicación: ".$book['fecha_publicacion']."</h2>";
echo "<img src='".$book['url_imagen']."' alt='Portada'>";
?>
