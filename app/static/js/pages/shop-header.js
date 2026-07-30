/* ==========================================================
   SHOP HEADER CONTROLS

   الملف:
   app/static/js/pages/shop-header.js

   الوظيفة:
   - بحث صغير منسدل على الكمبيوتر.
   - بحث يظهر مكان الشعار على الجوال.
   - البحث الفوري داخل المنتجات.
   - قوائم المشاركة واللغة والقائمة الرئيسية.
========================================================== */

(function () {
    "use strict";


    /* ==================================================
       عناصر الهيدر
    ================================================== */

    const searchButton = document.querySelector(
        "[data-shop-search-button]"
    );

    const desktopSearch = document.querySelector(
        "[data-shop-desktop-search]"
    );

    const mobileSearch = document.querySelector(
        "[data-shop-mobile-search]"
    );

    const headerBrand = document.querySelector(
        "[data-shop-header-brand]"
    );

    const searchInputs = document.querySelectorAll(
        "[data-shop-search-input]"
    );

    const searchClearButtons = document.querySelectorAll(
        "[data-shop-search-clear]"
    );


    /* ==================================================
       معرفة هل الشاشة جوال
    ================================================== */

    function isMobileScreen() {
        return window.matchMedia(
            "(max-width: 760px)"
        ).matches;
    }


    /* ==================================================
       إغلاق القوائم المنسدلة

       يستثني البحث لأنه أصبح بنظام مستقل.
    ================================================== */

    function closeShopHeaderDropdowns(exceptName = null) {
        const dropdowns = document.querySelectorAll(
            "[data-shop-dropdown]"
        );

        const buttons = document.querySelectorAll(
            "[data-shop-dropdown-button]"
        );

        dropdowns.forEach(function (dropdown) {
            const name = dropdown.getAttribute(
                "data-shop-dropdown"
            );

            if (name !== exceptName) {
                dropdown.hidden = true;
                dropdown.classList.remove("is-open");
            }
        });

        buttons.forEach(function (button) {
            const name = button.getAttribute(
                "data-shop-dropdown-button"
            );

            const isOpen = name === exceptName;

            button.classList.toggle(
                "active",
                isOpen
            );

            button.setAttribute(
                "aria-expanded",
                isOpen ? "true" : "false"
            );
        });
    }


    /* ==================================================
       فتح البحث

       الكمبيوتر:
       يظهر تحت الأيقونة.

       الجوال:
       يخفي الشعار ويظهر مكانه.
    ================================================== */

    function openShopSearch() {
        closeShopHeaderDropdowns();

        if (isMobileScreen()) {
            if (headerBrand) {
                headerBrand.hidden = true;
            }

            if (mobileSearch) {
                mobileSearch.hidden = false;
            }
        } else {
            if (desktopSearch) {
                desktopSearch.hidden = false;
            }
        }

        if (searchButton) {
            searchButton.classList.add("active");

            searchButton.setAttribute(
                "aria-expanded",
                "true"
            );
        }

        window.requestAnimationFrame(function () {
            const visibleInput = Array.from(
                searchInputs
            ).find(function (input) {
                return input.offsetParent !== null;
            });

            if (visibleInput) {
                visibleInput.focus();
            }
        });
    }


    /* ==================================================
       إغلاق البحث
    ================================================== */

    function closeShopSearch() {
        if (desktopSearch) {
            desktopSearch.hidden = true;
        }

        if (mobileSearch) {
            mobileSearch.hidden = true;
        }

        if (headerBrand) {
            headerBrand.hidden = false;
        }

        if (searchButton) {
            searchButton.classList.remove("active");

            searchButton.setAttribute(
                "aria-expanded",
                "false"
            );
        }
    }


    /* ==================================================
       التأكد هل البحث مفتوح
    ================================================== */

    function isShopSearchOpen() {
        const desktopOpen =
            desktopSearch &&
            !desktopSearch.hidden;

        const mobileOpen =
            mobileSearch &&
            !mobileSearch.hidden;

        return Boolean(
            desktopOpen || mobileOpen
        );
    }


    /* ==================================================
       مزامنة حقلي الكمبيوتر والجوال

       عند الكتابة في أحدهما،
       يتم وضع القيمة نفسها في الآخر.
    ================================================== */

    function syncSearchInputs(value, currentInput) {
        searchInputs.forEach(function (input) {
            if (input !== currentInput) {
                input.value = value;
            }
        });
    }


    /* ==================================================
       البحث داخل بطاقات المنتجات

       يعمل اعتمادًا على النص الموجود داخل البطاقة:
       - اسم المنتج.
       - الوصف.
       - السعر.
       - أي نص آخر داخل البطاقة.
    ================================================== */

    function filterShopProducts(searchValue) {
        const normalizedSearch = searchValue
            .trim()
            .toLocaleLowerCase();

        const productCards = document.querySelectorAll(
            ".product-card"
        );

        let visibleProducts = 0;

        productCards.forEach(function (card) {
            const productText = card.textContent
                .replace(/\s+/g, " ")
                .trim()
                .toLocaleLowerCase();

            const matchesSearch =
                normalizedSearch === "" ||
                productText.includes(normalizedSearch);

            /*
             * نستخدم class بدل تعديل CSS الأصلي للبطاقة.
             */
            card.classList.toggle(
                "shop-search-hidden",
                !matchesSearch
            );

            if (matchesSearch) {
                visibleProducts += 1;
            }
        });

        updateShopSearchResults(
            visibleProducts,
            productCards.length
        );
    }


    /* ==================================================
       تحديث عداد النتائج والرسالة

       تعمل فقط إذا كانت العناصر موجودة في الصفحة.
    ================================================== */

    function updateShopSearchResults(
        visibleProducts,
        totalProducts
    ) {
        const resultCounters =
            document.querySelectorAll(
                "[data-shop-results-count]"
            );

        resultCounters.forEach(function (counter) {
            counter.textContent = visibleProducts;
        });

        const noResults = document.querySelector(
            "[data-shop-no-results]"
        );

        if (noResults) {
            noResults.hidden =
                visibleProducts !== 0 ||
                totalProducts === 0;
        }
    }


    /* ==================================================
       فتح وإغلاق قوائم الهيدر الأخرى
    ================================================== */

    function toggleShopHeaderDropdown(button) {
        const dropdownName = button.getAttribute(
            "data-shop-dropdown-button"
        );

        if (!dropdownName) {
            return;
        }

        const dropdown = document.querySelector(
            `[data-shop-dropdown="${dropdownName}"]`
        );

        if (!dropdown) {
            return;
        }

        closeShopSearch();

        const shouldOpen = dropdown.hidden;

        closeShopHeaderDropdowns(
            shouldOpen ? dropdownName : null
        );

        dropdown.hidden = !shouldOpen;

        dropdown.classList.toggle(
            "is-open",
            shouldOpen
        );

        button.classList.toggle(
            "active",
            shouldOpen
        );

        button.setAttribute(
            "aria-expanded",
            shouldOpen ? "true" : "false"
        );
    }


    /* ==================================================
       روابط المشاركة
    ================================================== */

    function setupShopHeaderShare() {
        const pageUrl = window.location.href;
        const pageTitle = document.title;

        const encodedUrl =
            encodeURIComponent(pageUrl);

        const encodedTitle =
            encodeURIComponent(pageTitle);

        const shareLinks = {
            whatsapp:
                "https://wa.me/?text=" +
                encodeURIComponent(
                    pageTitle + "\n" + pageUrl
                ),

            telegram:
                "https://t.me/share/url?url=" +
                encodedUrl +
                "&text=" +
                encodedTitle,

            facebook:
                "https://www.facebook.com/sharer/sharer.php?u=" +
                encodedUrl,

            x:
                "https://twitter.com/intent/tweet?text=" +
                encodedTitle +
                "&url=" +
                encodedUrl
        };

        Object.entries(shareLinks).forEach(
            function ([service, url]) {
                const link = document.querySelector(
                    `[data-header-share="${service}"]`
                );

                if (link) {
                    link.href = url;
                }
            }
        );
    }


    /* ==================================================
       نسخ رابط الصفحة
    ================================================== */

    async function copyShopPageLink(button) {
        const originalContent = button.innerHTML;

        try {
            await navigator.clipboard.writeText(
                window.location.href
            );
        } catch (error) {
            const temporaryInput =
                document.createElement("input");

            temporaryInput.value =
                window.location.href;

            document.body.appendChild(
                temporaryInput
            );

            temporaryInput.select();
            document.execCommand("copy");
            temporaryInput.remove();
        }

        button.innerHTML =
            '<i class="fa-solid fa-check"></i> تم نسخ الرابط';

        window.setTimeout(function () {
            button.innerHTML = originalContent;
        }, 1400);
    }


    /* ==================================================
       مشاركة الجهاز
    ================================================== */

    async function openNativeShare() {
        if (!navigator.share) {
            return;
        }

        try {
            await navigator.share({
                title: document.title,
                url: window.location.href
            });
        } catch (error) {
            if (error.name !== "AbortError") {
                console.error(error);
            }
        }
    }


    /* ==================================================
       أحداث البحث
    ================================================== */

    if (searchButton) {
        searchButton.addEventListener(
            "click",
            function (event) {
                event.preventDefault();
                event.stopPropagation();

                if (isShopSearchOpen()) {
                    closeShopSearch();
                } else {
                    openShopSearch();
                }
            }
        );
    }


    searchInputs.forEach(function (input) {
        input.addEventListener(
            "input",
            function () {
                const value = input.value;

                syncSearchInputs(
                    value,
                    input
                );

                filterShopProducts(value);
            }
        );
    });


    searchClearButtons.forEach(function (button) {
        button.addEventListener(
            "click",
            function (event) {
                event.preventDefault();
                event.stopPropagation();

                searchInputs.forEach(
                    function (input) {
                        input.value = "";
                    }
                );

                filterShopProducts("");
                closeShopSearch();
            }
        );
    });


    /* ==================================================
       أحداث الهيدر العامة
    ================================================== */

    document.addEventListener(
        "click",
        function (event) {
            const dropdownButton =
                event.target.closest(
                    "[data-shop-dropdown-button]"
                );

            if (dropdownButton) {
                event.preventDefault();
                event.stopPropagation();

                toggleShopHeaderDropdown(
                    dropdownButton
                );

                return;
            }

            const copyButton =
                event.target.closest(
                    '[data-header-share="copy"]'
                );

            if (copyButton) {
                event.preventDefault();
                event.stopPropagation();

                copyShopPageLink(copyButton);

                return;
            }

            const deviceShareButton =
                event.target.closest(
                    '[data-header-share="device"]'
                );

            if (deviceShareButton) {
                event.preventDefault();
                event.stopPropagation();

                openNativeShare();

                return;
            }

            const insideDropdown =
                event.target.closest(
                    "[data-shop-dropdown]"
                );

            const insideDesktopSearch =
                event.target.closest(
                    "[data-shop-desktop-search]"
                );

            const insideMobileSearch =
                event.target.closest(
                    "[data-shop-mobile-search]"
                );

            if (
                !insideDropdown &&
                !insideDesktopSearch &&
                !insideMobileSearch
            ) {
                closeShopHeaderDropdowns();
                closeShopSearch();
            }
        }
    );


    /* ==================================================
       زر Escape
    ================================================== */

    document.addEventListener(
        "keydown",
        function (event) {
            if (event.key === "Escape") {
                closeShopHeaderDropdowns();
                closeShopSearch();
            }
        }
    );


    /* ==================================================
       تغيير حجم الشاشة

       يمنع بقاء حالة الكمبيوتر مفتوحة عند الانتقال للجوال
       أو العكس.
    ================================================== */

    window.addEventListener(
        "resize",
        function () {
            closeShopSearch();
        }
    );


    /* ==================================================
       التشغيل
    ================================================== */

    if (document.readyState === "loading") {
        document.addEventListener(
            "DOMContentLoaded",
            setupShopHeaderShare
        );
    } else {
        setupShopHeaderShare();
    }

})();

