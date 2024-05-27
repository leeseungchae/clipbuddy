// 1페이지 -> 파일 있고 없고로 색 좌우하는 함수
$(document).on('change', '.pc-upload', function(){    
    if($('.pc-upload')[0].files.length > 0){
        $('.pc-upload-icon').addClass('active')
    }
    else{
        $('.pc-upload-icon').removeClass('active')
    }
});


$(document).ready(function(){
    $(".new-chat-button").hover(
        function(){
            $('.new-chat-icon').addClass('icon-white')
            $('.new-chat-icon').removeClass('icon-gray')
        },
        function(){
            $('.new-chat-icon').addClass('icon-gray')
            $('.new-chat-icon').removeClass('icon-white')
        }
    )
})

$(document).ready(function(){
    $(".etc-source-button-box").click(
        function(){
            if($(this).hasClass('active') == false ) $(this).addClass('active')
            else $(this).removeClass('active')

            if($(this).hasClass('active') == true){
                $(this).children().first().addClass('icon-white')            
                $(this).children().first().removeClass('icon-blue')
            }

            else{
                $(this).children().first().removeClass('icon-white')            
                $(this).children().first().addClass('icon-blue')
            }

        }

    )
})

    
// post 함수
async function postData(url, formData){
    await fetch(url, {
        method: "POST",
        // Set the FormData instance as the request body
        body: formData,
    });
} 

// const response = await postData('http://127.0.0.1:8000/upload-video', formData);
// const data = await response.json();


// 여기에 클릭이벤트 만들어서 파일 전송!