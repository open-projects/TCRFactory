//
// TCRpiper - a pipeline for TCR sequences treatment. Copyright (C) 2020  D. Malko
//

// check/uncheck checkboxes in a table
$(".check-all-table").click(function (e) {
    $this = this;  
    $.each($(this).parents('table').find('input'), function(i, item){
        $(item).prop('checked', $this.checked);
    });
});

// the name of the file appear on select
$(".custom-file-input").on("change", function() {
    var fileName = $(this).val().split("\\").pop();
    $(this).siblings(".custom-file-label").addClass("selected").html(fileName);
});

// dropdown inputs
$(".dropdown-item").click(function (e) {
    $this = this;
    var name = $(this).attr('name');
    var data = $(this).attr('data-dropdown'); //  custom attribute
    var dropdown_with_input = $(this).closest('.dropdown-with-input');
    var input = dropdown_with_input.find('input');
    input.val(name)
    input.attr('data-dropdown', data); //  custom attribute
    input.trigger("change");
});

