<?php
$db = mysqli_connect('172.16.0.2', 'root', '1234', 'mysitedb') or die('No se pudo conectar a la base de datos');
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

echo "<h3>Comentarios:</h3><ul>";
$query_comments = "SELECT * FROM tComentarios WHERE juego_id = $id";
$result_comments = mysqli_query($db, $query_comments) or die('Error en la consulta de comentarios');
while ($comment = mysqli_fetch_array($result_comments)) {
    echo "<li>".$comment['comentario']." -<small>".$comment['fecha']."</small></li>";
}
echo "</ul>";
?>

<p>Deja un nuevo comentario:</p>
<form action="/comment.php" method="post">
<textarea rows="4" cols="50" name="new_comment"></textarea><br>
<input type="hidden" name="juego_id" value="<?php echo $juego_id; ?>">
<input type="submit" value="Comentar">
</form>
<a href="logout.php">Cerrar sesión</a>
<?php
mysqli_close($db);
?>