/* ==========================================================
   GLOBAL HEADER SEARCH

   الوظيفة:
   - من خارج المتجر:
     الضغط على Enter ينقل الزائر إلى المتجر.

   - داخل المتجر:
     يترك البحث الفوري الحالي يعمل.

   - عند الوصول إلى المتجر من صفحة أخرى:
     يستعيد كلمة البحث من الرابط ويطبقها تلقائيًا.
========================================================== */

document.addEventListener("DOMContentLoaded", function () {
    "use strict";

    const siteHeader = document.getElementById("siteHeader");

    if (!siteHeader) {
        return;
    }

    const isShopPage =
        siteHeader.dataset.isShopPage === "true";

    const shopUrl =
        siteHeader.dataset.shopUrl || "/shop";

    const searchInputs = document.querySelectorAll(
        "[data-shop-search-input]"
    );


    /* ==================================================
       الانتقال إلى المتجر عند البحث من أي صفحة أخرى
    ================================================== */

    searchInputs.forEach(function (input) {
        input.addEventListener("keydown", function (event) {
            if (event.key !== "Enter") {
                return;
            }

            const searchValue = input.value.trim();

            if (!searchValue) {
                return;
            }

            event.preventDefault();

            /*
             * داخل المتجر:
             * يبقى البحث الفوري الحالي هو المسؤول.
             */
            if (isShopPage) {
                input.dispatchEvent(
                    new Event("input", {
                        bubbles: true
                    })
                );

                return;
            }

            /*
             * خارج المتجر:
             * ننتقل للمتجر ونضع عبارة البحث في الرابط.
             */
            const destination =
                shopUrl
                + "?search="
                + encodeURIComponent(searchValue);

            window.location.href = destination;
        });
    });


    /* ==================================================
       استعادة البحث عند الوصول إلى المتجر
    ================================================== */

    if (!isShopPage) {
        return;
    }

    const urlParameters =
        new URLSearchParams(window.location.search);

    const initialSearch =
        urlParameters.get("search");

    if (!initialSearch) {
        return;
    }

    searchInputs.forEach(function (input) {
        input.value = initialSearch;

        input.dispatchEvent(
            new Event("input", {
                bubbles: true
            })
        );
    });
});


/* ==========================================================
   SMART HEADER
========================================================== */

(function(){

const header=document.getElementById("siteHeader");

if(!header) return;

function updateHeader(){

if(window.scrollY>70){

header.classList.add("header-scrolled");

}else{

header.classList.remove("header-scrolled");

}

}

updateHeader();

window.addEventListener("scroll",updateHeader,{
passive:true
});

})();

