from rest_framework import serializers
from .models import QueryRecord, SentimentRecord


class QueryRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = QueryRecord
        fields = ['query', 'last_updated']


class SentimentRecordSerializer(serializers.ModelSerializer):

    class Meta:
        model = SentimentRecord
        fields = ['query', 'date', 'score']
