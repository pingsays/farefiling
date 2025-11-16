from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    def json(self, indent=2):
        return self.model_dump_json(indent=indent)
