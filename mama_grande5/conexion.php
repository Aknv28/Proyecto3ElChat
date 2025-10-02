<?php
$servername = "mysql-36c9da87-javi777-8e45.l.aivencloud.com"; // Host de tu base de datos
$username = "avnadmin"; // Usuario
$password = "AVNS_wy6GYw5PhJXt3y-6f8E"; // Contraseña
$dbname = "mama_grande"; // Nombre de la base de datos
$port = 16659; // Puerto

// Crear la conexión
$conn = new mysqli($servername, $username, $password, $dbname, $port);

// Verificar la conexión
if ($conn->connect_error) {
    die("Conexión fallida: " . $conn->connect_error);
}
?>
