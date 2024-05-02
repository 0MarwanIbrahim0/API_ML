from fastapi import FastAPI , File, UploadFile, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json
from typing import List
from OCR import Read_Text


app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
data ={}
@app.post("/upload", summary="Upload an image file and read text from it", response_model=dict)
async def upload_image(
    file: UploadFile = File(...),
    required_values: List[str] = Query(
        ["HGB", "RBC", "HCT", "WBC"],
        description="List of required values to extract from the image",
        alias="values",
    ),
) -> dict:
    try:
        with open(f"uploads/{file.filename}", "wb") as buffer:
            buffer.write(await file.read())
    except Exception as e:
        return {"error": f"Failed to save file to disk: {e}"}

    try:
        data = Read_Text(f"uploads/{file.filename}")
    except Exception as e:
        return {"error": f"Failed to read text from file: {e}"}

    missing_values = [value for value in required_values if value not in data]
    if missing_values:
        return {"error": f"Missing required values: {', '.join(missing_values)}"}

    return data



# class InputData_heart(BaseModel):
#     age : int
#     sex : int
#     cp : int
#     restbp : int
#     chol : int
#     # fbs : int
#     restecg : int
#     maxhr : int
#     exang : int
#     oldpeak : float
#     slope : int
#     ca : int
#     thal : int
#     # target : bool
class InputData_kidney(BaseModel):
    age: int
    blood_urea: float
    ser_crea: float
    sodium: float
    potassium: float

@app.post("/predict_kidney")
async def predict(input_data_kidney: InputData_kidney):
    with open('Models/kidney_Model.joblib', 'rb') as f:
        model_kidney = pickle.load(f)
    
    # Prepare features for prediction
    features = [[input_data_kidney.age, input_data_kidney.blood_urea, input_data_kidney.ser_crea, input_data_kidney.sodium,
                 input_data_kidney.potassium]]
    
    # Make prediction
    prediction = model_kidney.predict(features)
    
    # Convert prediction to native Python integer
    prediction = int(prediction[0])
    
    return {"prediction": prediction}

# @app.post("/predict_heart")
# async def predict(input_data_heart: InputData_heart):
#     with open('Models/heart_update.pkl','rb') as f:
#         model_heart = pickle.load(f)
    
#     features = [[input_data_heart.age, input_data_heart.sex, input_data_heart.cp, input_data_heart.restbp,
#              input_data_heart.chol, input_data_heart.restecg, input_data_heart.maxhr,
#              input_data_heart.exang, input_data_heart.oldpeak,input_data_heart.slope, input_data_heart.ca,
#                  input_data_heart.thal]]

#     # Make prediction
#     prediction = model_heart.predict(features)
    
#     # Convert prediction to native Python integer
#     prediction = int(prediction[0])
    
#     return {"prediction": prediction}
