<?php
session_start();

if ($_SESSION['rol'] != 'cocinero') {
    header("Location: login.php"); // Redirigir si no es cocinero
    exit();
}

echo "<h1>Bienvenido, Cocinero " . $_SESSION['nombre'] . "</h1>";
// Aquí puedes agregar la funcionalidad exclusiva para el cocinero

echo '<a href="logout.php">Cerrar sesión</a>';
?>
