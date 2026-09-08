"""Utils."""

import base64

import cloudpickle


def serialize(obj: object) -> str:
    """Serialize an object to a string.

    Parameters
    ----------
    obj : object
        The object to serialize.

    Returns
    -------
    str
        UTF-8 string containing a Base64-encoded, cloudpickle-serialized object.

    Raises
    ------
    ValueError
        If the object cannot be serialized.
    """
    try:
        return base64.b64encode(cloudpickle.dumps(obj)).decode("utf-8")
    except Exception as e:
        err_msg = f"Object cannot be serialized: {e}"
        raise ValueError(err_msg) from e


def deserialize[T](serialized_obj: str, obj_class: type[T]) -> T:
    """Deserialize an object and validate its type.

    Parameters
    ----------
    serialized_obj : str
        UTF-8 string containing a Base64-encoded, cloudpickle-serialized object.
    obj_class : type[T]
        Expected type of the deserialized object.

    Returns
    -------
    T
        The deserialized object.

    Raises
    ------
    ValueError
        If the object cannot be deserialized.
    TypeError
        If the deserialized object is not of type ``obj_class``.
    """
    try:
        payload = cloudpickle.loads(base64.b64decode(serialized_obj.encode("utf-8"), validate=True))
    except Exception as e:
        err_msg = f"Object cannot be deserialized: {e}"
        raise ValueError(err_msg) from e

    if not isinstance(payload, obj_class):
        err_msg = f"Deserialized object is not of type {obj_class.__name__}"
        raise TypeError(err_msg)

    return payload


"""
TODO
maybe custom exceptions for utils as well?
i could re-use SerializeError but that inherits from SubprocessError
"""
