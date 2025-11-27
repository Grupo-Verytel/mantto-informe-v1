"""
Middlewares y helpers para control de permisos
"""
from typing import List, Callable
from fastapi import HTTPException, status, Depends
from functools import wraps

from .auth_middleware import get_current_user
import logging

logger = logging.getLogger(__name__)


def require_access_role(*allowed_access_roles: str):
    """
    Decorator que verifica que el usuario tenga uno de los roles de acceso permitidos
    
    Args:
        *allowed_access_roles: Roles de acceso permitidos
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtener usuario del contexto
            user = kwargs.get("user") or (args[0] if args else None)
            
            if not user:
                # Intentar obtener de dependencies
                user = kwargs.get("current_user")
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no autenticado"
                )
            
            user_access_role = user.get("access_role_name")
            
            if not user_access_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario sin rol asignado"
                )
            
            # Superadmin tiene acceso a todo
            if user_access_role == "superadmin":
                return await func(*args, **kwargs)
            
            # Verificar si el rol del usuario está en los permitidos
            if user_access_role not in allowed_access_roles:
                logger.warning(
                    f"Acceso denegado: usuario {user.get('email')} con rol {user_access_role} "
                    f"intentó acceder a recurso que requiere {allowed_access_roles}"
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No tiene permisos para acceder a este recurso"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def require_write_permission(module: str):
    """
    Decorator que verifica que el usuario tenga permisos de escritura en el módulo
    
    Args:
        module: Nombre del módulo (ej: 'info_general', 'mesa_servicio')
        
    Returns:
        Decorator function
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("user") or kwargs.get("current_user")
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Usuario no autenticado"
                )
            
            user_access_role = user.get("access_role_name")
            
            if not user_access_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Usuario sin rol asignado"
                )
            
            # Verificar permisos de escritura
            if not can_write(user_access_role, module):
                logger.warning(
                    f"Escritura denegada: usuario {user.get('email')} con rol {user_access_role} "
                    f"intentó escribir en módulo {module}"
                )
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"No tiene permisos de escritura en el módulo {module}"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper
    return decorator


def can_read(user_access_role: str, module: str) -> bool:
    """
    Verifica si un usuario puede leer un módulo
    
    Args:
        user_access_role: Rol de acceso del usuario
        module: Nombre del módulo
        
    Returns:
        True si puede leer, False en caso contrario
    """
    if user_access_role == "superadmin":
        return True
    
    # Verificar si el rol corresponde al módulo
    if user_access_role == f"admin_{module}" or user_access_role == f"readonly_{module}":
        return True
    
    return False


def can_write(user_access_role: str, module: str) -> bool:
    """
    Verifica si un usuario puede escribir en un módulo
    
    Args:
        user_access_role: Rol de acceso del usuario
        module: Nombre del módulo
        
    Returns:
        True si puede escribir, False en caso contrario
    """
    if user_access_role == "superadmin":
        return True
    
    # Solo admin puede escribir
    if user_access_role == f"admin_{module}":
        return True
    
    return False


# Dependency para verificar permisos de lectura
async def require_read_permission(module: str, current_user: dict = Depends(get_current_user)):
    """
    Dependency que verifica permisos de lectura en un módulo
    
    Args:
        module: Nombre del módulo
        current_user: Usuario actual (inyectado)
        
    Returns:
        Usuario si tiene permisos
        
    Raises:
        HTTPException: Si no tiene permisos
    """
    user_access_role = current_user.get("access_role_name")
    
    if not user_access_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario sin rol asignado"
        )
    
    if not can_read(user_access_role, module):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tiene permisos de lectura en el módulo {module}"
        )
    
    return current_user


# Dependency para verificar permisos de escritura
async def require_write_permission_dep(module: str, current_user: dict = Depends(get_current_user)):
    """
    Dependency que verifica permisos de escritura en un módulo
    
    Args:
        module: Nombre del módulo
        current_user: Usuario actual (inyectado)
        
    Returns:
        Usuario si tiene permisos
        
    Raises:
        HTTPException: Si no tiene permisos
    """
    user_access_role = current_user.get("access_role_name")
    
    if not user_access_role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario sin rol asignado"
        )
    
    if not can_write(user_access_role, module):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"No tiene permisos de escritura en el módulo {module}"
        )
    
    return current_user



