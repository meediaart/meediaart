  // ==========================================
// عناصر البحث والفلاتر
// ==========================================

const orderSearch = document.getElementById("orderSearch");
const filterStatus = document.getElementById("filterStatus");
const filterPayment = document.getElementById("filterPayment");
const filterMethod = document.getElementById("filterMethod");
const dateFrom = document.getElementById("dateFrom");
const dateTo = document.getElementById("dateTo");
const resetFilters = document.getElementById("resetFilters");

// ==========================================
// محرك الفلترة
// ==========================================

function filterOrders() {

    const keyword = orderSearch.value.trim().toLowerCase();

    const status = filterStatus.value;

    const payment = filterPayment.value;

    const method = filterMethod.value;

    const from = dateFrom.value;

    const to = dateTo.value;

    const rows = document.querySelectorAll(
    ".admin-table tbody tr:not(#noOrdersResult)"
);

const visibleOrdersCount =
    document.getElementById("visibleOrdersCount");

const noOrdersResult =
    document.getElementById("noOrdersResult");

let visibleCount = 0;
const statistics = {
    total: 0,
    created: 0,
    processing: 0,
    shipped: 0,
    delivered: 0,
    cancelled: 0,
    paid: 0,
    unpaid: 0
};

    rows.forEach(function(row){

        const customer = row.dataset.customer;

        const phone = row.dataset.phone;

        const orderId = row.dataset.orderId;

        const rowStatus = row.dataset.status;

        const rowPayment = row.dataset.payment;

        const rowMethod = row.dataset.method;

        const rowDate = row.dataset.date;

        let visible = true;

        // -------------------------
        // البحث
        // -------------------------

        if(keyword !== ""){

            const found =
                customer.includes(keyword) ||
                phone.includes(keyword) ||
                orderId.includes(keyword);

            if(!found){

                visible = false;

            }

        }

        // -------------------------
        // حالة الطلب
        // -------------------------

        if(status !== "" && rowStatus !== status){

            visible = false;

        }

        // -------------------------
        // حالة الدفع
        // -------------------------

        if(payment !== "" && rowPayment !== payment){

            visible = false;

        }

        // -------------------------
        // طريقة الدفع
        // -------------------------

        if(method !== "" && rowMethod !== method){

            visible = false;

        }

        // -------------------------
        // من تاريخ
        // -------------------------

        if(from !== "" && rowDate < from){

            visible = false;

        }

        // -------------------------
        // إلى تاريخ
        // -------------------------

        if(to !== "" && rowDate > to){

            visible = false;

        }

        row.style.display = visible ? "" : "none";

      if (visible) {
    visibleCount++;
    statistics.total++;

    /*
        نحول أسماء الحالات القديمة إلى الأسماء الجديدة
        حتى تُحسب الطلبات القديمة بصورة صحيحة.
    */
    let normalizedStatus = rowStatus;

    if (normalizedStatus === "pending") {
        normalizedStatus = "created";
    }

    if (normalizedStatus === "in_progress") {
        normalizedStatus = "processing";
    }

    if (normalizedStatus === "completed") {
        normalizedStatus = "delivered";
    }

    if (
        Object.prototype.hasOwnProperty.call(
            statistics,
            normalizedStatus
        )
    ) {
        statistics[normalizedStatus]++;
    }

    if (rowPayment === "paid") {
        statistics.paid++;
    }

    if (rowPayment === "unpaid") {
        statistics.unpaid++;
    }
}

    });

visibleOrdersCount.textContent = visibleCount;

if (noOrdersResult) {
    noOrdersResult.style.display =
        visibleCount === 0 ? "" : "none";
}

document.getElementById("statsTotal").textContent =
    statistics.total;

document.getElementById("statsCreated").textContent =
    statistics.created;

document.getElementById("statsProcessing").textContent =
    statistics.processing;

document.getElementById("statsShipped").textContent =
    statistics.shipped;

document.getElementById("statsDelivered").textContent =
    statistics.delivered;

document.getElementById("statsCancelled").textContent =
    statistics.cancelled;

document.getElementById("statsPaid").textContent =
    statistics.paid;

document.getElementById("statsUnpaid").textContent =
    statistics.unpaid;
    
}

