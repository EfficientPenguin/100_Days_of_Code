'''
    This class defines the PropertyData structure along with various data manip methods
    to format things in a more human-readable way.
'''

class PropertyData():
    def __init__(self, price: str, address: str, url: str):
        self.price = self._fmt_price(price)
        self.address = self._fmt_address(address)
        self.url = url
    
    def _fmt_price(self, price: str) -> int:
        ''' Format the price data.'''
        # Remove /mo, +, $, and , in the text field for the price -- NOTE: Some are listed with 1 bd, etc.
        # E.g, $2,895+/mo
        # $2,895/mo
        # $2,895+ 1bd
        fmt_price = ""
    
        for char in price:
            if char.isdecimal():
                fmt_price += char
            if char == "+" or char == "/":
                break
            
        return int(fmt_price)

    def _fmt_address(self, address: str) -> str:
        ''' Format the address data. '''
        # return fmt_address
        fmt_address = address.strip()

        # remote '|' char
        if '|' in fmt_address:
            fmt_address = fmt_address.split('|')[1].strip()
        
        # Remove extra meta info at front of address, like name of location that's not the address itself by ','
        # E.g., 125 Gardenside, 125 Gardenside Dr, San Francisco, CA 94114 -- first Gardenside should be removed
        if len(fmt_address.split(',')) == 4:
            fmt_address = ",".join(fmt_address.split(',')[1::]).strip()
        
        return fmt_address
