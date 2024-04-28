from grpc_interceptor import ServerInterceptor

class ErrorLogger(ServerInterceptor):
    def intercept(self, method, request, context, method_name):
        try:
            print("----- intercptor ------")
            return method(request, context)
        except Exception as e:
            self.log_error(e)
            raise

    def log_error(self, e: Exception) -> None:
        print(e)