from os import system
from prisma.client import Prisma

# Run migrations
print("Running migrations...")
system("prisma migrate deploy")

prisma = Prisma(auto_register=True)
