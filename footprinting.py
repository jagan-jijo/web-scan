
# Footprinting gathers WHOIS and DNS information for a given domain.
import whois
import subprocess

class Footprinting:
    def __init__(self, domain):
        self.domain = domain

    def domain_info(self):
        """
        Retrieve WHOIS information and perform nslookup for the domain.
        """
        results = []
        try:
            # WHOIS information
            domain_info = whois.whois(self.domain)
            results.append(str(domain_info))
        except Exception as e:
            results.append(f"Error retrieving Whois information: {e}")

        try:
            # DNS lookup using nslookup
            nslookup_result = subprocess.check_output(["nslookup", self.domain], stderr=subprocess.STDOUT).decode()
            results.append(nslookup_result)
        except Exception as e:
            results.append(f"Error performing nslookup: {e}")
        
        return results
