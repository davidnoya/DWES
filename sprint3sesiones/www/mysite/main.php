<?php
// Me conecto a la base de datos 'mysitedb' usando mysqli_connect
// Utilizo el usuario 'root', la contraseña '1234', y selecciono la base de datos 'mysitedb'
$db = mysqli_connect('172.16.0.2', 'root', '1234', 'mysitedb') or die('Error al conectar con la base de datos');
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Valiño estuvo aquí</title>
    <style>
        body {
            background-color: pink;
            color: #333;
            margin: 0;
            padding: 0;


            min-height: 100vh;
        }

        ul {
            align-items: center;
            padding: 0;
            margin: 0;
            list-style: none;
        }
        h1{
            text-align: center;
        }
        li {
            background-color: beige;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin: 20px 0;
            padding: 20px;
            width: 300px;
            display: inline-block;
            margin-left: 35px;
            text-align: top;
        }
        h2 {
            color: magenta;
        }
        img {
            width: 300px;
            height: 400px;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        a {
            text-decoration: none;
            color: magenta ;
            font-weight: bold;
        }
        a:hover {
            color: #333;
	    transform: scale(1.05);
        }

	@keyframes fadeIn {
  	    0% {
       		opacity: 0;
        	transform: translateY(20px);
    	    }
    	    100% {
        	opacity: 1;
        	transform: translateY(0);
    	    }
	}
    </style>
</head>
<body>
    <?php
    echo "<h1>Conexión establecida</h1>";
    echo  "<br/><br/>";

    $query = 'SELECT * FROM tJuegos';

    // Ejecuto la consulta y la guardo en $result
    $result = mysqli_query($db, $query) or die('Error en la consulta');

    // Verifico si la consulta funciona
    if (mysqli_num_rows($result) > 0) {
        // Abro una lista (<ul>) para mostrar cada serie
        echo '<ul>';

        // Recorro los resultados uno por uno usando un bucle while
        while ($row = mysqli_fetch_array($result)) {

            echo '<li>';
            echo '<h2>' . $row['nombre'] . '</h2>';
           
            echo '<p><strong>Temática:</strong> ' . $row['tematica'] . '</p>';
           

            echo '<p><strong>fecha de publicación:</strong> ' . $row['fecha_publicacion'] . '</p>';
           

            echo '<img src="' . $row['url_imagen'] . '" alt="Imagen de ' . $row['nombre'] . '">';
           

            echo '<p><a href="/detail.php?id=' . $row['id'] . '">Ver más detalles</a></p>';
            echo '</li>';
        }

        // Cierro la lista
        echo '</ul>';
    } else {
        echo '<p>No se encontraron juegos en la base de datos.</p>';
    }

    //Cierro la conexión con la base de datos
    mysqli_close($db);
    ?>

    <a href="logout.php">Cerrar sesión</a>
</body>
</html>
