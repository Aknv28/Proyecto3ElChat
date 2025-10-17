document.querySelectorAll('input[type="number"]').forEach(input => {
    input.addEventListener('change', () => {
        let total = 0;
        document.querySelectorAll('input[type="number"]').forEach(input => {
            const precio = parseFloat(input.dataset.precio);
            total += precio * parseInt(input.value);
        });
        document.getElementById('total').innerText = 'Total: ' + total + ' Bs';
    });
});
