l = [('DS', None), ('SQL', 23), ('SQL ', 34), ('ML', 139)]
lll =  [i[0] for i in l if i[1]!= None]



ll = [i[0] for i in l]
distinct_subjects =  [i[0] for i in l if i[1]!= None]
learn_total_per_subject = [i[1] for i in l if i[1]!= None]



print (ll)

print (l[0][1])
print ('THis is what you want ' , distinct_subjects)