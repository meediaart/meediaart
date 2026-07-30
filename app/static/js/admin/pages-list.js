<script>
document.addEventListener("DOMContentLoaded", function () {

    // عناصر البحث والفلاتر
    const searchInput = document.getElementById("pageSearch");
    const statusFilter = document.getElementById("pageStatusFilter");
    const homeFilter = document.getElementById("pageHomeFilter");
    const resetButton = document.getElementById("resetPageFilters");

    // صفوف الصفحات
    const pageRows = Array.from(
        document.querySelectorAll(".page-row")
    );

    // عداد النتائج ورسالة عدم وجود نتائج
    const resultsCount = document.getElementById("pagesResultsCount");
    const noResultsRow = document.getElementById("noPagesResults");

    /**
     * توحيد النصوص لتسهيل البحث والمقارنة.
     */
    function normalizeText(value) {
        return String(value || "")
            .toLowerCase()
            .trim();
    }

    /**
     * تنفيذ البحث والفلاتر.
     */
    function filterPages() {

        const searchValue = normalizeText(searchInput.value);
        const statusValue = normalizeText(statusFilter.value);
        const homeValue = normalizeText(homeFilter.value);

        let visibleCount = 0;

        pageRows.forEach(function (row) {

            const title = normalizeText(row.dataset.title);
            const slug = normalizeText(row.dataset.slug);
            const status = normalizeText(row.dataset.status);
            const home = normalizeText(row.dataset.home);

            // البحث في عنوان الصفحة والرابط
            const matchesSearch =
                searchValue === "" ||
                title.includes(searchValue) ||
                slug.includes(searchValue);

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

        // إظهار أو إخفاء رسالة عدم وجود نتائج
        if (pageRows.length > 0 && visibleCount === 0) {
            noResultsRow.classList.remove("admin-hidden");
        } else {
            noResultsRow.classList.add("admin-hidden");
        }
    }

    /**
     * إعادة البحث والفلاتر إلى الوضع الافتراضي.
     */
    function resetFilters() {
        searchInput.value = "";
        statusFilter.value = "";
        homeFilter.value = "";

        filterPages();
        searchInput.focus();
    }

    // البحث المباشر
    searchInput.addEventListener("input", filterPages);

    // الفلاتر
    statusFilter.addEventListener("change", filterPages);
    homeFilter.addEventListener("change", filterPages);

    // زر إعادة التعيين
    resetButton.addEventListener("click", resetFilters);

    // تشغيل أولي
    filterPages();
});
</script>