// ==========================================
// ربط الأحداث
// ==========================================

orderSearch.addEventListener("keyup", filterOrders);

filterStatus.addEventListener("change", filterOrders);

filterPayment.addEventListener("change", filterOrders);

filterMethod.addEventListener("change", filterOrders);

dateFrom.addEventListener("change", filterOrders);

dateTo.addEventListener("change", filterOrders);

// ==========================================
// إعادة تعيين
// ==========================================

resetFilters.addEventListener("click", function(){

    orderSearch.value = "";

    filterStatus.value = "";

    filterPayment.value = "";

    filterMethod.value = "";

    dateFrom.value = "";

    dateTo.value = "";

    filterOrders();

});
// تشغيل الفلترة والحسابات عند فتح الصفحة أول مرة
filterOrders();
// ==========================================
// ترتيب أعمدة جدول الطلبات
// ==========================================

let currentSortColumn = "";
let currentSortDirection = "asc";

const sortableHeaders = document.querySelectorAll(
    ".admin-table thead .sortable"
);

sortableHeaders.forEach(function (header) {
    header.addEventListener("click", function () {
        const column = this.dataset.sort;

        if (currentSortColumn === column) {
            currentSortDirection =
                currentSortDirection === "asc" ? "desc" : "asc";
        } else {
            currentSortColumn = column;
            currentSortDirection = "asc";
        }

        sortOrderRows(column, currentSortDirection);
        updateSortIndicators(this, currentSortDirection);
    });
});


function sortOrderRows(column, direction) {
    const tableBody = document.querySelector(".admin-table tbody");

    const noOrdersResult =
        document.getElementById("noOrdersResult");

    const rows = Array.from(
        tableBody.querySelectorAll("tr:not(#noOrdersResult)")
    );

    rows.sort(function (firstRow, secondRow) {
        let firstValue = "";
        let secondValue = "";

        if (column === "id") {
            firstValue = Number(firstRow.dataset.orderId || 0);
            secondValue = Number(secondRow.dataset.orderId || 0);
        }

        if (column === "customer") {
            firstValue =
                (firstRow.dataset.customer || "").toLowerCase();

            secondValue =
                (secondRow.dataset.customer || "").toLowerCase();
        }

        if (column === "price") {
            firstValue = Number(firstRow.dataset.price || 0);
            secondValue = Number(secondRow.dataset.price || 0);
        }

        if (column === "date") {
            firstValue = firstRow.dataset.date || "";
            secondValue = secondRow.dataset.date || "";
        }

        let comparison = 0;

        if (
            typeof firstValue === "number" &&
            typeof secondValue === "number"
        ) {
            comparison = firstValue - secondValue;
        } else {
            comparison = String(firstValue).localeCompare(
                String(secondValue),
                "ar",
                {
                    numeric: true,
                    sensitivity: "base"
                }
            );
        }

        return direction === "asc"
            ? comparison
            : comparison * -1;
    });

    rows.forEach(function (row) {
        tableBody.appendChild(row);
    });

    if (noOrdersResult) {
        tableBody.appendChild(noOrdersResult);
    }
}


function updateSortIndicators(activeHeader, direction) {
    sortableHeaders.forEach(function (header) {
        const cleanTitle =
            header.textContent
                .replace(" ↑", "")
                .replace(" ↓", "")
                .replace(" ↕", "")
                .trim();

        header.textContent = cleanTitle + " ↕";
        header.classList.remove(
            "sort-ascending",
            "sort-descending"
        );
    });

    const activeTitle =
        activeHeader.textContent
            .replace(" ↑", "")
            .replace(" ↓", "")
            .replace(" ↕", "")
            .trim();

    activeHeader.textContent =
        activeTitle + (direction === "asc" ? " ↑" : " ↓");

    activeHeader.classList.add(
        direction === "asc"
            ? "sort-ascending"
            : "sort-descending"
    );
}
// ==========================================
// التحديد الجماعي للطلبات
// ==========================================

const selectAllOrders =
    document.getElementById("selectAllOrders");

const orderCheckboxes =
    document.querySelectorAll(".orderCheckbox");


