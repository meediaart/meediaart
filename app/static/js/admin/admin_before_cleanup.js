"use strict";

/*/*
|--------------------------------------------------------------------------
| القائمة الجانبية للوحة الإدارة
|--------------------------------------------------------------------------
|
| مسؤول عن:
| 1. فتح القائمة في الجوال.
| 2. إغلاقها عند الضغط على الخلفية.
| 3. إغلاقها بعد الضغط على أحد الروابط.
| 4. تحديث خصائص الوصول aria.
|
*/

/*document.addEventListener("DOMContentLoaded", function () {

    const menuButton =
        document.getElementById(
            "adminMenuBtn"
        );

    const sidebar =
        document.getElementById(
            "adminSidebar"
        );

    const backdrop =
        document.getElementById(
            "adminSidebarBackdrop"
        );

    if (!menuButton || !sidebar) {
        return;
    }

    function openSidebar() {

        sidebar.classList.add("active");

        menuButton.setAttribute(
            "aria-expanded",
            "true"
        );

        document.body.classList.add(
            "admin-sidebar-open"
        );

        if (backdrop) {
            backdrop.hidden = false;
        }
    }

    function closeSidebar() {

        sidebar.classList.remove("active");

        menuButton.setAttribute(
            "aria-expanded",
            "false"
        );

        document.body.classList.remove(
            "admin-sidebar-open"
        );

        if (backdrop) {
            backdrop.hidden = true;
        }
    }

    function toggleSidebar() {

        const isOpen =
            sidebar.classList.contains(
                "active"
            );

        if (isOpen) {
            closeSidebar();
        } else {
            openSidebar();
        }
    }

    menuButton.addEventListener(
        "click",
        toggleSidebar
    );

    if (backdrop) {

        backdrop.addEventListener(
            "click",
            closeSidebar
        );
    }

    sidebar
        .querySelectorAll("a")
        .forEach(function (link) {

            link.addEventListener(
                "click",
                closeSidebar
            );
        });

    document.addEventListener(
        "keydown",
        function (event) {

            if (event.key === "Escape") {
                closeSidebar();
            }
        }
    );

});*/
