from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.encoders import jsonable_encoder

from ..models.tareas_asignadas import TareasAsignadas as ModelTareasAsignadas

routertareas_asignadas = APIRouter()

class TareaAsignada(BaseModel):
    id: Optional[int]=None
    tarea_id:int
    user_id:int

@routertareas_asignadas.post('/tareasasignadas', tags=['TareasAsignadas'])
def create_tarea(tarea_asignada: TareaAsignada, db: Session = Depends(get_db)):
    try:
        new_tarea = ModelTareasAsignadas(**tarea_asignada.model_dump())
        db.add(new_tarea)
        db.commit()
        db.refresh(new_tarea)
        return JSONResponse(
            status_code=201,  
            content={
                "message": "Tarea creada correctamente",
                "tarea_id": new_tarea.id
            }
        )
    except Exception as e:
        db.rollback()  
        return JSONResponse(
            status_code=422,
            content={
                "message": "Error al crear la tarea asignada",
                "detail": str(e)
            }
        )
    
@routertareas_asignadas.get('/tareasasignadas/{user_id}', tags=['TareasAsignadas']) 
def tareas_usuario(user_id: int, db: Session = Depends(get_db)):
    try:
        
        data = db.query(ModelTareasAsignadas).filter(
            ModelTareasAsignadas.user_id == user_id
        ).all()
        
        return JSONResponse(
            status_code=200,
            content={
                "user_id": user_id,
                "tareas": jsonable_encoder(data)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al listar tareas del usuario {user_id}",
                "detail": str(e)
            }
        )





@routertareas_asignadas.get('/tareasasignadas/{user_id}/count', tags=['TareasAsignadas'])
def count_tareas_usuario(user_id: int, db: Session = Depends(get_db)):
    try:
        
        count = db.query(ModelTareasAsignadas).filter(
            ModelTareasAsignadas.user_id == user_id
        ).count()
        
        return JSONResponse(
            status_code=200,
            content={
                "user_id": user_id,
                "total_tareas": count
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "message": "Error al contar tareas",
                "detail": str(e)
            }
        )
    
@routertareas_asignadas.delete('/tareasasignadas/{tarea_id}', tags=['TareasAsignadas'])
def delete_tarea_asignada(tarea_id: int, db: Session = Depends(get_db)):
    #para borrar mas de un registro no se utiliza all(), se utiliza delete()
    data=db.query(ModelTareasAsignadas).filter(ModelTareasAsignadas.tarea_id==tarea_id).delete() 
         
    db.commit()
    return JSONResponse(content={"message":"Se ha eliminado la/s tarea/s asignada/s"})





#endpoint el cual recibe el id_tarea + id_usuario y borrar una tarea_asignada
@routertareas_asignadas.delete('/tareasasignadas', tags=['TareasAsignadas'])
def delete_tarea_asignada(tarea_id: int, user_id:int, db: Session = Depends(get_db)):       
    db.query(ModelTareasAsignadas).filter((ModelTareasAsignadas.tarea_id==tarea_id) & (ModelTareasAsignadas.user_id==user_id)).delete()      
    db.commit()
    return JSONResponse(content={"message":"Se ha eliminado la tarea asignada"})