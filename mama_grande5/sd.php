<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Estado de los Pedidos</title>
    <link rel="stylesheet" href="style.css">
</head>
<style>
    /* GENERAL / body { margin: 0; background: #000; / Fondo negro / font-family: Arial, sans-serif; display: flex; justify-content: center; color: #fff; / Texto en blanco por defecto / } .contenedor { width: 90%; max-width: 950px; padding: 20px; } / ENCABEZADO / .encabezado { background: #111; / negro más claro / padding: 15px; border-radius: 10px; text-align: center; border: 2px solid #e50914; / rojo estilo Netflix / } .encabezado h1 { margin: 0; font-size: 2.3rem; font-weight: bold; color: #e50914; / título en rojo / } .leyenda { display: flex; justify-content: center; gap: 30px; margin-top: 10px; font-weight: bold; color: #fff; } .color { display: inline-block; width: 25px; height: 15px; margin-right: 5px; border-radius: 3px; } / COLORES ESTADO / .color.pendiente { background: #e50914; } / rojo / .color.proceso { background: #444; } / gris oscuro / .color.terminado { background: #00e676; } / verde brillante / .tabla { margin-top: 20px; } / FILAS DE PEDIDOS / .fila { display: grid; grid-template-columns: 1fr 0.5fr 1fr 1fr; background: #111; margin-bottom: 8px; padding: 10px; border-radius: 5px; align-items: center; border: 1px solid #333; } .col p { margin: 2px 0; font-weight: bold; color: #fff; } .pedido { color: #e50914; font-weight: bold; text-align: center; } / ESTADOS CUADRADOS / .estados { display: flex; gap: 10px; justify-content: center; } .estado { width: 30px; height: 30px; border-radius: 5px; background: #222; } .estado.pendiente { background: #e50914; } .estado.proceso { background: #444; } .estado.terminado { background: #00e676; } / MENSAJE DEL DÍA / .mensaje { background: #111; padding: 15px; border-radius: 10px; margin: 20px 0; text-align: center; border: 2px solid #e50914; } .mensaje h2 { margin: 0 0 10px; color: #fff; } .motos { font-size: 1.5rem; color: #e50914; } / BOTÓN */
.btn-recoger {
    display: block;
    margin: 0 auto;
    padding: 12px 25px;
    background: #e50914;
    color: #fff;
    font-weight: bold;
    font-size: 1.3rem;
    border: none;
    border-radius: 10px;
    cursor: pointer;
    transition: 0.3s;
}

.btn-recoger:hover {
    background: #b20710;
}
    </style>

<body>
    <div class="contenedor"> <!-- ENCABEZADO -->
        <div class="encabezado">
            <h1>ESTADO DE LOS PEDIDOS</h1>
            <div class="leyenda">
                <div><span class="color pendiente"></span> PENDIENTE</div>
                <div><span class="color proceso"></span> PROCESO</div>
                <div><span class="color terminado"></span> TERMINADO</div>
            </div>
        </div> <!-- TABLA DE PEDIDOS -->
        <div class="tabla"> <!-- PEDIDO 1 -->
            <div class="fila">
                <div class="col hamburguesas">
                    <p>TSUNAMI</p>
                    <p>H.3</p>
                    <p>V.NEGRA</p>
                </div>
                <div class="col cantidades">
                    <p>0</p>
                    <p>0</p>
                    <p>8</p>
                </div>
                <div class="col pedido">PEDIDO Nº</div>
                <div class="col estados"> <span class="estado proceso"></span> <span class="estado vacio"></span> <span
                        class="estado terminado"></span> </div>
            </div> <!-- PEDIDO 2 -->
            <div class="fila">
                <div class="col hamburguesas">
                    <p>TSUNAMI</p>
                    <p>H.3</p>
                    <p>V.NEGRA</p>
                </div>
                <div class="col cantidades">
                    <p>8</p>
                    <p>0</p>
                    <p>0</p>
                </div>
                <div class="col pedido">PEDIDO Nº</div>
                <div class="col estados"> <span class="estado proceso"></span> <span class="estado vacio"></span> <span
                        class="estado terminado"></span> </div>
            </div> <!-- PEDIDO 3 -->
            <div class="fila">
                <div class="col hamburguesas">
                    <p>TSUNAMI</p>
                    <p>H.3</p>
                    <p>V.NEGRA</p>
                </div>
                <div class="col cantidades">
                    <p>0</p>
                    <p>0</p>
                    <p>8</p>
                </div>
                <div class="col pedido">PEDIDO Nº</div>
                <div class="col estados"> <span class="estado proceso"></span> <span class="estado proceso"></span>
                    <span class="estado terminado"></span> </div>
            </div>
        </div> <!-- MENSAJE DEL DÍA -->
        <div class="mensaje">
            <h2>MENSAJE DEL DÍA</h2>
            <div class="motos">🏍 🏍 🏍 🏍</div>
        </div> <!-- BOTÓN --> <button class="btn-recoger">RECOGER</button>
    </div>
</body>

</html>