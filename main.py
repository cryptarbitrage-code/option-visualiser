from tkinter import *
from tkinter import ttk
import time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import option_calculations as oc

# Some chart parameters
step_number = 100
chart_size = (6, 4)

# tkinter set up
root = Tk()
root.title("Option Visualiser - Cryptarbitrage")
root.iconbitmap('cryptarbitrage_icon_96px.ico')
root.minsize(600, 400)

# Details input frame
details_frame = LabelFrame(root, text="Details", padx=2, pady=2)
details_frame.grid(row=0, column=0, padx=2, pady=2, sticky=NW)
# Chart frames
chart1_frame = LabelFrame(root, text="Option Profit/Loss", padx=2, pady=2)
chart1_frame.grid(row=0, column=1, padx=2, pady=2)


def calculate_profit():
    premium = float(premium_input.get())
    strike = float(strike_price_input.get())
    chart_low = float(chart_minprice_input.get())
    chart_high = float(chart_maxprice_input.get())
    if selected_option_type.get() == "Call":
        option_type = "C"
    else:
        option_type = "P"
    profit_list = oc.option_profit_expiry(premium, strike, chart_low, chart_high, option_type, step_number)
    return profit_list


def plot_charts():
    # Destroy old charts if any
    for widgets in chart1_frame.winfo_children():
        widgets.destroy()
    # Generate x axis values
    x_range = []
    chart_low = float(chart_minprice_input.get())
    chart_high = float(chart_maxprice_input.get())
    for step in range(0, step_number + 1):
        x_range.append(step * (chart_high - chart_low) / 100 + chart_low)
    option1_data = calculate_profit()
    option1_np = np.array(option1_data)
    zero_np = np.array([0] * (step_number + 1))

    # CHART 1
    # the figure that will contain the plot
    fig1 = Figure(figsize=chart_size, dpi=100)
    # adding the subplot
    plot1 = fig1.add_subplot(111)
    # plotting the graph
    plot1.plot(x_range, option1_data, linewidth=2, label='$' + str(strike_price_input.get()) + ' ' + selected_option_type.get())
    plot1.fill_between(x_range, option1_data, 0, where=(option1_np < zero_np), facecolor='red', interpolate=True, alpha=0.15)
    plot1.fill_between(x_range, option1_data, 0, where=(option1_np >= zero_np), facecolor='green', interpolate=True, alpha=0.15)
    plot1.set_xlabel('Underlying Price')
    plot1.set_ylabel('Profit/Loss')
    # plot1.set_title('Chart Title')
    plot1.legend()
    plot1.grid(True, alpha=0.25)
    fig1.tight_layout()
    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas1 = FigureCanvasTkAgg(fig1, master=chart1_frame)
    canvas1.draw()
    # placing the canvas on the Tkinter window
    canvas1.get_tk_widget().pack()
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas1, chart1_frame)
    toolbar.update()
    # placing the toolbar on the Tkinter window
    canvas1.get_tk_widget().pack()

    plt.show()


# details_frame components
selected_option_type = StringVar()
selected_option_type.set("Call")
option_type_label = Label(details_frame, text="Option Type: ")
option_type_label.grid(row=0, column=0)
option_type_dropdown = OptionMenu(details_frame, selected_option_type, "Call", "Put")
option_type_dropdown.grid(row=0, column=1)
option_type_dropdown.config(width=10)

premium_label = Label(details_frame, text="Option Premium: ")
premium_label.grid(row=1, column=0)
premium_input = Entry(details_frame, width=15)
premium_input.grid(row=1, column=1, padx=5, pady=5)

strike_price_label = Label(details_frame, text="Strike Price: ")
strike_price_label.grid(row=2, column=0)
strike_price_input = Entry(details_frame, width=15)
strike_price_input.grid(row=2, column=1, padx=5, pady=5)

chart_minprice_label = Label(details_frame, text="Chart Min Price: ")
chart_minprice_label.grid(row=3, column=0)
chart_minprice_input = Entry(details_frame, width=15)
chart_minprice_input.grid(row=3, column=1, padx=5, pady=5)

chart_maxprice_label = Label(details_frame, text="Chart Max Price: ")
chart_maxprice_label.grid(row=4, column=0)
chart_maxprice_input = Entry(details_frame, width=15)
chart_maxprice_input.grid(row=4, column=1, padx=5, pady=5)

# button that displays the plot
plot_button = Button(master=details_frame,
                     command=plot_charts,
                     height=2,
                     width=10,
                     text="Plot")

plot_button.grid(row=5, column=0, columnspan=2)

root.mainloop()
