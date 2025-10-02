
<?php
include 'conexion.php'; // Conexión a la base de datos

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $nombre = $_POST['nombre'];
    $email = $_POST['email'];
    $password = $_POST['password'];
    $rol = $_POST['rol'];

    // Comprobar si el correo ya está registrado
    $sql = "SELECT * FROM Usuarios WHERE email = '$email'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        echo "Este correo ya está registrado.";
    } else {
        // Insertar el nuevo usuario en la base de datos
        $sql_insert = "INSERT INTO Usuarios (nombre, email, contrasena, rol, estado) 
                       VALUES ('$nombre', '$email', '$password', '$rol', 'activo')";

        if ($conn->query($sql_insert) === TRUE) {
            echo "Usuario registrado exitosamente.";
        } else {
            echo "Error al registrar usuario: " . $conn->error;
        }
    }
    $conn->close(); // Cerrar la conexión
}
?>
