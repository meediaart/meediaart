document.addEventListener("DOMContentLoaded", function () {

    // عناصر البحث والفلاتر
    const searchInput = document.getElementById("projectSearch");
    const typeFilter = document.getElementById("projectTypeFilter");
    const statusFilter = document.getElementById("projectStatusFilter");
    const homeFilter = document.getElementById("projectHomeFilter");
    const resetButton = document.getElementById("resetProjectFilters");

    // جميع صفوف المشاريع
    const projectRows = Array.from(
        document.querySelectorAll(".project-row")
    );

    // عداد النتائج
    const resultsCount = document.getElementById("projectsResultsCount");

    // رسالة عدم وجود نتائج
    const noResultsRow = document.getElementById("noProjectsResults");

    /**
     * تنظيف وتوحيد النصوص قبل البحث والمقارنة.
     */
    function normalizeText(value) {
        return String(value || "")
            .toLowerCase()
            .trim();
    }

    /**
     * تطبيق البحث والفلاتر على صفوف المشاريع.
     */
    function filterProjects() {

        const searchValue = normalizeText(searchInput.value);
        const typeValue = normalizeText(typeFilter.value);
        const statusValue = normalizeText(statusFilter.value);
        const homeValue = normalizeText(homeFilter.value);

        let visibleCount = 0;

        projectRows.forEach(function (row) {

            const title = normalizeText(row.dataset.title);
            const client = normalizeText(row.dataset.client);
            const type = normalizeText(row.dataset.type);
            const status = normalizeText(row.dataset.status);
            const home = normalizeText(row.dataset.home);

            // البحث يشمل العنوان واسم العميل ونوع المشروع
            const matchesSearch =
                searchValue === "" ||
                title.includes(searchValue) ||
                client.includes(searchValue) ||
                type.includes(searchValue);

            // فلتر نوع المشروع
            const matchesType =
                typeValue === "" ||
                type === typeValue;

            // فلتر حالة النشر
            const matchesStatus =
                statusValue === "" ||
                status === statusValue;

            // فلتر الظهور في الرئيسية
            const matchesHome =
                homeValue === "" ||
                home === homeValue;

            const shouldShow =
                matchesSearch &&
                matchesType &&
                matchesStatus &&
                matchesHome;

            row.style.display = shouldShow ? "" : "none";

            if (shouldShow) {
                visibleCount++;
            }
        });

        // تحديث عداد النتائج
        resultsCount.textContent = visibleCount;

        // إظهار رسالة عدم وجود نتائج
        if (projectRows.length > 0 && visibleCount === 0) {
            noResultsRow.style.display = "";
        } else {
            noResultsRow.style.display = "none";
        }
    }

    /**
     * إعادة البحث والفلاتر إلى الوضع الافتراضي.
     */
    function resetFilters() {
        searchInput.value = "";
        typeFilter.value = "";
        statusFilter.value = "";
        homeFilter.value = "";

        filterProjects();
        searchInput.focus();
    }

    // البحث المباشر أثناء الكتابة
    searchInput.addEventListener("input", filterProjects);

    // تشغيل الفلاتر عند تغيير القيم
    typeFilter.addEventListener("change", filterProjects);
    statusFilter.addEventListener("change", filterProjects);
    homeFilter.addEventListener("change", filterProjects);

    // زر إعادة التعيين
    resetButton.addEventListener("click", resetFilters);

    // تشغيل أولي عند فتح الصفحة
    filterProjects();
});
