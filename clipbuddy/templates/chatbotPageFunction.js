const setInitialChat = (function(){
    const myName = "You";
 
    // init 함수
    function init() {
        // enter 키 이벤트
        $(document).on('keydown', 'div.question-input-box textarea', function(e){
            if(e.keyCode == 13 && !e.shiftKey) {
                e.preventDefault();
                const message = $(this).val();
                location.replace('chatbotPageTalking.html?message='+message)
                // // 메시지 전송
                // sendMessage(message);
                // // 입력창 clear
                // clearTextarea();
            }
        });

        // 클릭 이벤트
        $(document).on('click', 'div.question-example-box', function(e){
            e.preventDefault();
                const message = $(this).children()[0].textContent;
                location.replace('chatbotPageTalking.html?message='+message)

        });
    }
    return {
        'init': init
    };
})();

setInitialChat.init();