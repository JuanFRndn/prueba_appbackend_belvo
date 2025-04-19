from fastapi import APIRouter, Depends, HTTPException, Query
from src.service.belvo_service import BelvoService

router = APIRouter(
    prefix="/api",
    tags=["Api"]
)

belvo = BelvoService()

@router.get("/banks")
async def list_banks():
    try:
        belvo_response = belvo.get_banks()
        
        if not isinstance(belvo_response.get("data"), list):
            raise HTTPException(
                status_code=502,
                detail="La respuesta del servicio bancario no tiene formato válido"
            )
        
        return {
            "data": belvo_response["data"],
        }
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"No se pudieron obtener los bancos: {str(e)}"
        )
    
@router.get("/links")
async def list_links(
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=50)
):
    try:
        belvo_response = belvo.get_links(page=page, page_size=page_size)
        
        if not isinstance(belvo_response.get("data"), list):
            raise HTTPException(
                status_code=502,
                detail="La respuesta del servicio bancario no tiene formato válido"
            )
        
        return {
            "data": belvo_response["data"],
            "pagination": belvo_response["pagination"]
        }
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"No se pudieron obtener los bancos: {str(e)}"
        )

@router.get("/accounts")
async def list_accounts(link_id:str):
    try:
        return belvo.get_accounts(link_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/transactions")
async def list_transactions(
    link: str = Query(...),
    account: str = Query(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=1, le=50)
):
    try:
        belvo_response = belvo.get_transactions(link,account,page=page, page_size=page_size)
        
        if not isinstance(belvo_response.get("data"), list):
            raise HTTPException(
                status_code=502,
                detail="La respuesta del servicio bancario no tiene formato válido"
            )

        return {
            "data": belvo_response["data"],
            "account_flows": belvo_response["account_flows"],
            "pagination": belvo_response["pagination"]
        }
    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"No se pudieron obtener las transacciones: {str(e)}"
        )
