from rest_framework.response import Response
from rest_framework.views import status

"""
    Decorador definido para que valide que algunos campos de la sentencia
    que llegan en la petición no estén vacíos
"""
def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        input_code = args[0].request.data.get("input_code", "")
        if not input_code :
            return Response(
                data={
                    "message": "Input Code is required!"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorated