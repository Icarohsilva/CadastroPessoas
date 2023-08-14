// Script para mostrar/ocultar senha
function togglePasswordVisibility(inputId, toggleId) {
    const input = document.getElementById(inputId);
    const toggle = document.getElementById(toggleId);

    let isMouseDown = false;

    toggle.addEventListener('mousedown', () => {
        isMouseDown = true;
        input.type = 'text';
    });

    document.addEventListener('mouseup', () => {
        if (isMouseDown) {
            input.type = 'password';
        }
        isMouseDown = false;
    });

    toggle.addEventListener('mouseout', () => {
        if (!isMouseDown) {
            input.type = 'password';
        }
    });
}
