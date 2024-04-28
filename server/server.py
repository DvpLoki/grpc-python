from protobuf_generated.recommendations_pb2  import ( BookCategory,BookRecommendation, RecommendationResponse)
from   protobuf_generated.recommendations_pb2_grpc import (RecommendationsServicer,add_RecommendationsServicer_to_server)
from concurrent import futures
import random
import time
import grpc
import threading
from interceptor import ErrorLogger

books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="The Maltese Falcon"),
        BookRecommendation(id=2, title="Murder on the Orient Express"),
        BookRecommendation(id=3, title="The Hound of the Baskervilles"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(
            id=4, title="The Hitchhiker's Guide to the Galaxy"
        ),
        BookRecommendation(id=5, title="Ender's Game"),
        BookRecommendation(id=6, title="The Dune Chronicles"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(
            id=7, title="The 7 Habits of Highly Effective People"
        ),
        BookRecommendation(
            id=8, title="How to Win Friends and Influence People"
        ),
        BookRecommendation(id=9, title="Man's Search for Meaning"),
    ],
}


class RecommendationService(RecommendationsServicer):
    
    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND,"Category not found")
        books=books_by_category[request.category]
        num_results=min(request.max_results,len(books))    
        res=random.sample(books,num_results)
        return RecommendationResponse(recommendations=res)
    
def Server():
    interceptors=[ErrorLogger()]
    server=grpc.server(futures.ThreadPoolExecutor(max_workers=3),interceptors=interceptors)
    add_RecommendationsServicer_to_server(RecommendationService(),server)
    server.add_insecure_port("0.0.0.0:5001")
    server.start()
    print("server started .. on port 5001")
    try: 
        while True:
            print(f"server on :threads {threading.active_count()}")
            time.sleep(10)
    except KeyboardInterrupt:
        print(" server stopped : keyboardInterrpt") 
        server.stop(0)       


if __name__ == "__main__":
    Server()