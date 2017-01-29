import re
import netaddr

class SubnetHandler():
	def __init__(self, subnets_filename):
		self.subnets = {}
		self.read_subnets_from_file(subnets_filename)

	# String -> Void
	def read_subnets_from_file(self, filename):
		with open(filename) as f:
			lines = f.readlines()
			for line in lines:
				if not line.startswith("#"):
					comps = line.split("=")
					address_ranges = [adrange.replace(" ", "") for adrange in comps[0].split(",")]
					quoted_regex = re.compile('"[^"]*"') #http://stackoverflow.com/questions/2076343/extract-string-from-between-quotations
					name = quoted_regex.findall(comps[1])[0].replace('"', '')
					for address_range in address_ranges:
						self.subnets[address_range] = name

	# String -> String
	def name_for_address(self, address):
		largest_prefix_len = 0
		name = None
		ip_address = netaddr.IPAddress(address)
		for subnet_string, subnet_name in self.subnets.iteritems():
			subnet = netaddr.IPNetwork(subnet_string)
			if ip_address in subnet and subnet.prefixlen > largest_prefix_len:
				largest_prefix_len = subnet.prefixlen
				name = subnet_name
		return name

# Testing
if __name__ == "__main__":
	handler = SubnetHandler("Subnets.txt")
	print handler.name_for_address("128.135.1.1")
	print handler.name_for_address("128.135.6.1")
	print handler.name_for_address("128.135.9.1")