def checkFilyType(key):
    if key.lower().endswith('osw'):
        return 'osw'
    if key.lower().endswith('tsv'):
        return 'tsv'
    if key.lower().endswith('featureXML'):
        return 'featureXML'