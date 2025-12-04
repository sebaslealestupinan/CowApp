from sqlmodel import Session, select
from typing import List, Optional

from app.models.usuario import Usuario
from app.schemas.user_schemas import CreateUser, UpdateUser


def get_user_by_email(email: str, session: Session) -> Optional[Usuario]:
    """
    Busca un Usuario por su dirección de correo electrónico.
    """
    return session.exec(select(Usuario).where(Usuario.email == email)).first()


def create_user(data: CreateUser, session: Session) -> Usuario:
    """
    Crea un nuevo Usuario y sus teléfonos asociados.
    """

    db_user = Usuario(
        name=data.name,
        email=data.email,
        password=data.password,
        role=data.role,
        status=data.status,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    telefonos_a_crear = []
    if data.telefonos:
        for numero in data.telefonos:
            db_telefono = Telefono(
                numero=numero,
                user_id=db_user.id
            )
            telefonos_a_crear.append(db_telefono)

        session.add_all(telefonos_a_crear)
        session.commit()
        session.refresh(db_user)

    return db_user


def get_user(user_id: int, session: Session) -> Optional[Usuario]:
    """
    Obtiene un Usuario por su ID.
    """
    return session.get(Usuario, user_id)


def get_users(session: Session, role: Optional[str] = None, search: Optional[str] = None) -> List[Usuario]:
    """
    Obtiene la lista de todos los Usuarios, opcionalmente filtrados por rol y nombre.
    """
    query = select(Usuario)
    if role:
        query = query.where(Usuario.role == role)
    if search:
        query = query.where(Usuario.name.ilike(f"%{search}%"))
    return session.exec(query).all()


def update_user(
        user_id: int,
        user_update: UpdateUser,
        session: Session
) -> Optional[Usuario]:
    """
    Actualiza un Usuario existente.
    """
    db_user = session.get(Usuario, user_id)
    if not db_user:
        return None

    update_data = user_update.model_dump(exclude_unset=True)
    telefonos_update = update_data.pop("telefonos", None)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    session.add(db_user)

    if telefonos_update is not None:
        # Delete old phones
        telefonos_antiguos = session.exec(
            select(Telefono).where(Telefono.user_id == db_user.id)
        ).all()
        for t in telefonos_antiguos:
            session.delete(t)

        # Add new phones
        telefonos_a_crear = []
        for numero in telefonos_update:
            db_telefono = Telefono(
                numero=numero,
                user_id=db_user.id
            )
            telefonos_a_crear.append(db_telefono)

        session.add_all(telefonos_a_crear)

    session.commit()
    session.refresh(db_user)

    return db_user


def delete_user(user_id: int, session: Session) -> bool:
    """
    Elimina un Usuario por su ID.
    """
    db_user = session.get(Usuario, user_id)
    if not db_user:
        return False

    # Manually delete phones to avoid FK constraint errors if cascade is not set
    telefonos = session.exec(select(Telefono).where(Telefono.user_id == user_id)).all()
    for telefono in telefonos:
        session.delete(telefono)

    session.delete(db_user)
    session.commit()
    return True
