import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Project

app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Portfolio API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"

            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"

    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Payloads
class ProjectCreate(Project):
    pass

class ProjectOut(Project):
    id: str

# Helpers

def serialize_project(doc) -> ProjectOut:
    return ProjectOut(
        id=str(doc.get("_id")),
        title=doc.get("title"),
        subtitle=doc.get("subtitle"),
        description=doc.get("description"),
        image_url=doc.get("image_url"),
        tags=doc.get("tags", []),
        playstore_url=doc.get("playstore_url"),
        mediafire_url=doc.get("mediafire_url"),
        website_url=doc.get("website_url"),
        featured=doc.get("featured", False),
    )

# Routes
@app.post("/api/projects", response_model=dict)
def create_project(payload: ProjectCreate):
    try:
        inserted_id = create_document("project", payload)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/projects", response_model=List[ProjectOut])
def list_projects(tag: Optional[str] = None, featured: Optional[bool] = None, limit: int = 50):
    try:
        query = {}
        if tag:
            query["tags"] = {"$in": [tag]}
        if featured is not None:
            query["featured"] = featured
        docs = get_documents("project", query, limit)
        return [serialize_project(d) for d in docs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/projects/seed", response_model=dict)
def seed_projects():
    """Insert demo portfolio items if collection is empty"""
    try:
        existing = get_documents("project", {}, limit=1)
        if existing:
            return {"message": "Already seeded"}
        demos = [
            {
                "title": "KasirKu - POS UMKM",
                "subtitle": "Aplikasi kasir offline untuk UMKM",
                "description": "Aplikasi kasir sederhana dengan manajemen produk, stok, struk, dan laporan penjualan harian. Ringan dan mudah digunakan tanpa internet.",
                "image_url": "https://images.unsplash.com/photo-1556742393-d75f468bfcb0?q=80&w=1200&auto=format&fit=crop",
                "tags": ["Android", "Flutter", "POS"],
                "playstore_url": "https://play.google.com/store/apps/details?id=com.example.kasirku",
                "mediafire_url": "https://www.mediafire.com/file/example/kasirku.apk",
                "website_url": None,
                "featured": True,
            },
            {
                "title": "CatatanKeu - Keuangan Pribadi",
                "subtitle": "Budgeting & catat pengeluaran harian",
                "description": "Pantau pemasukan dan pengeluaran, kategori custom, grafik mingguan, dan ekspor ke CSV.",
                "image_url": "https://images.unsplash.com/photo-1553729784-e91953dec042?q=80&w=1200&auto=format&fit=crop",
                "tags": ["Android", "Kotlin", "Finance"],
                "playstore_url": "https://play.google.com/store/apps/details?id=com.example.catatankeu",
                "mediafire_url": "https://www.mediafire.com/file/example/catatankeu.apk",
                "website_url": None,
                "featured": False,
            },
            {
                "title": "AbsensiQR - Kehadiran",
                "subtitle": "Absensi karyawan dengan QR code",
                "description": "Scan QR, lokasi GPS, dan dashboard rekap. Cocok untuk sekolah/UKM.",
                "image_url": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=1200&auto=format&fit=crop",
                "tags": ["Android", "React Native", "Productivity"],
                "playstore_url": "https://play.google.com/store/apps/details?id=com.example.absensiqr",
                "mediafire_url": "https://www.mediafire.com/file/example/absensiqr.apk",
                "website_url": None,
                "featured": False,
            },
        ]
        inserted = 0
        for d in demos:
            create_document("project", Project(**d))
            inserted += 1
        return {"message": f"Seeded {inserted} projects"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
