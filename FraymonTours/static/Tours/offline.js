document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("database-error-modal");
    const closeButton = document.getElementById("database-error-close");

    function showDatabaseError() {
        if (!modal) {
            alert("ERROR: No puede ingresar a la página por el momento, inténtelo más tarde.");
            return;
        }
        modal.hidden = false;
        modal.style.position = "fixed";
        modal.style.inset = "0";
        modal.style.zIndex = "9999";
        modal.style.background = "rgba(20, 20, 20, 0.72)";
    }

    if (closeButton) {
        closeButton.addEventListener("click", function () {
            modal.hidden = true;
        });
    }

    const offlineMode = document.body.dataset.offlineMode === "true";

    document.querySelectorAll("a[href], button[type='submit'], form").forEach(function (element) {
        element.addEventListener("click", function (event) {
            if (element.tagName === "A") {
                const href = element.getAttribute("href") || "";
                if (href.startsWith("#")) return;
            }

            if (offlineMode) {
                event.preventDefault();
                showDatabaseError();
                return;
            }

            event.preventDefault();
            event.stopImmediatePropagation();

            fetch("/api/tours/", { cache: "no-store" })
                .then(function (response) {
                    if (!response.ok) throw new Error("Database unavailable");
                    return response.json();
                })
                .then(function () {
                    if (element.tagName === "FORM") {
                        element.submit();
                    } else if (element.tagName === "A") {
                        window.location.assign(element.href);
                    }
                })
                .catch(showDatabaseError);
        }, true);
    });

    document.querySelectorAll("form").forEach(function (form) {
        form.addEventListener("submit", function (event) {
            event.preventDefault();
            if (offlineMode) {
                showDatabaseError();
                return;
            }

            fetch("/api/tours/", { cache: "no-store" })
                .then(function (response) {
                    if (!response.ok) throw new Error("Database unavailable");
                    return response.json();
                })
                .then(function () { HTMLFormElement.prototype.submit.call(form); })
                .catch(showDatabaseError);
        }, true);
    });
});
