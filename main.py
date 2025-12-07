from fastapi import FastAPI, Path, HTTPException, status, Query
from fastapi.responses import JSONResponse
import json
from schemas import Patient, EnumsModel, PatientUpdate

app = FastAPI()


def read():
    with open("pat.json", "r") as f:
        data = json.load(f)
        # print(data)
    return data

def save_data(data):
    with open("pat.json", "w") as f:
        json.dump(data,f)


@app.get("/")
def home():
    return {"msg": "First api"}


@app.get("/data")
def data():
    patients = read()
    return patients


# Path Parameters -> /{id:int}
    # Path() is used to declare and validate path parameters in FastAPI routes.
    # It allows you to:
    # Add validation rules
    # Add metadata (title, description)
    # Set default values
    # Add constraints (min/max length, regex, etc.)
    # Make documentation clearer in Swagger UI


@app.get("/data/{id}")
def get_patients(id: str = Path(..., description="ID of the patients", example="P001")):    # ... means mandatry
                                                                            #(item_id: int = Path(..., description="The ID of the item", gt=0)): lt/lte/le/regex/
                                                                            # (item_id: int = Path(10, description="The ID of the item", gt=0)): set default value
                                                                            # name: str = Path(..., min_length=3, max_length=50) inforce string length
    data = read()
    if id in data:
        return data[id]
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "Patient not found")


# Query Parameter -> sorted data /  validations
@app.get("/search")
def search_patients(
    gender: str = Query(None, description="Filter patients by gender", example="Male"),
    min_age: int = Query(0, ge=0, description="Minimum age filter"),
    max_age: int = Query(120, le=120, description="Maximum age filter"),
    limit: int = Query(10, gt=0, le=50, description="Number of records to return")
):
    # gender: Optional (default None)
    # min_age: Default 0, must be >= 0
    # max_age: Default 120, must be <= 120
    # limit: Default 10, must be > 0 and <= 50

    data = read()   # your patient JSON dict

    # Convert dict → list for filtering
    patients = list(data.values())
    # print(patients)

    if gender:
        patients = [p for p in patients if p["gender"].lower() == gender.lower()]

    patients = [p for p in patients if min_age <= p["age"] <= max_age]

    patients = patients[:limit]

    if not patients:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No matching patients found"
        )

    return patients

@app.get("/sorted")
def sort_patient(
        sort_by: str = Query(...,description="Sort on the basis of height_cm, weight_kg and bmi"),
        order: str = Query("asc",description="sort in asc or desc order")
):
    valid_sort = ["height_cm","weight_kg","bmi"]
    if not sort_by in valid_sort:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Invalid sort_by value")

    if not order in ["asc","desc"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order value")

    data = read()
    sort_order = True if order == "desc" else False
    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by), reverse=sort_order)
    if sort_by:
        return sorted_data

@app.post("/create")
def create(patient:Patient):
    # load patient data
    data = read()

    # Check id already exist or not
    if patient.id in data:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Patient id already exist")

    #convert to python data
    data[patient.id] = patient.model_dump(exclude=["id"])

    # if not then create entry in db
    save_data((data))



    return JSONResponse(status_code=status.HTTP_201_CREATED, content= {"msg":"Data inserted successfully"})


@app.patch("/update/{patient_id}")
def update(
    patient_id: str,
    patient:PatientUpdate
    ):
    data = read()
    if not patient_id in data.keys():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Patient id")
    
    updated_data = patient.model_dump(exclude_unset=True)
    data[patient_id].update(updated_data)

    save_data(data)

    return {"updated_data":data[patient_id]}

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id : str):
    data = read()

    if not patient_id in data.keys():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Patient id")
    
    deleted_data = data.pop(patient_id)
    save_data(data)
    return {"msg":f"Patient {patient_id} deleted successfully","deleted_data": deleted_data}


@app.get("/filter/{gender}")        #selecting options path parameters
def filter(gender:EnumsModel):
    data = read()
    patients = list(data.values())
    patients_data = [p for p in patients if p["gender"].lower()==gender.value.lower()]
    return {"patients":patients_data }




@app.get("/pagination")
def pagination(skip: int = 0, limit:int = 10):
    data = read()
    data_list = list(data.items())
    # print(data_list)
    show = []
    # for i in range(limit):
    show.append(data_list[skip:skip + limit])

    return {
        "total": len(data_list),
        "skip":skip,
        "limit":limit,
        "data": show
            }
