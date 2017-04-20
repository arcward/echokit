from echopy import request, response


def lambda_handler(event, context):
    req = request.Request.from_json(event)