def cryptonomicon(to_decrypt, key_path="./crypto.key"):
    from cryptography.fernet import Fernet

    try:
        # load crypto key - and sanity check
        fhc = open(key_path, "r")
        key = fhc.read()
        key = key.strip()
        cryptonizer = Fernet(key)

        to_decrypt = bytes(to_decrypt, 'utf-8')
        result = cryptonizer.decrypt(to_decrypt)

        return result.decode("utf-8")
    except Exception as e:
        print("error processing crypto key file")
        raise e

def encrypt(to_encrypt):
    from cryptography.fernet import Fernet
    try:
        # load crypto key - and sanity check
        fhc = open("crypto.key", "r")
        key = fhc.read()
        key = key.strip()
        cryptonizer = Fernet(key)
        to_encrypt = bytes(str(to_encrypt), 'utf-8')
        result = cryptonizer.encrypt(to_encrypt)
        return result
    except Exception as e:
        print("error processing crypto key file")
