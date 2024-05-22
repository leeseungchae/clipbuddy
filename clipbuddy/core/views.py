from django.shortcuts import render
from django.http import JsonResponse,HttpResponseBadRequest
from core.utils import save_video,extract_audio_from_video,transcribe_audio,text_summary_gpt,chat_gpt
from django.views.decorators.csrf import csrf_exempt
from core.models import UploadSession, Conversation
import uuid
import json

# Create your views here.
@csrf_exempt
def upload_video(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        try:
            video_path = save_video(file)
            audio_path = extract_audio_from_video(video_path)
            text= transcribe_audio(audio_path)

            # text = "200억 년 전의 우주는 칠흑 같은 어둠뿜이었어요. 그리고 거기에는 기체와 고밀도의 에너지들이 웅축해 있었죠. 그런데 어느 날 여기가 이제 우주의 중심이라고 가정했을 때 뻥 하고 대폭팔이 일어난 거예요. 이 대폭팔을 우리는 뭐라고 부르죠? 빅뱅이라고 부릅니다. 왜 이런 대폭팔이 일어났는지에 대해서는 알 수 없다라고 저자는 이야기하고 있는데 이 대폭팔의 수많은 파편들이 여기를 이제 중심이라고 가정을 했을 때 여기서부터 파편이 엄청나게 퍼져나가기 시작했어요. 그리고 이제 한 10억 년 정도가 흐르면서 여기 있는 우주의 파편들이 이렇게 무리지어서 덩어리를 짓기 시작합니다. 그러다 보니 여기 밀도가 조밀하니까 주변에 있는 작은 파편들을 끌어들이기 시작하고 이런 하나의 집단, 군을 형성하기 시작했죠. 이 군을 우리는 뭐라고 부르냐면 은하, 이렇게 얘기를 하는 거죠. 보통 하늘 하에 천억 개 정도의 별이고요. 그리고 별을 도는 행성이 또한 천억 개 정도 있다는 거예요. 이 안에. 그런데 여기는 우주의 중심에서 비세 속도로 달립니다. 비세 속도로 한 80억 년 정도로 오잖아요. 그러면 저기 우주의 완전 변두리 동네 제일 끝에 이렇게 은하의 무리가 있대요. 그런데 여기 있는 이 은하는요. 생각보다 별이 많습니다. 한 4천억 개 정도의 별로 구성이 돼 있는데 그중에 하나의 별이 있어요. 반짝반짝 빛나는 작은 먼지만 한 별. 이 별이 태양이에요. 이 태양 주변을 수, 금, 지, 화, 목, 토, 천, 해 같이 이런 별들이 이 사이를 뱅글뱅글 돌고 있다는 얘기예요. 그래서 이 범주를 뭐라고 부르냐면 태양계라고 불러요. 인류가 가장 관심을 가졌던 게 처음에는 금성이었어요. 그 이유는 뭐냐면 지구하고 모든 게 비슷하다는 거예요. 조금 더울까? 뭐 플로리다, 올리브 어느 정도 더운데. 펄펄 끓어. 맞아요. 표면 480도. 에이, 살 수가 없네. 불바다에서 심지어 수성보다 더 뜨거워요. 이해가 안 되잖아요. 왜? 이산화탄소 온실효과 때문에. 여기서 우리 지구의 환경을 또 비판을 합니다. 그러니까 이 이산화탄소가 나쁜 건 아니에요. 만약에 이산화탄소가 없잖아. 그럼 태양 복사율이 다 빠져나가서 지구가 빙하기가 온다는 거예요. 그런데 뭐든 지나치면 안 좋듯이 이 지구가 화석연료를 계속돼서 이산화탄소가 높아지면 우리도 금성처럼 불탈 수 있다. 책에서는 지구를 천국, 여기는 금성을 지옥으로 표현하죠. 그 다음에 사람들이 금성이 불타고 있으니까 생명체가 없구나. 우리는 외계인이 있었으면 하는 마음이 있잖아요. 그래서 여기는 화성에 있을 거라고 생각을 했는데 웰스의 소설, 우주전쟁 봐도 항상 화성에서 외계인이 오잖아요. 그런데 화성에 탐사선이 가고 있어요. 그런데 화성에 탐사선이 가고 있어요. 그런데 화성에 탐사선이 가고 있어요. 그런데 화성에 탐사선이 가고 있어요. 우주전쟁 봐도 항상 화성에서 외계인이 오잖아요. 그런데 화성에 탐사선이 갔어. 소련의 탐사선 말에 쓰는 실패. 미국의 바이킹이 화성에 다리를 내리고 그 다음에 영상을 전송을 하는데 화성의 지평선을 인류에게 처음 보여준 영상을 그만 넋을 잃고 바라봤다. 이건 외계의 세상이 아니라는 생각이 들었다. 지구상의 어느 풍경과 다를 바 없는 자연 그대로의 바윗덩이와 모래 언덕들이 무심하게 놓여있었고 지평선 멀리에는 높은 산이 자리 잡고 있었다. 화성은 그저 하나의 장소일 뿐이었다. 머리가 반백이 된 광산 채굴꾼이 노세를 끌면서 모래 언덕 뒤에서 나타나기라도 할 것 같았다. 라고 표현하고 있습니다. 그래서 생명체 있었을까요? 없었어요. 우리가 지구를 지키고 대변해야 되는 이유에 대해서 얘기하는데 저는 이 문장을 지금도 잊을 수가 없어요. 우리는 종으로서 인류를 사랑해야 하며 지구에게 충성해야 한다. 아니면 그 누가 우리의 지구를 대변해줄 수 있겠는가? 우리의 생존은 우리 자신만이 이룩한 업적이 아니다. 그러므로 오늘을 사는 우리는 인류를 여기에 있게 한 코스모스에게 감사해야 할 것이다. 라고 마무리하고 있습니다. 자막이 도움이 되셨다면 구독과 좋아요 부탁드립니다."
            # print(text)

            summry_text = text_summary_gpt(text=text)
            # summry_text = "200억 년 전의 우주는 어둠 속에 기체와 고밀도 에너지로 가득 차 있었고, 어느 날 대폭팔이 일어나 우주의 중심으로부터 파편들이 퍼져나가기 시작했다. 이 대폭팔을 빅뱅이라고 부르며, 대폭팔이 일어난 이유는 알 수 없다고 한다. 10억 년이 지난 후 우주의 파편들이 모여 덩어리를 이루기 시작했다.은하 안에는 천억 개의 별과 행성이 있으며, 우주의 중심에서 비세 속도로 이동하는 은하의 무리가 있다. 이 은하에는 4천억 개의 별로 구성된 태양이 있으며, 이 주변에는 다양한 행성들이 돌고 있다.태양계에서 금성과 지구의 비교를 통해 환경 문제를 다룬 글. 이산화탄소의 중요성과 지구의 미래에 대한 우려를 표현하며 화성에 대한 탐사와 외계 생명체에 대한 상상 등을 다루고 있음. 글은 지구를 사랑하고 보호해야 한다는 메시지를 강조하며 우리의 생존은 우리 스스로가 책임져야 한다는 주장을 하고 있음."
            # print(summry_text)

            user_id = str(uuid.uuid4())
            # DB에 세션 정보 저장
            session = UploadSession(user_id=user_id, upload_status='complete')
            session.save()

            conversation = Conversation(session=session, message=summry_text)
            conversation.save()

            response = JsonResponse({'message': 'success'})
            response.set_cookie('user_id', user_id)  # 세션 쿠키 설정 (브라우저 세션 종료 시 만료)
            return response

        except Exception as e:

            return JsonResponse({'message':str(e)}, status=500)
        # audio_path = None
            # 파일 저장
    else:
        return HttpResponseBadRequest("Invalid request")


@csrf_exempt
def add_conversation(request):
    user_id = request.COOKIES.get('user_id')
    if user_id and request.method == 'POST':
        body = json.loads(request.body)
        message = body.get('message')

        upload_sessions = UploadSession.objects.filter(user_id=user_id)

    # 해당 UploadSession과 연관된 모든 Conversation 객체 가져오기
        conversations = Conversation.objects.filter(session__in=upload_sessions)
        for conversation in conversations:
            summry_text = conversation.message
        result = chat_gpt(summry_text,user_input=message)

        response = JsonResponse({'message': result})
        return response
        # print(conversations.message)
        # print(message)
        # print(user_id)



    return JsonResponse({'error': 'Invalid request'}, status=400)