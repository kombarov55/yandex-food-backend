from sqlalchemy.orm import Session

from model.compilation import CompilationVO, CompilationDto, CompilationResponse
from repository import compilation_repository, food_repository


def find(session: Session, email: str):
    vo_list = compilation_repository.find_all(session, email)

    payload = []
    for vo in vo_list:
        food_list = food_repository.find_by_ids(vo.values)
        payload.append(CompilationDto(
            id=vo.id,
            name=vo.name,
            food_list=food_list
        ))
    return CompilationResponse(payload=payload)


def convert_to_dto(vo: CompilationVO):
    return CompilationDto(
        id=vo.id,
        name=vo.name,
        values=vo.values.split(", ")
    )