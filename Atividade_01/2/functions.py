def formatToHeaderParams(dataArray):
    formatedString = ''
    for data in dataArray:
        if (formatedString != ''):
            formatedString = formatedString + '\n' + str(data)
        else: 
            formatedString = str(data)

    return formatedString

def asByteArray(array):
    return bytearray(array, 'UTF-8')
