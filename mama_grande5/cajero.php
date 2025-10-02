<?php
session_start();

if ($_SESSION['rol'] != 'cajero') {
    header("Location: login.php");
    exit();
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cajero - Mamá Grande</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'negro-principal': '#111111',
                        'gris-oscuro': '#1C1C1C',
                        'gris-medio': '#AAAAAA',
                        'rojo-intenso': '#B51E23',
                        'rojo-suave': '#D9322A',
                        'gris-claro': '#E0E0E0',
                    },
                    fontFamily: {
                        'display': ['Montserrat', 'sans-serif'],
                        'body': ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        body { font-family: 'Inter', sans-serif; }
        .font-display { font-family: 'Montserrat', sans-serif; }
        .product-image { width: 100%; height: 180px; object-fit: cover; border-radius: 8px; }
        .image-overlay { position: relative; overflow: hidden; border-radius: 8px; margin-bottom: 1rem; }
        .image-overlay::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 50%; background: linear-gradient(to top, rgba(17, 17, 17, 0.8), transparent); }
    </style>
</head>
<body class="bg-negro-principal text-white">
    
    <!-- Pantalla 1: Menú -->
    <div id="menu-screen" class="min-h-screen">
        <header class="bg-negro-principal border-b border-gris-oscuro sticky top-0 z-50">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <div class="flex justify-between items-center">
                    <div>
                        <h1 class="font-display font-black text-3xl sm:text-4xl tracking-tight">MAMÁ GRANDE</h1>
                        <p class="text-gris-medio mt-2 font-medium">Cajero: <span class="text-rojo-intenso"><?php echo $_SESSION['nombre']; ?></span></p>
                    </div>
                    <a href="logout.php" class="bg-gris-oscuro border-2 border-rojo-intenso hover:bg-rojo-intenso text-white font-display font-black py-2 px-6 rounded-xl uppercase text-sm transition-all duration-300">Salir</a>
                </div>
            </div>
        </header>

        <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <section class="mb-12">
                <h2 class="font-display font-bold text-2xl mb-6">HAMBURGUESAS</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&h=400&fit=crop" alt="Simple" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <div><h3 class="font-display font-bold text-xl">SIMPLE</h3><p class="text-gris-medio text-sm">Clásica</p></div>
                            <span class="font-display font-bold text-xl text-rojo-intenso">35 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('simple', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="simple-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('simple', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1550547660-d9450f859349?w=500&h=400&fit=crop" alt="Pasión Dulce" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <div><h3 class="font-display font-bold text-xl">PASIÓN DULCE</h3><p class="text-gris-medio text-sm">Única</p></div>
                            <span class="font-display font-bold text-xl text-rojo-intenso">40 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('pasion', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="pasion-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('pasion', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=500&h=400&fit=crop" alt="Clásica" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <div><h3 class="font-display font-bold text-xl">CLÁSICA</h3><p class="text-gris-medio text-sm">Favorita</p></div>
                            <span class="font-display font-bold text-xl text-rojo-intenso">35 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('clasica', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="clasica-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('clasica', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1606755962773-d324e0a13086?w=500&h=400&fit=crop" alt="Hawaiana" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <div><h3 class="font-display font-bold text-xl">HAWAIANA</h3><p class="text-gris-medio text-sm">Tropical</p></div>
                            <span class="font-display font-bold text-xl text-rojo-intenso">40 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('hawaiana', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="hawaiana-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('hawaiana', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1565299507177-b0ac66763828?w=500&h=400&fit=crop" alt="Primavera" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <div><h3 class="font-display font-bold text-xl">PRIMAVERA</h3><p class="text-gris-medio text-sm">Fresca</p></div>
                            <span class="font-display font-bold text-xl text-rojo-intenso">38 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('primavera', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="primavera-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('primavera', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1553979459-d2229ba7433b?w=500&h=400&fit=crop" alt="Viuda Negra" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <div><h3 class="font-display font-bold text-xl">VIUDA NEGRA</h3><p class="text-gris-medio text-sm">Picante</p></div>
                            <span class="font-display font-bold text-xl text-rojo-intenso">42 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('viuda', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="viuda-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('viuda', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1572802419224-296b0aeee0d9?w=500&h=400&fit=crop" alt="Master Buey" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <div><h3 class="font-display font-bold text-xl">MASTER BUEY</h3><p class="text-gris-medio text-sm">Premium</p></div>
                            <span class="font-display font-bold text-xl text-rojo-intenso">45 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('master', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="master-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('master', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                </div>
            </section>

            <section class="mb-12">
                <h2 class="font-display font-bold text-2xl mb-6">REFRESCOS</h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1554866585-cd94860890b7?w=500&h=400&fit=crop" alt="Coca Cola" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <h3 class="font-display font-bold text-xl">COCA COLA</h3>
                            <span class="font-display font-bold text-xl text-rojo-intenso">7 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('coca', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="coca-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('coca', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1624517452488-04869289c4ca?w=500&h=400&fit=crop" alt="Fanta" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <h3 class="font-display font-bold text-xl">FANTA</h3>
                            <span class="font-display font-bold text-xl text-rojo-intenso">7 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('fanta', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="fanta-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('fanta', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                </div>
            </section>

            <section class="mb-12">
                <h2 class="font-display font-bold text-2xl mb-6">SALSAS EXTRAS</h2>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1472476443507-c7a5948772fc?w=500&h=400&fit=crop" alt="Mayonesa" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <h3 class="font-display font-bold text-xl">MAYONESA</h3>
                            <span class="font-display font-bold text-xl text-rojo-intenso">3 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('mayo', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="mayo-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('mayo', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                    <div class="bg-gris-oscuro rounded-lg p-5 hover:bg-opacity-80 transition-all">
                        <div class="image-overlay"><img src="https://images.unsplash.com/photo-1530655275210-579024715cbe?w=500&h=400&fit=crop" alt="Salsa de Casa" class="product-image"></div>
                        <div class="flex justify-between items-start mb-4">
                            <h3 class="font-display font-bold text-xl">SALSA DE CASA</h3>
                            <span class="font-display font-bold text-xl text-rojo-intenso">3 Bs</span>
                        </div>
                        <div class="flex items-center justify-between bg-negro-principal rounded-lg p-2">
                            <button onclick="updateQuantity('casa', -1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">-</button>
                            <span id="casa-qty" class="font-bold text-lg min-w-[2rem] text-center">0</span>
                            <button onclick="updateQuantity('casa', 1)" class="w-10 h-10 rounded-lg bg-gris-oscuro hover:bg-rojo-intenso transition-colors font-bold text-lg">+</button>
                        </div>
                    </div>
                </div>
            </section>

            <div class="flex justify-center">
                <button onclick="confirmarPedido()" class="w-full sm:w-auto px-12 py-4 bg-rojo-intenso hover:bg-rojo-suave text-white font-display font-bold text-xl rounded-lg transition-colors shadow-lg">CONFIRMAR PEDIDO</button>
            </div>
        </main>
    </div>

    <!-- Pantalla 2: Resumen -->
    <div id="summary-screen" class="min-h-screen hidden">
        <header class="bg-negro-principal border-b border-gris-oscuro sticky top-0 z-50">
            <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                <h1 class="font-display font-black text-3xl text-center">RESUMEN DEL PEDIDO</h1>
                <p class="text-gris-medio text-center mt-2 font-medium">Verificar antes de enviar a cocina</p>
            </div>
        </header>

        <main class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <form id="order-form" method="POST" action="guardar_pedido.php">
                <input type="hidden" name="cajero_id" value="<?php echo $_SESSION['id']; ?>">
                <input type="hidden" name="cajero_nombre" value="<?php echo $_SESSION['nombre']; ?>">
                <input type="hidden" id="productos_json" name="productos_json">
                <input type="hidden" id="total_pedido" name="total_pedido">

                <div class="bg-gris-oscuro rounded-lg overflow-hidden mb-8">
                    <table class="w-full">
                        <thead class="bg-negro-principal">
                            <tr>
                                <th class="px-6 py-4 text-left font-display font-bold">PRODUCTO</th>
                                <th class="px-6 py-4 text-center font-display font-bold">CANT.</th>
                                <th class="px-6 py-4 text-right font-display font-bold">SUBTOTAL</th>
                            </tr>
                        </thead>
                        <tbody id="order-items" class="divide-y divide-negro-principal"></tbody>
                    </table>
                </div>

                <div class="bg-gris-oscuro rounded-lg p-8 mb-8">
                    <div class="flex justify-between items-center">
                        <span class="font-display font-bold text-3xl">TOTAL A PAGAR</span>
                        <span id="total-amount" class="font-display font-black text-4xl text-rojo-intenso">0 Bs</span>
                    </div>
                </div>

                <div class="bg-gris-oscuro rounded-lg p-8 mb-8">
                    <h3 class="font-display font-bold text-xl mb-6">TIPO DE SERVICIO</h3>
                    <div class="space-y-4">
                        <label class="flex items-center gap-4 cursor-pointer">
                            <input type="radio" name="tipo_servicio" value="local" checked class="w-6 h-6">
                            <span class="font-bold text-lg">Comer en el local</span>
                        </label>
                        <label class="flex items-center gap-4 cursor-pointer">
                            <input type="radio" name="tipo_servicio" value="llevar" class="w-6 h-6">
                            <span class="font-bold text-lg">Para llevar</span>
                        </label>
                    </div>
                </div>

                <div class="flex flex-col sm:flex-row gap-4">
                    <button type="button" onclick="editarOrden()" class="flex-1 px-6 py-4 bg-gris-oscuro hover:bg-opacity-80 text-white font-display font-bold text-lg rounded-lg transition-all">EDITAR ORDEN</button>
                    <button type="button" onclick="cancelarOrden()" class="flex-1 px-6 py-4 bg-rojo-suave hover:bg-opacity-80 text-white font-display font-bold text-lg rounded-lg transition-all">CANCELAR ORDEN</button>
                    <button type="submit" class="flex-1 px-6 py-4 bg-rojo-intenso hover:bg-rojo-suave text-white font-display font-bold text-lg rounded-lg transition-all shadow-lg">ENVIAR A COCINA</button>
                </div>
            </form>
        </main>
    </div>

    <script>
        const productos = {
            simple: { nombre: 'Simple', precio: 35, cantidad: 0 },
            pasion: { nombre: 'Pasión Dulce', precio: 40, cantidad: 0 },
            clasica: { nombre: 'Clásica', precio: 35, cantidad: 0 },
            hawaiana: { nombre: 'Hawaiana', precio: 40, cantidad: 0 },
            primavera: { nombre: 'Primavera', precio: 38, cantidad: 0 },
            viuda: { nombre: 'Viuda Negra', precio: 42, cantidad: 0 },
            master: { nombre: 'Master Buey', precio: 45, cantidad: 0 },
            coca: { nombre: 'Coca Cola', precio: 7, cantidad: 0 },
            fanta: { nombre: 'Fanta', precio: 7, cantidad: 0 },
            mayo: { nombre: 'Mayonesa', precio: 3, cantidad: 0 },
            casa: { nombre: 'Salsa de Casa', precio: 3, cantidad: 0 }
        };

        function updateQuantity(id, delta) {
            productos[id].cantidad = Math.max(0, productos[id].cantidad + delta);
            document.getElementById(`${id}-qty`).textContent = productos[id].cantidad;
        }

        function confirmarPedido() {
            const hasItems = Object.values(productos).some(p => p.cantidad > 0);
            if (!hasItems) {
                alert('Por favor, selecciona al menos un producto');
                return;
            }

            const orderItems = document.getElementById('order-items');
            orderItems.innerHTML = '';
            let total = 0;
            const productosArray = [];

            Object.entries(productos).forEach(([id, producto]) => {
                if (producto.cantidad > 0) {
                    const subtotal = producto.precio * producto.cantidad;
                    total += subtotal;

                    productosArray.push({
                        id: id,
                        nombre: producto.nombre,
                        precio: producto.precio,
                        cantidad: producto.cantidad,
                        subtotal: subtotal
                    });

                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td class="px-6 py-4 font-medium">${producto.nombre}</td>
                        <td class="px-6 py-4 text-center font-bold">${producto.cantidad}</td>
                        <td class="px-6 py-4 text-right font-bold">${subtotal} Bs</td>
                    `;
                    orderItems.appendChild(row);
                }
            });

            document.getElementById('total-amount').textContent = `${total} Bs`;
            document.getElementById('productos_json').value = JSON.stringify(productosArray);
            document.getElementById('total_pedido').value = total;

            document.getElementById('menu-screen').classList.add('hidden');
            document.getElementById('summary-screen').classList.remove('hidden');
        }

        function editarOrden() {
            document.getElementById('summary-screen').classList.add('hidden');
            document.getElementById('menu-screen').classList.remove('hidden');
        }

        function cancelarOrden() {
            if (confirm('¿Estás seguro de cancelar este pedido?')) {
                Object.values(productos).forEach(p => p.cantidad = 0);
                Object.keys(productos).forEach(id => {
                    const el = document.getElementById(`${id}-qty`);
                    if (el) el.textContent = '0';
                });
                document.getElementById('summary-screen').classList.add('hidden');
                document.getElementById('menu-screen').classList.remove('hidden');
            }
        }

        document.getElementById('order-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            
            fetch('guardar_pedido.php', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('¡Pedido enviado a cocina exitosamente!');
                    Object.values(productos).forEach(p => p.cantidad = 0);
                    Object.keys(productos).forEach(id => {
                        const el = document.getElementById(`${id}-qty`);
                        if (el) el.textContent = '0';
                    });
                    document.getElementById('summary-screen').classList.add('hidden');
                    document.getElementById('menu-screen').classList.remove('hidden');
                } else {
                    alert('Error al guardar el pedido: ' + data.message);
                }
            })
            .catch(error => {
                alert('Error de conexión. Por favor intenta nuevamente.');
                console.error('Error:', error);
            });
        });
    </script>
</body>
</html>