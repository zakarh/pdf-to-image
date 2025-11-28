from uuid import uuid4


def gen_id(r=8):
    return "".join([str(uuid4()).replace("-", "") for i in range(r)])
