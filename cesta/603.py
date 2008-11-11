'''
Utility script for automatically generating a 
newforms-admin admin.py file based on an old-style models.py file.
The generated source code is printed to standard output.

Usage: ./newforms_gen.py my.module > admin.py
where my.module contains a models.py file.
'''

import sys
import os.path
import re
import StringIO
import imp
import copy

def _update_admin_line(s):
    s = re.sub(r"'classes':\s*'(.*?)'", r"'classes': ('\1',)", s)  # make 'classes' a tuple
    s = re.sub(r'fields\s*=', 'fieldsets =', s)                    # change fields into fieldsets
    return s

def generate_newforms_admin(module_name):
    # read the source code
    path = imp.find_module(module_name.split('.')[0])[1]
    filepath = os.path.join(*[path] + module_name.split('.')[1:] + ['models.py'])
    source = open(filepath, 'r').read()

    # initialize some variables
    output = StringIO.StringIO()    
    inline_classes = []
    model_names = []
    model_admin = {}

    # initialize mapping from admin fields to formatting functions
    def format_tuple(data, name, indentation):
        return '%s%s = %s' % (indentation, key, repr(tuple(data)))
    def format_lines(data, name, indentation):
        return '\n'.join([_update_admin_line(line) for line in data if line.strip() != 'pass'])
    def format_dict(data, name, indentation):
        items = ', '.join(("'%s': %s" % (field, value) for field, value in data.items()))
        return '%s%s = {%s}' % (indentation, key, items)
    def format_list_of_names(data, name, indentation):
        return '%s%s = [%s]' % (indentation, name, ', '.join(data))

    default_admin_info ={'admin_lines': [],  
                         'inlines': [],
                         'prepopulated_fields': {},
                         'filter_horizontal': [],
                         'filter_vertical': [],
                         'raw_id_fields': [],
                        }
    field_format_func = {'admin_lines':         format_lines,
                         'inlines':             format_list_of_names,
                         'prepopulated_fields': format_dict,
                         'filter_horizontal':   format_tuple,
                         'filter_vertical':     format_tuple,
                         'raw_id_fields':       format_tuple,}

    parts = re.compile(r'^class (\w+).*$', re.M).split(source)
    for class_name, code in zip(parts[1::2], parts[2::2]):
        # add model to list and initialize admin info for this model
        model_names.append(class_name)
        model_admin[class_name] = copy.deepcopy(default_admin_info)

        # determine indentation 
        first_line = [line for line in code.split('\n') if line.strip()][0]
        indentation = first_line[ : len(first_line) - len(first_line.lstrip())]    

        # find any Admin class declaration
        m = re.search(r'(?m)^%sclass Admin:.*\n((%s[ \t]+.+\n)*)' % (indentation, indentation), code)
        if m:            
            model_admin[class_name]['admin_lines'] = [line.replace(indentation, '', 1) 
                                                      for line in m.group(1).split('\n') if line.strip()]

        # find the fields in this class
        fields = re.findall(r'(?m)^%s(\w+) *= *models\.(\w+).*?\((.*\n((%s[ \t]+.+\n)*))' % (indentation, indentation), code)             

        for field in fields:
            # extract field name, type and rest of line
            field_name, field_type, field_data = field[0:3]

            # extract the field initialization kwargs (only works for simple values, not tuple values)
            params = dict(re.findall(r'(\w+) *= *([a-zA-Z0-9._]+)', field_data))
            first_param = field_data.split(',')[0].strip()

            # find foreign keys with inline editing
            if field_type.endswith('ForeignKey') and 'edit_inline' in params:                        
                if 'TABULAR' in params['edit_inline']:
                    inline_class = 'admin.TabularInline'
                else:
                    inline_class = 'admin.StackedInline'

                fk_class = first_param
                if fk_class.startswith("'") or fk_class.startswith('"'):
                    fk_class = fk_class[1:-1]

                # build inline class
                lines = ['class %s_Inline(%s):' % (class_name, inline_class)]
                lines.append('%smodel = %s' % (indentation, class_name))            
                for input_field, output_field in [('num_in_admin', 'extra'), ]:
                    if input_field in params:
                        lines.append('%s%s = %s' % (indentation, output_field, params[input_field]))

                # add to list of inline classes and add an entry in the ForeignKey model linking to this class
                inline_classes.append('\n'.join(lines) + '\n')
                if not fk_class in model_admin:
                    model_admin[fk_class] = copy.deepcopy(default_admin_info)
                model_admin[fk_class]['inlines'].append('%s_Inline' % class_name)

            # store info used for the admin options class fields
            m = re.search(r'prepopulate_from=(\(.+?\))', field_data)
            if m:            
                model_admin[class_name]['prepopulated_fields'][field_name] = m.group(1)
            if 'filter_interface' in params and ('HORIZONTAL' in params['filter_interface'] or 'True' in params['filter_interface']):
                model_admin[class_name]['filter_horizontal'].append(field_name)
            if 'filter_interface' in params and 'VERTICAL' in params['filter_interface']:
                model_admin[class_name]['filter_vertical'].append(field_name)
            if 'raw_id_admin' in params and params['raw_id_admin'] == 'True':
                model_admin[class_name]['raw_id_fields'].append(field_name)

    register_classes = []    # admin classes to register

    for model in set(model_names) | set(model_admin.keys()):
        if model in model_admin:                    
            # build admin class
            lines = ['class %sOptions(admin.ModelAdmin):' % model]
            for key, value in model_admin[model].items():
                if value:
                    line = field_format_func[key](value, key, indentation)
                    if line:
                        lines.append(line)

            # if the admin class has any contents
            if len(lines) >= 2:                            
                admin_class = '\n'.join(lines)                
                if model in model_names:
                    register_classes.append((model, '%sOptions' % model))
                else:
                    # if the model is not defined in this module comment out the Admin class declaration
                    # (it's the user's responsibility to move relevant parts of the code to the right place)
                    admin_class = '\n'.join(['# ' + line for line in admin_class.split('\n')])                
                   
                output.write(admin_class + '\n\n') # output admin class definition

            # else if the admin class lacks contents but there was an 
            # empty Admin class with just a 'pass' line in the original source
            # and the model class was defined in the current module
            elif model_admin[model]['admin_lines'] and model in model_names:
                register_classes.append((model,))

    for class_names in register_classes:
        output.write('admin.site.register(%s)\n' % ', '.join(class_names))

    # construct final output
    output = output.getvalue()
    lines = []        
    lines.append('from django.contrib import admin')
    lines.append('from django.utils.translation import ugettext_lazy as _\n')
    lines.extend(inline_classes)    
    lines.append(output)
    output = '\n'.join(lines)

    # add an import line that imports all models referenced in the code
    referenced_models = [m for m in model_names if re.search(r'\b%s\b' % m, output)]        
    if referenced_models:
        output = '\n'.join(['from %s.models import ' % module_name + ', '.join(referenced_models), output])

    return output

if __name__ == '__main__':
    print generate_newforms_admin(sys.argv[1])