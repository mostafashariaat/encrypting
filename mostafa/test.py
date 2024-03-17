from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from mostafa.serializers import MostafaSerializer
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
from Crypto.Util.Padding import pad, unpad


def list(self, request, *args, **kwargs):
    queryset = self.get_queryset()
    serializer = self.get_serializer(self.paginate_queryset(queryset), many=True)

    data = serializer.data
    # ساخت کلید و آبجکت رمزنگاری برای رمز کردن ریسپانس در مرحله اول!
    first_key = get_random_bytes(16)
    cipher = AES.new(first_key, AES.MODE_ECB)

    # ساخت کلید و آبجکت رمزنگاری برای رمز کردن ریسپانس در مرحله دوم!
    # second_key = get_random_bytes(16)
    # second_cipher = AES.new(second_key, AES.MODE_ECB)

    # ساخت آبجکت رمزنگاری برای رمز کردن کلید در مرحله اول با استفاده از کلید ثابت داخل فایل .env
    # first_key_for_key = config('FIRST_KEY')
    # first_key_for_key_cipher = AES.new(first_key_for_key.encode(), AES.MODE_ECB)

    # ساخت آبجکت رمزنگاری برای رمز کردن کلید در مرحله دوم با استفاده از کلید ثابت داخل فایل .env
    # second_key_for_key = config('SECOND_KEY')
    # second_key_for_key_cipher = AES.new(second_key_for_key.encode(), AES.MODE_ECB)

    # ساخت پد دیتا برای رمز کردن کلید اول در مرحله اول
    # first_key_padded_data = pad(first_key, AES.block_size)
    # رمز گذاری کلید اول در مرحله اول
    # first_key_ciphertext = first_key_for_key_cipher.encrypt(first_key_padded_data)

    # ساخت پد دیتا برای رمز کردن کلید اول یکبار رمز شده
    # first_key_encrypted_padded_data = pad(first_key_ciphertext, AES.block_size)
    # # رمز گذاری کلید اول در مرحله دوم
    # first_key_encrypted_ciphertext = second_key_for_key_cipher.encrypt(first_key_encrypted_padded_data)

    # ساخت پد دیتا برای رمز کردن کلید دوم در مرحله اول
    # second_key_padded_data = pad(second_key, AES.block_size)
    # # رمز گذاری کلید دوم در مرحله اول
    # second_key_ciphertext = second_key_for_key_cipher.encrypt(second_key_padded_data)

    # ساخت پد دیتا برای رمز کردن کلید دوم یکبار رمز شده
    # second_key_encrypted_padded_data = pad(second_key_ciphertext, AES.block_size)
    # رمز گذاری کلید دوم در مرحله دوم
    # second_key_encrypted_ciphertext = first_key_for_key_cipher.encrypt(second_key_encrypted_padded_data)

    # رمز گذاری ریسپانس با استفاده از پد دیتا مرحله اول
    padded_data = pad(str(data).encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)

    # رمز گذاری ریسپانس رمز شده با استفاده از پد دیتا مرحله دوم
    # second_padded_data = pad(ciphertext, AES.block_size)
    # second_ciphertext = second_cipher.encrypt(second_padded_data)

    encrypted_final_data = base64.b64encode(ciphertext).decode()
    # encrypted_final_data = base64.b64encode(first_key).decode() + config('KEY_SEPARATOR') + base64.b64encode(
    # second_key).decode() + config('KEY_SEPARATOR') + str(base64.b64encode(second_ciphertext).decode())

    data = {
        'encrypted_data': encrypted_final_data,
        'key1': base64.b64encode(first_key).decode(),
        # 'key2': base64.b64encode(second_key).decode(),
        # 'key1_encrypted': base64.b64encode(first_key_ciphertext).decode(),
        # 'key2_encrypted': base64.b64encode(second_key_ciphertext).decode(),
        # 'key1_encrypted_encrypted': base64.b64encode(first_key_encrypted_ciphertext).decode(),
        # 'key2_encrypted_encrypted': base64.b64encode(second_key_encrypted_ciphertext).decode(),
    }

    response = self.get_paginated_response(data=data)

    return response
