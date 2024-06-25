from fastapi import APIRouter, Depends, status
from fastapi_pagination import Page
from app.settings import get_settings
from app.models.Patient import Patient
from app.logs import get_logger
from app.services.patient_service import PatientService

logger = get_logger(__name__)
settings = get_settings()

router = APIRouter(
    prefix='/patients',
    tags=['Patients'],
)


@router.get('/my-patients', status_code=status.HTTP_200_OK, response_model=Page[Patient])
async def get_my_patients(patients = Depends(PatientService().get_my_patients)):
    return patients


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=Patient)
async def get_patient_by_id(patient: Patient = Depends(PatientService().get_by_id)):
    return patient


@router.post('', status_code=status.HTTP_201_CREATED, response_model=Patient)
async def create_patient(patient: Patient = Depends(PatientService().create)):
    return patient


@router.patch('/{id}', status_code=status.HTTP_200_OK, response_model=Patient)
async def update_patient(patient: Patient = Depends(PatientService().update)):
    return patient


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(PatientService().delete)])
async def delete_patient() -> None:
    pass
