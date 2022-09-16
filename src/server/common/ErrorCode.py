from fastapi import HTTPException


class ErrorCode:

    @property
    def name(self) -> str:
        return self._name

    @property
    def internal_code(self) -> int:
        return self._internal_code

    @property
    def http_code(self) -> int:
        return self._http_code

    @property
    def label(self) -> str:
        return self._label

    def __init__(self, name: str, internal_code: int, http_code:int, label: str):
        self._name = name
        self._internal_code = internal_code
        self._http_code = http_code
        self._label = label

    @staticmethod
    def throw(error_code: 'ErrorCode'):
        """
        Throw a HTTPException using this ErrorCode details.
        """
        details = {
            'name': error_code.name,
            'internal_code': error_code.internal_code,
            'label': error_code.label
        }
        raise HTTPException(status_code=error_code.http_code, detail=details)


# Login errors
LOGIN_INVALID_REQUEST_ID = ErrorCode(name='LOGIN_INVALID_REQUEST_ID', internal_code=0x00000101, http_code=500,
                                     label="This request id is not valid")
LOGIN_INVALID_STOMP_ID = ErrorCode(name='LOGIN_INVALID_STOMP_ID', internal_code=0x00000102, http_code=500,
                                   label="This STOMP id is not valid")
LOGIN_INVALID_MQTT_ID = ErrorCode(name='LOGIN_INVALID_MQTT_ID', internal_code=0x00000103, http_code=500,
                                  label="This MQTT id is not valid")

# Team errors
TEAM_DOES_NOT_EXISTS = ErrorCode(name='TEAM_DOES_NOT_EXISTS', internal_code=0x00000201, http_code=404,
                                 label="The team does not exist")
TEAM_IS_FULL = ErrorCode(name='TEAM_DOES_NOT_EXISTS', internal_code=0x00000202, http_code=500,
                         label="The team is full")

# Bot errors
BOT_DOES_NOT_EXISTS = ErrorCode(name='BOT_DOES_NOT_EXISTS', internal_code=0x00000301, http_code=404,
                                label="The bot does not exist")

# Display errors
DISPLAY_BAD_TOKEN = ErrorCode(name='DISPLAY_BAD_TOKEN', internal_code=0x00000401, http_code=500,
                              label="The token is not valid")

