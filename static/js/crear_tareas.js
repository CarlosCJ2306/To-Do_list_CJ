// Espera a que todo el contenido del DOM se haya cargado antes de ejecutar el código
document.addEventListener('DOMContentLoaded', () => {
    // Referencias a los elementos del DOM
    const formularioTarea = document.getElementById('formulario-tarea');
    const listaTareas = document.getElementById('lista-tareas');

    // Obtiene las tareas almacenadas en el localStorage o inicializa un array vacío
    let tareas = JSON.parse(localStorage.getItem('tareas')) || [];

    /**
     * Renderiza la lista de tareas en la interfaz de usuario.
     * Actualiza el contenido HTML de listaTareas con las tareas almacenadas.
     */
    function renderizarTareas() {
        // Limpia la lista de tareas actual para evitar duplicados
        listaTareas.innerHTML = '';

        // Itera sobre cada tarea y crea un elemento <li> para mostrar en la lista
        tareas.forEach((tarea, index) => {
            const li = document.createElement('li');
            li.dataset.estado = tarea.estado; // Añade un atributo de estado para estilo o lógica adicional

            // Construye el HTML para cada tarea
            li.innerHTML = `
                <div class="tarea-info">
                    <strong>${tarea.titulo}</strong>
                    <p>${tarea.descripcion}</p>
                </div>
                <div class="actions">
                    <button class="editar" data-index="${index}">Editar</button>
                    <button class="eliminar" data-index="${index}">Eliminar</button>
                    <button class="estado" data-index="${index}">${tarea.estado === 'pendiente' ? 'Marcar como Hecha' : 'Marcar como Pendiente'}</button>
                </div>
            `;
            listaTareas.appendChild(li);
        });
    }

    /**
     * Guarda las tareas en el localStorage.
     * Convierte el array de tareas a formato JSON y lo almacena.
     */
    function guardarTareas() {
        localStorage.setItem('tareas', JSON.stringify(tareas));
    }

    // Maneja el envío del formulario para agregar una nueva tarea
    formularioTarea.addEventListener('submit', (event) => {
        event.preventDefault(); // Previene el comportamiento predeterminado del formulario

        // Obtiene los valores del formulario y elimina espacios en blanco
        const titulo = event.target.titulo.value.trim();
        const descripcion = event.target.descripcion.value.trim();
        const estado = event.target.estado.value;

        // Verifica que el título y la descripción no estén vacíos antes de agregar la tarea
        if (titulo && descripcion) {
            // Agrega la nueva tarea al array y guarda las tareas actualizadas
            tareas.push({ titulo, descripcion, estado });
            guardarTareas();
            renderizarTareas(); // Actualiza la interfaz con la nueva tarea
            formularioTarea.reset(); // Limpia el formulario después de agregar la tarea
        }
    });

    // Maneja los eventos de clic en la lista de tareas para editar, eliminar o cambiar el estado de una tarea
    listaTareas.addEventListener('click', (event) => {
        // Identifica el tipo de acción que se debe realizar según la clase del botón clicado
        if (event.target.classList.contains('eliminar')) {
            // Elimina la tarea correspondiente del array y actualiza el almacenamiento y la interfaz
            const index = event.target.dataset.index;
            tareas.splice(index, 1);
            guardarTareas();
            renderizarTareas();
        } else if (event.target.classList.contains('editar')) {
            // Rellena el formulario con los datos de la tarea seleccionada para editar
            const index = event.target.dataset.index;
            const tarea = tareas[index];
            document.getElementById('titulo').value = tarea.titulo;
            document.getElementById('descripcion').value = tarea.descripcion;
            document.getElementById('estado').value = tarea.estado;

            // Elimina la tarea del array y actualiza el almacenamiento y la interfaz
            tareas.splice(index, 1);
            guardarTareas();
            renderizarTareas();
        } else if (event.target.classList.contains('estado')) {
            // Cambia el estado de la tarea entre 'pendiente' y 'hecha'
            const index = event.target.dataset.index;
            tareas[index].estado = tareas[index].estado === 'pendiente' ? 'hecha' : 'pendiente';
            guardarTareas();
            renderizarTareas();
        }
    });

    // Renderiza las tareas al cargar la página para mostrar el estado actual
    renderizarTareas();
});
