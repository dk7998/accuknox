from rest_framework import serializers

from .typings import REQUEST


class DKModelSerializer(serializers.ModelSerializer):
    
    @property
    def _request(self) -> REQUEST:
        return self.context.get("request")