from pydantic import BaseModel, Field, computed_field
from typing import List, Annotated, Literal, Optional
from enum import Enum


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
        height_m = self.height_cm / 100
        return round(self.weight_kg / (height_m ** 2), 2)

    

class EnumsModel(str,Enum):
    Male = "male"
    Female = "female"



class PatientUpdate(BaseModel):
    # id: Annotated[Optional[str], Field(None, description="Id of the patient", example="P001")]
    name: Annotated[Optional[str], Field(None, description="Name of the patients")]
    age: Annotated[Optional[int], Field(None, gt=0, lt=120, description="Age of the patient")]
    gender: Annotated[Optional[Literal["male", "female", "other"]], Field(None, description="gender of patient")]
    contact: Annotated[Optional[str], Field(None, description="Contact number of patient")]
    address: Annotated[Optional[str], Field(None, description="Address of patient")]
    height_cm: Annotated[Optional[float], Field(None, gt=0, description="Height of patient")]
    weight_kg: Annotated[Optional[float], Field(None, gt=0, description="Weight of patient")]
    medical_history: Annotated[Optional[List[str]], Field(None, description="Height of patient")]

    @computed_field
    @property
    def bmi(self) -> float:
        if self.height_cm and self.weight_kg:
            height_m = self.height_cm / 100
            return round(self.weight_kg / (height_m ** 2), 2)
        return None