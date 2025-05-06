import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("🎨 AI Photo Editor MVP")

def display_result(response):
    if "result_url" in response:
        st.image(response["result_url"], caption="Результат", use_column_width=True)  # Исправлено здесь
    elif "error" in response:
        st.error(f"Ошибка: {response['error']}")

uploaded_file = st.file_uploader("Загрузите изображение", type=["jpg", "jpeg", "png"])

if uploaded_file:
    col1, col2 = st.columns(2)
    
    with col1:
        st.header("Оригинал")
        st.image(uploaded_file, use_column_width=True)  # Исправлено здесь
    
    with col2:
        st.header("Действия")
        
        # Основные операции
        operation = st.radio(
            "Основная операция",
            ["Без изменений", "Удалить фон", "Чёрно-белый фильтр"]
        )
        
        # Дополнительные фильтры
        st.subheader("Дополнительные фильтры")
        blur = st.checkbox("Размытие")
        blur_level = st.slider("Уровень размытия", 1, 15, 5, step=2) if blur else 0
        
        adjust = st.checkbox("Яркость/Контраст")
        brightness = st.slider("Яркость", -100, 100, 0) if adjust else 0.0
        contrast = st.slider("Контраст", 0.1, 3.0, 1.0, 0.1) if adjust else 1.0
        
        if st.button("Применить"):
            with st.spinner("Обработка..."):
                try:
                    params = {
                        "operation": "none",
                        "blur": blur_level,
                        "brightness": brightness,
                        "contrast": contrast
                    }
                    
                    if operation == "Удалить фон":
                        params["operation"] = "remove-bg"
                    elif operation == "Чёрно-белый фильтр":
                        params["operation"] = "grayscale"
                    
                    response = requests.post(
                        "http://0.0.0.0:8000/process",
                        files={"file": uploaded_file},
                        data=params
                    ).json()
                    
                    # Добавляем домен к URL
                    if "result_url" in response:
                        response["result_url"] = f"http://0.0.0.0:8000{response['result_url']}"
                    
                    display_result(response)
                
                except Exception as e:
                    st.error(f"Ошибка соединения: {str(e)}")