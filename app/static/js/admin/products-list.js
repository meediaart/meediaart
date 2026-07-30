document.addEventListener("DOMContentLoaded", function () {

    // =========================
    // عناصر البحث والفلاتر
    // =========================

    const searchInput =
        document.getElementById("productSearch");

    const categoryFilter =
        document.getElementById("categoryFilter");

    const statusFilter =
        document.getElementById("statusFilter");

    const homeFilter =
        document.getElementById("homeFilter");

    const resetButton =
        document.getElementById("resetProductFilters");

    const productRows = Array.from(
        document.querySelectorAll(".product-row")
    );

    const resultsCount =
        document.getElementById("productsResultsCount");

    const noResultsRow =
        document.getElementById("noProductsResults");

    // =========================
    // عناصر الإجراءات الجماعية
    // =========================

    const bulkBar =
        document.getElementById("productsBulkBar");

    const selectAllCheckbox =
        document.getElementById("selectAllProducts");

    const productCheckboxes = Array.from(
        document.querySelectorAll(".product-select-checkbox")
    );

    const selectedCount =
        document.getElementById("selectedProductsCount");

    const bulkForm =
        document.getElementById("productsBulkForm");

    const bulkAction =
        document.getElementById("bulkAction");

    const categoryGroup =
        document.getElementById("bulkCategoryGroup");

    const categoryInput =
        document.getElementById("bulkCategoryId");

    const discountGroup =
        document.getElementById("bulkDiscountGroup");

    const discountInput =
        document.getElementById("bulkDiscountPercent");

    /**
     * تنظيف النص قبل البحث والمقارنة.
     */
    function normalizeText(value) {
        return String(value || "")
            .toLowerCase()
            .trim();
    }

    /**
     * الحصول على مربعات المنتجات الظاهرة فقط.
     */
    function getVisibleCheckboxes() {
        return productRows
            .filter(function (row) {
                return row.style.display !== "none";
            })
            .map(function (row) {
                return row.querySelector(
                    ".product-select-checkbox"
                );
            })
            .filter(Boolean);
    }

    /**
     * تحديث حالة مربع تحديد الكل.
     */
    function updateSelectAllState() {

        const visibleCheckboxes =
            getVisibleCheckboxes();

        const checkedVisible =
            visibleCheckboxes.filter(function (checkbox) {
                return checkbox.checked;
            });

        if (!visibleCheckboxes.length) {
            selectAllCheckbox.checked = false;
            selectAllCheckbox.indeterminate = false;
            return;
        }

        selectAllCheckbox.checked =
            checkedVisible.length === visibleCheckboxes.length;

        selectAllCheckbox.indeterminate =
            checkedVisible.length > 0 &&
            checkedVisible.length < visibleCheckboxes.length;
    }

    /**
     * تحديث عدد المنتجات المحددة وإظهار أو إخفاء الشريط.
     */
    function updateSelectedCount() {

        const count = productCheckboxes.filter(
            function (checkbox) {
                return checkbox.checked;
            }
        ).length;

        selectedCount.textContent =
            "تم تحديد: " + count;

        if (count > 0) {
            bulkBar.style.display = "flex";
        } else {
            bulkBar.style.display = "none";
        }

        updateSelectAllState();
    }

    /**
     * تنفيذ البحث والفلاتر.
     */
    function filterProducts() {

        const searchValue =
            normalizeText(searchInput.value);

        const categoryValue =
            normalizeText(categoryFilter.value);

        const statusValue =
            normalizeText(statusFilter.value);

        const homeValue =
            normalizeText(homeFilter.value);

        let visibleCount = 0;

        productRows.forEach(function (row) {

            const productName =
                normalizeText(row.dataset.name);

            const productCategory =
                normalizeText(row.dataset.category);

            const productStatus =
                normalizeText(row.dataset.status);

            const productHome =
                normalizeText(row.dataset.home);

            const matchesSearch =
                searchValue === "" ||
                productName.includes(searchValue) ||
                productCategory.includes(searchValue);

            const matchesCategory =
                categoryValue === "" ||
                productCategory === categoryValue;

            const matchesStatus =
                statusValue === "" ||
                productStatus === statusValue;

            const matchesHome =
                homeValue === "" ||
                productHome === homeValue;

            const shouldShow =
                matchesSearch &&
                matchesCategory &&
                matchesStatus &&
                matchesHome;

            row.style.display =
                shouldShow ? "" : "none";

            if (shouldShow) {
                visibleCount++;
            }
        });

        resultsCount.textContent =
            visibleCount;

        noResultsRow.style.display =
            productRows.length > 0 && visibleCount === 0
                ? ""
                : "none";

        updateSelectAllState();
    }

    /**
     * إعادة الفلاتر للوضع الافتراضي.
     */
    function resetFilters() {

        searchInput.value = "";
        categoryFilter.value = "";
        statusFilter.value = "";
        homeFilter.value = "";

        filterProducts();
        searchInput.focus();
    }

    /**
     * إظهار الحقل الإضافي المناسب حسب الإجراء.
     */
    function updateBulkExtraFields() {

        categoryGroup.style.display =
            "none";

        discountGroup.style.display =
            "none";

        categoryInput.required =
            false;

        discountInput.required =
            false;

        if (bulkAction.value === "change_category") {
            categoryGroup.style.display =
                "flex";

            categoryInput.required =
                true;
        }

        if (bulkAction.value === "set_discount") {
            discountGroup.style.display =
                "flex";

            discountInput.required =
                true;
        }
    }

    // =========================
    // أحداث البحث والفلاتر
    // =========================

    searchInput.addEventListener(
        "input",
        filterProducts
    );

    categoryFilter.addEventListener(
        "change",
        filterProducts
    );

    statusFilter.addEventListener(
        "change",
        filterProducts
    );

    homeFilter.addEventListener(
        "change",
        filterProducts
    );

    resetButton.addEventListener(
        "click",
        resetFilters
    );

    // =========================
    // تحديد الكل
    // =========================

    selectAllCheckbox.addEventListener(
        "change",
        function () {

            const visibleCheckboxes =
                getVisibleCheckboxes();

            visibleCheckboxes.forEach(
                function (checkbox) {
                    checkbox.checked =
                        selectAllCheckbox.checked;
                }
            );

            updateSelectedCount();
        }
    );

    // =========================
    // تحديد منتج منفرد
    // =========================

    productCheckboxes.forEach(
        function (checkbox) {

            checkbox.addEventListener(
                "change",
                updateSelectedCount
            );
        }
    );

    // =========================
    // تغيير الإجراء الجماعي
    // =========================

    bulkAction.addEventListener(
        "change",
        updateBulkExtraFields
    );

    // =========================
    // التحقق قبل إرسال النموذج
    // =========================

    bulkForm.addEventListener(
        "submit",
        function (event) {

            const selectedProducts =
                productCheckboxes.filter(
                    function (checkbox) {
                        return checkbox.checked;
                    }
                );

            if (!selectedProducts.length) {
                event.preventDefault();

                alert(
                    "يرجى تحديد منتج واحد على الأقل."
                );

                return;
            }

            if (!bulkAction.value) {
                event.preventDefault();

                alert(
                    "يرجى اختيار الإجراء الجماعي."
                );

                return;
            }

            if (bulkAction.value === "delete") {

                const confirmed = confirm(
                    "هل أنت متأكد من حذف المنتجات المحددة نهائيًا؟"
                );

                if (!confirmed) {
                    event.preventDefault();
                }
            }
        }
    );

    // =========================
    // تشغيل أولي
    // =========================

    updateBulkExtraFields();
    filterProducts();
    updateSelectedCount();
});
