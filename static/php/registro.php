<?php
if ($_SERVER["REQUEST_METHOD"] === "POST") {
  // Recibir los datos del formulario
  $username = $_POST["username"];
  $password = $_POST["password"];

  // Aquí puedes realizar validaciones adicionales, como comprobar si el usuario ya existe en la base de datos.

  // Conexión a la base de datos (ejemplo con MySQLi)
  $servername = "localhost";
  $username_db = "tu_usuario_db";
  $password_db = "tu_contraseña_db";
  $dbname = "nombre_de_tu_base_de_datos";

  $conn = new mysqli($servername, $username_db, $password_db, $dbname);

  if ($conn->connect_error) {
    die("Error de conexión: " . $conn->connect_error);
  }

  // Insertar datos en la base de datos (ejemplo con una tabla "usuarios")
  $sql = "INSERT INTO usuarios (username, password) VALUES ('$username', '$password')";

  if ($conn->query($sql) === TRUE) {
    echo "Registro exitoso. ¡Bienvenido, $username!";
  } else {
    echo "Error en el registro: " . $conn->error;
  }

  $conn->close();
}
?>