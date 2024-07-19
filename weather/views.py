from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.status import (HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_503_SERVICE_UNAVAILABLE,
                                   HTTP_500_INTERNAL_SERVER_ERROR)

from weather.services import format_response
from weather.weather_service import get_weather_four_days, ServiceUnavailableError


def index(request):
    return render(request, 'index.html')


@api_view(['GET'])
def weather(request):
    city = request.query_params.get('city')
    if city:
        try:
            data = get_weather_four_days(city)
        except ValueError as e:
            return Response({"code": 404, "error": "Nod Found", "message": str(e)}, HTTP_404_NOT_FOUND)

        except ServiceUnavailableError as e:
            return Response({"code": 503, "error": "Service Unavailable", "message": str(e)},
                            HTTP_503_SERVICE_UNAVAILABLE)

        except RuntimeError as e:
            return Response({"code": 503, "error": "Internal Server Error", "message": str(e)},
                            HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            return Response({"code": 503, "error": "Service Unavailable", "message": "Произошла непредвиденная ошибка"},
                            HTTP_503_SERVICE_UNAVAILABLE)

        format_data = format_response(data)

        return Response(format_data, HTTP_200_OK)
    return Response({"code": 400, "error": "Validation error", "message": "Отсутствующий или пустой параметр city"},
                    HTTP_400_BAD_REQUEST
                    )
