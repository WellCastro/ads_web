$(document).ready(function() {
    $('#property').DataTable( {
        "language": {
            "lengthMenu": "Exibindo _MENU_ por página",
            "zeroRecords": "Nenhum registro",
            "info": "página _PAGE_ de _PAGES_",
            "infoEmpty": "Nenhum registro",
            "infoFiltered": "(filtered from _MAX_ total records)",
            'search': "Procurar:",
            paginate: {
                first:      "Primeira",
                previous:   "Anterior",
                next:       "Próxima",
                last:       "Última"
            }
        }
    } );
} );

$(".delete").click(function(){
    var id_json = this.id;
    delete_all(id_json);
});

function delete_all(id) {
    $.ajax({
        url : "/api/property/remove/"+id,
        type : "DELETE", 

        // handle a successful response
        success : function(json) {
            var node = "tr[id="+id+"]"
            $(node).remove();
            console.log("deleted id"+id)

        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
};
