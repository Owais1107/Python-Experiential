import matplotlib.pyplot as plt
import pandas as pd
# Smart Home Energy Consumption Monitor
appliances = []
electricity_rate = 8  # Cost per unit in rupees
def add_appliance():
    name = input("Enter appliance name: ")
    power = float(input("Enter power rating (Watts): "))
    hours = float(input("Enter daily usage (Hours): "))
    energy = (power * hours) / 1000
    cost = energy * electricity_rate
    appliances.append({
        "Appliance": name,
        "Power (W)": power,
        "Hours/Day": hours,
        "Energy (kWh/day)": energy,
        "Daily Cost (Rs)": cost
    })
    print("Appliance added successfully!")
def display_consumption():
    if not appliances:
        print("No appliance data available.")
        return
    df = pd.DataFrame(appliances)
    print("\n--- Energy Consumption Report ---")
    print(df.to_string(index=False))
    total_energy = df["Energy (kWh/day)"].sum()
    total_cost = df["Daily Cost (Rs)"].sum()
    print("\nTotal Daily Consumption:", round(total_energy, 2), "kWh")
    print("Total Daily Cost: Rs.", round(total_cost, 2))
    print("Estimated Monthly Cost: Rs.", round(total_cost * 30, 2))
def identify_high_energy():
    if not appliances:
        print("No appliance data available.")
        return
    df = pd.DataFrame(appliances)
    average = df["Energy (kWh/day)"].mean()
    print("\n--- High Energy Appliances ---")
    high_energy = df[df["Energy (kWh/day)"] > average]
    if high_energy.empty:
        print("No appliances consume more than the average.")
    else:
        print(high_energy[["Appliance", "Energy (kWh/day)"]])
def energy_recommendations():
    if not appliances:
        print("Please add appliances first.")
        return
    print("\n--- Energy Saving Recommendations ---")
    for item in appliances:
        name = item["Appliance"].lower()
        hours = item["Hours/Day"]
        power = item["Power (W)"]
        if hours >= 8:
            print(f"{item['Appliance']}: Reduce unnecessary operating hours.")
        if power >= 1000:
            print(f"{item['Appliance']}: Use energy-efficient settings.")
        if "light" in name or "bulb" in name:
            print(f"{item['Appliance']}: Consider using LED bulbs.")
def visualize_consumption():
    if not appliances:
        print("No data available for visualization.")
        return
    df = pd.DataFrame(appliances)
    plt.figure(figsize=(9, 5))
    plt.bar(df["Appliance"], df["Energy (kWh/day)"])
    plt.xlabel("Appliances")
    plt.ylabel("Energy Consumption (kWh/day)")
    plt.title("Daily Appliance Energy Consumption")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()
    plt.figure(figsize=(7, 7))
    plt.pie(
        df["Energy (kWh/day)"],
        labels=df["Appliance"],
        autopct="%1.1f%%"
    )
    plt.title("Household Energy Consumption Distribution")
    plt.show()
def main():
    while True:
        print("\n===== SMART HOME ENERGY MONITOR =====")
        print("1. Add Appliance")
        print("2. Display Consumption Report")
        print("3. Identify High Energy Appliances")
        print("4. Energy Saving Recommendations")
        print("5. Visualize Consumption")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_appliance()
        elif choice == "2":
            display_consumption()
        elif choice == "3":
            identify_high_energy()
        elif choice == "4":
            energy_recommendations()
        elif choice == "5":
            visualize_consumption()
        elif choice == "6":
            print("Thank you for using the Energy Monitor!")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
