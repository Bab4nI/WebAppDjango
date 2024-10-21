// Открытие всплывающего окна
const popup = document.getElementById("popup");
const popupInnerContent = document.getElementById("popupInnerContent");
const closeBtn = document.querySelector(".close");
const doneButton = document.getElementById("doneButton");

function openPopup(content) {
    popupInnerContent.innerHTML = content;
    popup.style.display = "flex";
}

closeBtn.onclick = function() {
    popup.style.display = "none";
};

// Закрытие окна при нажатии вне области окна
window.onclick = function(event) {
    if (event.target === popup) {
        popup.style.display = "none";
    }
};

// Проверка заполненности полей
function validateForm() {
    const inputs = document.querySelectorAll("#popupInnerContent input");
    let allFilled = true;

    inputs.forEach(input => {
        if (input.value.trim() === "") {
            allFilled = false;
        }
    });

    // Активируем кнопку только если все поля заполнены
    doneButton.disabled = !allFilled;
}



document.getElementById("addRecord").onclick = function() {
    openPopup(`
        <h3>Добавить запись</h3>
        <p>Введите данные:</p>
        <input type="text" id="serialNumber" placeholder="ID записи" class="input-field"><br>
        <input type="text" id="name" placeholder="Название" class="input-field"><br>
        <input type="text" id="location" placeholder="Местоположение" class="input-field"><br>
        <input type="text" id="responsibleEmployee" placeholder="Сотрудник" class="input-field"><br><br>
    `);

    // Добавляем валидацию полей
    const inputs = document.querySelectorAll("#popupInnerContent .input-field");
    inputs.forEach(input => {
        input.addEventListener("input", validateForm);
    });

    // Сброс состояния кнопки "Готово"
    doneButton.disabled = true;

    doneButton.onclick = function() {
        const serialNumber = document.getElementById("serialNumber").value; 
        const name = document.getElementById("name").value;
        const location = document.getElementById("location").value;
        const responsibleEmployee = document.getElementById("responsibleEmployee").value;
    
        // Подготовка данных для отправки
        const data = {
            serialNumber: serialNumber,
            name: name,
            location: location,
            responsibleEmployee: responsibleEmployee
        };
    
        // Отправка данных на сервер с использованием fetch
        fetch("/save-record", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            console.log("Данные успешно отправлены:", result);
            // Закрытие всплывающего окна после отправки данных
            popup.style.display = "none";
        })
        .catch(error => {
            console.error("Ошибка при отправке данных:", error);
        });
    
        popup.style.display = "none";
    };
};



document.getElementById("changeRecord").onclick = function() {
    openPopup(`
        <h3>Изменить запись</h3>
        <p>Выберите запись для изменения:</p>
        <input type="text" id="serialNumber" placeholder="ID записи" class="input-field"><br>
        <p>Введите новые данные:</p>
        <input type="text" id="name" placeholder="Новое название" class="input-field"><br>
        <input type="text" id="location" placeholder="Новое местоположение" class="input-field"><br>
        <input type="text" id="responsibleEmployee" placeholder="Новый сотрудник" class="input-field"><br><br>
    `);

    const inputs = document.querySelectorAll("#popupInnerContent .input-field");
    inputs.forEach(input => {
        input.addEventListener("input", validateForm);
    });

    doneButton.disabled = true;

    doneButton.onclick = function() {
        const serialNumber = document.getElementById("serialNumber").value; 
        const name = document.getElementById("name").value;
        const location = document.getElementById("location").value;
        const responsibleEmployee = document.getElementById("responsibleEmployee").value;

        // Подготовка данных для отправки
        const data = {
            serialNumber: serialNumber,
            name: name,
            location: location,
            responsibleEmployee: responsibleEmployee
        };

        // Отправка данных на сервер с использованием fetch для изменения записи
        fetch(`/api/changeRecord/${serialNumber}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            console.log("Запись успешно изменена:", result);
            // Закрытие всплывающего окна после успешного изменения данных
            popup.style.display = "none";
        })
        .catch(error => {
            console.error("Ошибка при изменении записи:", error);
        });

        popup.style.display = "none";
    };
};



document.getElementById("deleteRecord").onclick = function() {
    openPopup('<h3>Удалить запись</h3><p>Введите ID записи для удаления:</p><input type="text" id="serialNumber" placeholder="ID записи" class="input-field"><br><br>');

    // Добавляем валидацию полей
    const inputs = document.querySelectorAll("#popupInnerContent .input-field");
    inputs.forEach(input => {
        input.addEventListener("input", validateForm);
    });

    // Сброс состояния кнопки "Готово"
    doneButton.disabled = true;

    // Обработка нажатия на кнопку "Готово"
    doneButton.onclick = function() {
        const serialNumber = document.getElementById("serialNumber").value;

        // Отправка данных на сервер с использованием fetch для изменения записи
        fetch(`/api/deleteRecord/${serialNumber}`, {
            method: "DELETE",
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Запись успешно удалена');
                closePopup(); // Закрыть окно после успешного удаления
            } else {
                alert('Ошибка при удалении записи');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });

        popup.style.display = "none";
    };
};

document.getElementById("addWarehouse").onclick = function() {
    openPopup(`
        <h3>Добавить склад</h3>
        <p>Введите данные склада:</p>
        <input type="text" id="warehouseId" placeholder="ID склада" class="input-field"><br>
        <input type="text" id="warehouseName" placeholder="Название склада" class="input-field"><br><br>
    `);

    // Добавляем валидацию полей
    const inputs = document.querySelectorAll("#popupInnerContent .input-field");
    inputs.forEach(input => {
        input.addEventListener("input", validateForm);
    });

    // Сброс состояния кнопки "Готово"
    doneButton.disabled = true;

    doneButton.onclick = function() {
        const warehouseId = document.getElementById("warehouseId").value; 
        const warehouseName = document.getElementById("warehouseName").value;

        // Подготовка данных для отправки
        const data = {
            warehouseId: warehouseId,
            warehouseName: warehouseName,
        };
    
        // Отправка данных на сервер с использованием fetch
        fetch("/save-record", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            console.log("Данные успешно отправлены:", result);
            // Закрытие всплывающего окна после отправки данных
            popup.style.display = "none";
        })
        .catch(error => {
            console.error("Ошибка при отправке данных:", error);
        });
    
        popup.style.display = "none";
    };
};

// Действие по нажатию на "Изменить склад"
document.getElementById("changeWarehouse").onclick = function() {
    openPopup(`
        <h3>Изменить склад</h3>
        <p>Введите ID склада для изменения:</p>
        <input type="text" id="warehouseId" placeholder="ID склада" class="input-field"><br>
        <p>Введите новые данные склада:</p>
        <input type="text" id="warehouseName" placeholder="Новое название склада" class="input-field"><br><br>
    `);

    // Добавляем валидацию полей
    const inputs = document.querySelectorAll("#popupInnerContent .input-field");
    inputs.forEach(input => {
        input.addEventListener("input", validateForm);
    });

    // Сброс состояния кнопки "Готово"
    doneButton.disabled = true;

    doneButton.onclick = function() {
        const warehouseId = document.getElementById("warehouseId").value; 
        const warehouseName = document.getElementById("warehouseName").value;

        // Подготовка данных для отправки
        const data = {
            warehouseId: warehouseId,
            warehouseName: warehouseName,
        };

        // Отправка данных на сервер с использованием fetch для изменения записи
        fetch(`/api/changeRecord/${warehouseId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            console.log("Запись успешно изменена:", result);
            // Закрытие всплывающего окна после успешного изменения данных
            popup.style.display = "none";
        })
        .catch(error => {
            console.error("Ошибка при изменении записи:", error);
        });

        popup.style.display = "none";
    };
};

