from sqlalchemy import *
from sqlalchemy.orm import *
from datetime import datetime


engine = create_engine("sqlite:///kol3.db", echo=False)
Base = declarative_base()

class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    address = Column(String(100))
    items = relationship('Item', back_populates='shop')

    def __repr__(self):
        return f"Name: {self.name} | Address: {self.address}"

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    barcode = Column(String(32), unique=True)
    name = Column(String(40), nullable=False)
    description = Column(String(200), default='')
    unit_price = Column(Numeric(10, 2), nullable=False, default=1.00)
    created_at = Column(DateTime, default=datetime.now())
    shop_id = Column(Integer, ForeignKey('shops.id'))
    shop = relationship("Shop", back_populates="items")
    components = relationship("Components", back_populates="item")

    def __repr__(self):
        return f"Barcode: {self.barcode} | Name: {self.name} | Description: {self.description} | Unit Price: {self.unit_price} | Created at: {self.created_at}"

class Components(Base):
    __tablename__ = 'components'

    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    quantity = Column(Numeric(10, 2), default = 1.00)
    item_id = Column(Integer, ForeignKey('items.id'))
    item = relationship("Item", back_populates="components")

    def __repr__(self):
        return f"Name: {self.name} | Quantity: {self.quantity}"


def createEntries():
    try:
        shop_iki = Shop(name="IKI", address="Kaunas, Iki gatvė 1")
        shop_maxima = Shop(name="MAXIMA", address="Kaunas, Maksima gatvė 2")

        item_duona_iki = Item(barcode="112233112233", name="Žemaičių duona", unit_price=1.55, shop=shop_iki)
        item_pienas_iki = Item(barcode="33333222111", description="Pienas iš Žemaitijos", name="Žemaičių pienas", unit_price=2.69, shop=shop_iki)
        item_duona_maxima = Item(barcode="99898989898", name="Aukštaičių duona", unit_price=1.65, shop=shop_maxima)
        item_pienas_maxima = Item(barcode="99919191991", description="Pienas iš Aukštaitijos", name="Aukštaičių pienas", unit_price=2.99, shop=shop_maxima)

        component_miltai_iki = Components(name="Miltai", quantity=1.50, item=item_duona_iki)
        component_vanduo_iki = Components(name="Vanduo", quantity=1.00, item=item_duona_iki)
        component_pienas_iki = Components(name="Pienas", quantity=1.00, item=item_pienas_iki)
        component_miltai_maxima = Components(name="Miltai", quantity=1.60, item=item_duona_maxima)
        component_vanduo_maxima = Components(name="Vanduo", quantity=1.10, item=item_duona_maxima)
        component_pienas_maxima = Components(name="Pienas", quantity=1.10, item=item_pienas_maxima)

        session.add_all([shop_iki, shop_maxima, item_duona_iki, item_pienas_iki, item_duona_maxima, item_pienas_maxima, component_pienas_maxima, component_vanduo_maxima, component_miltai_maxima, component_pienas_iki, component_vanduo_iki, component_miltai_iki])
        session.commit()
    except:
        print("~~~~~~~~~~~~Values duplicates or are incorrect!~~~~~~~~~~~~")


def thirdTask():

    # * Pakeisti 'IKI' parduotuvės, 'Žemaičių duonos' komponento 'Vandens' kiekį (quantity) iš 1.00 į 1.45.

    iki_shop = session.query(Shop).filter_by(name='IKI').first()
    ziem_duona = session.query(Item).filter_by(name='Žemaičių duona', shop=iki_shop).first()
    vanduo_component = session.query(Components).filter_by(name='Vanduo', item=ziem_duona).first()
    print(vanduo_component.name, vanduo_component.quantity)
    vanduo_component.quantity = 1.45
    session.commit()
    print(vanduo_component.name, vanduo_component.quantity)

    # * Ištrinti 'MAXIMA' parduotuvės, 'Aukštaičių pieno' komponentą 'Pienas'.

    maxima_shop = session.query(Shop).filter_by(name='MAXIMA').first()
    aukst_pienas = session.query(Item).filter_by(name='Aukštaičių pienas', shop=maxima_shop).first()
    pienas_component = session.query(Components).filter_by(name='Pienas', item=aukst_pienas).first()
    try:
        aukst_pienas = session.query(Item).filter_by(name='Aukštaičių pienas', shop=maxima_shop).first()
        session.delete(pienas_component)
        session.commit()
    except:
        print("Not found")

