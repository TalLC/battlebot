from pydantic import BaseModel, validator
from common.ErrorCode import *


class BotsIdActionMoveModel(BaseModel):
    action: str

    @validator('action')
    def action_must_be_one_of_these(cls, v):
        """
        Validating sent value and lowering if validated.
        """
        if v.lower() not in ['start', 'stop']:
            ErrorCode.throw(BOT_BAD_COMMAND_ARGS)
        return v.lower()
