from rest_framework import serializers


class TopProductsRequestSerializer(serializers.Serializer):
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    limit = serializers.IntegerField(default=10, min_value=1, max_value=100)
    category_id = serializers.IntegerField(required=False)


class AvgCheckRequestSerializer(serializers.Serializer):
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)


class PopularByAgeRequestSerializer(serializers.Serializer):
    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    age_from = serializers.IntegerField(required=True, min_value=18)
    age_to = serializers.IntegerField(required=True, min_value=18)
    limit = serializers.IntegerField(default=10, min_value=1, max_value=100)

    def validate(self, data):
        data = super().validate(data)
        if data["age_from"] > data["age_to"]:
            raise serializers.ValidationError("age_from не может быть больше age_to")
        return data


class TopProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_title = serializers.CharField()
    product_category_title = serializers.CharField()
    total_amount = serializers.IntegerField()
    total_revenue = serializers.IntegerField()
    order_count = serializers.IntegerField()


class AvgCheckSerializer(serializers.Serializer):
    avg_check = serializers.FloatField()
    total_revenue = serializers.IntegerField()
    orders_count = serializers.IntegerField()


class PopularProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    product_title = serializers.CharField()
    total_amount = serializers.IntegerField()


class PopularByAgeSerializer(serializers.Serializer):
    data = serializers.DictField(
        child=PopularProductSerializer(many=True)
    )
