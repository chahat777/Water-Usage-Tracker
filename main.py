import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import pyttsx3
from matplotlib.animation import FuncAnimation
from matplotlib import font_manager

data_file = "water_usage_data.csv"

def bol_de(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    for voice in voices:
        if "male" in voice.name.lower() or "hindi" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.say(text)
    engine.runAndWait()

def load_data():
    if os.path.exists(data_file):
        return pd.read_csv(data_file)
    return pd.DataFrame(columns=["Date", "Brushing", "Bathing", "Cooking", "Other"])

def save_data(data):
    data.to_csv(data_file, index=False)

def add_entry(data):
    date = datetime.now().strftime("%d-%m-%Y")
    brushing = int(input("Brushing (liters): "))
    bathing = int(input("Bathing (liters): "))
    cooking = int(input("Cooking (liters): "))
    other = int(input("Other (liters): "))
    new_row = pd.DataFrame([{"Date": date, "Brushing": brushing, "Bathing": bathing, "Cooking": cooking, "Other": other}])
    data = pd.concat([data, new_row], ignore_index=True)
    save_data(data)
    print("Data successfully saved!")
    bol_de(f"Your water usage data has been saved for {date}.")
    return data

def view_usage(data):
    if data.empty:
        print("No data available.")
        return
    total = data[["Brushing", "Bathing", "Cooking", "Other"]].sum()
    categories = total.index.tolist()
    values = total.values.tolist()
    colors = ['#FFD700', '#00CED1', '#F5A623', '#D0021B']
    fig, ax = plt.subplots(figsize=(14, 8))
    bars = ax.barh(categories, values, color=colors, picker=True)
    title_font = font_manager.FontProperties(family='Verdana', weight='bold', size=30)
    label_font = font_manager.FontProperties(family='Verdana', weight='bold', size=18)
    tick_font = font_manager.FontProperties(family='Verdana', size=16)
    ax.set_title("Total Water Usage by Chahat Kumar", fontproperties=title_font, pad=20)
    ax.set_xlabel("Total Water Usage (liters)", fontproperties=label_font)
    ax.set_ylabel("Activities", fontproperties=label_font)
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontproperties(tick_font)
    def animate(i):
        for bar in bars:
            bar.set_width(bar.get_width() * 1.01)
        return bars
    FuncAnimation(fig, animate, frames=50, interval=300, blit=False)
    annot = ax.annotate("", xy=(0,0), xytext=(20,20), textcoords="offset points", bbox=dict(boxstyle="round,pad=0.5", fc="yellow", alpha=0.8), arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)
    def update_annot(bar):
        x = bar.get_width()
        y = bar.get_y() + bar.get_height()/2
        idx = bars.index(bar)
        annot.xy = (x, y)
        annot.set_text(f"{categories[idx]}: {values[idx]} L")
    def on_move(event):
        if event.inaxes == ax:
            for bar in bars:
                cont, _ = bar.contains(event)
                if cont:
                    update_annot(bar)
                    annot.set_visible(True)
                    fig.canvas.draw_idle()
                    return
        if annot.get_visible():
            annot.set_visible(False)
            fig.canvas.draw_idle()
    fig.canvas.mpl_connect("motion_notify_event", on_move)
    footer_font = font_manager.FontProperties(family='Verdana', weight='normal', size=20)
    plt.figtext(0.5, 0.92, "Project by Chahat Kumar", ha="center", fontproperties=footer_font, color="darkblue")
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    plt.show()
    bol_de(f"Today, you have used {int(sum(values))} liters of water.")

def view_by_date(data):
    date = input("Which date's data do you want to view? (DD-MM-YYYY): ")
    entry = data[data["Date"] == date]
    if entry.empty:
        print("No data found for this date.")
    else:
        print(entry.to_string(index=False))

def export_csv(data):
    filename = input("Enter CSV file name (e.g., output.csv): ")
    data.to_csv(filename, index=False)
    print(f"Data has been exported to '{filename}'!")

def clear_data():
    if os.path.exists(data_file):
        os.remove(data_file)
        print("All data has been deleted!")
        bol_de("All data has been deleted.")
    else:
        print("No data file found.")

def main():
    data = load_data()
    while True:
        print("\n✨💧 ===== AquaTrack by Chahat Kumar ===== 💧✨")
        print("╔══════════════════════════════════════╗")
        print("║ 1. 📊 View Water Usage               ║")
        print("║ 2. 📝 Add New Entry                  ║")
        print("║ 3. 📅 View Entries By Date           ║")
        print("║ 4. 💾 Export Data To CSV             ║")
        print("║ 5. 🧹 Clear All Data                 ║")
        print("║ 6. 🚪 Exit                            ║")
        print("╚══════════════════════════════════════╝")
        choice = input("➡ Choose your action (1/2/3/4/5/6): ")
        if choice == "1":
            view_usage(data)
        elif choice == "2":
            data = add_entry(data)
        elif choice == "3":
            view_by_date(data)
        elif choice == "4":
            export_csv(data)
        elif choice == "5":
            clear_data()
            data = pd.DataFrame(columns=["Date", "Brushing", "Bathing", "Cooking", "Other"])
        elif choice == "6":
            bol_de("Thank you! See you again.")
            break
        else:
            print("Invalid choice. Please choose between 1-6.")

if __name__ == "__main__":
    main()