from django.views.generic import TemplateView
import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


class HomeView(TemplateView):
    template_name = "home.html"


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES["file"]
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg"]:
            return JsonResponse({"error": "Wrong file format"})

        # 파일 저장 경로 설정
        upload_path = os.path.join(settings.MEDIA_ROOT, "uploads", file_obj.name)

        # 파일 저장
        with open(upload_path, "wb+") as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        # TinyMCE에 반환할 이미지 URL
        location = settings.MEDIA_URL + "uploads/" + file_obj.name
        return JsonResponse({"location": location})

    return JsonResponse({"error": "Wrong request"})
