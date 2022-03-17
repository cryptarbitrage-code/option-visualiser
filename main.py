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
# Details input frame
option_details_frame = LabelFrame(root, text="Option Details", padx=2, pady=2)
option_details_frame.grid(row=1, column=0, padx=2, pady=2, sticky=NW)
# Chart frames
chart1_frame = LabelFrame(root, text="Option Profit/Loss", padx=2, pady=2)
chart1_frame.grid(row=0, column=1, rowspan=2, padx=2, pady=2)


def calculate_profit():
    individual_option_profits = []
    total_profit = [0] * (step_number + 1)
    # calculate profit for each included option
    for i in range(0, number_of_options):
        if option_details_list[i]['include_variable'].get():
            premium = float(option_details_list[i]['premium_input'].get())
            strike = float(option_details_list[i]['strike_input'].get())
            chart_low = float(chart_minprice_input.get())
            chart_high = float(chart_maxprice_input.get())
            if option_details_list[i]['option_type_var'].get() == "Call":
                option_type = "C"
            else:
                option_type = "P"
            if selected_contract_type.get() == "Linear":
                profit_list = oc.option_profit_expiry(premium, strike, chart_low, chart_high, option_type, step_number)
            else:
                profit_list = oc.inverse_option_profit_expiry(premium, strike, chart_low, chart_high, option_type, step_number)
            individual_option_profits.append(profit_list)
    # calculate the total profit
    for option in individual_option_profits:
        for step in range(0, step_number + 1):
            total_profit[step] = total_profit[step] + option[step]

    return total_profit


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
    plot1.plot(x_range, option1_data, linewidth=2, label='Total PNL')
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
selected_contract_type = StringVar()
selected_contract_type.set("Linear")
contract_type_label = Label(details_frame, text="Contract Type: ")
contract_type_label.grid(row=0, column=0)
contract_type_dropdown = OptionMenu(details_frame, selected_contract_type, "Linear", "Inverse")
contract_type_dropdown.grid(row=0, column=1)
contract_type_dropdown.config(width=10)

chart_minprice_label = Label(details_frame, text="Chart Min Price: ")
chart_minprice_label.grid(row=1, column=0)
chart_minprice_input = Entry(details_frame, width=15)
chart_minprice_input.grid(row=1, column=1, padx=5, pady=5)

chart_maxprice_label = Label(details_frame, text="Chart Max Price: ")
chart_maxprice_label.grid(row=2, column=0)
chart_maxprice_input = Entry(details_frame, width=15)
chart_maxprice_input.grid(row=2, column=1, padx=5, pady=5)

# option_details_frame
selected_option_type = StringVar()
selected_option_type.set("Call")
option_type_label = Label(option_details_frame, text="Option Type:")
option_type_label.grid(row=0, column=0)
premium_label = Label(option_details_frame, text="Option Premium:")
premium_label.grid(row=0, column=1)
strike_price_label = Label(option_details_frame, text="Strike Price:")
strike_price_label.grid(row=0, column=2)
include_label = Label(option_details_frame, text="Size:")
include_label.grid(row=0, column=3)
include_label = Label(option_details_frame, text="Include:")
include_label.grid(row=0, column=4)

# initialise the array of option details
number_of_options = 4
number_of_fields = 7
option_details_list = []
for i in range(0, number_of_options):
    single_option = {'option_type_var': 'Call',
                     'option_type_input': 0,
                     'premium_input': 0,
                     'strike_input': 0,
                     'quantity': 0,
                     'include_variable': 0,
                     'include_checkbox': 0}
    option_details_list.append(single_option)
print(option_details_list)
# populate the array with the correct elements
for i in range(0, number_of_options):
    # option type variable
    option_details_list[i]['option_type_var'] = StringVar()
    option_details_list[i]['option_type_var'].set("Call")
    # option type input
    option_details_list[i]['option_type_input'] = OptionMenu(option_details_frame, option_details_list[i]['option_type_var'], "Call", "Put")
    option_details_list[i]['option_type_input'].grid(row=i + 2, column=0)
    option_details_list[i]['option_type_input'].config(width=10)
    # premium input
    option_details_list[i]['premium_input'] = Entry(option_details_frame, width=15)
    option_details_list[i]['premium_input'].grid(row=i + 2, column=1, padx=5, pady=5)
    # strike input
    option_details_list[i]['strike_input'] = Entry(option_details_frame, width=15)
    option_details_list[i]['strike_input'].grid(row=i + 2, column=2, padx=5, pady=5)
    # quantity
    option_details_list[i]['quantity'] = Entry(option_details_frame, width=15)
    option_details_list[i]['quantity'].grid(row=i + 2, column=3, padx=5, pady=5)
    # include variable
    option_details_list[i]['include_variable'] = IntVar()
    # include checkbox
    option_details_list[i]['include_checkbox'] = Checkbutton(option_details_frame, variable=option_details_list[i]['include_variable'])
    option_details_list[i]['include_checkbox'].grid(row=i + 2, column=4, padx=5, pady=5)


# button that displays the plot
plot_button = Button(master=option_details_frame,
                     command=plot_charts,
                     height=2,
                     width=10,
                     text="Plot")

plot_button.grid(row=6, column=0, columnspan=2)

root.mainloop()
