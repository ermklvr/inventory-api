import random
from decimal import Decimal

from app.database import SessionLocal
from app.models import Category, Product, MovementType
from app.schemas import MovementCreate
from app.crud import create_movement


CATEGORIES = {
    "Eletrônicos": [
        ("Notebook Pro 14", 4599.90),
        ("Notebook Air 13", 3899.90),
        ("Monitor 24 Full HD", 899.90),
        ("Monitor 27 QHD", 1599.90),
        ("Smartphone X1", 2499.90),
    ],
    "Periféricos": [
        ("Mouse sem fio", 89.90),
        ("Mouse Gamer", 199.90),
        ("Teclado Mecânico", 349.90),
        ("Teclado Sem Fio", 179.90),
        ("Headset Gamer", 299.90),
    ],
    "Informática": [
        ("SSD 1TB", 499.90),
        ("SSD 2TB", 899.90),
        ("Memória RAM 8GB", 159.90),
        ("Memória RAM 16GB", 289.90),
        ("HD Externo 2TB", 449.90),
    ],
    "Celulares": [
        ("Smartphone Alpha", 1899.90),
        ("Smartphone Beta", 2299.90),
        ("Smartphone Gamma", 3199.90),
        ("Tablet 10 Polegadas", 1299.90),
        ("Tablet Pro", 2199.90),
    ],
    "Áudio": [
        ("Fone Bluetooth", 149.90),
        ("Fone TWS", 249.90),
        ("Caixa de Som", 399.90),
        ("Soundbar", 899.90),
        ("Microfone USB", 499.90),
    ],
    "Escritório": [
        ("Cadeira Escritório", 899.90),
        ("Mesa Escritório", 699.90),
        ("Luminária LED", 129.90),
        ("Suporte para Monitor", 159.90),
        ("Gaveteiro", 299.90),
    ],
    "Acessórios": [
        ("Cabo HDMI", 49.90),
        ("Cabo USB-C", 39.90),
        ("Hub USB", 119.90),
        ("Carregador Universal", 99.90),
        ("Adaptador Bluetooth", 59.90),
    ],
    "Gaming": [
        ("Controle Wireless", 299.90),
        ("Console Gamer", 3999.90),
        ("Mousepad RGB", 129.90),
        ("Cadeira Gamer", 1499.90),
        ("Volante Gamer", 1299.90),
    ],
    "Redes": [
        ("Roteador Wi-Fi 5", 249.90),
        ("Roteador Wi-Fi 6", 499.90),
        ("Switch 8 Portas", 299.90),
        ("Access Point", 449.90),
        ("Repetidor Wi-Fi", 179.90),
    ],
    "Armazenamento": [
        ("Pendrive 64GB", 39.90),
        ("Pendrive 128GB", 69.90),
        ("Cartão SD 128GB", 89.90),
        ("Cartão SD 256GB", 149.90),
        ("SSD Externo 1TB", 599.90),
    ],
    "Casa Inteligente": [
        ("Lâmpada Inteligente", 69.90),
        ("Tomada Inteligente", 89.90),
        ("Câmera Wi-Fi", 299.90),
        ("Sensor de Movimento", 119.90),
        ("Campainha Inteligente", 399.90),
    ],
    "Impressão": [
        ("Impressora Multifuncional", 899.90),
        ("Impressora Laser", 1299.90),
        ("Scanner", 699.90),
        ("Cartucho Preto", 129.90),
        ("Toner Compatível", 199.90),
    ],
}


def seed():
    db = SessionLocal()

    try:
        # Evita duplicar a seed
        if db.query(Category).first():
            print("Banco já possui dados. Seed não executado.")
            return

        # ---------------------------------
        # 1. Categorias
        # ---------------------------------

        categories = {}

        for category_name in CATEGORIES:
            category = Category(name=category_name)
            db.add(category)
            categories[category_name] = category

        db.flush()

        # ---------------------------------
        # 2. Produtos
        # ---------------------------------

        products = []

        for category_name, category_products in CATEGORIES.items():
            category = categories[category_name]

            for name, price in category_products:
                product = Product(
                    name=name,
                    price=Decimal(str(price)),
                    stock_quantity=0,
                    category_id=category.id,
                    active=True,
                )

                db.add(product)
                products.append(product)

        db.commit()

        # ---------------------------------
        # 3. Movimentações
        # ---------------------------------

        random_generator = random.Random(42)

        total_movements = 0

        for product in products:
            # Toda mercadoria começa recebendo estoque.
            initial_quantity = random_generator.randint(20, 100)

            create_movement(
                db,
                MovementCreate(
                    product_id=product.id,
                    type=MovementType.IN,
                    quantity=initial_quantity,
                ),
            )

            total_movements += 1

            # Mais algumas movimentações aleatórias
            number_of_movements = random_generator.randint(2, 4)

            for _ in range(number_of_movements):
                current_stock = product.stock_quantity

                # Se o estoque estiver baixo,
                # garantimos uma entrada.
                if current_stock < 10:
                    movement_type = MovementType.IN
                else:
                    movement_type = random_generator.choice(
                        [
                            MovementType.IN,
                            MovementType.IN,
                            MovementType.OUT,
                        ]
                    )

                if movement_type == MovementType.IN:
                    quantity = random_generator.randint(5, 40)

                else:
                    quantity = random_generator.randint(
                        1,
                        min(current_stock, 20),
                    )

                create_movement(
                    db,
                    MovementCreate(
                        product_id=product.id,
                        type=movement_type,
                        quantity=quantity,
                    ),
                )

                total_movements += 1

        print("Seed executado com sucesso!")
        print(f"Categorias criadas: {len(categories)}")
        print(f"Produtos criados: {len(products)}")
        print(f"Movimentações criadas: {total_movements}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()