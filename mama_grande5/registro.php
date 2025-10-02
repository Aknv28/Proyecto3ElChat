<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro de Usuario</title>
</head>
<body>

<h2>Formulario de Registro</h2>

<form action="registro_action.php" method="POST">
    <label for="nombre">Nombre:</label>
    <input type="text" name="nombre" required><br>

    <label for="email">Correo:</label>
    <input type="email" name="email" required><br>

    <label for="password">Contraseña:</label>
    <input type="password" name="password" required><br>

    <label for="rol">Rol:</label>
    <select name="rol" required>
        <option value="administrador">Administrador</option>
        <option value="cajero">Cajero</option>
        <option value="cocinero">Cocinero</option>
    </select><br>

    <input type="submit" value="Registrar">
</form>

</body>
</html>
