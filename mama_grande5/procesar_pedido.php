<?php
session_start();
header('Content-Type: application/json');

// Verificar que sea cajero
if (!isset($_SESSION['rol']) || $_SESSION['rol'] != 'cajero') {
    echo json_encode(['success' => false, 'error' => 'No autorizado']);
    exit();
}

// Conexión a la base de datos
$conexion = new mysqli('localhost', 'root', '', 'mama_grande');

if ($conexion->connect_error) {
    echo json_encode(['success' => false, 'error' => 'Error de conexión a la base de datos']);
    exit();
}

// Obtener datos del pedido
$input = file_get_contents('php://input');
$pedidoData = json_decode($input, true);

if (!$pedidoData || empty($pedidoData['productos'])) {
    echo json_encode(['success' => false, 'error' => 'Datos de pedido inválidos']);
    exit();
}

// Iniciar transacción
$conexion->begin_transaction();

try {
    // Calcular total
    $total = 0;
    foreach ($pedidoData['productos'] as $producto) {
        $total += $producto['precio'] * $producto['cantidad'];
    }

    // Insertar pedido principal
    $stmt = $conexion->prepare("INSERT INTO Pedidos (id_usuario, estado, total) VALUES (?, 'preparando', ?)");
    $id_usuario = $_SESSION['id_usuario'];
    $stmt->bind_param("id", $id_usuario, $total);
    
    if (!$stmt->execute()) {
        throw new Exception('Error al crear el pedido');
    }
    
    $id_pedido = $conexion->insert_id;
    $stmt->close();

    // Insertar detalles del pedido
    foreach ($pedidoData['productos'] as $key => $producto) {
        $tipo = $producto['tipo'];
        $id = $producto['id'];
        $cantidad = $producto['cantidad'];
        $precio = $producto['precio'];

        if ($tipo === 'hamburguesa') {
            // Insertar en Detalles_Pedido
            $stmt = $conexion->prepare("INSERT INTO Detalles_Pedido (id_pedido, id_hamburguesa, cantidad, precio) VALUES (?, ?, ?, ?)");
            $stmt->bind_param("iiid", $id_pedido, $id, $cantidad, $precio);
            
            if (!$stmt->execute()) {
                throw new Exception('Error al insertar detalle de hamburguesa');
            }
            $stmt->close();
        } 
        elseif ($tipo === 'refresco') {
            // Insertar refrescos (uno por cada unidad)
            for ($i = 0; $i < $cantidad; $i++) {
                $stmt = $conexion->prepare("INSERT INTO Detalles_Extras (id_pedido, id_refresco, id_salsa) VALUES (?, ?, NULL)");
                $stmt->bind_param("ii", $id_pedido, $id);
                
                if (!$stmt->execute()) {
                    throw new Exception('Error al insertar refresco');
                }
                $stmt->close();
            }
        } 
        elseif ($tipo === 'salsa') {
            // Insertar salsas (una por cada unidad)
            for ($i = 0; $i < $cantidad; $i++) {
                $stmt = $conexion->prepare("INSERT INTO Detalles_Extras (id_pedido, id_refresco, id_salsa) VALUES (?, NULL, ?)");
                $stmt->bind_param("ii", $id_pedido, $id);
                
                if (!$stmt->execute()) {
                    throw new Exception('Error al insertar salsa');
                }
                $stmt->close();
            }
        }
    }

    // Confirmar transacción
    $conexion->commit();

    // Respuesta exitosa
    echo json_encode([
        'success' => true,
        'id_pedido' => $id_pedido,
        'total' => number_format($total, 2),
        'mensaje' => 'Pedido procesado correctamente'
    ]);

} catch (Exception $e) {
    // Revertir transacción en caso de error
    $conexion->rollback();
    
    echo json_encode([
        'success' => false,
        'error' => $e->getMessage()
    ]);
}

$conexion->close();
?>