from pydantic import BaseModel, validator


class BotsIdActionTurnModel(BaseModel):
    direction: str

    @validator('direction')
    def action_must_be_one_of_these(cls, v):
        """
        Validating sent value and lowering if validated.
        """
        if v.lower() not in ['left', 'right', 'stop']:
            ErrorCode.throw(BOT_BAD_COMMAND_ARGS)
        return v.lower()
