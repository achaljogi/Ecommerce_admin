from pydantic import BaseModel, ConfigDict, Field


# =========================
# AUTH
# =========================

class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# =========================
# BRAND
# =========================

class BrandBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    logo_url: str | None = None
    is_active: bool = True


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    logo_url: str | None = None
    is_active: bool | None = None


class BrandResponse(BrandBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# CATEGORY
# =========================

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    image_url: str | None = None
    is_active: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    image_url: str | None = None
    is_active: bool | None = None


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# SUBCATEGORY
# =========================

class SubCategoryBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    image_url: str | None = None
    is_active: bool = True
    category_id: int


class SubCategoryCreate(SubCategoryBase):
    pass


class SubCategoryUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    image_url: str | None = None
    is_active: bool | None = None
    category_id: int | None = None


class SubCategoryResponse(SubCategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# PRODUCT
# =========================

class ProductBase(BaseModel):
    name: str
    slug: str
    description: str | None = None
    sku: str
    base_price: float = Field(ge=0)
    is_active: bool = True

    brand_id: int
    category_id: int
    subcategory_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    sku: str | None = None
    base_price: float | None = Field(default=None, ge=0)
    is_active: bool | None = None

    brand_id: int | None = None
    category_id: int | None = None
    subcategory_id: int | None = None


class ProductResponse(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# =========================
# PRODUCT VARIANT
# =========================

class VariantBase(BaseModel):
    product_id: int
    sku: str
    variant_name: str
    price: float = Field(ge=0)
    stock_quantity: int = Field(default=0, ge=0)
    is_active: bool = True


class VariantCreate(VariantBase):
    pass


class VariantUpdate(BaseModel):
    product_id: int | None = None
    sku: str | None = None
    variant_name: str | None = None
    price: float | None = Field(default=None, ge=0)
    stock_quantity: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class VariantResponse(VariantBase):
    id: int

    model_config = ConfigDict(from_attributes=True)