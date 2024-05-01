import matplotlib.pyplot as plt
# import pandas as pd

# new_data = pd.DataFrame({'candidate name': ['annas', 'fang'], 'developer': [4, 4], 'python': [1, 1]})


# print(new_data)
def plot(new_data):
    plt.rcParams.update({'font.size': 16})
    ax = new_data.plot.barh(title="Resume keywords by category", legend=False, figsize=(25, 7), stacked=True)
    labels = []
    for j in new_data.columns:
        for i in new_data.index:
            label = str(j) + ": " + str(new_data.loc[i][j])
            labels.append(label)
    patches = ax.patches
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(x + width / 2., y + height / 2., label, ha='center', va='center')
    plt.savefig(f'plots/new_plot.png')
