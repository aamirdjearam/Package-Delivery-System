class Package:
    def __init__(self, id, address, city, state, zip, deliveryTime, size, notes, start_time, end_time):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deliveryTime = deliveryTime
        self.size = size
        self.notes = notes
        self.start_time = start_time
        self.end_time = end_time
        self.status = "At Hub"
        self.truck = "Not Loaded"

