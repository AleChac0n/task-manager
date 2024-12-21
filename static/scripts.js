document.getElementById("createTaskForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Obtener valores del formulario
    const title = document.getElementById("title").value.trim();
    const description = document.getElementById("description").value.trim();
    const status = document.getElementById("status").value.trim();
    const userId = parseInt(document.getElementById("user_id").value, 10);

    // Validar que no haya campos vacíos
    if (!title || !description || !status || isNaN(userId)) {
        alert("Por favor, completa todos los campos correctamente.");
        return;
    }

    // Realizar la solicitud al backend para crear la tarea
    fetch("/task", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title,
            description: description,
            status: status,
            user_id: userId
        })
    })
    .then(response => {
        console.log("Respuesta del servidor:", response);
        if (!response.ok) {
            return response.json().then(error => {
                throw new Error(error.message || "Error en la creación de la tarea");
            });
        }
        return response.json();
    })
    .then(data => {
        console.log("Datos de respuesta:", data);
        alert(data.message || "Tarea creada con éxito");
        document.getElementById("createTaskForm").reset();
        fetchTasks(userId);  // Actualiza la lista de tareas
    })
    .catch(error => {
        console.error("Error:", error);
        alert(`Error: ${error.message}`);
    });

    // Función para obtener y mostrar las tareas
    function fetchTasks(userId) {
        fetch(`/tasks/${userId}`)
            .then(response => response.json())
            .then(data => {
                if (data.length > 0) {
                    let taskList = document.getElementById('taskList');
                    taskList.innerHTML = '';  // Limpiar la lista antes de agregar nuevas tareas
                    data.forEach(task => {
                        let taskItem = document.createElement('li');
                        taskItem.textContent = `${task.title} - ${task.status}`;
                        taskList.appendChild(taskItem);
                    });
                } else {
                    alert("No hay tareas para mostrar.");
                }
            })
            .catch(error => {
                console.error("Error al obtener tareas:", error);
            });
    }
});
