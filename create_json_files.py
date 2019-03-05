from gcmd_tools import gcmdFile

platform_url = 'https://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/platforms'
instrument_url = 'https://gcmdservices.gsfc.nasa.gov/kms/concepts/concept_scheme/instruments'


instruments = gcmdFile(instrument_url)
instruments.save('instruments.json')

platforms = gcmdFile(platform_url)
platforms.save('platforms.json')

