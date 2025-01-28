def str_to_markdown(sting):
    sting = sting.replace('%', '\\%')
    sting = sting.replace('#', '\\#')
    sting = sting.replace('+', '\\+')
    sting = sting.replace('&', '\\&')
    sting = sting.replace('-', '\\-')
    sting = sting.replace('.', '\\.')
    return sting
