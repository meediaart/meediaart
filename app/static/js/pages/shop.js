"use strict";

/* ==================================================
   MediaArt Shop
   الملف:
   app/static/js/pages/shop.js

   الوظائف:
   - مشاركة المنتجات.
   - البحث في المنتجات.
   - فلترة التصنيف والسعر.
   - ترتيب المنتجات.
   - فلاتر الجوال.
   - أزرار شريط التصنيفات.
   - السحب بالماوس.
   - إخفاء أدوات المتجر عند النزول.
================================================== */


/* ==================================================
   01 — نافذة مشاركة المنتج
================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const shareModal =
        document.getElementById("productShareModal");

    const shareMessage =
        document.getElementById("productShareMessage");

    if (!shareModal) {
        return;
    }

    let currentShareData = {
        title: "",
        text: "",
        url: ""
    };

    function updateShareLinks() {

        const encodedUrl =
            encodeURIComponent(currentShareData.url);

        const completeText = [
            currentShareData.text,
            currentShareData.title,
            currentShareData.url
        ]
            .filter(Boolean)
            .join("\n");

        const encodedText =
            encodeURIComponent(completeText);

        const encodedTitle =
            encodeURIComponent(currentShareData.title);

        const whatsappLink =
            shareModal.querySelector(
                '[data-share-service="whatsapp"]'
            );

        const telegramLink =
            shareModal.querySelector(
                '[data-share-service="telegram"]'
            );

        const facebookLink =
            shareModal.querySelector(
                '[data-share-service="facebook"]'
            );

        const xLink =
            shareModal.querySelector(
                '[data-share-service="x"]'
            );

        const emailLink =
            shareModal.querySelector(
                '[data-share-service="email"]'
            );

        if (whatsappLink) {
            whatsappLink.href =
                "https://wa.me/?text=" + encodedText;
        }

        if (telegramLink) {
            telegramLink.href =
                "https://t.me/share/url?url=" +
                encodedUrl +
                "&text=" +
                encodeURIComponent(
                    currentShareData.text ||
                    currentShareData.title
                );
        }

        if (facebookLink) {
            facebookLink.href =
                "https://www.facebook.com/sharer/sharer.php?u=" +
                encodedUrl;
        }

        if (xLink) {
            xLink.href =
                "https://twitter.com/intent/tweet?text=" +
                encodeURIComponent(
                    currentShareData.text ||
                    currentShareData.title
                ) +
                "&url=" +
                encodedUrl;
        }

        if (emailLink) {
            emailLink.href =
                "mailto:?subject=" +
                encodedTitle +
                "&body=" +
                encodedText;
        }
    }

    function openShareModal(button) {

        currentShareData = {
            title:
                button.dataset.title ||
                document.title,

            text:
                button.dataset.shareText ||
                "",

            url:
                button.dataset.url ||
                window.location.href
        };

        updateShareLinks();

        if (shareMessage) {
            shareMessage.textContent = "";
        }

        shareModal.hidden = false;

        document.body.style.overflow =
            "hidden";
    }

    function closeShareModal() {

        shareModal.hidden = true;

        document.body.style.overflow =
            "";
    }

    document
        .querySelectorAll(".js-share-product")
        .forEach(function (button) {

            button.addEventListener(
                "click",
                function (event) {

                    event.preventDefault();
                    event.stopPropagation();

                    openShareModal(button);
                }
            );
        });

    shareModal
        .querySelectorAll(
            "[data-close-share-modal]"
        )
        .forEach(function (button) {

            button.addEventListener(
                "click",
                closeShareModal
            );
        });

    const copyButton =
        shareModal.querySelector(
            '[data-share-service="copy"]'
        );

    if (copyButton) {

        copyButton.addEventListener(
            "click",
            async function () {

                try {

                    await navigator.clipboard.writeText(
                        currentShareData.url
                    );

                    if (shareMessage) {
                        shareMessage.textContent =
                            "تم نسخ رابط المنتج";
                    }

                } catch (error) {

                    console.error(
                        "Copy link error:",
                        error
                    );

                    if (shareMessage) {
                        shareMessage.textContent =
                            "تعذر نسخ الرابط";
                    }
                }
            }
        );
    }

    const deviceShareButton =
        shareModal.querySelector(
            '[data-share-service="device"]'
        );

    if (deviceShareButton) {

        deviceShareButton.addEventListener(
            "click",
            async function () {

                if (!navigator.share) {

                    if (shareMessage) {
                        shareMessage.textContent =
                            "مشاركة الجهاز غير مدعومة في هذا المتصفح";
                    }

                    return;
                }

                try {

                    await navigator.share({
                        title:
                            currentShareData.title,

                        text:
                            currentShareData.text,

                        url:
                            currentShareData.url
                    });

                    closeShareModal();

                } catch (error) {

                    if (
                        error.name !==
                        "AbortError"
                    ) {
                        console.error(
                            "Native share error:",
                            error
                        );
                    }
                }
            }
        );
    }

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape" &&
                !shareModal.hidden
            ) {
                closeShareModal();
            }
        }
    );
});


/* ==================================================
   02 — البحث والفلاتر والترتيب
================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const productsGrid =
        document.getElementById(
            "shopProductsGrid"
        );

    if (!productsGrid) {
        return;
    }

    const categoryFilter =
        document.getElementById(
            "shopCategoryFilter"
        );

    const minPriceInput =
        document.getElementById(
            "shopMinPrice"
        );

    const maxPriceInput =
        document.getElementById(
            "shopMaxPrice"
        );

    const sortSelect =
        document.getElementById(
            "shopSortSelect"
        );

    const resetButton =
        document.getElementById(
            "resetShopFilters"
        );

    const resetMobileButton =
        document.getElementById(
            "resetShopFiltersMobile"
        );

    const resultsCount =
        document.getElementById(
            "shopResultsCount"
        );

    const noResults =
        document.getElementById(
            "shopNoResults"
        );

    /*
     البحث قد يوجد في الهيدر الأساسي
     أو داخل صفحة المتجر.
    */
    const searchInputs = Array.from(
        document.querySelectorAll(
            [
                "#shopProductSearch",
                "#shopCompactSearchInput",
                "[data-shop-search-input]"
            ].join(",")
        )
    );

    const productItems = Array.from(
        productsGrid.querySelectorAll(
            ".shop-product-item"
        )
    );

    let currentSearchValue = "";

    function normalizeText(value) {

        return String(value || "")
            .toLowerCase()
            .trim();
    }

    function getSearchValue() {

        const activeSearchInput =
            searchInputs.find(function (input) {

                return (
                    document.activeElement ===
                    input
                );
            });

        if (activeSearchInput) {
            return normalizeText(
                activeSearchInput.value
            );
        }

        const filledInput =
            searchInputs.find(function (input) {

                return (
                    normalizeText(input.value) !==
                    ""
                );
            });

        if (filledInput) {
            return normalizeText(
                filledInput.value
            );
        }

        return normalizeText(
            currentSearchValue
        );
    }

    function syncSearchInputs(
        sourceInput
    ) {

        currentSearchValue =
            sourceInput.value || "";

        searchInputs.forEach(
            function (input) {

                if (input !== sourceInput) {
                    input.value =
                        sourceInput.value;
                }
            }
        );
    }

    function sortProducts() {

        const sortValue =
            sortSelect
                ? sortSelect.value
                : "";

        const sortedItems =
            [...productItems];

        if (sortValue === "price-asc") {

            sortedItems.sort(
                function (
                    firstItem,
                    secondItem
                ) {

                    return (
                        Number(
                            firstItem.dataset
                                .price || 0
                        ) -
                        Number(
                            secondItem.dataset
                                .price || 0
                        )
                    );
                }
            );

        } else if (
            sortValue === "price-desc"
        ) {

            sortedItems.sort(
                function (
                    firstItem,
                    secondItem
                ) {

                    return (
                        Number(
                            secondItem.dataset
                                .price || 0
                        ) -
                        Number(
                            firstItem.dataset
                                .price || 0
                        )
                    );
                }
            );

        } else if (
            sortValue === "name-asc"
        ) {

            sortedItems.sort(
                function (
                    firstItem,
                    secondItem
                ) {

                    return normalizeText(
                        firstItem.dataset.title
                    ).localeCompare(
                        normalizeText(
                            secondItem.dataset
                                .title
                        )
                    );
                }
            );

        } else if (
            sortValue === "name-desc"
        ) {

            sortedItems.sort(
                function (
                    firstItem,
                    secondItem
                ) {

                    return normalizeText(
                        secondItem.dataset.title
                    ).localeCompare(
                        normalizeText(
                            firstItem.dataset
                                .title
                        )
                    );
                }
            );

        } else {

            sortedItems.sort(
                function (
                    firstItem,
                    secondItem
                ) {

                    return (
                        Number(
                            firstItem.dataset
                                .originalOrder || 0
                        ) -
                        Number(
                            secondItem.dataset
                                .originalOrder || 0
                        )
                    );
                }
            );
        }

        sortedItems.forEach(
            function (item) {

                productsGrid.appendChild(
                    item
                );
            }
        );

        if (noResults) {
            productsGrid.appendChild(
                noResults
            );
        }
    }

    function refreshMasonry() {

        if (
            typeof window
                .layoutProductMasonry ===
            "function"
        ) {

            window.requestAnimationFrame(
                function () {

                    window
                        .layoutProductMasonry();
                }
            );
        }
    }

    function filterProducts() {

        const searchValue =
            getSearchValue();

        const categoryValue =
            categoryFilter
                ? String(
                    categoryFilter.value ||
                    ""
                )
                : "";

        const minimumPrice =
            minPriceInput &&
            minPriceInput.value !== ""
                ? Number(
                    minPriceInput.value
                )
                : null;

        const maximumPrice =
            maxPriceInput &&
            maxPriceInput.value !== ""
                ? Number(
                    maxPriceInput.value
                )
                : null;

        let visibleCount = 0;

        productItems.forEach(
            function (item) {

                const title =
                    normalizeText(
                        item.dataset.title
                    );

                const description =
                    normalizeText(
                        item.dataset.description
                    );

                const category =
                    String(
                        item.dataset.category ||
                        ""
                    );

                const price =
                    Number(
                        item.dataset.price ||
                        0
                    );

                const matchesSearch =
                    searchValue === "" ||
                    title.includes(
                        searchValue
                    ) ||
                    description.includes(
                        searchValue
                    );

                const matchesCategory =
                    categoryValue === "" ||
                    category ===
                        categoryValue;

                const matchesMinimumPrice =
                    minimumPrice === null ||
                    Number.isNaN(
                        minimumPrice
                    ) ||
                    price >=
                        minimumPrice;

                const matchesMaximumPrice =
                    maximumPrice === null ||
                    Number.isNaN(
                        maximumPrice
                    ) ||
                    price <=
                        maximumPrice;

                const shouldShow =
                    matchesSearch &&
                    matchesCategory &&
                    matchesMinimumPrice &&
                    matchesMaximumPrice;

                item.hidden =
                    !shouldShow;

                if (shouldShow) {
                    visibleCount += 1;
                }
            }
        );

        sortProducts();

        if (resultsCount) {
            resultsCount.textContent =
                visibleCount;
        }

        if (noResults) {

            noResults.hidden =
                !(
                    productItems.length > 0 &&
                    visibleCount === 0
                );
        }

        refreshMasonry();
    }

    function resetFilters() {

        currentSearchValue = "";

        searchInputs.forEach(
            function (input) {

                input.value = "";
            }
        );

        if (categoryFilter) {
            categoryFilter.value = "";
        }

        if (minPriceInput) {
            minPriceInput.value = "";
        }

        if (maxPriceInput) {
            maxPriceInput.value = "";
        }

        if (sortSelect) {
            sortSelect.value = "";
        }

        document
            .querySelectorAll(
                "[data-mobile-sort]"
            )
            .forEach(
                function (button) {

                    button.classList.toggle(
                        "active",
                        button.dataset
                            .mobileSort === ""
                    );
                }
            );


        filterProducts();
    }

    searchInputs.forEach(
        function (input) {

            input.addEventListener(
                "input",
                function () {

                    syncSearchInputs(input);

                    filterProducts();
                }
            );
        }
    );

    if (categoryFilter) {

        categoryFilter.addEventListener(
            "change",
            filterProducts
        );
    }

    if (minPriceInput) {

        minPriceInput.addEventListener(
            "input",
            filterProducts
        );
    }

    if (maxPriceInput) {

        maxPriceInput.addEventListener(
            "input",
            filterProducts
        );
    }

    if (sortSelect) {

        sortSelect.addEventListener(
            "change",
            filterProducts
        );
    }

    if (resetButton) {

        resetButton.addEventListener(
            "click",
            resetFilters
        );
    }

    if (resetMobileButton) {

        resetMobileButton.addEventListener(
            "click",
            resetFilters
        );
    }

    /*
     أزرار الترتيب السريع في الجوال.
    */
    document
        .querySelectorAll(
            "[data-mobile-sort]"
        )
        .forEach(function (button) {

            button.addEventListener(
                "click",
                function () {

                    const sortValue =
                        button.dataset
                            .mobileSort || "";

                    if (sortSelect) {
                        sortSelect.value =
                            sortValue;
                    }

                    document
                        .querySelectorAll(
                            "[data-mobile-sort]"
                        )
                        .forEach(
                            function (
                                otherButton
                            ) {

                                otherButton
                                    .classList
                                    .toggle(
                                        "active",
                                        otherButton ===
                                            button
                                    );
                            }
                        );

                    filterProducts();
                }
            );
        });

    /*
     زر السعر في الجوال:
     ضغطة أولى تصاعدي،
     ضغطة ثانية تنازلي.
    */
    const mobilePriceButton =
        document.getElementById(
            "shopMobilePriceSort"
        );

    if (mobilePriceButton) {

        mobilePriceButton.addEventListener(
            "click",
            function () {

                const currentSort =
                    mobilePriceButton.dataset
                        .currentPriceSort ||
                    "";

                const nextSort =
                    currentSort ===
                    "price-asc"
                        ? "price-desc"
                        : "price-asc";

                mobilePriceButton.dataset
                    .currentPriceSort =
                    nextSort;

                if (sortSelect) {
                    sortSelect.value =
                        nextSort;
                }

                document
                    .querySelectorAll(
                        ".shop-mobile-toolbar-btn"
                    )
                    .forEach(
                        function (button) {

                            button.classList
                                .remove(
                                    "active"
                                );
                        }
                    );

                mobilePriceButton.classList
                    .add("active");

                filterProducts();
            }
        );
    }

    /*
     إتاحة الدوال لبقية وحدات الصفحة.
    */
    window.shopFilterProducts =
        filterProducts;

    window.shopResetFilters =
        resetFilters;

    filterProducts();
});


