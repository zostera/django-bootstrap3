def split_css_classes(css_classes):
    classes_list = unicode(css_classes or '').split(' ')
    return [c for c in classes_list if c]


def add_css_class(css_classes, css_class):
    classes_list = split_css_classes(css_classes)
    for c in split_css_classes(css_class):
        if c not in classes_list:
            classes_list.append(c)
    return ' '.join(classes_list)


def remove_css_class(css_classes, css_class):
    remove = set(split_css_classes(css_class))
    classes_list = [c for c in split_css_classes(css_classes) if c not in remove]
    return ' '.join(classes_list)
