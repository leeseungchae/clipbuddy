from core.src.customtexttiling import text_tiling
from clipbuddy.settings.base import ROOT_DIR,OPENAI_API_KEY
import os
import uuid
import openai
import ffmpeg
import yaml
from  core.src.customtexttiling import text_tiling
# from langchain.chains import LLMChain
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from core.dto import LlmItem
import yaml
import re
import json
from dotenv import load_dotenv  
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import HumanMessage, SystemMessage
from langchain.chains import LLMChain
load_dotenv()

def parse_yaml(path) -> dict:
    with open(path, "r") as f:
        topic_data = yaml.safe_load(f)
        return topic_data


settings = parse_yaml(path=os.path.join(ROOT_DIR, 'settings.yaml'))
sentence_settings = settings['sentence_processing']



openai.api_key = OPENAI_API_KEY
def save_video(file):

    new_uuid = uuid.uuid4()
    save_dir = os.path.join(ROOT_DIR, 'data')
    os.makedirs(save_dir,exist_ok=True)
    path = os.path.join(save_dir, f'{new_uuid}.mp4')
    with open(path, 'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
    return path

def extract_audio_from_video(video_path: str):

    audio_path = video_path.replace(".mp4", ".wav")
    ffmpeg.input(video_path).output(audio_path, ar=16000, ac=1).run()

    return audio_path


def transcribe_audio(audio_path: str):
    with open(audio_path, "rb") as audio_file:
        audio_file= open(audio_path, "rb")
    try:    
        transcription = openai.Audio.transcribe(
        model="whisper-1", 
        file=audio_file
        )
        return transcription.text
    except Exception as e:
        print(e)


def process_sentences(sentence_list,min_length_for_split:int =50 ,chunk_size:int = 30):
    """
    주어진 문장 리스트를 분할하는 함수입니다. 설정 파일에서 분할 기준을 로드하여,
    문장의 수가 이 기준을 충족하면 text_tiling 함수로 분할을 시도합니다. 
    text_tiling 실행 시 오류가 발생하면, 설정된 청크 크기에 따라 문장을 분할합니다.
    문장 수가 기준 미만이면, 각 문장에 대해 인덱스와 함께 단일 리스트로 반환합니다.
    """

    if len(sentence_list) >= min_length_for_split:
        try:
            return text_tiling(sentence_list=sentence_list,sent_size=min_length_for_split)
        except Exception as e:  # 구체적인 예외 타입으로 교체하는 것이 좋습니다.
            print("Error occurred while text tiling. Splitting sentences by chunk size", str(e))
            return split_sentences(sentence_list=sentence_list, chunk_size=chunk_size)
    else:
        return [[{i: sent["new_text"]} for i, sent in enumerate(sentence_list)]]

def split_list(input_list:list, chunk_size:int):
    """리스트를 지정된 크기의 청크로 나눕니다."""
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i : i + chunk_size]


def split_sentences(sentence_list, chunk_size=100):
    """
    주어진 리스트를 chunk_size 단위로 분할하여 각 청크마다 인덱스와 함께 사전 형태로 반환합니다.
    """
    return [
            [{i + j * chunk_size: item["new_text"]} for i, item in enumerate(chunk)]
            for j, chunk in enumerate(split_list(input_list=sentence_list, chunk_size=chunk_size))
            ]

def text_summary_gpt(text):

    parse = r'[.,!?]'
    sentence_list = re.split(parse, text)
    sentence_list = [token.strip() for token in sentence_list if token.strip()]
    splited_dict = process_sentences(sentence_list=sentence_list, min_length_for_split=sentence_settings['min_length_for_split'], chunk_size=sentence_settings['chunk_size'])
    model = get_model(config_data=settings['summary'])
    summary_template = settings['summary']['summary_template']
    summary_results = []

    for i in splited_dict:
        combined_text = ""
        for item in i:
            for key, value in item.items():
                combined_text += str(value) + " "
        combined_text = combined_text.strip()

        prompt = get_template(str(summary_template), combined_text)
        chain = LLMChain(llm=model, prompt=prompt)
        response = chain.run({"text": ''})
        parsed_data = json.loads(response)
        summary_results.append(parsed_data['summary'])

    single_summary = ''.join(summary_results)

    return single_summary



def get_model(config_data) -> ChatOpenAI:
        """모델 구성에 따라 ChatOpenAI 인스턴스를 생성하고 반환합니다.

        주어진 구성 데이터(LlmItem)를 기반으로, 특정 모델의 파라미터(온도, 최대 토큰 수, 요청 시간 제한 등)를 설정하여 ChatOpenAI 모델 인스턴스를 초기화합니다.

        Args:
            config_data (LlmItem): 모델 구성 데이터를 담고 있는 객체. 모델 이름, 온도, 최대 토큰 수, 요청 시간 제한, 응답 형식 등의 정보를 포함합니다.

        Returns:
            ChatOpenAI: 초기화된 ChatOpenAI 모델 인스턴스.

        Example:
            config = LlmItem(model="gpt-3.5-turbo", temperature=0.7, max_tokens=100, request_timeout=30, response_format="text")
            model_instance = _get_model(config)
            print(model_instance)
        """

        config_data = LlmItem(**config_data)

        model_configs = {
            config_data.model: {
                "temperature": float(config_data.temperature),
                "max_tokens": int(config_data.max_tokens),
                "request_timeout": int(config_data.request_timeout),
                "model_kwargs": {
                "response_format": config_data.response_format},
                
                # "callbacks": [handler],
                # "metadata": dict(callback_data),
            },
        }
        return ChatOpenAI(model=config_data.model, **model_configs[config_data.model])



def get_template(template, content):

    return ChatPromptTemplate.from_messages([
            ("system", f"text: {template}"),
            ("human", f"Summarize the following text: {content}")
        ])


def chat_gpt(single_summary,user_input:str):

    prompt_template =ChatPromptTemplate(
    messages=[
        MessagesPlaceholder(variable_name="history"),
        HumanMessage(content="{user_input} + Answer in Korean. Use 'json' format for the response.")
    ]
    )
    model = get_model(config_data=settings['summary'])
    chain = LLMChain(llm=model, prompt=prompt_template)
    history_template = settings['summary']['summary_template']
    initial_message = SystemMessage(content=f"text: {single_summary} + {history_template}")
    history = [initial_message]
    history.append(HumanMessage(content=user_input))
    response = chain.run(history=history, user_input=user_input)
    return response