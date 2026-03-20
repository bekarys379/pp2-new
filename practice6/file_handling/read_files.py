#To open a file for reading it is enough to specify the name of the file:
f=open("example1.txt")
print()

'''To open the file, use the built-in open() function.

The open() function returns a file object, which has a read() method for reading the content of the file:'''
f=open("example1.txt")
print(f.read())