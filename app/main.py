from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Brand, Category, SubCategory, Product, ProductVariant
from .schema import *
from .auth import login, get_current_admin

Base.metadata.create_all(bind=engine)

app = FastAPI(title="E-Commerce Admin API")

@app.get("/")
def home():
    return {"message": "E-Commerce API is running"}

# ---------- AUTH ----------

@app.post("/auth/login", response_model=TokenResponse)
def admin_login(data: LoginRequest):
    return {
        "access_token": login(data.username, data.password),
        "token_type": "bearer"
    }


# ---------- BRAND ----------

@app.post("/brands", response_model=BrandResponse)
def create_brand(data: BrandCreate, db: Session = Depends(get_db),
                 admin=Depends(get_current_admin)):
    brand = Brand(**data.model_dump())
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand


@app.get("/brands", response_model=list[BrandResponse])
def get_brands(db: Session = Depends(get_db),
               admin=Depends(get_current_admin)):
    return db.query(Brand).all()


@app.get("/brands/{id}", response_model=BrandResponse)
def get_brand(id: int, db: Session = Depends(get_db),
              admin=Depends(get_current_admin)):
    brand = db.get(Brand, id)
    if not brand:
        raise HTTPException(404, "Brand not found")
    return brand


@app.put("/brands/{id}", response_model=BrandResponse)
def update_brand(id: int, data: BrandUpdate,
                 db: Session = Depends(get_db),
                 admin=Depends(get_current_admin)):
    brand = db.get(Brand, id)
    if not brand:
        raise HTTPException(404, "Brand not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(brand, key, value)

    db.commit()
    db.refresh(brand)
    return brand


@app.delete("/brands/{id}")
def delete_brand(id: int, db: Session = Depends(get_db),
                 admin=Depends(get_current_admin)):
    brand = db.get(Brand, id)
    if not brand:
        raise HTTPException(404, "Brand not found")

    db.delete(brand)
    db.commit()
    return {"message": "Brand deleted"}


# ---------- CATEGORY ----------

@app.post("/categories", response_model=CategoryResponse)
def create_category(data: CategoryCreate,
                    db: Session = Depends(get_db),
                    admin=Depends(get_current_admin)):
    category = Category(**data.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@app.get("/categories", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db),
                   admin=Depends(get_current_admin)):
    return db.query(Category).all()


@app.get("/categories/{id}", response_model=CategoryResponse)
def get_category(id: int, db: Session = Depends(get_db),
                 admin=Depends(get_current_admin)):
    category = db.get(Category, id)
    if not category:
        raise HTTPException(404, "Category not found")
    return category


@app.put("/categories/{id}", response_model=CategoryResponse)
def update_category(id: int, data: CategoryUpdate,
                    db: Session = Depends(get_db),
                    admin=Depends(get_current_admin)):
    category = db.get(Category, id)
    if not category:
        raise HTTPException(404, "Category not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(category, key, value)

    db.commit()
    db.refresh(category)
    return category


@app.delete("/categories/{id}")
def delete_category(id: int, db: Session = Depends(get_db),
                    admin=Depends(get_current_admin)):
    category = db.get(Category, id)
    if not category:
        raise HTTPException(404, "Category not found")

    db.delete(category)
    db.commit()
    return {"message": "Category deleted"}


# ---------- SUBCATEGORY ----------

@app.post("/subcategories", response_model=SubCategoryResponse)
def create_subcategory(data: SubCategoryCreate,
                       db: Session = Depends(get_db),
                       admin=Depends(get_current_admin)):
    sub = SubCategory(**data.model_dump())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


@app.get("/subcategories", response_model=list[SubCategoryResponse])
def get_subcategories(db: Session = Depends(get_db),
                      admin=Depends(get_current_admin)):
    return db.query(SubCategory).all()


@app.put("/subcategories/{id}", response_model=SubCategoryResponse)
def update_subcategory(id: int, data: SubCategoryUpdate,
                       db: Session = Depends(get_db),
                       admin=Depends(get_current_admin)):
    sub = db.get(SubCategory, id)
    if not sub:
        raise HTTPException(404, "Subcategory not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(sub, key, value)

    db.commit()
    db.refresh(sub)
    return sub


@app.delete("/subcategories/{id}")
def delete_subcategory(id: int, db: Session = Depends(get_db),
                       admin=Depends(get_current_admin)):
    sub = db.get(SubCategory, id)
    if not sub:
        raise HTTPException(404, "Subcategory not found")

    db.delete(sub)
    db.commit()
    return {"message": "Subcategory deleted"}


# ---------- PRODUCTS ----------

@app.post("/products", response_model=ProductResponse)
def create_product(data: ProductCreate,
                   db: Session = Depends(get_db),
                   admin=Depends(get_current_admin)):
    product = Product(**data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get("/products", response_model=list[ProductResponse])
def get_products(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    return (
        db.query(Product)
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )


@app.get("/products/{id}", response_model=ProductResponse)
def get_product(id: int, db: Session = Depends(get_db),
                admin=Depends(get_current_admin)):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(404, "Product not found")
    return product


@app.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, data: ProductUpdate,
                   db: Session = Depends(get_db),
                   admin=Depends(get_current_admin)):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(404, "Product not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product


@app.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db),
                   admin=Depends(get_current_admin)):
    product = db.get(Product, id)
    if not product:
        raise HTTPException(404, "Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}


# ---------- VARIANTS ----------

@app.post("/variants", response_model=VariantResponse)
def create_variant(data: VariantCreate,
                   db: Session = Depends(get_db),
                   admin=Depends(get_current_admin)):
    variant = ProductVariant(**data.model_dump())
    db.add(variant)
    db.commit()
    db.refresh(variant)
    return variant


@app.get("/variants", response_model=list[VariantResponse])
def get_variants(db: Session = Depends(get_db),
                 admin=Depends(get_current_admin)):
    return db.query(ProductVariant).all()


@app.put("/variants/{id}", response_model=VariantResponse)
def update_variant(id: int, data: VariantUpdate,
                   db: Session = Depends(get_db),
                   admin=Depends(get_current_admin)):
    variant = db.get(ProductVariant, id)
    if not variant:
        raise HTTPException(404, "Variant not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(variant, key, value)

    db.commit()
    db.refresh(variant)
    return variant


@app.delete("/variants/{id}")
def delete_variant(id: int, db: Session = Depends(get_db),
                   admin=Depends(get_current_admin)):
    variant = db.get(ProductVariant, id)
    if not variant:
        raise HTTPException(404, "Variant not found")

    db.delete(variant)
    db.commit()
    return {"message": "Variant deleted"}