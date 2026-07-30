console.log("services-list.js loaded");
document.addEventListener("DOMContentLoaded", function () {

    // عناصر البحث والفلاتر
    const searchInput = document.getElementById("serviceSearch");
    const statusFilter = document.getElementById("serviceStatusFilter");
    const homeFilter = document.getElementById("serviceHomeFilter");
    const resetButton = document.getElementById("resetServiceFilters");

    // صفوف الخدمات
    const serviceRows = Array.from(
        document.querySelectorAll(".service-row")
    );

    // عداد النتائج
    const resultsCount = document.getElementById("servicesResultsCount");

    // رسالة عدم وجود نتائج
    const noResultsRow = document.getElementById("noServicesResults");

    /**
     * توحيد النصوص قبل البحث والمقارنة.
     */
    function normalizeText(value) {
        return String(value || "")
            .toLowerCase()
            .trim();
    }

    /**
     * تطبيق البحث والفلاتر.
     */
    function filterServices() {

        const searchValue = normalizeText(searchInput.value);
        const statusValue = normalizeText(statusFilter.value);
        const homeValue = normalizeText(homeFilter.value);

        let visibleCount = 0;

        serviceRows.forEach(function (row) {

            const title = normalizeText(row.dataset.title);
            const description = normalizeText(row.dataset.description);
            const status = normalizeText(row.dataset.status);
            const home = normalizeText(row.dataset.home);

            // البحث في العنوان والوصف
            const matchesSearch =
                searchValue === "" ||
                title.includes(searchValue) ||
                description.includes(searchValue);

            // فلتر الحالة
            const matchesStatus =
                statusValue === "" ||
                status === statusValue;

            // فلتر الظهور في الرئيسية
            const matchesHome =
                homeValue === "" ||
                home === homeValue;

            const shouldShow =
                matchesSearch &&
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
        if (serviceRows.length > 0 && visibleCount === 0) {
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
        statusFilter.value = "";
        homeFilter.value = "";

        filterServices();
        searchInput.focus();
    }

    // البحث المباشر أثناء الكتابة
    searchInput.addEventListener("input", filterServices);

    // الفلاتر
    statusFilter.addEventListener("change", filterServices);
    homeFilter.addEventListener("change", filterServices);

    // إعادة التعيين
    resetButton.addEventListener("click", resetFilters);

    // تشغيل أولي
    filterServices();
});
