document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("userSearch");
    const roleFilter = document.getElementById("roleFilter");
    const resetButton = document.getElementById("resetUserFilters");
    const resultsCount = document.getElementById("usersResultsCount");
    const noResultsRow = document.getElementById("noUsersResults");
    

    const userRows = Array.from(
        document.querySelectorAll(".user-row")
    );

    if (
        !searchInput ||
        !roleFilter ||
        !resetButton ||
        !resultsCount ||
        !noResultsRow
    ) {
        return;
    }

    function normalizeText(value) {
        return String(value || "")
            .toLowerCase()
            .trim();
    }

    function filterUsers() {
        const searchValue = normalizeText(searchInput.value);
        const roleValue = normalizeText(roleFilter.value);

        let visibleCount = 0;

        userRows.forEach(function (row) {
            const username = normalizeText(row.dataset.username);
            const email = normalizeText(row.dataset.email);
            const role = normalizeText(row.dataset.role);

            const matchesSearch =
                searchValue === "" ||
                username.includes(searchValue) ||
                email.includes(searchValue) ||
                role.includes(searchValue);

            const matchesRole =
                roleValue === "" ||
                role === roleValue;

            const shouldShow =
                matchesSearch &&
                matchesRole;

            row.classList.toggle(
                "admin-hidden",
                !shouldShow
            );

            if (shouldShow) {
                visibleCount += 1;
            }
        });

        resultsCount.textContent = String(visibleCount);

        noResultsRow.classList.toggle(
            "admin-hidden",
            userRows.length === 0 || visibleCount > 0
        );
    }

    function resetFilters() {
        searchInput.value = "";
        roleFilter.value = "";

        filterUsers();
        searchInput.focus();
    }

    searchInput.addEventListener("input", filterUsers);
    roleFilter.addEventListener("change", filterUsers);
    resetButton.addEventListener("click", resetFilters);

    filterUsers();
});

console.log("orders-list.js loaded");
