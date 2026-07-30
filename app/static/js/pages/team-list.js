document.addEventListener("DOMContentLoaded", () => {

    const searchInput = document.getElementById("teamSearch");
    const statusFilter = document.getElementById("teamStatusFilter");
    const orderFilter = document.getElementById("teamOrderFilter");
    const resetButton = document.getElementById("resetTeamFilters");

    const tableBody = document.getElementById("teamTableBody");
    const rows = Array.from(document.querySelectorAll(".team-row"));

    const results = document.getElementById("teamResultsCount");
    const emptyRow = document.getElementById("noTeamResults");

    const originalRows = [...rows];

    function normalize(value) {
        return String(value || "").toLowerCase().trim();
    }

    function sortRows() {

        let currentRows = [...rows];

        if (orderFilter.value === "asc") {

            currentRows.sort((a, b) =>
                Number(a.dataset.order) - Number(b.dataset.order)
            );

        } else if (orderFilter.value === "desc") {

            currentRows.sort((a, b) =>
                Number(b.dataset.order) - Number(a.dataset.order)
            );

        } else {

            currentRows = [...originalRows];

        }

        currentRows.forEach(row => tableBody.appendChild(row));

        tableBody.appendChild(emptyRow);

    }

    function filterRows() {

        const keyword = normalize(searchInput.value);
        const status = normalize(statusFilter.value);

        let visible = 0;

        rows.forEach(row => {

            const name = normalize(row.dataset.name);
            const job = normalize(row.dataset.job);

            const matchSearch =
                !keyword ||
                name.includes(keyword) ||
                job.includes(keyword);

            const matchStatus =
                !status ||
                row.dataset.status === status;

            const show = matchSearch && matchStatus;

            row.style.display = show ? "" : "none";

            if (show) visible++;

        });

        sortRows();

        results.textContent = visible;

        emptyRow.classList.toggle(
            "admin-hidden",
            visible !== 0
        );

    }

    searchInput.addEventListener("input", filterRows);
    statusFilter.addEventListener("change", filterRows);
    orderFilter.addEventListener("change", filterRows);

    resetButton.addEventListener("click", () => {

        searchInput.value = "";
        statusFilter.value = "";
        orderFilter.value = "";

        filterRows();

    });

    filterRows();

});