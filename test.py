from faker import Faker

f = Faker('ru_Ru')

for i in range(100):
    print(f.address())