var load = ()=> {
    $('#main-block').html(`
    <form>
        <div class="form-group row">
            <div class="col-sm-12">
            <input type="text" class="form-control" id="url" placeholder="URL" value="">
            <button id="getURLbtn"style="margin-top: 2%;" class="g-recaptcha btn btn-lg btn-secondary" data-sitekey="6LfOd2oUAAAAANE8S_j9DYzMbf-RF8gmh7-96WyO" data-callback="YourOnSubmitFn">
                Generate URL
            </button>
            </div>
        </div>
    </form>`)
}

var concatHTTP = (url) => {
    if (!/^(?:f|ht)tps?\:\/\//.test(url)) {
        url = "http://" + url;
    }
    return url;
}

var YourOnSubmitFn = ((token) => {
    var url = $('#url').val()
    jQuery.ajax ({
        url: '/',
        type: "POST",
        data: JSON.stringify({url: url, token: token}),
        dataType: "json",
        contentType: "application/json; charset=utf-8",
        success: function(data){
            var shortURL = window.location.host + "/" + data.code
            var oldLink = ['<a href="'+ concatHTTP(url) +'" target="_blank"><h3 style="margin-bottom: 20px;">'+url+'</h3></a>',
                            '<div class="arrow_box  style="margin-bottom: 20px;"">',
                                '<h3 class="logo">Converted to </h3>',
                            '</div>'].join('\n')
            var newLink = ['<a href="' + window.location.protocol + '//' + shortURL +'" target="_blank"><h3 style="margin-top: 40px;">'+shortURL+'</h3></a>',
                            '<img src="https://chart.googleapis.com/chart?cht=qr&chl='+shortURL+'L&chs=160x160&chld=L|0" style="margin-top: 40px;">',
                        ].join('\n')
            $('#main-block').html(oldLink+newLink)
            $('#head').html(`
            <a class="nav-link active" href=""><i class="fa fa-arrow-left" aria-hidden="true"></i>Back</a>`)
        }
    })
})


$(() => {
    load()
})