$(".add-table-items").on('click', '.remove-btn', function () {
    $(this).closest('.add-row').remove();
    return false;
});

$(document).on("click", ".add-btn", function () {
    var rowCount = $(".add-table-items tr ").length;
    var experiencecontent = '<tr class="add-row">' +
        '<td>' +
        '<input type="text" class="form-control" readonly value=" '+ rowCount + '">' +
        '</td>' +
        '<td>' +
        // '<input type="text" class="form-control" name="medicine" list="medicine"><datalist id="medicine">{% for p in product %}<option value="{{p.product.name}}">{% endfor %}</datalist>' +
        '<input type="text" class="form-control" name="medicine" list="medicine" onchange=changedname('+rowCount+') id="medicinename' + rowCount + '">' +
        
        '</td>' +
        '<td>' +
        '<input type="text" class="form-control" onchange=changedqty('+rowCount+') id="qty' + rowCount + '">' +
        '</td>' +
        '<td>' +
        '<input id="price'+rowCount+'" type="text" class="form-control">' +
        '</td>' +

        '<td>' +
        '<input type="text" class="form-control" id="itemtotal'+rowCount+'">' +
        '</td>' +
        '<td class="add-remove text-end">' +
        '<a href="javascript:void(0);" class="add-btn me-2"><i class="fas fa-plus-circle"></i></a> ' +
        '<a href="javascript:void(0);" class="remove-btn" onclick=remove()><i class="fas fa-trash"></i></a>' +
        '</td>' +
        '</tr>';

    $(".add-table-items").append(experiencecontent);
    return false;
});

// for getting price of a product

function changedname(rowCount){
    $.ajax({
        url:'/branchapp/medprice',
        type:'GET',
        data:{
            'name':$("#medicinename"+rowCount).val()
        },
        success:function(response){
            $('#price'+rowCount).val(response.product.price)
        }
    })
}

// item total

function changedqty(rowCount){
    var unitPrice=parseInt($('#price'+rowCount).val())
    var qty=parseInt($('#qty'+rowCount).val())
    var totalAmount=unitPrice*qty
    $('#itemtotal'+rowCount).val(totalAmount)

    
    var Available_rowCount = $(".add-table-items tr ").length;
    var sum=0
    for(var i=1;i<Available_rowCount;i++){
        sum+=parseInt($('#itemtotal'+i).val())
    }
    var gst=sum*5/100;
    $('#gst').html(gst)
    $('#subtotal').html(sum);
    $('#total_amount').html(parseInt(gst+sum))
}




// function remove(rowCount){

// }