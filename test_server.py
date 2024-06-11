import grpc
import unittest
import zkp_auth_pb2
import zkp_auth_pb2_grpc
from concurrent import futures
from server import AuthServicer, INT64_MAX

class TestAuthServicer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Set up the server
        cls.server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
        zkp_auth_pb2_grpc.add_AuthServicer_to_server(AuthServicer(), cls.server)
        cls.port = cls.server.add_insecure_port('localhost:0')
        cls.server.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop(None)

    def setUp(self):
        self.channel = grpc.insecure_channel(f'localhost:{self.port}')
        self.stub = zkp_auth_pb2_grpc.AuthStub(self.channel)

    def test_register_and_challenge(self):
        g, h = 2, 3  # Public values
        x = 12345
        r1 = 3
        r2 = 4

        # Calculate y1 and y2
        y1 = pow(g, x, INT64_MAX)
        y2 = pow(h, x, INT64_MAX)

        print(f"Calculated y1: {y1}")
        print(f"Calculated y2: {y2}")

        # Test Registration
        register_request = zkp_auth_pb2.RegisterRequest(user="test_user", y1=y1, y2=y2)
        register_response = self.stub.Register(register_request)
        self.assertIsInstance(register_response, zkp_auth_pb2.RegisterResponse)

        # Test CreateAuthenticationChallenge
        challenge_request = zkp_auth_pb2.AuthenticationChallengeRequest(
            user="test_user", r1=r1, r2=r2
        )
        challenge_response = self.stub.CreateAuthenticationChallenge(challenge_request)
        self.assertIsInstance(challenge_response, zkp_auth_pb2.AuthenticationChallengeResponse)
        auth_id = challenge_response.auth_id
        c = challenge_response.c

        print(f"Challenge for test_user: auth_id={auth_id}, r1={r1}, r2={r2}, c={c}")

        # Test VerifyAuthentication
        s = (c * x + x) % INT64_MAX

        print(f"Calculated s: {s}")

        # Calculate expected values for debugging
        lhs_g = pow(g, s, INT64_MAX)
        lhs_h = pow(h, s, INT64_MAX)
        y1_c_mod = pow(y1, c, INT64_MAX)
        y2_c_mod = pow(y2, c, INT64_MAX)
        rhs_g = (r1 * y1_c_mod) % INT64_MAX
        rhs_h = (r2 * y2_c_mod) % INT64_MAX

        print(f"lhs_g (g^s % INT64_MAX): {lhs_g}")
        print(f"lhs_h (h^s % INT64_MAX): {lhs_h}")
        print(f"y1^c % INT64_MAX: {y1_c_mod}")
        print(f"y2^c % INT64_MAX: {y2_c_mod}")
        print(f"rhs_g (r1 * y1^c % INT64_MAX): {rhs_g}")
        print(f"rhs_h (r2 * y2^c % INT64_MAX): {rhs_h}")

        verify_request = zkp_auth_pb2.AuthenticationAnswerRequest(auth_id=auth_id, s=s)
        verify_response = self.stub.VerifyAuthentication(verify_request)

        print(f"Test VerifyAuthentication response: {verify_response.session_id}")
        self.assertEqual(verify_response.session_id, "valid_session")

        # This test is currently failing on one of the above lines; I am still troubleshooting it
        # I believe it is an issue with the final calculations, specifically the modulus of INT64_MAX
        # This might be solved once I introduce BigInts, so I'm not trying to waste too much time on it

    def test_invalid_auth_id(self):
        # Test VerifyAuthentication with invalid auth_id
        verify_request = zkp_auth_pb2.AuthenticationAnswerRequest(auth_id="invalid_auth_id", s=12345)
        try:
            verify_response = self.stub.VerifyAuthentication(verify_request)
        except grpc.RpcError as e:
            self.assertEqual(e.code(), grpc.StatusCode.NOT_FOUND)

    def test_invalid_user(self):
        # Test CreateAuthenticationChallenge with unregistered user
        challenge_request = zkp_auth_pb2.AuthenticationChallengeRequest(
            user="invalid_user", r1=12345, r2=67890
        )
        try:
            self.stub.CreateAuthenticationChallenge(challenge_request)
        except grpc.RpcError as e:
            self.assertEqual(e.code(), grpc.StatusCode.NOT_FOUND)

if __name__ == '__main__':
    unittest.main()
