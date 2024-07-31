from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import math

app = Flask(__name__, static_folder='static', static_url_path='')

class ParkingSlot:
    def __init__(self, slot_id):
        self.slot_id = slot_id
        self.is_occupied = False
        self.vehicle_number = None
        self.entry_time = None

class ParkingLot:
    def __init__(self, total_slots, rate_per_hour):
        self.slots = [ParkingSlot(i) for i in range(total_slots)]
        self.rate_per_hour = rate_per_hour

    def display_empty_slots(self):
        empty_slots = [slot.slot_id for slot in self.slots if not slot.is_occupied]
        return ' '.join(map(str, empty_slots)) if empty_slots else "No slots are available"

    def park_vehicle(self, vehicle_number):
        if self.is_full():
            return "Parking lot is full. Cannot park any more vehicles."
        for slot in self.slots:
            if not slot.is_occupied:
                slot.is_occupied = True
                slot.vehicle_number = vehicle_number
                slot.entry_time = datetime.now()
                return f"Vehicle {vehicle_number} parked at slot {slot.slot_id}"
        return "No empty slots available"

    def remove_vehicle(self, vehicle_number):
        for slot in self.slots:
            if slot.is_occupied and slot.vehicle_number == vehicle_number:
                exit_time = datetime.now()
                parked_duration = exit_time - slot.entry_time
                hours_parked = parked_duration.total_seconds() / 3600
                fee = math.ceil(hours_parked * self.rate_per_hour)
                slot.is_occupied = False
                slot.vehicle_number = None
                slot.entry_time = None
                return f"Vehicle {vehicle_number} removed from slot {slot.slot_id}.Total hours parked: {hours_parked:.2f}. Fee: ₹{fee:.2f}"
        return "Vehicle not found"

    def is_full(self):
        return all(slot.is_occupied for slot in self.slots)

parking_lot = ParkingLot(total_slots=10, rate_per_hour=2.0)

@app.route('/display_empty_slots', methods=['GET'])
def display_empty_slots():
    slots = parking_lot.display_empty_slots()
    return jsonify(message=slots)

@app.route('/park_vehicle', methods=['POST'])
def park_vehicle():
    vehicle_number = request.json.get('vehicle_number')
    result = parking_lot.park_vehicle(vehicle_number)
    return jsonify(message=result)

@app.route('/remove_vehicle', methods=['POST'])
def remove_vehicle():
    vehicle_number = request.json.get('vehicle_number')
    result = parking_lot.remove_vehicle(vehicle_number)
    return jsonify(message=result)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)