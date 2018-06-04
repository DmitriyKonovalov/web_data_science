from rest_framework import serializers

from data_science_app.models import Analysis


class AnalysisSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='User')

    class Meta:
        model = Analysis
        fields = ('id', 'url', 'user', 'name', 'ws', 'wd', 'wd_step', 'wd_start', 'wd_stop', 'ws_start', 'ws_stop',
                  'date_create', 'date_modified', 'file_data', 'file_zip')
