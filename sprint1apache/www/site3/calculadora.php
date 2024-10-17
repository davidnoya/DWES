<html>
	<body>
		<h1>Calculadora</h1>
		<form action="calculadora.php" method="post">
			<label for="n1">Numero 1:</label>
			<input type="number" name="n1" id="n1" required>
			<br><br>
			<label for="n2">Numero 2:</label>
			<input type="number" name="n2" id="n2" required>
			<br><br>
			<label for="op">Operacion:</label>
			<select name="op" id="op" required>
				<option value="suma">Suma</option>
				<option value="resta">Resta</option>
				<option value="multiplicacion">Multiplicacion</option>
				<option value="division">Division</option>
			</select>
			<br><br>
			<input type="submit" name="calcular" value="Calcular">
		</form>
		<?php
			if ($_SERVER["REQUEST_METHOD"] == "POST"){
				$n1 = $_POST['n1'];
				$n2 = $_POST['n2'];
				$op = $_POST['op'];
				$resultado = 0;
			
			switch ($op){
				case 'suma':
					$resultado = $n1 + $n2;
					break;
				case 'resta':
					$resultado = $n1 -  $n2;
					break;
				case 'multiplicacion':
					$resultado = $n1 * $n2;
					break;
				case 'division':
					if ($n2 != 0){
						$resultado = $n1 / $n2;
					}else{
						echo "Error: No se puede dividir entre cero.";
						exit();
					}
					break;
				default:
					echo "Operacion no valida";
					exit();
			}
			echo "Resultado: ".$resultado;
			}
		?>
	</body>
</html>
