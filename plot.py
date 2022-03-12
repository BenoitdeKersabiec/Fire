import matplotlib.pyplot as plt
from matplotlib.widgets import Cursor
import matplotlib.dates as mdates

coord = []


def human_format(num):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    # add more suffixes if you need them
    return '%.2f%s' % (num, ['', 'K', 'M', 'G', 'T', 'P'][magnitude])


def plot_data(data):
    fig = plt.figure()
    ax = fig.subplots()
    data.plot(ax=ax, ylabel="€")

    cursor = Cursor(ax, horizOn=True, vertOn=True, useblit=True,
                    color='r', linewidth=1)
    annot = ax.annotate("", xy=(26000, 26000), xytext=(40, 40), textcoords="offset points",
                        bbox=dict(boxstyle='round4', fc='linen', ec='k', lw=1),
                        arrowprops=dict(arrowstyle='-|>'))
    annot.set_visible(False)

    def onclick(event):
        global coord
        coord.append((event.xdata, event.ydata))
        x = event.xdata
        y = event.ydata

        # printing the values of the selected point
        print([x, y])
        annot.xy = (x, y)
        text = "Date: {}\nNet-worth: {}".format(mdates.num2date(x*365/12).strftime("%d/%m/%Y"), human_format(int(y)))
        annot.set_text(text)
        annot.set_visible(True)
        fig.canvas.draw()

    fig.canvas.mpl_connect('button_press_event', onclick)
    return ax
