// EventHub Main JavaScript Engine

document.addEventListener('DOMContentLoaded', function() {
    // 1. Mobile Navigation Toggle
    const navToggleBtn = document.getElementById('mobileNavToggle');
    const navMenu = document.getElementById('navMenu');

    if (navToggleBtn && navMenu) {
        navToggleBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            navMenu.classList.toggle('show');
        });

        // Close menu on click outside
        document.addEventListener('click', function(e) {
            if (!navMenu.contains(e.target) && !navToggleBtn.contains(e.target)) {
                navMenu.classList.remove('show');
            }
        });
    }

    // 2. User Menu Dropdown Toggle
    const userMenuBtn = document.getElementById('userMenuBtn');
    const userDropdownContent = document.getElementById('userDropdownContent');

    if (userMenuBtn && userDropdownContent) {
        userMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            userDropdownContent.classList.toggle('show');
        });

        document.addEventListener('click', function(e) {
            if (!userDropdownContent.contains(e.target) && !userMenuBtn.contains(e.target)) {
                userDropdownContent.classList.remove('show');
            }
        });
    }

    // 3. Flash Alert Auto Dismiss
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.transition = 'opacity 0.4s ease';
            alert.style.opacity = '0';
            setTimeout(function() { alert.remove(); }, 400);
        }, 5000);
    });
});

// 4. Password Toggle Function
function togglePasswordVisibility(inputId, buttonEl) {
    const inputField = document.getElementById(inputId);
    if (!inputField) return;

    const icon = buttonEl.querySelector('i');

    if (inputField.type === 'password') {
        inputField.type = 'text';
        if (icon) {
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
        }
    } else {
        inputField.type = 'password';
        if (icon) {
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
        }
    }
}
