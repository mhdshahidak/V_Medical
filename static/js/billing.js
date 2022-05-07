$(".add-table-items").on('click', '.remove-btn', function () {
    $(this).closest('.add-row').remove();
    return false;
});

$(document).on("click", ".add-btn", function () {
    var rowCount = $(".add-table-items tr ").length;
    var experiencecontent = '<tr class="add-row">' +
        '<td>' +
        '<input type="text" class="form-control" readonly   value=" '+ rowCount + ' style="border: 0;background-color: white;"">' +
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
        '<a href="javascript:void(0);" class="remove-btn" onclick="DeleteRow(' + rowCount + ')"><i class="fas fa-trash"></i></a>' +
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



//multilple adding

$('#generatebutton').click(function () {
    var invoiceId = $('#invId').val()
    var customer_phone = $('#cphone').val()
    var type = $('#type').val()
    var gst = $('#gst').html()
    var grand_total = $('#total_amount').html()

    var rowCount = $(".add-table-items tr").length;
    for (var i = 1; i < rowCount; i++) {
        var medicinename= $('#medicinename' + i).val()
        var qty = $('#qty' + i).val()
        var itemtotal = $('#itemtotal' + i).val()
        

        var data = {
            "invoiceId": invoiceId,
            "customer_phone": customer_phone,
            "medicinename": medicinename,
            "qty": qty,
            "itemtotal": itemtotal,
            "type": type,
            "gst": gst,
            "grand_total": grand_total,

        }
        
        // console.log(data)
        $.ajax({
            url: "datadding",
            type: 'POST',
            data: data,
            success: function (responce) {
                alert(responce.msg)
                $(ducument).html(response)

            }

        })



    }
    return false;
})

// senting total

$('#generatebutton').click(function(){
    var itotal = $('#total_amount').html()
    console.log(itotal)
    $.ajax({
        url:'/branchapp/incomeadding',
        type:'GET',
        data:{
            'total': itotal,
            'invoice_id':$('#invId').val()
        },
        success:function(response){
            
        }
    })
})

// deleting row

function DeleteRow(id){

    var completeTotal =0
    var amount=parseInt($("#itemtotal" + id).val())  
    var total=$("#total_amount" ).html()
    var sub = $("#subtotal").html()
    var gst = $("#gst").html()
    sub_total = parseInt(sub) - amount
    $("#subtotal").html(sub_total)
    fgst = parseInt(gst) - amount*5/100;
    $("#gst").html(fgst)
    completeTotal =  sub_total + fgst
    $("#total_amount").html(completeTotal)

}