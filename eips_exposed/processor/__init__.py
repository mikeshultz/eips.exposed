from eips_exposed.processor.objects import EIP


def parse_eip(eip_text):
    """ Parse an EIP into an EIP object """
    return EIP(eip_text)
