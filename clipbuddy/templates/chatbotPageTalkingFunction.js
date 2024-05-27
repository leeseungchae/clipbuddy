window.onload = function(){
    let params = new URLSearchParams(location.search);
    let message = params.get('message')

    if(message != undefined && message != null){
        receiveChatFromHref.init();
    }
}

const receiveChatFromHref = (function() {
    const myName = "You";

    // init 함수
    function initialInit() {

        let params =  new URLSearchParams(location.search);
        let message = params.get('message')

        // 메시지 전송
        sendInitialMessage(message);
        // 입력창 clear
        clearInitialTextarea();
    }

    // 메시지 태그 생성
    function createInitialMessageTag(LR_className, senderName, message) {
        // 형식 가져오기
        let chatLi = $('div.chat.format ul li').clone();

        // 값 채우기
        chatLi.addClass(LR_className);
        chatLi.find('.sender span').text(senderName);
        chatLi.find('.message span').text(message);

        return chatLi;
    }

    // 메시지 태그 append
    function appendMessageTag(LR_className, senderName, message) {
        const chatLi = createInitialMessageTag(LR_className, senderName, message);

        $('div.chat:not(.format) ul').prepend(chatLi);

        // 스크롤바 아래 고정
        $('div.chat').scrollTop($('div.chat').prop('scrollHeight'));
    }

    // 메시지 전송
    async function sendInitialMessage(message) {
        // 서버에 전송하는 데이터
        user_id = sessionStorage.getItem('user_id');
        const data = {
            "senderName": "You",
            "message": message,
            user_id: user_id
        };
        console.log(data);
        initialReceive(data);
        // 서버에 POST 요청 보내기
        let response = await fetch('http://localhost:8000/random-answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            credentials: 'include'  // 메시지를 본문에 포함
        })
        .catch((error)=>{
            let responsedMessage = {
                "senderName"    : "Buddy",
                "message"   : '질문을 이해하지 못했어요.',
                user_id: user_id
            }
            // 통신하는 기능이 없으므로 여기서 receive
            initialReceive(responsedMessage);
            return false;
        });

        if(response != false){
            // 서버로부터 응답 받기
            if (response.ok) {
                let responsedData = await response.json();

                // 서버 응답 데이터로 메시지 구성
                let responsedMessage = {
                    "senderName": "Buddy",
                    "message": responsedData.message // 서버 응답의 키를 수정된 대로 변경
                };
                
                const data = {
                    "senderName": "You",
                    "message": message,
                };
                // 응답 메시지 처리
                initialReceive(responsedMessage);
            } else {
                console.error('Error:', response.statusText);
            }
        }
    }

    // 메시지 입력박스 내용 지우기
    function clearInitialTextarea() {
        $('div.input-div textarea').val('');
    }

    // 메시지 수신
    function initialReceive(data) {
        const LR = (data.senderName != myName)? "left" : "right";
        appendMessageTag(LR, data.senderName, data.message);
    }

    return {
        'init': initialInit
    };
})();

const Chat = (function() {
    const myName = "You";

    // init 함수
    function init() {
        // enter 키 이벤트
        $(document).on('keydown', 'div.input-div textarea', function(e){
            if(e.keyCode == 13 && !e.shiftKey) {
                e.preventDefault();
                const message = $(this).val();
 
                // 메시지 전송
                sendMessage(message);
                // 입력창 clear
                clearTextarea();
            }
        });
    }
    function createMessageTag(LR_className, senderName, message) {
        // 형식 가져오기
        let chatLi = $('div.chat.format ul li').clone();
 
        // 값 채우기
        chatLi.addClass(LR_className);
        chatLi.find('.sender span').text(senderName);
        chatLi.find('.message span').text(message);
 
        return chatLi;
    }
 
 

    // 메시지 태그 생성
    function appendMessageTag(LR_className, senderName, message) {
        const chatLi = createMessageTag(LR_className, senderName, message);
 
        $('div.chat:not(.format) ul').prepend(chatLi);
 
        // 스크롤바 아래 고정
        $('div.chat').scrollTop($('div.chat').prop('scrollHeight'));
    }

    // 메시지 전송
    async function sendMessage(message) {
        // 서버에 전송하는 데이터
        const userId = sessionStorage.getItem('user_id');
        const data = {
            "senderName": "You",
            "message": message,
            "user_id": userId,
        };
        receive(data);
        // 서버에 POST 요청 보내기
        let response = await fetch('http://localhost:8000/random-answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
            credentials: 'include'  // 메시지를 본문에 포함,

        })
        .catch((error)=>{
            let responsedMessage = {
                "senderName"    : "Buddy",
                "message"   : '질문을 이해하지 못했어요.'
            }
            // 통신하는 기능이 없으므로 여기서 receive
            receive(responsedMessage);
            return false;
        });

        if(response!= false){
            // 서버로부터 응답 받기
            if (response.ok) {
                let responsedData = await response.json();

                // 서버 응답 데이터로 메시지 구성
                let responsedMessage = {
                    "senderName": "Buddy",
                    "message": responsedData.message // 서버 응답의 키를 수정된 대로 변경
                };
                const data = {
                    "senderName": "You",
                    "message": message,
                };
                // 응답 메시지 처리
                receive(responsedMessage);
            } else {
                console.error('Error:', response.statusText);
            }
        }
    }

    // 메시지 입력박스 내용 지우기
    function clearTextarea() {
        $('div.input-div textarea').val('');
    }

    // 메시지 수신
    function receive(data) {
        const LR = (data.senderName != myName)? "left" : "right";
        appendMessageTag(LR, data.senderName, data.message);
    }

    return {
        'init': init
    };
})();

// $(function() {
//     Chat.init();
// });