/* ==================================================
   03 — فتح وإغلاق فلاتر الجوال
================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const sheet =
        document.getElementById(
            "shopMobileFiltersSheet"
        );

    const backdrop =
        document.getElementById(
            "shopMobileFiltersBackdrop"
        );

    const openButton =
        document.getElementById(
            "openShopMobileFilters"
        );

    const categoryButton =
        document.getElementById(
            "openShopCategoryFilter"
        );

    const priceButton =
        document.getElementById(
            "openShopPriceFilter"
        );

    const closeButton =
        document.getElementById(
            "closeShopMobileFilters"
        );

    const applyButton =
        document.getElementById(
            "applyShopMobileFilters"
        );

    if (!sheet || !backdrop) {
        return;
    }

    function openFilters(
        focusElement
    ) {

        backdrop.hidden = false;

        sheet.classList.add(
            "open"
        );

        sheet.setAttribute(
            "aria-hidden",
            "false"
        );

        document.body.style.overflow =
            "hidden";

        if (focusElement) {

            window.setTimeout(
                function () {

                    focusElement.focus();
                },
                280
            );
        }
    }

    function closeFilters() {

        sheet.classList.remove(
            "open"
        );

        sheet.setAttribute(
            "aria-hidden",
            "true"
        );

        backdrop.hidden = true;

        document.body.style.overflow =
            "";
    }

    if (openButton) {

        openButton.addEventListener(
            "click",
            function () {

                openFilters();
            }
        );
    }

    if (categoryButton) {

        categoryButton.addEventListener(
            "click",
            function () {

                openFilters(
                    document.getElementById(
                        "shopCategoryFilter"
                    )
                );
            }
        );
    }

    if (priceButton) {

        priceButton.addEventListener(
            "click",
            function () {

                openFilters(
                    document.getElementById(
                        "shopMinPrice"
                    )
                );
            }
        );
    }

    if (closeButton) {

        closeButton.addEventListener(
            "click",
            closeFilters
        );
    }

    if (applyButton) {

        applyButton.addEventListener(
            "click",
            function () {

                if (
                    typeof window
                        .shopFilterProducts ===
                    "function"
                ) {
                    window
                        .shopFilterProducts();
                }

                closeFilters();
            }
        );
    }

    /*
 منع الضغط داخل لوحة الفلاتر من الوصول
 إلى الخلفية وإغلاق اللوحة.
*/
sheet.addEventListener(
    "click",
    function (event) {
        event.stopPropagation();
    }
);ے

    backdrop.addEventListener(
        "click",
        closeFilters
    );

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key === "Escape" &&
                sheet.classList.contains(
                    "open"
                )
            ) {
                closeFilters();
            }
        }
    );
});

