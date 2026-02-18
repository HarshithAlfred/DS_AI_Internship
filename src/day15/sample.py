p_ham=0.9
p_spam=0.1
p_free_spam = 0.9
p__free_ham = 0.05

p_free = (p_free_spam * p_spam) + (p__free_ham *p_ham)
print(p_free)
# Bays formula
 
p_spam_free = p_free_spam * p_spam / p_free

print(p_spam_free)
