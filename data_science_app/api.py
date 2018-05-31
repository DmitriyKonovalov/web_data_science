from data_science_app.serializers import AnalysisSerializer, UserSerializer
from django.http import JsonResponse
from .models import Analysis, User


def client_get_analysis(request):
    analyses = AnalysisSerializer(Analysis.objects.all().order_by('-date_modified'), many=True,
                                  context={'request': request}).data
    return JsonResponse({'analyses': analyses})


def client_get_users(request):
    users = UserSerializer(User.objects.all().order_by('id'), many=True, context={'request': request}).data
    return JsonResponse({'users': users})
