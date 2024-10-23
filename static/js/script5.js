document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value; // Получаем CSRF-токен из шаблона

    // Привязка события к кнопкам удаления
    document.querySelectorAll('.deleteRecord').forEach(button => {
        button.addEventListener('click', function () {
            const itemId = this.getAttribute('data-item-id'); // Получаем корректный ID элемента
            const confirmationPopup = document.getElementById('deleteConfirmation');
            
            if (confirmationPopup) {
                confirmationPopup.style.display = 'block';

                // Привязываем обработчик к кнопке подтверждения "Да"
                const confirmDeleteButton = document.getElementById('confirmDeleteButton');
                confirmDeleteButton.onclick = function () {
                    if (itemId) {
                        fetch(`/stock/item/${itemId}/delete/`, { // абсолютный путь
                            method: 'DELETE',
                            headers: {
                                'X-CSRFToken': csrfToken, // используем загруженный токен
                            },
                        })
                        .then(response => {
                            if (response.ok) {
                                window.location.reload(); // Перезагружаем страницу после успешного удаления
                            } else {
                                console.error('Ошибка удаления');
                            }
                        })
                        .catch(error => console.error('Ошибка запроса:', error));

                        confirmationPopup.style.display = 'none';
                    } else {
                        console.error('ID элемента не был получен.');
                    }
                };

                // Кнопка "Нет" просто закрывает popup
                const cancelDeleteButton = document.getElementById('cancelDeleteButton');
                cancelDeleteButton.onclick = function () {
                    confirmationPopup.style.display = 'none';
                };
            } else {
                console.error("Всплывающее окно подтверждения удаления не найдено.");
            }
        });
    });
});