// إنشاء عداد الطلبات المحددة
const selectedOrdersCounter =
    document.getElementById("selectedOrdersCount");


// تحديث عدد الطلبات المحددة
function updateSelectedOrdersCount() {

    const selectedCount =
        document.querySelectorAll(
            ".orderCheckbox:checked"
        ).length;

    if (selectedOrdersCounter) {
        selectedOrdersCounter.textContent =
            selectedCount;
    }

    /*
        إذا كانت جميع الطلبات محددة،
        نجعل مربع تحديد الكل محددًا.
    */
    if (selectAllOrders) {

        const totalCheckboxes =
            orderCheckboxes.length;

        selectAllOrders.checked =
            totalCheckboxes > 0 &&
            selectedCount === totalCheckboxes;

        /*
            الحالة الوسطية تظهر عندما يكون
            بعض الطلبات محددًا وليس كلها.
        */
        selectAllOrders.indeterminate =
            selectedCount > 0 &&
            selectedCount < totalCheckboxes;
    }
}


// تحديد أو إلغاء تحديد جميع الطلبات
if (selectAllOrders) {

    selectAllOrders.addEventListener(
        "change",
        function () {

            orderCheckboxes.forEach(
                function (checkbox) {

                    /*
                        نحدد الصفوف الظاهرة فقط،
                        حتى لا يحدد طلبات مخفية
                        بسبب الفلاتر.
                    */
                    const row =
                        checkbox.closest("tr");

                    if (
                        row &&
                        row.style.display !== "none"
                    ) {
                        checkbox.checked =
                            selectAllOrders.checked;
                    }
                }
            );

            updateSelectedOrdersCount();
        }
    );
}


// مراقبة كل مربع طلب
orderCheckboxes.forEach(
    function (checkbox) {

        checkbox.addEventListener(
            "change",
            updateSelectedOrdersCount
        );
    }
);


// تشغيل العداد عند فتح الصفحة
updateSelectedOrdersCount();

// ==========================================
// تنفيذ الإجراءات الجماعية
// ==========================================

const bulkOrdersForm =
    document.getElementById("bulkOrdersForm");

const bulkAction =
    document.getElementById("bulkAction");

const selectedOrderInputs =
    document.getElementById("selectedOrderInputs");


if (bulkOrdersForm) {

    bulkOrdersForm.addEventListener(
        "submit",
        function (event) {

            /*
                نجمع الطلبات التي وضع المستخدم
                علامة تحديد عليها.
            */
            const selectedCheckboxes =
                document.querySelectorAll(
                    ".orderCheckbox:checked"
                );

            /*
                منع الإرسال إذا لم يتم تحديد طلبات.
            */
            if (selectedCheckboxes.length === 0) {
                event.preventDefault();

                alert(
                    "يرجى تحديد طلب واحد على الأقل."
                );

                return;
            }

            /*
                منع الإرسال إذا لم يتم اختيار إجراء.
            */
            if (!bulkAction.value) {
                event.preventDefault();

                alert(
                    "يرجى اختيار الإجراء الجماعي."
                );

                return;
            }

            /*
                تنظيف الأرقام القديمة قبل إضافة
                الأرقام المحددة حاليًا.
            */
            selectedOrderInputs.innerHTML = "";

            /*
                إنشاء input مخفي لكل طلب محدد.
                جميع الحقول تحمل الاسم نفسه لكي
                يستقبلها Flask كقائمة.
            */
            selectedCheckboxes.forEach(
                function (checkbox) {

                    const hiddenInput =
                        document.createElement("input");

                    hiddenInput.type = "hidden";
                    hiddenInput.name = "order_ids";
                    hiddenInput.value = checkbox.value;

                    selectedOrderInputs.appendChild(
                        hiddenInput
                    );
                }
            );

            /*
                تأكيد تنفيذ العملية الجماعية.
            */
            const confirmed = confirm(
                "هل أنت متأكد من تطبيق هذا الإجراء على " +
                selectedCheckboxes.length +
                " طلب؟"
            );

            if (!confirmed) {
                event.preventDefault();
            }
        }
    );
}
