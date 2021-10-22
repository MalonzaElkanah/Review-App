from django import template

register = template . Library ()


@register.filter(name = "convert_drivelink") 
def convert_drivelink ( url ):
    return "http://drive.google.com/uc?export=view&id=" + url . split ( "/" ) [ 5 ]
 