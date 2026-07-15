document.addEventListener("DOMContentLoaded", function () {

    // ===========================
    // Drag & Drop Upload
    // ===========================

    const dropArea = document.getElementById("drop-area");

    if (dropArea) {

        const input = dropArea.querySelector("input");
        const fileName = document.getElementById("file-name");

        dropArea.addEventListener("click", function () {
            input.click();
        });

        input.addEventListener("change", function () {

            if (input.files.length) {
                fileName.textContent = input.files[0].name;
            }

        });

        dropArea.addEventListener("dragover", function (e) {

            e.preventDefault();
            dropArea.style.borderColor = "#00ff88";

        });

        dropArea.addEventListener("dragleave", function () {

            dropArea.style.borderColor = "#dc3545";

        });

        dropArea.addEventListener("drop", function (e) {

            e.preventDefault();

            input.files = e.dataTransfer.files;

            if (input.files.length) {
                fileName.textContent = input.files[0].name;
            }

            dropArea.style.borderColor = "#dc3545";

        });

    }
    // ===========================
    // Navbar Shadow on Scroll
    // ===========================

    const navbar = document.querySelector(".navbar");

    if (navbar) {

        window.addEventListener("scroll", function () {

            if (window.scrollY > 30) {

                navbar.classList.add("shadow-lg");
                navbar.classList.add("scrolled");

            } else {

                navbar.classList.remove("shadow-lg");
                navbar.classList.remove("scrolled");

            }

        });

    }

    // ===========================
    // Mobile Navbar Auto Close
    // ===========================

    const navLinks = document.querySelectorAll(".navbar-collapse .nav-link");
    const navbarCollapse = document.getElementById("navbarNav");

    navLinks.forEach(function (link) {

        link.addEventListener("click", function () {

            if (
                navbarCollapse &&
                navbarCollapse.classList.contains("show")
            ) {

                bootstrap.Collapse.getOrCreateInstance(navbarCollapse).hide();

            }

        });

    });
    // ===========================
    // Auto Close Alerts
    // ===========================

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();

        }, 5000);

    });

});