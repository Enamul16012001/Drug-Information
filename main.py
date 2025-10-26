from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
from typing import Optional

app = FastAPI(title="Drug Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_URL = "https://api.fda.gov/drug/drugsfda.json"

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

@app.get("/api/search/all")
async def search_all_fields(query: str, limit: int = 20):
    """Search across all major fields"""
    fields = [
        "openfda.brand_name",
        "openfda.generic_name", 
        "openfda.manufacturer_name",
        "openfda.substance_name",
        "application_number",
        "openfda.route",
        "products.dosage_form"
    ]
    
    all_results = []
    seen_app_numbers = set()
    
    for field in fields:
        try:
            search_query = f"{field}:{query}"
            params = {"search": search_query, "limit": 10}
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(BASE_URL, params=params)
                if response.status_code == 200:
                    data = response.json()
                    for result in data.get("results", []):
                        app_num = result.get("application_number", "")
                        if app_num and app_num not in seen_app_numbers:
                            seen_app_numbers.add(app_num)
                            all_results.append(result)
                            
        except:
            continue
    
    return {
        "results": all_results[:limit],
        "meta": {"results": {"total": len(all_results)}}
    }

@app.get("/api/search")
async def search_drugs(
    query: str,
    field: str = "openfda.brand_name",
    limit: int = 10
):
    """Search drugs by field and query term"""
    try:
        search_query = f"{field}:{query}"
        params = {
            "search": search_query,
            "limit": min(limit, 99)
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/application/{app_number}")
async def get_by_application(app_number: str):
    """Search by application number (NDA/ANDA/BLA)"""
    try:
        search_query = f"application_number:{app_number}"
        params = {"search": search_query, "limit": 10}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/manufacturer")
async def search_by_manufacturer(name: str, limit: int = 10):
    """Search by manufacturer name"""
    try:
        search_query = f"openfda.manufacturer_name:{name}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/active-ingredient")
async def search_by_ingredient(name: str, limit: int = 10):
    """Search by active ingredient"""
    try:
        search_query = f"openfda.substance_name:{name}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/route")
async def search_by_route(route: str, limit: int = 10):
    """Search by route of administration (e.g., ORAL, INTRAVENOUS)"""
    try:
        search_query = f"openfda.route:{route}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dosage-form")
async def search_by_dosage_form(form: str, limit: int = 10):
    """Search by dosage form (e.g., TABLET, CAPSULE, SOLUTION)"""
    try:
        search_query = f"products.dosage_form:{form}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ndc")
async def search_by_ndc(ndc: str, limit: int = 10):
    """Search by NDC (National Drug Code)"""
    try:
        search_query = f"openfda.package_ndc:{ndc}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/rxcui")
async def search_by_rxcui(rxcui: str, limit: int = 10):
    """Search by RxNorm Concept Unique Identifier"""
    try:
        search_query = f"openfda.rxcui:{rxcui}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/unii")
async def search_by_unii(unii: str, limit: int = 10):
    """Search by UNII (Unique Ingredient Identifier)"""
    try:
        search_query = f"openfda.unii:{unii}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/pharm-class")
async def search_by_pharm_class(
    class_name: str, 
    class_type: str = "epc",
    limit: int = 10
):
    """
    Search by pharmacologic class
    class_type options: 'epc', 'pe', 'moa', 'cs'
    epc = Established Pharmacologic Class
    pe = Physiologic Effect
    moa = Mechanism of Action
    cs = Chemical Structure
    """
    try:
        field_map = {
            "epc": "openfda.pharm_class_epc",
            "pe": "openfda.pharm_class_pe",
            "moa": "openfda.pharm_class_moa",
            "cs": "openfda.pharm_class_cs"
        }
        
        field = field_map.get(class_type.lower(), "openfda.pharm_class_epc")
        print(field)
        search_query = f"{field}:{class_name}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/spl-id")
async def search_by_spl_id(spl_id: str, limit: int = 10):
    """Search by SPL (Structured Product Label) ID"""
    try:
        search_query = f"openfda.spl_id:{spl_id}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/product-number")
async def search_by_product_number(product_number: str, limit: int = 10):
    """Search by product number"""
    try:
        search_query = f"products.product_number:{product_number}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/marketing-status")
async def search_by_marketing_status(status: str, limit: int = 10):
    """Search by marketing status (e.g., Prescription, Over-the-counter)"""
    try:
        search_query = f"products.marketing_status:{status}"
        params = {"search": search_query, "limit": min(limit, 99)}
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(BASE_URL, params=params)
            response.raise_for_status()
            return response.json()
            
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/static", StaticFiles(directory="static"), name="static")