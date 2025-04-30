# backend.py
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from rembg import remove
import cv2
import numpy as np
import os
import uuid

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

def generate_unique_filename(original_filename: str) -> str:
    unique_id = str(uuid.uuid4())[:8]
    return f"{unique_id}_{original_filename}"

@app.post("/process")
async def process_image(
    file: UploadFile = File(...),
    operation: str = Form("none"),
    blur: int = Form(0),
    brightness: float = Form(0.0),
    contrast: float = Form(1.0)
):
    try:
        unique_filename = generate_unique_filename(file.filename)
        output_path = f"static/result_{unique_filename}"
        
        # Чтение изображения
        img_bytes = await file.read()
        image = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        
        # Основная операция
        if operation == "remove-bg":
            result = remove(img_bytes)
            result = cv2.imdecode(np.frombuffer(result, np.uint8), cv2.IMREAD_COLOR)
        elif operation == "grayscale":
            result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            result = cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)
        else:
            result = image.copy()
        
        # Дополнительные фильтры
        if blur > 0:
            result = cv2.GaussianBlur(result, (blur*2+1, blur*2+1), 0)
        
        result = cv2.convertScaleAbs(result, alpha=contrast, beta=brightness)
        
        # Сохранение результата
        cv2.imwrite(output_path, result)
        return {"result_url": f"/static/result_{unique_filename}"}
    
    except Exception as e:
        return {"error": str(e)}

if not os.path.exists("static"):
    os.makedirs("static")