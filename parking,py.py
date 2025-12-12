import datetime
from typing import Dict, Optional, Tuple


class SmartParkingSystem:
    def __init__(self, total_slots: int = 50):   # FIXED __init__
        self.total_slots = total_slots
        self.parking_slots: Dict[int, Dict] = {i: None for i in range(1, total_slots + 1)}
        self.revenue_today = 0.0
        self.vehicles_today = 0
        self.daily_records = []

        self.pricing = {
            'bike': {'base': 10, 'hourly': 5},
            'car': {'base': 20, 'hourly': 10},
            'ev': {'base': 25, 'hourly': 12},
            'heavy': {'base': 50, 'hourly': 25}
        }

    def find_free_slot(self) -> Optional[int]:
        for slot, vehicle in self.parking_slots.items():
            if vehicle is None:
                return slot
        return None

    def vehicle_entry(self, vehicle_no: str, vehicle_type: str) -> str:
        if vehicle_type not in self.pricing:
            return f"Error: Invalid vehicle type '{vehicle_type}'. Use: bike, car, ev, heavy"

        free_slot = self.find_free_slot()
        if free_slot is None:
            return "Parking Full! No slots available."

        entry_time = datetime.datetime.now()
        self.parking_slots[free_slot] = {
            'vehicle_no': vehicle_no,
            'type': vehicle_type,
            'entry_time': entry_time
        }
        self.vehicles_today += 1

        return (
            f"Vehicle {vehicle_no} ({vehicle_type}) parked in Slot {free_slot} "
            f"at {entry_time.strftime('%H:%M:%S')}"
        )

    def calculate_charges(self, slot: int) -> Tuple[float, datetime.datetime]:
        vehicle_data = self.parking_slots.get(slot)
        if not vehicle_data:
            return 0.0, None

        exit_time = datetime.datetime.now()
        duration_hours = (exit_time - vehicle_data['entry_time']).total_seconds() / 3600

        rates = self.pricing[vehicle_data['type']]
        if duration_hours <= 2:
            charges = rates['base']
        else:
            charges = rates['base'] + (duration_hours - 2) * rates['hourly']

        return round(charges, 2), exit_time

    def vehicle_exit(self, slot: int) -> str:
        vehicle_data = self.parking_slots.get(slot)
        if not vehicle_data:
            return f"Slot {slot} is empty or invalid."

        charges, exit_time = self.calculate_charges(slot)
        entry_time = vehicle_data['entry_time']
        vehicle_no = vehicle_data['vehicle_no']
        vtype = vehicle_data['type']

        duration = (exit_time - entry_time).total_seconds() / 3600
        self.revenue_today += charges
        self.parking_slots[slot] = None

        return (
            f"Vehicle {vehicle_no} ({vtype}) exiting Slot {slot}\n"
            f"Entry: {entry_time.strftime('%H:%M:%S')} | Exit: {exit_time.strftime('%H:%M:%S')}\n"
            f"Duration: {duration:.2f} hours | Charges: ₹{charges}\n"
            f"Slot {slot} now FREE."
        )

    def display_status(self) -> None:
        print("\n=== PARKING LOT STATUS ===")
        occupied = sum(1 for v in self.parking_slots.values() if v is not None)

        print(f"Total Slots: {self.total_slots} | Occupied: {occupied} | Free: {self.total_slots - occupied}")
        print(f"Today's Revenue: ₹{self.revenue_today:.2f} | Vehicles Served: {self.vehicles_today}")

        print("\nOccupied Slots:")
        for slot, data in self.parking_slots.items():
            if data:
                duration = (datetime.datetime.now() - data['entry_time']).total_seconds() / 3600
                print(f"Slot {slot}: {data['vehicle_no']} ({data['type']}) - {duration:.1f}h")

    def daily_report(self) -> str:
        vehicles = self.vehicles_today
        avg = self.revenue_today / vehicles if vehicles else 0

        peak = sum(1 for s in self.parking_slots.values() if s is not None)

        report = f"""
=== DAILY PARKING REPORT ===
Date: {datetime.datetime.now().strftime('%Y-%m-%d')}
Total Vehicles: {vehicles}
Total Revenue: ₹{self.revenue_today:.2f}
Average per vehicle: ₹{avg:.2f}
Peak Occupancy: {peak}/{self.total_slots}
"""
        self.daily_records.append(report)
        return report

    def save_report(self, filename: str = "parking_report.txt") -> None:
        with open(filename, 'a') as f:
            f.write(self.daily_report())
        print(f"Report saved to {filename}")


def main():
    parking = SmartParkingSystem(10)

    while True:
        print("\n" + "=" * 50)
        print("SMART PARKING MANAGEMENT SYSTEM")
        print("1. Vehicle Entry  2. Vehicle Exit  3. Display Status")
        print("4. Daily Report   5. Save Report   6. Exit")
        choice = input("Enter choice (1-6): ").strip()

        if choice == '1':
            veh_no = input("Vehicle Number: ").strip().upper()
            veh_type = input("Vehicle Type (bike/car/ev/heavy): ").strip().lower()
            print(parking.vehicle_entry(veh_no, veh_type))

        elif choice == '2':
            try:
                slot = int(input("Enter Slot Number: "))
                print(parking.vehicle_exit(slot))
            except ValueError:
                print("Invalid slot number!")

        elif choice == '3':
            parking.display_status()

        elif choice == '4':
            print(parking.daily_report())

        elif choice == '5':
            parking.save_report()

        elif choice == '6':
            print("Thank you for using Smart Parking System!")
            break

        else:
            print("Invalid choice! Try again.")

if __name__ == "__main__":
    main()


