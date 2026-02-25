from rest_framework import status

from _library.dataclass import ResponseClient, SuccessResponse

# 201 SUCCESS RESPONSE
SUCCESS_RESPONSE_201 = SuccessResponse(
    status=status.HTTP_201_CREATED,
    message="Object created successfully",
    client=ResponseClient.USER,
    data={},
    links=None,
).model_dump()

# 200 SUCCESS RESPONSE
SUCCESS_RESPONSE_200 = SuccessResponse(
    status=status.HTTP_200_OK,
    message="Success",
    client=ResponseClient.USER,
    data={},
    links=None,
).model_dump()
