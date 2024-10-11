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

// Действие по нажатию на "Добавить запись"
document.getElementById("addRecord").onclick = function() {
    openPopup(`
        <h3>Добавить запись</h3>
        <p>Введите данные:</p>
        <input type="text" id="productName" placeholder="Название" class="input-field"><br>
        <input type="text" id="location" placeholder="Местоположение" class="input-field"><br>
        <input type="text" id="employee" placeholder="Сотрудник" class="input-field"><br>
        <button id="generateQrButton">Сгенерировать QR код</button>
        <div id="qrcode" style="margin-top: 20px;"></div>
        <button id="downloadQrButton" style="display:none;">Скачать QR-код</button>
    `);

    // Добавляем валидацию полей
    const inputs = document.querySelectorAll("#popupInnerContent .input-field");
    inputs.forEach(input => {
        input.addEventListener("input", validateForm);
    });

    // Сброс состояния кнопки "Готово"
    doneButton.disabled = true;

    // Обработка генерации QR-кода
    const generateQrButton = document.getElementById("generateQrButton");
    const downloadQrButton = document.getElementById("downloadQrButton");
    const qrCodeContainer = document.getElementById("qrcode");

    generateQrButton.onclick = function() {
        // Собираем данные для QR-кода
        const productName = document.getElementById("productName").value;
        const location = document.getElementById("location").value;
        const employee = document.getElementById("employee").value;

        const qrContent = `Название: ${productName}\nМестоположение: ${location}\nСотрудник: ${employee}`;
        
        // Генерация QR-кода
        qrCodeContainer.innerHTML = ""; // Очищаем предыдущий QR-код, если был
        const qrcode = new QRCode(qrCodeContainer, {
            text: qrContent,
            width: 128,
            height: 128
        });

        // Показать кнопку "Скачать QR-код"
        downloadQrButton.style.display = "block";

        // Скачать QR-код как PNG
        downloadQrButton.onclick = function() {
            const qrCanvas = qrCodeContainer.querySelector("canvas");
            if (qrCanvas) {
                const qrDataURL = qrCanvas.toDataURL("image/png");
                const link = document.createElement("a");
                link.href = qrDataURL;
                link.download = "qr_code.png";
                link.click();
            }
        };
    };
};

// Действие по нажатию на "Удалить запись"
document.getElementById("deleteRecord").onclick = function() {
    openPopup('<h3>Удалить запись</h3><p>Выберите запись для удаления.</p>');
};

// Действие по нажатию на "Добавить заголовок"
document.getElementById("addHeader").onclick = function() {
    openPopup('<h3>Добавить заголовок</h3><input type="text" placeholder="Новый заголовок"><br><button>Добавить</button>');
};

// Кнопка "Готово" закрывает окно и отправляет данные на сервер
doneButton.onclick = function() {
    const productName = document.getElementById("productName").value;
    const location = document.getElementById("location").value;
    const employee = document.getElementById("employee").value;

    // Подготовка данных для отправки
    const data = {
        productName: productName,
        location: location,
        employee: employee
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