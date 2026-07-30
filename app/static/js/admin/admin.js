"use strict";

/*
|--------------------------------------------------------------------------
| لوحة الإدارة
|--------------------------------------------------------------------------
|
| يحتوي هذا الملف على الوظائف العامة المشتركة في جميع صفحات لوحة الإدارة.
|
| الوظائف الحالية:
| - فتح وإغلاق القائمة الجانبية على الشاشات الصغيرة.
|
*/

document.addEventListener("DOMContentLoaded", function () {
    const mobileToggle = document.getElementById(
        "adminMobileToggle"
    );

    const mobileSidebar = document.getElementById(
        "adminMobileSidebar"
    );

    if (!mobileToggle || !mobileSidebar) {
        return;
    }

    mobileToggle.addEventListener("click", function () {
        const isOpen = mobileSidebar.classList.toggle(
            "active"
        );

        mobileToggle.setAttribute(
            "aria-expanded",
            isOpen ? "true" : "false"
        );
    });
});
