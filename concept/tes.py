huruf = ['a', 'b', 'c']
tes0 = ['d', 'a']
tes1 = ['e', 'd']

hasil0 = any([True for h in tes0 if h in huruf])
hasil1 = any([True for h in tes1 if h in huruf])

print(hasil0)
print(hasil1)

print(any([]))

angka = [1,2,3]
sambung = list(zip(huruf, angka))
# print(sambung[:,1])