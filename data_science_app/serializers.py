from data_science_app.models import Analysis, User
from rest_framework import serializers


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = ('id', 'user', 'name', 'ws', 'wd', 'wd_step', 'wd_start', 'wd_stop', 'ws_start', 'ws_stop',
                  'date_create', 'date_modified', 'file_data', 'file_zip')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
