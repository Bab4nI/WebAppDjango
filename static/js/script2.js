// Для загрузки фото профиля
const loadFile = (event) => {
    const profilePhoto = document.getElementById('profilePhoto');
    profilePhoto.src = URL.createObjectURL(event.target.files[0]);
};

// Проверка паролей
const form = document.getElementById('registerForm');
const password = document.getElementById('password');
const confirmPassword = document.getElementById('confirm_password');
const submitBtn = document.getElementById('submitBtn');

// Проверка перед отправкой формы
form.addEventListener('submit', function (e) {
    if (password.value !== confirmPassword.value) {
        e.preventDefault(); // Отмена отправки формы
        alert('Пароли не совпадают. Попробуйте снова.');
    }
});

// Проверка при вводе
confirmPassword.addEventListener('input', function () {
    if (password.value === confirmPassword.value) {
        confirmPassword.classList.remove('invalid');
        confirmPassword.classList.add('valid');
        submitBtn.disabled = false; // Разблокировать кнопку
    } else {
        confirmPassword.classList.remove('valid');
        confirmPassword.classList.add('invalid');
        submitBtn.disabled = true; // Заблокировать кнопку
    }
});
