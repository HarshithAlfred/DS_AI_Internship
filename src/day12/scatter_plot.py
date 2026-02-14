import matplotlib.pyplot as plt
study_hours = [1, 2, 3, 4, 5, 6, 7, 8]
scores = [50, 55, 65, 70, 75, 85, 90, 95]

plt.figure()
plt.scatter(study_hours,scores)
plt.title("Results")
plt.xlabel("study hours")
plt.ylabel("Scores")
plt.show()