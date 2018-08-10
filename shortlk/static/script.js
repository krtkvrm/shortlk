$(() => {
    let submitBTN = $('#submitbtn')

    submitBTN.click(() => {
        jQuery.ajax ({
            url: '/',
            type: "POST",
            data: JSON.stringify({url:$('#url').val()}),
            dataType: "json",
            contentType: "application/json; charset=utf-8",
            success: function(data){
                console.log(data)
            }
        })
    })  
})