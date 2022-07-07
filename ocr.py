import easyocr as ocr  #OCR
import streamlit as st  #Web App
from PIL import Image #Image Processing
import numpy as np #Image Processing 

from gtts import gTTS


st.title("Easy OCR - Extract Text from Images")
st.markdown("## Optical Character Recognition - Using `easyocr`, `streamlit`")
st.markdown("")
image = st.file_uploader(label = "Upload your image here",type=['png','jpg','jpeg'])

words_negative = ['envidia', 'orgullo', 'odio', 'ira', 'miedo']
keyword = 'valor'
keyword_exists = False


@st.cache
def load_model(): 
    reader = ocr.Reader(['en'], model_storage_directory='.')
    return reader 

reader = load_model()

if image is not None:
    input_image = Image.open(image)
    st.image(input_image)

    with st.spinner('Loading...'):
        result = reader.readtext(np.array(input_image))
        result_text = []
        words_prohibited = []

        for text in result:
            word = text[1]
            result_text.append(word)
            if word.lower() in words_negative:
                words_prohibited.append(word)

            if keyword.lower() in word.lower():
              keyword_exists = True

        st.write(result_text)
    
    language = 'es'
    if keyword_exists:
      keyword_message = 'Sí se encuentra la palabra clave: ' + keyword
      st.success(keyword_message)

      audio_keyword_file_name = 'words_prohibited.mp3'
      audio_keyword = gTTS(text=keyword_message, lang=language, slow=False)
      audio_keyword.save(audio_keyword_file_name)
      audio_keyword_file = open(audio_keyword_file_name, 'rb')
      audio_keyword_bytes = audio_keyword_file.read()
      st.audio(audio_keyword_bytes, format='audio/ogg')

    if len(words_prohibited) > 0:
      words_prohibited_message = 'Palabras no permitidas encontradas: ' + ', '.join(words_prohibited)
      st.error(words_prohibited_message)
    
      audio_words_prohibited_file_name = 'words_prohibited.mp3'
      audio_words_prohibited = gTTS(text=words_prohibited_message, lang=language, slow=False)
      audio_words_prohibited.save(audio_words_prohibited_file_name)
      audio_words_prohibited_file = open(audio_words_prohibited_file_name, 'rb')
      audio_words_prohibited_bytes = audio_words_prohibited_file.read()
      st.audio(audio_words_prohibited_bytes, format='audio/ogg')

    st.info("Texto completo:")
    audio_result_file_name = 'result.mp3'
    audio_result = gTTS(text=' '.join(result_text), lang=language, slow=False)
    audio_result.save(audio_result_file_name)
    audio_result_file = open(audio_result_file_name, 'rb')
    audio_result_bytes = audio_result_file.read()
    st.audio(audio_result_bytes, format='audio/ogg')
else:
    st.write('Upload an Image')

st.caption("Modificado por estudiantes UTP - ITD")