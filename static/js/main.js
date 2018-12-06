$(document).ready(function() {
    $('#dtVerticalScroll').DataTable({
        "scrollY": "200px",
        "scrollCollapse": true,
        order : [0, 'desc']
    });
    $('.dataTables_length').addClass('bs-select');
});
