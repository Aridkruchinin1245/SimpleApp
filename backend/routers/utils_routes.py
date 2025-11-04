from fastapi import APIRouter, HTTPException
from backend.utils.weather_api import get_weather

router = APIRouter()

@router.get('/weather/{city_name}')
def make_weather(city_name:str):
    try:
        data = get_weather(city_name)
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Ошибка вывода погоды {e}')