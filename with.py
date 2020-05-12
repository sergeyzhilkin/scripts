def foo():
    with open('somef','w') as f:
        try:
            f.write('a')
        except:
            print('unexpected_error') 
if __name__ == '__main__':
    foo()
