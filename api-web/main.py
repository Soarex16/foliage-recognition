import asyncio

import uvicorn
from fastapi import FastAPI, UploadFile, Depends, Request, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import validator, BaseModel, ValidationError
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseSettings

from recognition import ImageRecognitionPipeline
from utils.as_form import as_form
from utils import environment

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Settings(BaseSettings):
    """Base application settings"""
    environment: str = environment.DEV


settings = Settings()

ALLOWED_IMAGE_EXTENSIONS = ["image/png", "image/jpg", "image/jpeg"]


@as_form
class MultispectreRecognitionInputModel(BaseModel):
    """Input DTO"""
    f470: UploadFile
    f540: UploadFile
    f635: UploadFile
    f735: UploadFile
    f880: UploadFile

    @validator('*')
    def check_is_image(cls, v: UploadFile):
        if v.content_type not in ALLOWED_IMAGE_EXTENSIONS:
            raise ValueError('file must be png or jpeg image')
        return v


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler"""
    error_detail = exc if settings.environment == environment.DEV else None
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=jsonable_encoder({"detail": error_detail, "error": "Internal server error"}),
    )


@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Valdation exception handler"""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "error": "Validation error"}),
    )


@app.post("/recognize/img")
async def recognize_img_resp(
        form: MultispectreRecognitionInputModel = Depends(MultispectreRecognitionInputModel.as_form),
        recognizer: ImageRecognitionPipeline = Depends(ImageRecognitionPipeline)):
    files = await asyncio.gather(
        form.f470.read(),
        form.f540.read(),
        form.f635.read(),
        form.f735.read(),
        form.f880.read()
    )

    res = recognizer.recognize(files)
    result_image = recognizer.to_image(res)
    result_image.seek(0)
    return StreamingResponse(result_image, media_type="image/png")


@app.post("/recognize/json")
async def recognize_json_resp(
        form: MultispectreRecognitionInputModel = Depends(MultispectreRecognitionInputModel.as_form),
        recognizer: ImageRecognitionPipeline = Depends(ImageRecognitionPipeline)):
    files = await asyncio.gather(
        form.f470.read(),
        form.f540.read(),
        form.f635.read(),
        form.f735.read(),
        form.f880.read()
    )

    res = recognizer.recognize(files)
    response = recognizer.to_json(res)

    return JSONResponse(response)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
