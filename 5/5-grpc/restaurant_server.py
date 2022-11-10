import grpc
import sys
from proto import restaurant_pb2
from proto import restaurant_pb2_grpc
from concurrent import futures

RESTAURANT_ITEMS_FOOD = ["chips", "fish", "burger", "pizza", "pasta", "salad"]
RESTAURANT_ITEMS_DRINK = ["water", "fizzy drink", "juice", "smoothie", "coffee", "beer"]
RESTAURANT_ITEMS_DESSERT = ["ice cream", "chocolate cake", "cheese cake", "brownie", "pancakes", "waffles"]


class Restaurant(restaurant_pb2_grpc.RestaurantServicer):

    def FoodOrder(self, request, context):
        if len([item for item in request.items if item not in RESTAURANT_ITEMS_FOOD]) > 0:
            return restaurant_pb2.RestaurantResponse(
                orderID=request.orderID,
                status='REJECTED'
            )
        
        return restaurant_pb2.RestaurantResponse(
                orderID=request.orderID,
                status='ACCEPTED'
            )

    def DrinkOrder(self, request, context):
        if len([item for item in request.items if item not in RESTAURANT_ITEMS_DRINK]) > 0:
            return restaurant_pb2.RestaurantResponse(
                orderID=request.orderID,
                status='REJECTED'
            )
        
        return restaurant_pb2.RestaurantResponse(
                orderID=request.orderID,
                status='ACCEPTED'
            )

    def DessertOrder(self, request, context):
        if len([item for item in request.items if item not in RESTAURANT_ITEMS_DESSERT]) > 0:
            return restaurant_pb2.RestaurantResponse(
                orderID=request.orderID,
                status='REJECTED'
            )
        
        return restaurant_pb2.RestaurantResponse(
                orderID=request.orderID,
                status='ACCEPTED'
            )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    restaurant_pb2_grpc.add_RestaurantServicer_to_server(
        Restaurant(), server
    )
    port = sys.argv[1]
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
