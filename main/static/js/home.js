$(function(){
// Change the selector if needed
    $(".input-group").addClass("input-group-sm")
    $(".form-control").addClass("form-control-sm")
    $( ".dateinput" ).attr('type','date');
    var $table = $('table'),
        $bodyCells = $table.find('tbody tr:first').children(),
        $headCells = $table.find('thead tr:first').children(),
        colWidth,
        headWidth;
        
        colWidth = $bodyCells.map(function() {
            return $(this).width();
        }).get();              
        $table.find('thead tr').children().each(function(i, v) {
            $(v).width(colWidth[i]);
        });  
        headWidth = $headCells.map(function() {
            return $(this).width();
        }).get();
        $table.find('tbody tr').each(function(){
            $(this).children().each(function(i, v){
                $(v).width(Math.max(colWidth[i], headWidth[i]));
            });
        });    
});