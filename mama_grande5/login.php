<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
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
<body class="bg-negro-principal min-h-screen flex items-center justify-center px-4 relative overflow-hidden">
    
    <!-- Elementos decorativos de fondo -->
    <div class="absolute top-0 left-0 w-96 h-96 bg-rojo-intenso/5 rounded-full blur-3xl"></div>
    <div class="absolute bottom-0 right-0 w-96 h-96 bg-rojo-suave/5 rounded-full blur-3xl"></div>

    <div class="w-full max-w-md relative z-10">
        <div class="bg-gris-oscuro rounded-2xl shadow-2xl p-10 border border-gris-medio/10 backdrop-blur-sm">
            
            <!-- Título -->
            <div class="text-center mb-10">
                <div class="inline-block">
                    <h2 class="text-blanco text-5xl font-black mb-2 tracking-tight relative">
                        MAMA GRANDE
                        <div class="absolute -bottom-2 left-0 right-0 h-1 bg-gradient-to-r from-transparent via-rojo-intenso to-transparent"></div>
                    </h2>
                </div>
                <p class="text-gris-medio text-sm font-bold mt-6 tracking-wide">ACCEDE A TU CUENTA</p>
            </div>

            <!-- Formulario -->
            <form action="login_action.php" method="POST" class="space-y-6">
                
                <!-- Campo Email -->
                <div class="group">
                    <label for="email" class="block text-gris-claro text-xs font-black mb-3 uppercase tracking-widest">
                        Correo Electrónico
                    </label>
                    <input 
                        type="email" 
                        name="email" 
                        id="email" 
                        required
                        class="w-full px-5 py-4 bg-negro-principal border-2 border-gris-medio/20 rounded-xl text-blanco placeholder-gris-medio/50 focus:outline-none focus:border-rojo-intenso focus:shadow-lg focus:shadow-rojo-intenso/20 transition-all duration-300 font-bold group-hover:border-gris-medio/40"
                        placeholder="ejemplo@correo.com"
                    >
                </div>

                <!-- Campo Contraseña -->
                <div class="group">
                    <label for="password" class="block text-gris-claro text-xs font-black mb-3 uppercase tracking-widest">
                        Contraseña
                    </label>
                    <input 
                        type="password" 
                        name="password" 
                        id="password" 
                        required
                        class="w-full px-5 py-4 bg-negro-principal border-2 border-gris-medio/20 rounded-xl text-blanco placeholder-gris-medio/50 focus:outline-none focus:border-rojo-intenso focus:shadow-lg focus:shadow-rojo-intenso/20 transition-all duration-300 font-bold group-hover:border-gris-medio/40"
                        placeholder="••••••••••••"
                    >
                </div>

                <!-- Botón Submit -->
                <button 
                    type="submit"
                    class="w-full bg-gradient-to-r from-rojo-intenso to-rojo-suave hover:from-rojo-suave hover:to-rojo-intenso text-blanco font-black py-5 px-6 rounded-xl uppercase tracking-widest text-base transition-all duration-300 transform hover:scale-[1.02] hover:shadow-2xl hover:shadow-rojo-intenso/40 active:scale-[0.98] mt-8"
                >
                    INGRESAR
                </button>

            </form>



        </div>
    </div>

</body>
</html>