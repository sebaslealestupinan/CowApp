# ---------------------
# ENDPOINTS TELEFONO (Asociación Genérica)
# ---------------------

@app.post("/telefonos/", response_model=Telefono, status_code=status.HTTP_201_CREATED)
def create_telefono(telefono: Telefono, session: Session = Depends(get_session)):
    # Validación: asegurar que solo se asocia a un usuario
    if (telefono.ganadero_id is not None and telefono.veterinario_id is not None) or \
       (telefono.ganadero_id is None and telefono.veterinario_id is None):
        raise HTTPException(
            status_code=400,
            detail="Un teléfono debe estar asociado exactamente a un Ganadero o un Veterinario."
        )

    session.add(telefono)
    session.commit()
    session.refresh(telefono)
    return telefono

@app.get("/telefonos/{telefono_id}", response_model=Telefono)
def read_telefono(telefono_id: int, session: Session = Depends(get_session)):
    telefono = session.get(Telefono, telefono_id)
    if not telefono:
        raise HTTPException(status_code=404, detail="Teléfono no encontrado")
    return telefono