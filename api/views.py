from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .ch_service import ch_client
from .serializers import (
    TopProductsRequestSerializer,
    AvgCheckRequestSerializer,
    PopularByAgeRequestSerializer,
    TopProductSerializer,
    AvgCheckSerializer,
    PopularByAgeSerializer,
)


class TopProductsAPIView(APIView):
    serializer_class = TopProductSerializer

    @extend_schema(
        request=None,
        responses={200: TopProductSerializer(many=True)},
        parameters=[TopProductsRequestSerializer],
    )
    def get(self, request):
        request_serializer = TopProductsRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        params = request_serializer.validated_data

        where = []
        if params.get("start"):
            where.append(f"order_datetime >= toDateTime('{params['start']}')")
        if params.get("end"):
            where.append(f"order_datetime < toDateTime('{params['end']}')")
        if params.get("category_id"):
            where.append(f"product_category_id = {params['category_id']}")
        where_clause = " AND ".join(where) if where else "1=1"

        sql = f"""
            SELECT product_id, product_title, product_category_title,
                   sum(amount) AS total_amount,
                   sum(total_price) AS total_revenue,
                   countDistinct(order_id) AS order_count
            FROM orders_for_analytics
            WHERE {where_clause}
            GROUP BY product_id, product_title, product_category_title
            ORDER BY total_amount DESC
            LIMIT {params['limit']}
        """
        client = ch_client()
        result = client.query(sql)

        columns = ['product_id', 'product_title', 'product_category_title', 'total_amount', 'total_revenue', 'order_count']
        rows = [dict(zip(columns, row)) for row in result.result_rows]

        return Response(self.serializer_class(rows, many=True).data)


class AvgCheckAPIView(APIView):
    serializer_class = AvgCheckSerializer

    @extend_schema(
        request=None,
        responses={200: AvgCheckSerializer},
        parameters=[AvgCheckRequestSerializer],
    )
    def get(self, request):
        request_serializer = AvgCheckRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        params = request_serializer.validated_data

        where = []
        if params.get("start"):
            where.append(f"order_datetime >= toDateTime('{params['start']}')")
        if params.get("end"):
            where.append(f"order_datetime < toDateTime('{params['end']}')")
        where_clause = " AND ".join(where) if where else "1=1"

        sql = f"""
            SELECT avg(total_price) AS avg_check,
                   sum(total_price) AS total_revenue,
                   countDistinct(order_id) AS orders_count
            FROM orders_for_analytics
            WHERE {where_clause}
        """
        client = ch_client()
        result = client.query(sql)

        columns = ['avg_check', 'total_revenue', 'orders_count']
        row_dict = dict(zip(columns, result.result_rows[0])) if result.result_rows else {}

        return Response(self.serializer_class(row_dict).data)


class PopularByAgeAPIView(APIView):
    serializer_class = PopularByAgeSerializer

    @extend_schema(
        request=None,
        responses={200: PopularByAgeSerializer},
        parameters=[PopularByAgeRequestSerializer],
    )
    def get(self, request):
        request_serializer = PopularByAgeRequestSerializer(data=request.query_params)
        request_serializer.is_valid(raise_exception=True)
        params = request_serializer.validated_data

        where = []
        if params.get("start"):
            where.append(f"order_datetime >= toDateTime('{params['start']}')")
        if params.get("end"):
            where.append(f"order_datetime < toDateTime('{params['end']}')")
        where.append(f"customer_age BETWEEN {params['age_from']} AND {params['age_to']}")
        where_clause = " AND ".join(where)

        sql = f"""
            SELECT product_id, product_title, sum(amount) AS total_amount
            FROM orders_for_analytics
            WHERE {where_clause}
            GROUP BY product_id, product_title
            ORDER BY total_amount DESC
            LIMIT {params['limit']}
        """
        client = ch_client()
        result = client.query(sql)

        columns = ['product_id', 'product_title', 'total_amount']
        rows = [dict(zip(columns, row)) for row in result.result_rows]

        result_data = {
            f"{params['age_from']}-{params['age_to']}": rows
        }

        return Response(self.serializer_class({"data": result_data}).data)
