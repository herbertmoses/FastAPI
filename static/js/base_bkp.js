document.addEventListener("DOMContentLoaded", function () {

    console.log("base.js loaded");

    const registerForm = document.getElementById('registerForm');
    console.log("registerForm:", registerForm);

    if (registerForm) {

        registerForm.addEventListener('submit', async function (event) {

            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            if (data.password !== data.password2) {
                alert("Passwords do not match");
                return;
            }

            const payload = {
                email: data.email,
                username: data.username,
                first_name: data.first_name,
                last_name: data.last_name,
                role: data.role,
                phone_number: data.phone_number,
                password: data.password
            };

            console.log("Payload:", payload);

            const response = await fetch('/auth/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            const result = await response.json();
            console.log(result);

            if (response.ok) {
                window.location.href = '/auth/login-page';
            } else {
                alert(JSON.stringify(result));
            }

        });

    }

});