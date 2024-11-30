// Funcionalidad para mostrar/ocultar contraseñas
document.querySelectorAll('.toggle-password').forEach(button => {
    button.addEventListener('click', function () {
        const input = document.querySelector(this.getAttribute('data-target'));
        if (input.type === 'password') {
            input.type = 'text';
            this.textContent = '🙈'; // Cambia el ícono al de "ocultar"
        } else {
            input.type = 'password';
            this.textContent = '👁️'; // Cambia el ícono al de "mostrar"
        }
    });
});
