// JavaScript para la Calculadora de Notas

document.addEventListener('DOMContentLoaded', function() {
    console.log('Calculadora de Notas - Frontend cargado');
    
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            console.log('Búsqueda:', e.target.value);
        });
    }
    
    const courseCards = document.querySelectorAll('.course-card');
    courseCards.forEach(card => {
        card.addEventListener('click', function() {
            console.log('Curso seleccionado');
        });
    });
});
