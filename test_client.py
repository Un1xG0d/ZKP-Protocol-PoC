import client
import unittest
import zkp_auth_pb2
import zkp_auth_pb2_grpc
from unittest.mock import patch, MagicMock

class TestClient(unittest.TestCase):
    @patch('zkp_auth_pb2_grpc.AuthStub')
    def test_register_and_authenticate(self, MockAuthStub):
        stub = MockAuthStub.return_value
        stub.Register.return_value = zkp_auth_pb2.RegisterResponse()
        stub.CreateAuthenticationChallenge.return_value = zkp_auth_pb2.AuthenticationChallengeResponse(auth_id='test_user_1234', c=54321)
        stub.VerifyAuthentication.return_value = zkp_auth_pb2.AuthenticationAnswerResponse(session_id='valid_session')

        with patch('grpc.insecure_channel') as mock_channel:
            mock_channel.return_value = MagicMock()
            client.run()

        stub.Register.assert_called_once()
        stub.CreateAuthenticationChallenge.assert_called_once()
        stub.VerifyAuthentication.assert_called_once()

if __name__ == '__main__':
    unittest.main()
