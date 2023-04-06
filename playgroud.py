l = [('DS', None), ('SQL', 23), ('SQL ', 34), ('ML', 139)]
lll =  [i[0] for i in l if i[1]!= None]



ll = [i[0] for i in l]
distinct_subjects =  [i[0] for i in l if i[1]!= None]
learn_total_per_subject = [i[1] for i in l if i[1]!= None]



print (ll)

print (l[0][1])
print ('THis is what you want ' , distinct_subjects)

print ('-'*76)

l1 = ['SQL',  'SQLL ', 'ML']
l2 = ['#4393E5', '#43BAE5', '#7AE6EA']

for legend, color in list(zip(l1, l2)):
    print (legend, color )

print ('~'*99)

data = 

color_palette = ['#4393E5', '#43BAE5', '#7AE6EA', '#4933FF', '#33FF8A',
                     '#FF33C1', '#FF336E', '#FF4633', '#F9FF33', '#3FFF33'] 
#colors = random.choices(color_palette, k = len(data)) Radnom can repeat
colors = color_palette[:len(data)]
print (colors)