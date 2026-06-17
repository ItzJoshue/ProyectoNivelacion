import uuid

def nuevo_id(prefijo):
    return f"{prefijo}-{uuid.uuid4().hex[:6].upper()}"