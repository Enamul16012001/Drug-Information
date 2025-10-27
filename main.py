from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx

app = FastAPI(title="FDA Drug Search API - COMPLETE")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

DRUGSFDA_URL = "https://api.fda.gov/drug/drugsfda.json"
NDC_URL = "https://api.fda.gov/drug/ndc.json"
LABEL_URL = "https://api.fda.gov/drug/label.json"

@app.get("/")
async def read_root():
    return FileResponse("static/index.html")

async def search_endpoint(url, search_query, limit=10):
    try:
        params = {"search": search_query, "limit": min(limit, 99)}
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            return {"results": [], "meta": {"results": {"total": 0}}}
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== DRUGSFDA ENDPOINTS ====================
@app.get("/api/drugsfda/search/all")
async def drugsfda_search_all(query: str, limit: int = 20):
    fields = ["openfda.brand_name", "openfda.generic_name", "openfda.manufacturer_name", "openfda.substance_name", "application_number"]
    all_results, seen = [], set()
    for field in fields:
        try:
            data = await search_endpoint(DRUGSFDA_URL, f"{field}:{query}", 10)
            for r in data.get("results", []):
                app_num = r.get("application_number", "")
                if app_num and app_num not in seen:
                    seen.add(app_num)
                    all_results.append(r)
        except: pass
    return {"results": all_results[:limit], "meta": {"results": {"total": len(all_results)}}}

@app.get("/api/drugsfda/search")
async def drugsfda_search(query: str, field: str = "openfda.brand_name", limit: int = 10):
    return await search_endpoint(DRUGSFDA_URL, f"{field}:{query}", limit)

# ==================== NDC ENDPOINTS - ALL FIELDS ====================
@app.get("/api/ndc/search/all")
async def ndc_search_all(query: str, limit: int = 20):
    fields = ["brand_name", "generic_name", "openfda.manufacturer_name", "product_ndc", "dosage_form", "route"]
    all_results, seen = [], set()
    for field in fields:
        try:
            data = await search_endpoint(NDC_URL, f"{field}:{query}", 10)
            for r in data.get("results", []):
                pid = r.get("product_id", "")
                if pid and pid not in seen:
                    seen.add(pid)
                    all_results.append(r)
        except: pass
    return {"results": all_results[:limit], "meta": {"results": {"total": len(all_results)}}}

@app.get("/api/ndc/brand-name")
async def ndc_brand_name(name: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"brand_name:{name}", limit)

@app.get("/api/ndc/generic-name")
async def ndc_generic_name(name: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"generic_name:{name}", limit)

@app.get("/api/ndc/product-ndc")
async def ndc_product_ndc(ndc: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"product_ndc:{ndc}", limit)

@app.get("/api/ndc/package-ndc")
async def ndc_package_ndc(ndc: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"packaging.package_ndc:{ndc}", limit)

@app.get("/api/ndc/dosage-form")
async def ndc_dosage_form(form: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"dosage_form:{form}", limit)

@app.get("/api/ndc/route")
async def ndc_route(route: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"route:{route}", limit)

@app.get("/api/ndc/manufacturer")
async def ndc_manufacturer(name: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"openfda.manufacturer_name:{name}", limit)

@app.get("/api/ndc/product-type")
async def ndc_product_type(type: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"product_type:{type}", limit)

@app.get("/api/ndc/finished")
async def ndc_finished(finished: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"finished:{finished}", limit)

@app.get("/api/ndc/marketing-category")
async def ndc_marketing_category(category: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"marketing_category:{category}", limit)

@app.get("/api/ndc/application-number")
async def ndc_application_number(number: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"application_number:{number}", limit)

@app.get("/api/ndc/dea-schedule")
async def ndc_dea_schedule(schedule: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"dea_schedule:{schedule}", limit)

@app.get("/api/ndc/pharm-class")
async def ndc_pharm_class(class_name: str, class_type: str = "epc", limit: int = 10):
    field_map = {"epc": "openfda.pharm_class_epc", "pe": "openfda.pharm_class_pe", "moa": "openfda.pharm_class_moa", "cs": "openfda.pharm_class_cs"}
    field = field_map.get(class_type.lower(), "openfda.pharm_class_epc")
    return await search_endpoint(NDC_URL, f"{field}:{class_name}", limit)

