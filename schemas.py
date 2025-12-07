from pydantic import BaseModel, Field, computed_field
from typing import List, Annotated, Literal


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="Id of the patient", example="P001")]
    name: Annotated[str, Field(..., description="Name of the patients")]
    age: Annotated[int, Field(gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Literal["male", "female", "other"], Field(..., description="gender of patient")]
    contact: Annotated[str, Field(..., description="Contact number of patient")]
    address: Annotated[str, Field(..., description="Address of patient")]
    height_cm: Annotated[float, Field(..., gt=0, description="Height of patient")]
    weight_kg: Annotated[float, Field(..., gt=0, description="Weight of patient")]
    medical_history: Annotated[List[str], Field(None, description="Height of patient")]

    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight_kg / (self.height_cm ** 2), 2)
