document.addEventListener('DOMContentLoaded', function() {
    // Obtener los usuarios del script de JSON
    const usuarioList = JSON.parse(document.getElementById("usuarios").textContent);

    // Comprobar si la lista de usuarios está vacía
    if (usuarioList.length === 0) {
        // Recargar la página si no hay usuarios
        window.location.reload();
    } else {
        console.log("Usuarios registrados: ", usuarioList);
        // Aquí puedes agregar más lógica para manejar los usuarios si es necesario
    }
});
