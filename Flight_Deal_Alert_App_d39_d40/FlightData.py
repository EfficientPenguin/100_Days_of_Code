'''
    This class is responsbile for structuring the flight data.
'''

class FlightData:
    def __init__(self, sheet_data: list[dict]):
        ''' Initialize flight data'''
        self.data = self.init_flight_data(sheet_data)
    
    def init_flight_data(self, sheet_data: list[dict]) -> None:
        ''' Function to format the data retrieved from the sheet into dict[dict] ("iataCode": {"city", "lowestPrice})'''
        data = {entry['iataCode']:
                            {
                                'city':entry['city'],
                                'lowestPrice':entry['lowestPrice']
                            } 
                            for entry in sheet_data
                        }
        return data

    def get_lowest_price(self, iata_code: str) -> str:
        ''' Fetch the lowest price by iataCode.'''
        return self.data[iata_code]['lowestPrice']
    
    def get_best_flights_below_lowest_price(self, all_flight_info: dict, dst_iata_code: str) -> list[dict]:
        ''' Get the best flights below the lowest price threshold and return them to caller. '''
        lowest_fare_flights = []

        # Get only the best flights
        best_flights = all_flight_info['best_flights']

         # Iterate over best_flights to find if it's less than threshold
        for flight in best_flights:
            print(flight['price'])
            if flight['price'] < self.get_lowest_price(dst_iata_code):
                lowest_fare_flights.append(flight)
        
        return lowest_fare_flights

    def format_lowest_fare_flights(self, lowest_fare_flights: list[dict]) -> list[dict]:
        ''' Takes the list of lowest fare flights, extracts relevant data for the app, then returns it formatted.'''
        fmtd_fare_flights = []

        # Only get airline, arrival airport dict, dep airport dict, price, and type
        for flight_dict in lowest_fare_flights:
            flight = {
                "airline": flight_dict['flights'][0]['airline'],
                "arrival_airport": flight_dict['flights'][0]['arrival_airport'],
                "departure_airport": flight_dict['flights'][0]['departure_airport'],
                "price": flight_dict['price'],
                "type": flight_dict['type']
            }
            fmtd_fare_flights.append(flight)
        
        return fmtd_fare_flights
