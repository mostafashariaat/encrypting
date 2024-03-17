import json
import ast
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from mostafa.serializers import MostafaSerializer
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from Crypto.Util.Padding import pad, unpad


# Create your views here.

class MostafaViewSet(ReadOnlyModelViewSet):
    serializer_class = MostafaSerializer

    def encrypt(self, data):
        key = get_random_bytes(16)  # 128-bit encryption key
        cipher = AES.new(key, AES.MODE_ECB)

        # Pad the data to a multiple of block size
        padded_data = pad(str(data).encode('utf-8'), AES.block_size)

        ciphertext = cipher.encrypt(padded_data)

        final_data = base64.b64encode(ciphertext).decode()

        encrypted_data = {
            "ciphertext": final_data,
            "key": base64.b64encode(key).decode(),
        }

        return encrypted_data

    def decrypt(self, data):
        final_data_decoded = base64.b64decode(data['ciphertext'])
        cipher = AES.new(base64.b64decode(data['key']), AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(final_data_decoded), AES.block_size)
        data = decrypted_data.decode()
        # data = data.replace("'", '"')
        data = json.dumps(data)
        print(json.dumps(ast.literal_eval(data)))
        return data

        # return json.load(data)  # return decrypted

    def list(self, request, *args, **kwargs):
        data = {
            "name": "mostafa",
        }
        encrypted_data = self.encrypt(data)
        encrypted_data2 = self.encrypt(encrypted_data)  # Encrypting the encrypted data

        decrypted_data = self.decrypt(encrypted_data2)

        return Response(data={"encrypted_data": encrypted_data2, "result": encrypted_data})
