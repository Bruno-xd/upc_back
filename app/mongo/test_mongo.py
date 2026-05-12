from app.database import predicciones_collection

predicciones_collection.insert_one({
    "mensaje": "conexion exitosa"
})

print("Mongo conectado correctamente")