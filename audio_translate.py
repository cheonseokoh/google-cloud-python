import sounddevice as sd
import numpy as np
from google.cloud import speech
from google.cloud import translate_v2 as translate

# Google Cloud Speech-to-Text 클라이언트 초기화
speech_client = speech.SpeechClient()

# Google Translate 클라이언트 초기화
translate_client = translate.Client()

def process_audio(indata, frames, time, status):
    """오디오 데이터를 Google Speech-to-Text API로 스트리밍"""
    if status:
        print("Status:", status)
    
    # 오디오 데이터를 NumPy 배열로 변환
    audio_data = np.frombuffer(indata, dtype=np.int16)

    # Google Speech-to-Text API로 전송할 데이터 준비
    audio = speech.RecognitionAudio(content=audio_data.tobytes())
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # PCM 16비트 오디오
        sample_rate_hertz=44100,  # 샘플레이트 44.1kHz
        language_code="zh-CN",  # 중국어 간체 (게임 오디오는 주로 중국어일 가능성)
    )

    try:
        # 오디오 데이터가 텍스트로 변환되는 부분
        response = speech_client.recognize(config=config, audio=audio)
        for result in response.results:
            text = result.alternatives[0].transcript
            print(f"인식된 텍스트: {text}")
            
            # 텍스트 번역
            translation = translate_client.translate(text, target_language='ko')  # 한국어로 번역
            print(f"번역된 텍스트: {translation['translatedText']}")
    except Exception as e:
        print(f"오류 발생: {e}")

# 오디오 캡처 시작
print("오디오 캡처를 시작합니다...")
with sd.InputStream(device='CABLE Input (VB-Audio Virtual Cable)',  # VB-Cable Input 장치 선택
                    samplerate=44100, channels=1, callback=process_audio):
    sd.sleep(60000)  # 60초 동안 오디오 캡처
