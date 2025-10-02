<?php
session_start();

if ($_SESSION['rol'] != 'administrador') {
    header("Location: login.php");
    exit();
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Mama Grande</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800;900&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        'negro-principal': '#111111',
                        'gris-oscuro': '#1C1C1C',
                        'gris-medio': '#AAAAAA',
                        'blanco': '#FFFFFF',
                        'rojo-intenso': '#B51E23',
                        'rojo-suave': '#D9322A',
                        'gris-claro': '#E0E0E0'
                    },
                    fontFamily: {
                        'montserrat': ['Montserrat', 'sans-serif']
                    }
                }
            }
        }
    </script>
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
        }
    </style>
</head>
<body class="bg-negro-principal min-h-screen relative overflow-hidden">
    
    <!-- Elementos decorativos de fondo -->
    <div class="absolute top-0 left-0 w-96 h-96 bg-rojo-intenso/5 rounded-full blur-3xl"></div>
    <div class="absolute bottom-0 right-0 w-96 h-96 bg-rojo-suave/5 rounded-full blur-3xl"></div>

    <div class="relative z-10 min-h-screen p-6 md:p-10">
        
        <!-- Header -->
        <header class="mb-12">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 bg-gris-oscuro rounded-2xl p-6 md:p-8 border border-gris-medio/10 backdrop-blur-sm">
                <div>
                    <h1 class="text-blanco text-4xl md:text-5xl font-black tracking-tight mb-2">
                        MAMA GRANDE
                    </h1>
                    <p class="text-gris-medio text-sm font-bold tracking-wide">
                        BIENVENIDO, <span class="text-rojo-intenso"><?php echo strtoupper($_SESSION['nombre']); ?></span>
                    </p>
                </div>
                <a href="logout.php" class="bg-gris-oscuro border-2 border-rojo-intenso hover:bg-rojo-intenso text-blanco font-black py-3 px-8 rounded-xl uppercase tracking-widest text-sm transition-all duration-300 transform hover:scale-105">
                    Cerrar Sesión
                </a>
            </div>
        </header>

        <!-- Dashboard Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-7xl mx-auto">
            
            <!-- Card: Ver Cocina -->
            <a href="ver_cocina.php" class="group bg-gris-oscuro rounded-2xl p-8 border border-gris-medio/10 backdrop-blur-sm hover:border-rojo-intenso transition-all duration-300 transform hover:scale-[1.02] hover:shadow-2xl hover:shadow-rojo-intenso/20">
                <div class="flex flex-col h-full">
                    <div class="flex items-center justify-between mb-6">
                        <div class="w-16 h-16 bg-rojo-intenso/20 rounded-xl flex items-center justify-center group-hover:bg-rojo-intenso/30 transition-all duration-300">
                            <svg class="w-8 h-8 text-rojo-intenso" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"></path>
                            </svg>
                        </div>
                        <div class="text-rojo-intenso opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M9 5l7 7-7 7"></path>
                            </svg>
                        </div>
                    </div>
                    <h3 class="text-blanco text-2xl font-black mb-3 uppercase tracking-tight">Ver Cocina</h3>
                    <p class="text-gris-medio text-sm font-bold tracking-wide">Gestiona y supervisa las órdenes en preparación</p>
                </div>
            </a>

            <!-- Card: Ver Pedidos -->
            <a href="ver_pedidos.php" class="group bg-gris-oscuro rounded-2xl p-8 border border-gris-medio/10 backdrop-blur-sm hover:border-rojo-intenso transition-all duration-300 transform hover:scale-[1.02] hover:shadow-2xl hover:shadow-rojo-intenso/20">
                <div class="flex flex-col h-full">
                    <div class="flex items-center justify-between mb-6">
                        <div class="w-16 h-16 bg-rojo-intenso/20 rounded-xl flex items-center justify-center group-hover:bg-rojo-intenso/30 transition-all duration-300">
                            <svg class="w-8 h-8 text-rojo-intenso" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
                            </svg>
                        </div>
                        <div class="text-rojo-intenso opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M9 5l7 7-7 7"></path>
                            </svg>
                        </div>
                    </div>
                    <h3 class="text-blanco text-2xl font-black mb-3 uppercase tracking-tight">Ver Pedidos</h3>
                    <p class="text-gris-medio text-sm font-bold tracking-wide">Consulta el historial completo de pedidos</p>
                </div>
            </a>

            <!-- Card: Agregar Hamburguesa -->
            <a href="agregar_hamburguesa.php" class="group bg-gris-oscuro rounded-2xl p-8 border border-gris-medio/10 backdrop-blur-sm hover:border-rojo-intenso transition-all duration-300 transform hover:scale-[1.02] hover:shadow-2xl hover:shadow-rojo-intenso/20">
                <div class="flex flex-col h-full">
                    <div class="flex items-center justify-between mb-6">
                        <div class="w-16 h-16 bg-rojo-intenso/20 rounded-xl flex items-center justify-center group-hover:bg-rojo-intenso/30 transition-all duration-300">
                            <svg class="w-8 h-8 text-rojo-intenso" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
                            </svg>
                        </div>
                        <div class="text-rojo-intenso opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M9 5l7 7-7 7"></path>
                            </svg>
                        </div>
                    </div>
                    <h3 class="text-blanco text-2xl font-black mb-3 uppercase tracking-tight">Agregar Hamburguesa</h3>
                    <p class="text-gris-medio text-sm font-bold tracking-wide">Añade nuevos productos al menú</p>
                </div>
            </a>

            <!-- Card: Agregar Usuario -->
            <a href="agregar_usuario.php" class="group bg-gris-oscuro rounded-2xl p-8 border border-gris-medio/10 backdrop-blur-sm hover:border-rojo-intenso transition-all duration-300 transform hover:scale-[1.02] hover:shadow-2xl hover:shadow-rojo-intenso/20">
                <div class="flex flex-col h-full">
                    <div class="flex items-center justify-between mb-6">
                        <div class="w-16 h-16 bg-rojo-intenso/20 rounded-xl flex items-center justify-center group-hover:bg-rojo-intenso/30 transition-all duration-300">
                            <svg class="w-8 h-8 text-rojo-intenso" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
                            </svg>
                        </div>
                        <div class="text-rojo-intenso opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M9 5l7 7-7 7"></path>
                            </svg>
                        </div>
                    </div>
                    <h3 class="text-blanco text-2xl font-black mb-3 uppercase tracking-tight">Agregar Usuario</h3>
                    <p class="text-gris-medio text-sm font-bold tracking-wide">Registra nuevos usuarios en el sistema</p>
                </div>
            </a>

        </div>

    </div>

</body>
</html>