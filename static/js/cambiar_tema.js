// Obtiene una referencia al botón de cambio de tema mediante su ID
const botonCambiarTema = document.getElementById('cambiar_tema');

/**
 * Cambia el tema de la página entre claro y oscuro.
 * Alterna la clase 'light-theme' en el elemento <body> y guarda la preferencia en localStorage.
 */
function cambiarTema() {
    // Alterna la clase 'light-theme' en el <body> y devuelve si el tema es claro
    const esTemaClaro = document.body.classList.toggle('light-theme');
    
    // Guarda la preferencia del tema en localStorage ('light' o 'dark')
    localStorage.setItem('tema', esTemaClaro ? 'light' : 'dark');
}

// Carga y aplica el tema guardado al iniciar la página
document.addEventListener('DOMContentLoaded', () => {
    // Obtiene el tema guardado desde localStorage
    const temaGuardado = localStorage.getItem('tema');
    
    // Si el tema guardado es 'light', añade la clase 'light-theme' al <body>
    if (temaGuardado === 'light') {
        document.body.classList.add('light-theme');
    }
});

// Asocia la función 'cambiarTema' al evento de clic del botón de cambio de tema
botonCambiarTema.addEventListener('click', cambiarTema);