@app.get("/api/ndc/active-ingredient")
async def ndc_active_ingredient(name: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"active_ingredients.name:{name}", limit)

@app.get("/api/ndc/rxcui")
async def ndc_rxcui(rxcui: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"openfda.rxcui:{rxcui}", limit)

@app.get("/api/ndc/unii")
async def ndc_unii(unii: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"openfda.unii:{unii}", limit)

@app.get("/api/ndc/spl-id")
async def ndc_spl_id(spl_id: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"spl_id:{spl_id}", limit)

@app.get("/api/ndc/spl-set-id")
async def ndc_spl_set_id(spl_set_id: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"openfda.spl_set_id:{spl_set_id}", limit)

@app.get("/api/ndc/upc")
async def ndc_upc(upc: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"openfda.upc:{upc}", limit)

@app.get("/api/ndc/original-packager")
async def ndc_original_packager(is_original: str, limit: int = 10):
    return await search_endpoint(NDC_URL, f"openfda.is_original_packager:{is_original}", limit)

# ==================== DRUG LABEL ENDPOINTS - ALL FIELDS ====================
@app.get("/api/label/search/all")
async def label_search_all(query: str, limit: int = 20):
    fields = ["openfda.brand_name", "openfda.generic_name", "indications_and_usage", "warnings"]
    all_results, seen = [], set()
    for field in fields:
        try:
            data = await search_endpoint(LABEL_URL, f"{field}:{query}", 10)
            for r in data.get("results", []):
                sid = r.get("set_id", "")
                if sid and sid not in seen:
                    seen.add(sid)
                    all_results.append(r)
        except: pass
    return {"results": all_results[:limit], "meta": {"results": {"total": len(all_results)}}}

# Basic searches
@app.get("/api/label/brand-name")
async def label_brand_name(name: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"openfda.brand_name:{name}", limit)

@app.get("/api/label/generic-name")
async def label_generic_name(name: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"openfda.generic_name:{name}", limit)

@app.get("/api/label/manufacturer")
async def label_manufacturer(name: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"openfda.manufacturer_name:{name}", limit)

@app.get("/api/label/substance-name")
async def label_substance_name(name: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"openfda.substance_name:{name}", limit)

@app.get("/api/label/route")
async def label_route(route: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"openfda.route:{route}", limit)

@app.get("/api/label/product-type")
async def label_product_type(type: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"openfda.product_type:{type}", limit)

# Abuse and overdosage
@app.get("/api/label/abuse")
async def label_abuse(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"abuse:{query}", limit)

@app.get("/api/label/controlled-substance")
async def label_controlled_substance(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"controlled_substance:{query}", limit)

@app.get("/api/label/dependence")
async def label_dependence(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"dependence:{query}", limit)

@app.get("/api/label/overdosage")
async def label_overdosage(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"overdosage:{query}", limit)

# Adverse effects and interactions
@app.get("/api/label/adverse-reactions")
async def label_adverse_reactions(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"adverse_reactions:{query}", limit)

@app.get("/api/label/drug-interactions")
async def label_drug_interactions(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"drug_interactions:{query}", limit)

@app.get("/api/label/laboratory-test-interactions")
async def label_lab_test_interactions(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"drug_and_or_laboratory_test_interactions:{query}", limit)

# Clinical pharmacology
@app.get("/api/label/clinical-pharmacology")
async def label_clinical_pharmacology(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"clinical_pharmacology:{query}", limit)

@app.get("/api/label/mechanism-of-action")
async def label_mechanism_of_action(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"mechanism_of_action:{query}", limit)

@app.get("/api/label/pharmacodynamics")
async def label_pharmacodynamics(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"pharmacodynamics:{query}", limit)

@app.get("/api/label/pharmacokinetics")
async def label_pharmacokinetics(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"pharmacokinetics:{query}", limit)

# Indications, usage, and dosage
@app.get("/api/label/indications-and-usage")
async def label_indications(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"indications_and_usage:{query}", limit)

@app.get("/api/label/contraindications")
async def label_contraindications(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"contraindications:{query}", limit)

@app.get("/api/label/description")
async def label_description(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"description:{query}", limit)

