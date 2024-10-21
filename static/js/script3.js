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