def fourthTask():
    #     Atspausdinti visų parduotuvių prekes, bei tų prekių komponentus.
    shops = session.query(Shop).all()
    for shop in shops:
        print(shop)
        items = session.query(Item).filter(Item.shop_id == shop.id).all()
        for item in items:
            print(f'  * {item}')
            components = session.query(Components).filter(Components.item_id == item.id).all()
            for component in components:
                print(f"      - {component}")
        print('\n')

def fifthTask():

    while True:
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FIFTH TASK~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(f'[1] Atrinkti prekes, kurios turi susietų komponentų\n[2] Atrinkti prekes, kurių pavadinime yra tekstas "ien"\n[3] Suskaičiuoti iš kiek komponentų sudaryta kiekviena prekė\n[4] Suskaičiuoti kiekvienos prekės komponentų kiekį (quantity)\n[5] Išvesti komponentus kurių kiekis (quantity) didesnis nei nurodytas\n\n[0] Exit')
        
        try:
            userInput = int(input('Enter your choice: '))
        except:
            print("Error occured!")
            exit(1)
        if userInput == 1:
            # * Atrinkti prekes, kurios turi susietų komponentų
            stmt = session.query(Item).join(Components, Item.id == Components.item_id).distinct()
            for item in stmt:
                print(item)

        elif userInput == 2:
            # * Atrinkti prekes, kurių pavadinime yra tekstas 'ien'
            stmt = session.query(Item).filter(Item.name.like("%ien%")).all()
            for item in stmt:
                print(item)
            pass
        elif userInput == 3:
            # * Suskaičiuoti iš kiek komponentų sudaryta kiekviena prekė
            components_count = session.query(Item.id, func.count(Components.quantity)).filter(Item.id == Components.item_id).group_by(Item.id).all()
            for component in components_count:
                stmt = session.query(Item).filter(Item.id == component[0]).one()
                print(stmt.name, component[1])
            pass
        elif userInput == 4:
            # * Suskaičiuoti kiekvienos prekės komponentų kiekį (quantity)
            components_quant = session.query(Item.name, func.sum(Components.quantity)).join(Item.components).group_by(Item.name).all()
            for item_name, quantity_sum in components_quant:
                print(f"{item_name}: {quantity_sum}")
            pass
        elif userInput == 5:
            try:
                usr_inp = int(input("Enter quantity: "))
                stmt = session.query(Components).filter(Components.quantity > usr_inp).all()
                for item in stmt:
                    print(item)
            except:
                print("Must provide an integer")

            pass
        else:
            exit(0)

if __name__ == '__main__':
    Session = sessionmaker(bind=engine)
    session = Session()
    while True:
        print(f'[1] Create table (1 Task)\n[2] Create entries (2 Task)\n[3] Change components quantities (3 Task)\n[4] Print all shops, items and componenets\n[5] Queries\n[6] Drop tables\n\n[0] Exit')
        try:
            userInput = int(input('Enter your choice: '))
        except:
            print("Error occured! Wrong input, exiting task.")
            exit(1)
        if userInput == 1:
            Base.metadata.create_all(engine)
        elif userInput == 2:
            createEntries()
        elif userInput == 3:
            thirdTask()
        elif userInput == 4:
            fourthTask()
        elif userInput == 5:
            fifthTask()
        elif userInput == 6:
            Base.metadata.drop_all(engine)
        else:
            exit(0)