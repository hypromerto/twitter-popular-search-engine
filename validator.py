from flask import Response
import cerberus
import copy

types = {
    "search_key": {
        "type": "string",
        "required": False,
        "nullable": True,
        "minlength": 0,
        "maxlength": 512
    }
}

def field(key, required=None, nullable=None, minlength=None, maxlength=None):

    if key not in types:
        raise Exception("The key {} was not found in available types".format(key))

    cur_type = copy.deepcopy(types[key])

    if required is not None:
        cur_type["required"] = required

    if nullable is not None:
        cur_type["nullable"] = nullable

    if minlength is not None:
        cur_type["minlength"] = minlength
    
    if maxlength is not None:
        cur_type["maxlength"] = maxlength
    
    return cur_type

def validate(schema, body):

    v = cerberus.Validator(schema)
    
    if not v.validate(body):
        return Response(status = 400)

    return body