// Действие по нажатию на "Удалить склад"
document.getElementById("deleteWarehouse").onclick = function() {
    openPopup('<h3>Удалить склад</h3><p>Введите ID склада для удаления:</p><input type="text" id="warehouseId" placeholder="ID склада" class="input-field"><br><br>');

    const inputs = document.querySelectorAll("#popupInnerContent .input-field");
    inputs.forEach(input => {
        input.addEventListener("input", validateForm);
    });

    doneButton.disabled = true;

    doneButton.onclick = function() {
        const warehouseId = document.getElementById("warehouseId").value;

        // Отправка данных на сервер с использованием fetch для изменения записи
        fetch(`/api/deleteRecord/${warehouseId}`, {
            method: "DELETE",
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Запись успешно удалена');
                closePopup(); // Закрыть окно после успешного удаления
            } else {
                alert('Ошибка при удалении записи');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });

        popup.style.display = "none";
    };
};





document.addEventListener('DOMContentLoaded', function () {
    const warehouseSelect = document.getElementById('warehouseSelect');
    const tableBody = document.getElementById('tableBody');

    // Обработчик изменения склада
    warehouseSelect.addEventListener('change', function () {
        const warehouseId = warehouseSelect.value;

        // AJAX-запрос на сервер для получения данных по выбранному складу
        fetch(`/get-warehouse-data/${warehouseId}`)
            .then(response => response.json())
            .then(data => {
                // Очищаем таблицу перед обновлением
                tableBody.innerHTML = '';

                if (data.products.length > 0) {
                    data.products.forEach((product, index) => {
                        const row = document.createElement('tr');
                        row.innerHTML = `
                            <td>${index + 1}</td>
                            <td>${product.qrCode} <button>show qr</button></td>
                            <td>${product.name}</td>
                            <td>${product.location}</td>
                            <td>${product.responsible}</td>
                        `;
                        tableBody.appendChild(row);
                    });
                } else {
                    // Если данные не найдены
                    const noDataRow = document.createElement('tr');
                    noDataRow.innerHTML = `<td colspan="5">No products found.</td>`;
                    tableBody.appendChild(noDataRow);
                }
            })
            .catch(error => console.error('Ошибка при получении данных:', error));
    });

    // Инициировать загрузку данных для первого склада по умолчанию
    warehouseSelect.dispatchEvent(new Event('change'));
});



document.addEventListener('DOMContentLoaded', function () {
    const qrButtons = document.querySelectorAll('.qr-btn');
    const qrPopup = document.getElementById('qrPopup');
    const qrCodeImage = document.getElementById('qrCode');
    const closeQrPopup = document.getElementById('closeQrPopup');

    qrButtons.forEach(button => {
        button.addEventListener('click', function () {
            const qrCodeUrl = this.getAttribute('data-qrcode');
            
            // Устанавливаем URL для изображения QR-кода
            qrCodeImage.src = qrCodeUrl;

            // Показать всплывающее окно с QR-кодом
            qrPopup.style.display = 'block';
        });
    });

    // Обработчик для закрытия всплывающего окна
    closeQrPopup.addEventListener('click', function () {
        qrPopup.style.display = 'none';
    });

    // Закрытие окна при нажатии вне его области
    window.onclick = function(event) {
        if (event.target === qrPopup) {
            qrPopup.style.display = 'none';
        }
    };
});