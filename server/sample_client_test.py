from protobuf_generated.recommendations_pb2 import BookCategory,RecommendationRequest
from protobuf_generated.recommendations_pb2_grpc import RecommendationsStub
import grpc
import time

channel=grpc.insecure_channel("localhost:5001")

grpc_api=RecommendationsStub(channel)

req=RecommendationRequest(user_id=3,category=BookCategory.SCIENCE_FICTION ,max_results=3)
i=0
s=time.time()
while i<1:
    try:
        res=grpc_api.Recommend(req)
        #print(f"respone - {i}\n {res}")
    except KeyboardInterrupt:
        print('client stoped')
    i+=1
    
print(f'\n grpc testing\n  total time for 10,000 calls : {time.time() - s} \n')    
channel.close()