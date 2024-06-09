import grpc
import random
import zkp_auth_pb2
import zkp_auth_pb2_grpc
from concurrent import futures

# Define INT64_MAX constant
INT64_MAX = 2**63 - 1

class AuthServicer(zkp_auth_pb2_grpc.AuthServicer):
    def __init__(self):
        self.users = {}
        self.auth_challenges = {}

    def Register(self, request, context):
        self.users[request.user] = (request.y1, request.y2)
        print(f"Registered {request.user}: y1={request.y1}, y2={request.y2}")
        return zkp_auth_pb2.RegisterResponse()

    def CreateAuthenticationChallenge(self, request, context):
        auth_id = f"{request.user}_{random.randint(1000, 9999)}"
        c = random.randint(1, 100000)
        self.auth_challenges[auth_id] = (request.r1, request.r2, c, request.user)
        print(f"Challenge for {request.user}: auth_id={auth_id}, r1={request.r1}, r2={request.r2}, c={c}")
        return zkp_auth_pb2.AuthenticationChallengeResponse(auth_id=auth_id, c=c)

    def VerifyAuthentication(self, request, context):
        r1, r2, c, user = self.auth_challenges.get(request.auth_id, (None, None, None, None))
        if r1 is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("Auth ID not found")
            return zkp_auth_pb2.AuthenticationAnswerResponse()

        y1, y2 = self.users.get(user, (None, None))
        if y1 is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("User not found")
            return zkp_auth_pb2.AuthenticationAnswerResponse()

        # Verification logic
        g, h = 2, 3  # Public values
        s = request.s

        # Check if g^s == r1 * (y1^c) % INT64_MAX and h^s == r2 * (y2^c) % INT64_MAX
        lhs_g = pow(g, s, INT64_MAX)
        rhs_g = (r1 * pow(y1, c, INT64_MAX)) % INT64_MAX
        lhs_h = pow(h, s, INT64_MAX)
        rhs_h = (r2 * pow(y2, c, INT64_MAX)) % INT64_MAX

        print(f"Verification: g^s={lhs_g}, r1 * y1^c={rhs_g}, h^s={lhs_h}, r2 * y2^c={rhs_h}")

        if lhs_g == rhs_g and lhs_h == rhs_h:
            return zkp_auth_pb2.AuthenticationAnswerResponse(session_id="valid_session")
        else:
            return zkp_auth_pb2.AuthenticationAnswerResponse(session_id="invalid_session")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    zkp_auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
