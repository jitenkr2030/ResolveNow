// ResolveNow JavaScript
$(document).ready(function () {
    // Initialize DataTables on .rn-table elements
    if (typeof $.fn.DataTable !== "undefined") {
        $(".rn-table").DataTable({
            pageLength: 10,
            lengthMenu: [5, 10, 25, 50, 100],
            responsive: true,
        });
    }

    // Auto-dismiss alerts after 6 seconds
    setTimeout(function () {
        $(".alert:not(.alert-persistent)").fadeOut("slow");
    }, 6000);

    // Sidebar active link
    var currentPath = window.location.pathname;
    $(".rn-sidebar a").each(function () {
        if ($(this).attr("href") === currentPath) {
            $(this).addClass("active");
        }
    });

    // Confirm any destructive action
    $(".rn-confirm").click(function (e) {
        var message = $(this).data("confirm-message") || "Are you sure?";
        if (!confirm(message)) {
            e.preventDefault();
        }
    });
});
