
from django.http import Http404, HttpResponse
from rest_framework.exceptions import PermissionDenied
from data_science_app.models import Analysis
from data_science_app.permissions import IsOwnerOrReadOnly
from data_science_app.serializers import UserSerializer, AnalysisSerializer
from django.core.files import File
from rest_framework import viewsets, status
from rest_framework.authentication import BasicAuthentication, SessionAuthentication, TokenAuthentication

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ds_class.ds_execute import WebDataScienceExecute


class AnalysisViewSet(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication)
    #authentication_classes = (SessionAuthentication, BasicAuthentication)
    queryset = Analysis.objects.all()
    serializer_class = AnalysisSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    @action(detail=True)
    def execute(self, request, *args, **kwargs):
        analysis = self.get_object()
        if request.user == analysis.user:
            try:
                execute = WebDataScienceExecute(analysis)
                execute.execute()
                return Response({}, status=status.HTTP_200_OK)
            except:
                raise Http404
        raise PermissionDenied

    @action(methods=['post'], detail=True)
    def load_file_data(self, request, *args, **kwargs):
        analysis = self.get_object()
        if request.user == analysis.user:
            try:
                file_name = request.data['file_path']
                file_data = File(open(file_name, 'r'))
                analysis.file_data.save(f'{analysis.name}.csv', file_data, save=True)
                file_data.close()
                return Response({}, status=status.HTTP_200_OK)
            except:
                raise Http404
        raise PermissionDenied

    @action(detail=True)
    def download(self, request, *args, **kwargs):
        analysis = self.get_object()
        if request.user == analysis.user:
            if analysis.file_zip != "":
                response = HttpResponse(analysis.file_zip)
                response["Content-Disposition"] = 'attachment; filename="{}.zip"'.format(analysis.name)
                return response
            raise Http404
        raise PermissionDenied

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


