class Config:
    MANIFEST_FILE_DESCRIPTION = 'IIIF manifest'
    ANNOT_FILE_DESCRIPTION = 'Fichier extrait de Tropy avec les annotations'

    uploadsAPIHeaders = {
        'accept': 'application/json',
    }
    
    filesAPIHeaders = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    nakala_url_iiif = "/iiif/"
    nakala_url_data = "/data/"
    nakala_url_datas = "/datas/"
    annot_url_arg = "/Annotation"

    urlNakala = "https://api.nakala.fr"
    urlTestNakala = "https://apitest.nakala.fr"
    
    urlNakalaId = "https://nakala.fr"
    urlTestNakalaId = "https://test.nakala.fr"

    #data_identifier = "10.34847/nkl.10286c50"
    #api_key = "01234567-89ab-cdef-0123-456789abcdef"

