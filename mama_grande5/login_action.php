<?php
session_start(); // Iniciar sesión

include 'conexion.php'; // Incluir la conexión a la base de datos

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = $_POST['email'];
    $password = $_POST['password']; // Normalmente deberías cifrar las contraseñas

    // Consulta para verificar el usuario y su contraseña
    $sql = "SELECT * FROM Usuarios WHERE email = '$email'";
    $result = $conn->query($sql);

    if ($result->num_rows > 0) {
        $row = $result->fetch_assoc();

        // Verificar si la contraseña es correcta
        if ($row['contrasena'] == $password) {
            // Establecer sesión para el usuario
            $_SESSION['id_usuario'] = $row['id_usuario'];
            $_SESSION['nombre'] = $row['nombre'];
            $_SESSION['rol'] = $row['rol'];

            // Redirigir según el rol del usuario
            switch ($row['rol']) {
                case 'administrador':
                    header("Location: administrador.php");
                    break;
                case 'cajero':
                    header("Location: cajero.php");
                    break;
                case 'cocinero':
                    header("Location: cocinero.php");
                    break;
                default:
                    echo "Rol no reconocido";
                    break;
            }
        } else {
            echo "Contraseña incorrecta.";
        }
    } else {
        echo "No se encontró el usuario.";
    }

    $conn->close(); // Cerrar la conexión
}
?>
