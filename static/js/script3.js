function showContent(sectionId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active');
    });
    document.getElementById(sectionId).classList.add('active');
}

document.getElementById("exitBtn").addEventListener("click", function() {
    fetch('/logout', {
        method: 'POST',
        credentials: 'include' // Если нужно отправить куки
    })
    .then(response => {
        if (response.ok) {
            // Если выход успешен, перенаправляем на главную страницу
            window.location.href = '/index'; // Укажите ваш URL главной страницы
        } else {
            // Обработка ошибок, если выход не удался
            alert("Ошибка при выходе из аккаунта");
        }
    })
    .catch(error => {
        console.error("Ошибка:", error);
        alert("Ошибка при выходе из аккаунта");
    });
});

document.getElementById('submitRequest').onclick = function() {
    const employeeId = document.getElementById('employeesSelect').value;
    const warehouseId = document.getElementById('warehouseSelect').value;
    const deadline = document.getElementById('deadline').value;

    // Подготовка данных для отправки
    const requestData = {
        employee_id: employeeId,
        warehouse_id: warehouseId,
        deadline: deadline,
    };

    // Отправка данных на сервер с использованием fetch
    fetch('/create-request/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}',  // CSRF токен для защиты
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Заявка успешно создана');
        } else {
            alert('Ошибка при создании заявки');
        }
    })
    .catch(error => console.error('Ошибка:', error));
};




document.getElementById("submitRequest").onclick = function() {
    // Получаем данные из формы
    const employee = document.querySelector('select[name="employee"]').value;
    const warehouse = document.querySelector('select[name="warehouse"]').value;
    const deadline = document.querySelector('input[name="deadline"]').value;

    // Создаем объект данных для отправки
    const data = {
        employee: employee,
        warehouse: warehouse,
        deadline: deadline,
        csrfmiddlewaretoken: '{{ csrf_token }}'  // Обязательно передаём CSRF токен для защиты от CSRF атак
    };

    // Отправляем данные на сервер с использованием fetch API
    fetch("{% url 'название_вашего_url' %}", { // Укажите правильный URL, на который будут отправлены данные
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Заявка успешно создана');
            // Здесь можно добавить логику для обновления страницы или перехода
        } else {
            alert('Ошибка при создании заявки');
        }
    })
    .catch((error) => {
        console.error('Ошибка:', error);
    });
};