import base64


def base64_decoder(string: str) -> str:
    try:
        decoded_bytes = base64.b64decode(string)
        result = decoded_bytes.decode('utf-8')
        return result
    except Exception as e:
       raise e