@app.get("/api/label/dosage-and-administration")
async def label_dosage(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"dosage_and_administration:{query}", limit)

@app.get("/api/label/dosage-forms-and-strengths")
async def label_dosage_forms(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"dosage_forms_and_strengths:{query}", limit)

@app.get("/api/label/active-ingredient")
async def label_active_ingredient(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"active_ingredient:{query}", limit)

@app.get("/api/label/inactive-ingredient")
async def label_inactive_ingredient(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"inactive_ingredient:{query}", limit)

@app.get("/api/label/purpose")
async def label_purpose(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"purpose:{query}", limit)

# Nonclinical toxicology
@app.get("/api/label/animal-pharmacology-toxicology")
async def label_animal_pharmacology(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"animal_pharmacology_and_or_toxicology:{query}", limit)

@app.get("/api/label/carcinogenesis-mutagenesis-fertility")
async def label_carcinogenesis(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"carcinogenesis_and_mutagenesis_and_impairment_of_fertility:{query}", limit)

@app.get("/api/label/nonclinical-toxicology")
async def label_nonclinical_toxicology(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"nonclinical_toxicology:{query}", limit)

# Patient information
@app.get("/api/label/ask-doctor")
async def label_ask_doctor(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"ask_doctor:{query}", limit)

@app.get("/api/label/do-not-use")
async def label_do_not_use(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"do_not_use:{query}", limit)

@app.get("/api/label/information-for-patients")
async def label_info_for_patients(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"information_for_patients:{query}", limit)

@app.get("/api/label/instructions-for-use")
async def label_instructions_for_use(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"instructions_for_use:{query}", limit)

@app.get("/api/label/keep-out-of-reach")
async def label_keep_out_of_reach(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"keep_out_of_reach_of_children:{query}", limit)

@app.get("/api/label/stop-use")
async def label_stop_use(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"stop_use:{query}", limit)

@app.get("/api/label/when-using")
async def label_when_using(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"when_using:{query}", limit)

# References
@app.get("/api/label/clinical-studies")
async def label_clinical_studies(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"clinical_studies:{query}", limit)

@app.get("/api/label/references")
async def label_references(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"references:{query}", limit)

# Special populations
@app.get("/api/label/geriatric-use")
async def label_geriatric_use(limit: int = 10):
    return await search_endpoint(LABEL_URL, "_exists_:geriatric_use", limit)

@app.get("/api/label/labor-and-delivery")
async def label_labor_delivery(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"labor_and_delivery:{query}", limit)

@app.get("/api/label/nursing-mothers")
async def label_nursing_mothers(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"nursing_mothers:{query}", limit)

@app.get("/api/label/pediatric-use")
async def label_pediatric_use(limit: int = 10):
    return await search_endpoint(LABEL_URL, "_exists_:pediatric_use", limit)

@app.get("/api/label/pregnancy")
async def label_pregnancy(limit: int = 10):
    return await search_endpoint(LABEL_URL, "_exists_:pregnancy", limit)

@app.get("/api/label/teratogenic-effects")
async def label_teratogenic_effects(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"teratogenic_effects:{query}", limit)

# Supply, storage, and handling
@app.get("/api/label/how-supplied")
async def label_how_supplied(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"how_supplied:{query}", limit)

@app.get("/api/label/storage-and-handling")
async def label_storage_handling(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"storage_and_handling:{query}", limit)

# Warnings and precautions
@app.get("/api/label/boxed-warning")
async def label_boxed_warning(limit: int = 10):
    return await search_endpoint(LABEL_URL, "_exists_:boxed_warning", limit)

@app.get("/api/label/warnings")
async def label_warnings(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"warnings:{query}", limit)

@app.get("/api/label/precautions")
async def label_precautions(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"precautions:{query}", limit)

@app.get("/api/label/user-safety-warnings")
async def label_user_safety_warnings(query: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"user_safety_warnings:{query}", limit)

# Date range
@app.get("/api/label/date-range")
async def label_date_range(start_date: str, end_date: str, limit: int = 10):
    return await search_endpoint(LABEL_URL, f"effective_time:[{start_date}+TO+{end_date}]", limit)

app.mount("/static", StaticFiles(directory="static"), name="static")