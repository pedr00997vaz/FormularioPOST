from typing import List
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import json

app = FastAPI(title = "FastAPI con Jinja2")
app.mount("/rutarecursos", StaticFiles(directory="recursos"), name="recursos")
miPlantilla = Jinja2Templates(directory="plantillas")

async def cargarJSON():
    with open('lista_alumnos.json',"r") as archivo_json:
        datos = json.load(archivo_json)
        #print(datos)
    return datos

async def guardarJSON(datosAgregar:List):
    with open('lista_alumnos.json',"w") as archivo_json:
        #json.dump(datosAgregar, archivo_json)
        json.dump(datosAgregar, archivo_json, indent=4)


@app.get("/inicio/", response_class=HTMLResponse)
async def read_item(request: Request):
    datos = await cargarJSON()
    return miPlantilla.TemplateResponse("index.html",{"request":request, "lista":datos})


@app.get("/lista", response_class=HTMLResponse)
async def iniciar(request: Request):
    datos = await cargarJSON()
    Bmatricula=0
    return miPlantilla.TemplateResponse("integrantes.html",{"request":request,"lista":datos,"Bmatricula":Bmatricula})


@app.post("/agregar")
async def agregar(request:Request):
    datos = await cargarJSON()
    nuevos_datos = {}
    datos_formulario = await request.form()
    ultmimo_id = datos[-1].get("item_id")  #valor del ide del ultimo elemento de la lista
    nuevos_datos["item_id"] = ultmimo_id+1
    nuevos_datos["matricula"] = int(datos_formulario["f_matricula"])
    nuevos_datos["nombre"] = datos_formulario["f_nombre"]
    nuevos_datos["apaterno"] = (datos_formulario["f_apaterno"])
    nuevos_datos["amaterno"] = (datos_formulario["f_amaterno"])
    nuevos_datos["edad"] = int(datos_formulario["f_edad"])
    nuevos_datos["correo"] = (datos_formulario["f_correo"])
    nuevos_datos["telefono"] = int(datos_formulario["f_telefono"])
    nuevos_datos["carrera"] = (datos_formulario["f_carrera"])
    print(nuevos_datos)
    datos.append(nuevos_datos)
    print(datos)

    await guardarJSON(datos)

    return RedirectResponse("/lista",303)

@app.get("/eliminar/{id}")
async def eliminar(request:Request,id:int):
    datos = await cargarJSON()

    del datos[id]

    await guardarJSON(datos)

    return RedirectResponse("/lista",303)


@app.get("/ver_datoPersonal/{id}")
async def modificar(request:Request,id:int):
    datos = await cargarJSON()
    id1 = datos[id]
    id2 = id1['item_id']
    return miPlantilla.TemplateResponse("datoPersonal.html",{"request":request,"lista":datos,"id":id2})


@app.get("/modificar/{id}")
async def modificar(request:Request,id:int):
    datos = await cargarJSON()
    id1 = datos[id]
    id2 = id1['item_id']
    return miPlantilla.TemplateResponse("fmodificar.html",{"request":request,"lista":datos,"id":id2})

@app.post("/modificar_l/{id}")
async def modificar(request:Request,id:int):
    datos = await cargarJSON()
    #print (datos)
    #print (datos[id])
    datos[id]
    nuevos_datos = datos[id]
    datos_formulario = await request.form()
    nuevos_datos["matricula"] = int(datos_formulario["f_matricula"])
    nuevos_datos["nombre"] = datos_formulario["f_nombre"]
    nuevos_datos["apaterno"] = (datos_formulario["f_apaterno"])
    nuevos_datos["amaterno"] = (datos_formulario["f_amaterno"])
    nuevos_datos["edad"] = int(datos_formulario["f_edad"])
    nuevos_datos["correo"] = (datos_formulario["f_correo"])
    nuevos_datos["telefono"] = int(datos_formulario["f_telefono"])
    nuevos_datos["carrera"] = (datos_formulario["f_carrera"])
    datos[id] = nuevos_datos
    await guardarJSON(datos)
    return RedirectResponse("/lista",303)

@app.post("/buscar")
async def buscar(request:Request):
    datos = await cargarJSON()
    datos_formulario = await request.form()
    Bmatricula = datos_formulario["b_matricula"]
    print (Bmatricula)
    for fila in datos:
        if fila.get('matricula') == int(Bmatricula):
            item_id = fila.get('item_id')
            print ("este es ",item_id)
            return miPlantilla.TemplateResponse("fbuscar.html",{"request":request,"id":item_id, "Bmatricula":Bmatricula,"lista":datos})
    aviso="si"
    return miPlantilla.TemplateResponse("integrantes.html",{"request":request,"lista":datos,"Bmatricula":Bmatricula,"aviso":aviso})

