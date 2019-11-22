import os

print(os.pardir)
print(os.getcwd())
print(os.path.abspath(os.path.join(os.getcwd(), os.pardir)))

