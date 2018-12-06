$('#dtVerticalScroll').removeClass('d-none');

$(document).ready(function () {
    $('#dtVerticalScroll').DataTable({
        "scrollY": "50vh",
        "scrollCollapse": true,
        order : [0, 'desc']
    });
    $('.dataTables_length').addClass('bs-select');
});
