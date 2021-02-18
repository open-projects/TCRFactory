// request to delete a Sample
//$("#buttonDelete").click(function (e) {
//    $this = this;
//    var form = $(this).closest('form')
//    form.find('#action_id').val("delete");
//    form.submit();
//});

// request to cancel a New Sample
//$("#buttonCancel").click(function (e) {
//    $this = this;
//    var form = $(this).closest('form')
//    form.find('#action_id').val("cancel");
//    form.submit();
//});

// highlight equivalent alfa/beta sequences in the same sample
$('.alfa_beta_index').change(function() {
    $this = this;
    if ($('#alfa_index_name').attr('data-dropdown') && $('#alfa_index_name').attr('data-dropdown') == $('#beta_index_name').attr('data-dropdown')) {
        $('#alfa_index_name').css("color","red");
        $('#beta_index_name').css("color","red");
    } else {
        $('#alfa_index_name').css("color","");
        $('#beta_index_name').css("color","");
    }
});
