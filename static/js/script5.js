document.addEventListener('DOMContentLoaded', function () {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value; // Получаем CSRF-токен

    function bindDeleteButtons(selector, fetchUrlTemplate, confirmButtonId, cancelButtonId, popupId) {
        document.querySelectorAll(selector).forEach(button => {
            button.addEventListener('click', function () {
                const itemId = this.getAttribute('data-item-id') || this.getAttribute('data-warehouse-id'); // Получаем ID элемента
                const confirmationPopup = document.getElementById(popupId);
                
                if (confirmationPopup && itemId) {
                    confirmationPopup.style.display = 'flex';

                    // Привязываем обработчик к кнопке подтверждения удаления
                    const confirmDeleteButton = document.getElementById(confirmButtonId);
                    confirmDeleteButton.onclick = function () {
                        fetch(fetchUrlTemplate.replace('{id}', itemId), {
                            method: 'DELETE', // Изменено на POST
                            headers: {
                                'X-CSRFToken': csrfToken,
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify({ action: 'delete' })
                        })
                        .then(response => {
                            if (response.ok) {
                                window.location.reload(); // Перезагружаем страницу после успешного удаления
                            } else {
                                console.error('Ошибка удаления');
                            }
                        })
                        .catch(error => console.error('Ошибка запроса:', error));

                        confirmationPopup.style.display = 'none'; // Закрываем окно подтверждения
                    };

                    // Привязываем обработчик к кнопке "Нет", чтобы закрыть popup
                    const cancelDeleteButton = document.getElementById(cancelButtonId);
                    cancelDeleteButton.onclick = function () {
                        confirmationPopup.style.display = 'none'; // Закрываем окно подтверждения
                    };
                } else {
                    console.error("Ошибка: Окно подтверждения или ID элемента не найден.");
                }
            });
        });
    }

    // Привязываем обработчики к кнопкам удаления предметов и складов
    bindDeleteButtons('.deleteRecord', '/stock/item/{id}/delete/', 'confirmDeleteItemButton', 'cancelDeleteItemButton', 'deleteConfirmation');
    bindDeleteButtons('.WarehouseDeleteRecord', '/stock/warehouse/{id}/delete/', 'confirmDeleteWarehouseButton', 'cancelDeleteWarehouseButton', 'WarehouseDeleteConfirmation');
});
