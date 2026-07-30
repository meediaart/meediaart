console.log("posts-list.js loaded");
document.addEventListener("DOMContentLoaded", function () {

    // عناصر البحث والفلاتر
    const searchInput = document.getElementById("postSearch");
    const statusFilter = document.getElementById("postStatusFilter");
    const homeFilter = document.getElementById("postHomeFilter");
    const resetButton = document.getElementById("resetPostFilters");

    // صفوف المقالات
    const postRows = Array.from(
        document.querySelectorAll(".post-row")
    );

    // عداد النتائج
    const resultsCount = document.getElementById("postsResultsCount");

    // صف رسالة عدم وجود نتائج
    const noResultsRow = document.getElementById("noPostsResults");

    /**
     * توحيد النص قبل المقارنة والبحث.
     */
    function normalizeText(value) {
        return String(value || "")
            .toLowerCase()
            .trim();
    }

    /**
     * تطبيق البحث والفلاتر على المقالات.
     */
    function filterPosts() {

        const searchValue = normalizeText(searchInput.value);
        const statusValue = normalizeText(statusFilter.value);
        const homeValue = normalizeText(homeFilter.value);

        let visibleCount = 0;

        postRows.forEach(function (row) {

            const title = normalizeText(row.dataset.title);
            const slug = normalizeText(row.dataset.slug);
            const status = normalizeText(row.dataset.status);
            const home = normalizeText(row.dataset.home);

            // البحث في العنوان والرابط
            const matchesSearch =
                searchValue === "" ||
                title.includes(searchValue) ||
                slug.includes(searchValue);

            // مطابقة حالة النشر
            const matchesStatus =
                statusValue === "" ||
                status === statusValue;

            // مطابقة الظهور في الرئيسية
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

        // تحديث عدد النتائج
        resultsCount.textContent = visibleCount;

        // إظهار رسالة عند عدم وجود نتائج
        if (postRows.length > 0 && visibleCount === 0) {
            noResultsRow.style.display = "";
        } else {
            noResultsRow.style.display = "none";
        }
    }

    /**
     * تصفير البحث والفلاتر.
     */
    function resetFilters() {
        searchInput.value = "";
        statusFilter.value = "";
        homeFilter.value = "";

        filterPosts();
        searchInput.focus();
    }

    // البحث يعمل أثناء الكتابة
    searchInput.addEventListener("input", filterPosts);

    // تشغيل الفلاتر عند التغيير
    statusFilter.addEventListener("change", filterPosts);
    homeFilter.addEventListener("change", filterPosts);

    // زر إعادة التعيين
    resetButton.addEventListener("click", resetFilters);

    // تشغيل أولي
    filterPosts();
});
