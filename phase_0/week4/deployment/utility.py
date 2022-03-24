import calendar
from datetime import timedelta

from matplotlib import pyplot as plt


def offset_month(date, n):
    return date + timedelta(days=calendar.monthrange(date.year, date.month)[1] * n)


def plot_pie_chart(title, col):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.set_title(title)
    ax.pie(col.value_counts(), labels=col.value_counts().index, autopct='%1.1f%%')
    return fig
