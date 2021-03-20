def delimiterStringOutput(dataArray):
    formatedString = ''
    for data in dataArray:
        if (formatedString != ''):
            formatedString = formatedString + '\n' + str(data)
        else: 
            formatedString = str(data)

    return formatedString