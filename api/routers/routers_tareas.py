from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends, APIRouter
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Session
from ..database import get_db
from fastapi.encoders import jsonable_encoder

from ..models.tareas import Tareas as ModelTareas

routertareas = APIRouter()

class Tarea(BaseModel):
    id: Optional[int]=None
    user_id:int
    tarea_name: str = Field(min_length=3, max_length=35)
    tarea_ubicacion: str = Field(min_length=3, max_length=35)
    year:int
    month:int
    day:int
    turno:str
    voluntarios_necesarios: int
    voluntarios_asignados: Optional[int] = None
    id_voluntario_Asignado_1: Optional[int] = None
    id_voluntario_Asignado_2: Optional[int] = None
    id_voluntario_Asignado_3: Optional[int] = None
    id_voluntario_Asignado_4: Optional[int] = None
    id_voluntario_Asignado_5: Optional[int] = None
    coordinador: bool
    coordinador_Asignado: Optional[bool] = False




@routertareas.post('/tareas', tags=['Tareas'])
def create_tarea(tarea: Tarea, db: Session = Depends(get_db)):
    try:
        new_tarea = ModelTareas(**tarea.model_dump())
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
                "message": "Error al crear la tarea",
                "detail": str(e)
            }
        )


    
@routertareas.get('/tareas', tags=['Tareas'])
def get_tarea(db: Session = Depends(get_db)):    
    data= db.query(ModelTareas).all()    
    return JSONResponse(content=jsonable_encoder(data))


@routertareas.get('/tareas/{id}', tags=['Tareas'])
def get_tarea_id(id: int, db: Session = Depends(get_db)):
    data=db.query(ModelTareas).filter(ModelTareas.id==id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message":"Recurso no encontrado"})
    else:         
        return JSONResponse(status_code=200, content=jsonable_encoder(data))
    
    

@routertareas.delete('/tareas/{id}', tags=['Tareas'])
def delete_tarea(id: int, db: Session = Depends(get_db)):
    
    data=db.query(ModelTareas).filter(ModelTareas.id==id).first()     
    db.delete(data)
    db.commit()
    return JSONResponse(content={"message":"Se ha eliminado la tarea" , "tarea": jsonable_encoder(data)})

@routertareas.put('/tareas/{id}', tags=['Tareas'])
def update_tarea(tarea:Tarea, id:int, id_voluntario:int, db: Session = Depends(get_db)):
    
    data=db.query(ModelTareas).filter(ModelTareas.id==id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message":"Recurso no encontrado"})
    else:
        if data.voluntarios_asignados==None:
            data.voluntarios_asignados=1
        else:        
            data.voluntarios_asignados=data.voluntarios_asignados+1
        
        if data.id_voluntario_Asignado_1==None:
            data.id_voluntario_Asignado_1=id_voluntario
        elif data.id_voluntario_Asignado_2==None:
            data.id_voluntario_Asignado_2=id_voluntario
        elif data.id_voluntario_Asignado_3==None:
            data.id_voluntario_Asignado_3=id_voluntario
        elif data.id_voluntario_Asignado_4==None:
            data.id_voluntario_Asignado_4=id_voluntario
        elif data.id_voluntario_Asignado_5==None:
            data.id_voluntario_Asignado_5=id_voluntario
       
        db.commit()
        return JSONResponse(status_code=200, content=jsonable_encoder(tarea))
    

@routertareas.put('/tareasborrarusuario/{id}', tags=['Tareas'])
def update_tarea(id:int, id_voluntario:int, db: Session = Depends(get_db)):
    encontrado=False
    data=db.query(ModelTareas).filter(ModelTareas.id==id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message":"Recurso no encontrado"})
    else:
               
        data.voluntarios_asignados=data.voluntarios_asignados-1

        print(id_voluntario+1)
        
        if data.id_voluntario_Asignado_1==str(id_voluntario):
            data.id_voluntario_Asignado_1=None
            encontrado=True
        elif data.id_voluntario_Asignado_2==str(id_voluntario):
            data.id_voluntario_Asignado_2=None
            encontrado=True
        elif data.id_voluntario_Asignado_3==str(id_voluntario):
            data.id_voluntario_Asignado_3=None
            encontrado=True
        elif data.id_voluntario_Asignado_4==str(id_voluntario):
            data.id_voluntario_Asignado_4=None
            encontrado=True
        elif data.id_voluntario_Asignado_5==str(id_voluntario):
            data.id_voluntario_Asignado_5=None
            encontrado=True
        print(encontrado)
       
        db.commit()
        return JSONResponse(status_code=200,
                            content={"message": "Usuario eliminado correctamente de la tarea"})
    
@routertareas.put('/tareasedit/{id}', tags=['Tareas'])
def update_tarea(tarea:Tarea, id:int, db: Session = Depends(get_db)):
    
    data=db.query(ModelTareas).filter(ModelTareas.id==id).first()
    if not data:
        return JSONResponse(status_code=404, content={"message":"Recurso no encontrado"})
    else:
        data.tarea_name=tarea.tarea_name
        data.tarea_ubicacion=tarea.tarea_ubicacion
        data.turno=tarea.turno
        data.voluntarios_necesarios=tarea.voluntarios_necesarios
        data.day=tarea.day
        data.month=tarea.month
        data.year=tarea.year
        data.id_voluntario_Asignado_1=tarea.id_voluntario_Asignado_1
        data.id_voluntario_Asignado_2=tarea.id_voluntario_Asignado_2
        data.id_voluntario_Asignado_3=tarea.id_voluntario_Asignado_3
        data.id_voluntario_Asignado_4=tarea.id_voluntario_Asignado_4
        data.id_voluntario_Asignado_5=tarea.id_voluntario_Asignado_5
        data.coordinador=tarea.coordinador
        

       
       
        db.commit()
        return JSONResponse(status_code=200, content=jsonable_encoder(tarea))
    


# @routertareas.put('/tareaseditcoordinador/{id}', tags=['Tareas'])
# def update_tarea(id:int, coordinador:bool,db: Session = Depends(get_db)):
#     data=db.query(ModelTareas).filter(ModelTareas.id==id).first()
#     if not data:
#         return JSONResponse(status_code=404, content={"message":"Recurso no encontrado"})
#     else:
#         data.coordinador_Asignado=coordinador
#         db.commit()
#         return JSONResponse(status_code=200)



@routertareas.put('/tareaseditcoordinador/{id}', tags=['Tareas'])
async def update_tarea(id: int, coordinador_Asignado: bool = Query(...), db: Session = Depends(get_db)):
    try:
        data = db.query(ModelTareas).filter(ModelTareas.id==id).first()
        if not data:
            return JSONResponse(status_code=404, content={"message":"Recurso no encontrado"})
        
        data.coordinador_Asignado = coordinador_Asignado
        db.commit()
        return JSONResponse(status_code=200, content={"message": "Actualizado correctamente"})
    
    except Exception as e:
        db.rollback()
        print(f"Error: {str(e)}")  # Para debugging
        return JSONResponse(status_code=500, content={"message": "Error interno del servidor"})