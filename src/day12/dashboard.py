import matplotlib.pyplot as plt
categories =['Electronics', 'Clothing', 'Home']
values =[300, 450, 200]
plt.figure()
plt.subplot(1,2,1)
plt.bar(categories,values,color=['blue', 'green', 'orange'])
plt.xlabel("Appliances")
plt.ylabel("Rate")

plt.subplot(1,2,2)
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May']
trend = [200, 250, 300, 280, 350]
plt.plot(months , trend,marker='o')
plt.xlabel("Month")
plt.ylabel("Trend")


plt.tight_layout()
plt.show()