/* ==================================================
   04 — تشغيل شريط التصنيفات
================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const scroller =
        document.getElementById("shopCategoryScroller");

    if (!scroller) {
        return;
    }

    const scrollButtons =
        document.querySelectorAll(
            "[data-category-scroll]"
        );

    scrollButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            event.preventDefault();
            event.stopPropagation();

            const direction =
                button.dataset.categoryScroll;

            const amount =
                Math.max(
                    scroller.clientWidth * 0.65,
                    260
                );

            const isRtl =
                document.documentElement.dir === "rtl";

            let movement =
                direction === "end"
                    ? amount
                    : -amount;

            if (isRtl) {
                movement *= -1;
            }

            scroller.scrollBy({
                left: movement,
                behavior: "smooth"
            });
        });
    });

    /*
     لا نعترض الضغط على روابط التصنيفات.
     السحب بالإصبع يعمل تلقائيًا على الجوال.
    */
});

/* ==================================================
   05 — إخفاء أدوات المتجر عند النزول
   وإظهارها فور السحب للأعلى
================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const slidingControls =
        document.getElementById("shopSlidingControls");

    const mobileFiltersSheet =
        document.getElementById("shopMobileFiltersSheet");

    if (!slidingControls) {
        return;
    }

    let lastScrollY =
        Math.max(window.scrollY, 0);

    let downwardDistance = 0;
    let touchStartY = null;

    const hideThreshold = 35;

    function filtersAreOpen() {

        return (
            mobileFiltersSheet &&
            mobileFiltersSheet.classList.contains("open")
        );
    }

    function showControls() {

        slidingControls.classList.remove(
            "controls-hidden"
        );

        downwardDistance = 0;
    }

    function hideControls() {

        if (filtersAreOpen()) {
            return;
        }

        slidingControls.style.setProperty(
            "--shop-controls-height",
            slidingControls.scrollHeight + "px"
        );

        slidingControls.classList.add(
            "controls-hidden"
        );
    }

    function handleScroll() {

        const currentScrollY =
            Math.max(window.scrollY, 0);

        const movement =
            currentScrollY - lastScrollY;

        /*
         عند فتح نافذة الفلاتر لا نخفي الأدوات.
        */
        if (filtersAreOpen()) {

            showControls();
            lastScrollY = currentScrollY;

            return;
        }

        /*
         في بداية الصفحة تظهر دائمًا.
        */
        if (currentScrollY <= 80) {

            showControls();
            lastScrollY = currentScrollY;

            return;
        }

        /*
         أي حركة إلى الأعلى تُظهر الأدوات فورًا.
        */
        if (movement < -1) {

            showControls();
            lastScrollY = currentScrollY;

            return;
        }

        /*
         عند النزول نجمع المسافة قبل الإخفاء.
        */
        if (movement > 0) {

            downwardDistance += movement;

            if (downwardDistance >= hideThreshold) {

                hideControls();
                downwardDistance = 0;
            }
        }

        lastScrollY = currentScrollY;
    }

    /*
     دعم إضافي لسحب Safari في الآيفون.
    */
    document.addEventListener(
        "touchstart",
        function (event) {

            if (!event.touches.length) {
                return;
            }

            touchStartY =
                event.touches[0].clientY;
        },
        {
            passive: true
        }
    );

    document.addEventListener(
        "touchmove",
        function (event) {

            if (
                touchStartY === null ||
                !event.touches.length
            ) {
                return;
            }

            const currentTouchY =
                event.touches[0].clientY;

            const touchMovement =
                currentTouchY - touchStartY;

            /*
             تحريك الإصبع للأسفل يعني أن الصفحة تصعد.
            */
            if (touchMovement > 4) {
                showControls();
            }

            touchStartY = currentTouchY;
        },
        {
            passive: true
        }
    );

    document.addEventListener(
        "touchend",
        function () {
            touchStartY = null;
        },
        {
            passive: true
        }
    );

    window.addEventListener(
        "scroll",
        handleScroll,
        {
            passive: true
        }
    );

    window.addEventListener(
        "resize",
        function () {

            showControls();

            window.requestAnimationFrame(
                function () {

                    slidingControls.style.setProperty(
                        "--shop-controls-height",
                        slidingControls.scrollHeight + "px"
                    );
                }
            );
        }
    );

    /*
     إزالة أي خصائص قديمة وضعتها النسخ السابقة.
    */
    slidingControls.style.removeProperty("transform");
    slidingControls.style.removeProperty("opacity");
    slidingControls.style.removeProperty("pointer-events");
    slidingControls.style.removeProperty("transition");
    slidingControls.style.removeProperty("will-change");

    showControls();
});
/* ==================================================
   06 — زر العودة إلى بداية الصفحة
================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const backToTopButton =
        document.getElementById("shopBackToTop");

    if (!backToTopButton) {
        return;
    }

    function updateBackToTopButton() {

        const shouldShow =
            window.scrollY > 350;

        backToTopButton.hidden = false;

        backToTopButton.classList.toggle(
            "visible",
            shouldShow
        );

        backToTopButton.setAttribute(
            "aria-hidden",
            shouldShow ? "false" : "true"
        );

        backToTopButton.tabIndex =
            shouldShow ? 0 : -1;
    }

    backToTopButton.addEventListener(
        "click",
        function () {

            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        }
    );

    window.addEventListener(
        "scroll",
        updateBackToTopButton,
        {
            passive: true
        }
    );

    updateBackToTopButton();
});