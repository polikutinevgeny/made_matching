from typing import List, Optional

from sqlalchemy import Column, String
from sqlmodel import SQLModel, Field, Relationship


class Chain(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    stores: List["Store"] = Relationship(back_populates="chain")
    products: List["Product"] = Relationship(back_populates="chain")


class Store(SQLModel, table=True):
    store_id: int = Field(primary_key=True)
    chain_id: int = Field(foreign_key="chain.id")
    chain: Chain = Relationship(back_populates="stores")


class ProductToCategory(SQLModel, table=True):
    product_id: str = Field(foreign_key="product.item_id", primary_key=True)
    category_id: str = Field(foreign_key="category.category_id", primary_key=True)


class ProductToAdditionalCategory(SQLModel, table=True):
    product_id: str = Field(foreign_key="product.item_id", primary_key=True)
    category_id: str = Field(foreign_key="category.category_id", primary_key=True)


_category_id_column = Column("category_id", String, primary_key=True, nullable=False)


class Category(SQLModel, table=True):
    category_id: str = Field(sa_column=_category_id_column)
    chain_id: int = Field(foreign_key="chain.id")
    chain: Chain = Relationship()
    name: str
    parent_id: Optional[str] = Field(foreign_key="category.category_id")
    parent: Optional["Category"] = Relationship(
        back_populates="children", sa_relationship_kwargs=dict(remote_side=[_category_id_column]))
    children: List["Category"] = Relationship(back_populates="parent")
    is_main: bool
    products: List["Product"] = Relationship(back_populates="categories", link_model=ProductToCategory)
    external_products: List["Product"] = Relationship(back_populates="external_categories",
                                                      link_model=ProductToAdditionalCategory)


class Product(SQLModel, table=True):
    item_id: str = Field(primary_key=True)
    chain_id: int = Field(foreign_key="chain.id")
    chain: Chain = Relationship(back_populates="products")
    name: str
    categories: List[Category] = Relationship(back_populates="products", link_model=ProductToCategory)
    external_categories: List[Category] = Relationship(back_populates="external_products",
                                                       link_model=ProductToAdditionalCategory)
    brand_name: str
    grammar: Optional[int]
    volume: Optional[int]
    weight: Optional[int]
    prices: List["Price"] = Relationship(back_populates="item")


class Price(SQLModel, table=True):
    store_id: int = Field(foreign_key="store.store_id", primary_key=True)
    store: Store = Relationship()
    item_id: str = Field(foreign_key="product.item_id", primary_key=True)
    item: Product = Relationship(back_populates="prices")
    price: int
    discount_price: int
