import grpc
import os
import zkp_auth_pb2
import zkp_auth_pb2_grpc

# Define INT64_MAX constant
INT64_MAX = 2**63 - 1
INT64_MIN = -2**63

def safe_int64(value):
    """Ensure the value is within the int64 range"""
    if value > INT64_MAX or value < INT64_MIN:
        raise ValueError("Value out of range for int64")
    return value

# TODO - remove need for Int range checking when implementing BigInts for bonus points

def register(stub, user, x, g, h):
    y1 = pow(g, x, INT64_MAX)
    y2 = pow(h, x, INT64_MAX)
    y1 = safe_int64(y1)
    y2 = safe_int64(y2)
    print(f"Registering {user}: y1={y1}, y2={y2}")
    response = stub.Register(zkp_auth_pb2.RegisterRequest(user=user, y1=y1, y2=y2))
    print("Register Response:", response)

def authenticate(stub, user, x, g, h):
    r1 = pow(g, x, INT64_MAX)
    r2 = pow(h, x, INT64_MAX)
    r1 = safe_int64(r1)
    r2 = safe_int64(r2)
    print(f"Authenticating {user}: r1={r1}, r2={r2}")
    challenge_response = stub.CreateAuthenticationChallenge(
        zkp_auth_pb2.AuthenticationChallengeRequest(user=user, r1=r1, r2=r2)
    )
    auth_id = challenge_response.auth_id
    c = challenge_response.c
    s = (c * x + x) % INT64_MAX
    s = safe_int64(s)
    print(f"Challenge: auth_id={auth_id}, c={c}, s={s}")
    answer_response = stub.VerifyAuthentication(
        zkp_auth_pb2.AuthenticationAnswerRequest(auth_id=auth_id, s=s)
    )
    print("Authentication Response:", answer_response)

def run():
    host = os.getenv('HOST', 'localhost')
    with grpc.insecure_channel(host + ':50051') as channel:
        stub = zkp_auth_pb2_grpc.AuthStub(channel)
        user = "test_user"
        x = 12345
        g = 2
        h = 3
        register(stub, user, x, g, h)
        authenticate(stub, user, x, g, h)

if __name__ == '__main__':
    run()
