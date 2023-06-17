from rest_framework import serializers

class CategoriesSerializer(serializers.Serializer):
    class Meta:
        ref_name = "CategoriesSerializer"

class ModelPredictionSerializer(serializers.Serializer):
    class Meta:
        ref_name = "ModelPredictionSerializer"
    model_name = serializers.CharField()
    text = serializers.CharField()