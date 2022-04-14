$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: window.location.origin + "/graphs?videoId="+ $('#videoId').val(),
        contentType: "image/png",
        success: function(data){
            parsed = JSON.parse(data)
            $('.pie').append('<img src="' + parsed.image1 + '" />')
            $('.intensity').append('<img src="' + parsed.image2 + '" />')
            $('.date').append('<img src="' + parsed.image3 + '" />')
            $('.dateIntensity').append('<img src="' + parsed.image4 + '" />')
        },
        start: function(){
            console.log("started")
        }
    });

    $.ajax({
        type: "GET",
        url: window.location.origin + "/words?videoId="+ $('#videoId').val(),
        contentType: "image/png",
        success: function(data){
            dataObj = JSON.parse(data)
            i = 1
            for(const [key, value] of Object.entries(dataObj)) {
                words = value
                for (const [key, value] of Object.entries(words)) {
                    value.forEach(function(element) {
                        $('#'+i).append('<tr>')
                        $('#'+i).append('<td>'+ element.word +'</td>')
                        $('#'+i).append('<td>'+ element.context_sentiment +'</td>')
                        $('#'+i).append('<td>'+ element.positive +'</td>')
                        $('#'+i).append('<td>'+ element.neutral +'</td>')
                        $('#'+i).append('<td>'+ element.negative +'</td>')
                        $('#'+i).append('</tr>')
                    });
                    i = i+1
                }
            }
            $('.words').show()
            $('.warning').hide()
        },
        beforeSend: function(){
            $('.words').hide()
        }
    });
})
