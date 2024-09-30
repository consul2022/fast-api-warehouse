import uvicorn
from fastapi import FastAPI

from app.models import Base
from app.database import engine
from app.routers import products, orders

# Асинхронная функция для создания таблиц
async def create_tables():
    async with engine.begin() as conn:
        # Используем run_sync для выполнения синхронных операций
        await conn.run_sync(Base.metadata.create_all)

# Создание экземпляра приложения FastAPI
app = FastAPI(
    title="Warehouse API",
    description="API for managing warehouse processes",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Support Team",
        "url": "https://t.me/Slava_brave",
        "email": "lysenko-vyacheslav2008@yandex.ru",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    },
    openapi_tags=[
        {
            "name": "products",
            "description": "Operations with products"
        },
        {
            "name": "orders",
            "description": "Operations with orders"
        }
    ]
)


# Подключение роутеров
app.include_router(products.router)
app.include_router(orders.router)

# Включение инициализации базы данных при запуске приложения
@app.on_event("startup")
async def on_startup():
    await create_tables()

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


